from flask import Flask, render_template, request, make_response
from keys import APP_SECRET_KEY
from database.exchanges import Exchanges
from database.students import Students
from send_email import send_email, campus_dining_email

# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
app.secret_key = APP_SECRET_KEY
app.url_map.strict_slashes = False
import auth

emails_enabled = True


@app.route('/')
@app.route('/index', methods=['GET'])
def base():
    netid = auth.authenticate().strip()
    puid = Students.get_puid_from_netid(netid)
    student = Students.get_student_by_puid(puid)
    loc_id = Students.get_location_id_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)

    if not student.get_isValid():
        return render_template('exchangeerror.html', msg="You are not "
                                                         "on a meal plan that is valid for meal exchanges. Please "
                                                         "contact campus dining services if you think this is a "
                                                         "mistake.")
    response = render_template('index.html', name=name, netid=netid,
                               loc_id=loc_id)
    response = make_response(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/exchanges')
def show_exchanges():
    netid = auth.authenticate().strip()
    loc_id = Students.get_location_id_from_netid(netid)
    try:
        name = Students.get_first_name_from_netid(netid)
        studentid = Students.get_puid_from_netid(netid)
        curr_exchanges = Exchanges.get_current_exchanges(studentid)
        past_exchanges = Exchanges.get_past_exchanges(studentid)
    except Exception as e:
        print("tigermealx.py error [36]: " + str(e))
        return render_template('errordb.html')
    return render_template('exchanges.html',
                           curr_exchanges=curr_exchanges,
                           past_exchanges=past_exchanges, name=name,
                           user_puid=studentid, loc_id=loc_id)


@app.route('/about')
def faq():
    netid = auth.authenticate().strip()

    loc_id = Students.get_location_id_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)

    return render_template('about.html', name=name, loc_id=loc_id)


@app.route('/admin')
def admin_page():
    netid = auth.authenticate().strip()
    name = Students.get_first_name_from_netid(netid)

    return render_template('admin.html', name=name)


@app.route('/help')
def help_page():
    netid = auth.authenticate().strip()
    loc_id = Students.get_location_id_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)

    return render_template('help.html', name=name, loc_id=loc_id)


@app.route('/exchangeportal')
def initiate_exchange():
    netid = auth.authenticate().strip()
    puid1 = Students.get_puid_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)
    student1 = Students.get_student_by_puid(puid1)

    # other person
    puid2 = request.args.get('puid')

    if puid2 is None or puid2 == '':
        return render_template('error404.html')
    try:
        student2 = Students.get_student_by_puid(puid2)
    except Exception as e:
        print("tigermealx.py error [86]: " + str(e))
        return render_template('error404.html')

    name2 = student2.get_name()
    location2 = Students.get_location_name_from_puid(puid2)

    # students cannot meal exchange with someone who has an invalid plan

    if not student2.get_isValid():
        return render_template('exchangeerror.html',
                               msg="The student you are trying to " \
                                   "swap with has a meal plan that is " \
                                   "incompatible with the meal exchange program.")

    # students cannot exchange with themselves or with someone who eats at the same place
    if puid1 == puid2:
        return render_template('exchangeerror.html', msg="You cannot exchange a meal with yourself.")

    # students who belong to the same plan cannot meal exchange
    loc1_id = student1.get_loc_id()
    loc2_id = student2.get_loc_id()

    if loc1_id == loc2_id:
        return render_template('exchangeerror.html', msg="You cannot " \
                                                         "exchange a meal with " \
                                                         "someone who has a meal plan at same location as you.")

    # allowed exchange
    return render_template('exchange_init.html', name=name, puid2=puid2,
                           name2=name2,
                           location2=location2, loc_id=loc2_id)


@app.route('/postnewexchange', methods=['GET', 'POST'])
def post_new_exchange():
    netid1 = auth.authenticate().strip()
    loc_id = Students.get_location_id_from_netid(netid1)
    # if request.method == 'GET':
    try:
        name = Students.get_first_name_from_netid(netid1)

        puid1 = Students.get_puid_from_netid(netid1)
        puid2 = request.args.get('puid2')
        Exchanges.add_new_exchange(puid1, puid2)

        # get netid from puid for email purposes
        student1 = Students.get_student_by_puid(puid1)
        student2 = Students.get_student_by_puid(puid2)
        netid2 = student2.get_netid()

        if emails_enabled:
            # send emails with the name of the other student
            send_email(student2.get_name(), netid1)
            # UNCOMMENT WHEN WANT TO SEND EMAIL TO INVITED STUDENT
            # send_email(student1.get_name(), netid2)

        html = render_template("index.html", name=name, loc_id=loc_id)
        response = make_response(html)
        return response
    except Exception as e:
        print("tigermealx.py error: " + str(e))
        return render_template('error404.html', name=name, loc_id=loc_id)


@app.route('/emailcampusdining', methods=['POST'])
def email_campus_dining():
    subject = request.args.get('subject').strip()
    msg = request.args.get('msg').strip()

    netid = auth.authenticate().strip()
    loc_id = Students.get_location_id_from_netid(netid)

    try:
        name = Students.get_first_name_from_netid(netid)

        if emails_enabled:
            campus_dining_email(name, subject, msg)

        html = render_template("help.html", name=name, loc_id=loc_id)

        response = make_response(html)

    except Exception as e:
        print("tigermealx.py error: " + str(e))
        response = make_response(render_template("error404.html", name=name, loc_id=loc_id))

    return response


@app.route('/completeexchange', methods=['GET'])  # Could be POST?
def complete_exchange():
    netid1 = request.args.get('netid1').strip().lower()
    netid2 = request.args.get('netid2').strip().lower()

    puid1 = Students.get_puid_from_netid(netid1)
    puid2 = Students.get_puid_from_netid(netid2)

    location_name = request.args.get('location').strip()
    time = request.args.get('time')

    location_id = Exchanges.get_loc_id_from_loc_name(location_name)

    try:
        success, msg = Exchanges.update_exchange(puid1, puid2, location_id, time)
    except Exception:
        return 'An unknown error occurred'

    return msg


@app.route('/searchresults', methods=['GET'])
def search_results():
    Name = request.args.get('name')
    if len(Name) > 0:
        try:
            students = Students.search_students_by_name(Name)
        except Exception as e:
            print("tigermealx.py error [177]: " + str(e))
            return render_template('errordb.html')

        html = '<div class="table-wrapper-scroll-y my-custom-scrollbar"><table class="table table-bordered table-hover"><tbody>'
        pattern = "<tr onclick=\"startexchange(%s)\"><td width='130px'>%s</td><td width='130px'>%s</td></tr>"
        for student in students:
            html += pattern % (student.get_puid(), student.get_name(),
                               student.get_netid())
        html += '</tbody></div>'
        # assume it's a name for now but need to also check for PUID
    else:
        html = ''
    response = make_response(html)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.errorhandler(Exception)
def server_error(err):
    netid = auth.authenticate()

    loc_id = Students.get_location_name_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)
    app.logger.exception(err)
    return render_template('error404.html', name=name, loc_id=loc_id)


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
