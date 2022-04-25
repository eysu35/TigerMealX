from flask import Flask, request, render_template, request, make_response
from keys import APP_SECRET_KEY
from database.exchanges import Exchanges
from database.students import Students
from send_email import send_email


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
import auth
emails_enabled = False

@app.route('/')
@app.route('/index', methods=['GET'])
def base():
    netid = auth.authenticate()
    loc_id = Students.get_location_name_from_netid(netid)
    print(loc_id)
    name = Students.get_first_name_from_netid(netid)
    
    # search_puid = Students.get_puid_from_name(search_name)

    return render_template('index.html', name=name, netid=netid, loc_id=loc_id)


@app.route('/exchanges/')
def show_exchanges():
    netid = auth.authenticate()
    loc_id = Students.get_location_name_from_netid(netid)
    try:
        name = Students.get_first_name_from_netid(netid)
        studentid = Students.get_puid_from_netid(netid)
        curr_exchanges = Exchanges.get_current_exchanges(studentid)
        past_exchanges = Exchanges.get_past_exchanges(studentid)
    except Exception as e:
        print("tigermealx.py error [30]: " + str(e))
        return render_template('errordb.html')
    return render_template('exchanges.html',
                           curr_exchanges=curr_exchanges,
                           past_exchanges=past_exchanges, name=name,
                           user_puid=studentid, loc_id=loc_id)


@app.route('/about/')
def faq():
    netid = auth.authenticate()
    
    loc_id = Students.get_location_name_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)

    return render_template('about.html', name=name, loc_id=loc_id)

@app.route('/admin/')
def admin_page():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)

    return render_template('admin.html', name=name)

@app.route('/help/')
def help_page():
    netid = auth.authenticate()
    loc_id = Students.get_location_name_from_netid(netid)
    name = Students.get_first_name_from_netid(netid)

    return render_template('help.html', name=name, loc_id=loc_id)

@app.route('/exchangeportal')
def initiate_exchange():
    netid = auth.authenticate()
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
        print("tigermealx.py error [75]: " + str(e))
        return render_template('error404.html')
    
    name2 = student2.get_name()
    location2 = Students.get_location_name_from_puid(puid2)

    # students cannot exchange with themselves or with someone who eats at the same place
    if puid1 == puid2:
        return render_template('exchangeerror.html', msg="You cannot exchange a meal with yourself.")

    loc1_id = student1.get_loc_id()
    loc2_id = student2.get_loc_id()
    print(loc2_id)

    if loc1_id == loc2_id:
        return render_template('exchangeerror.html', msg="You cannot exchange a meal with someone who eats at the same location as you.")

    # allowed exchange
    return render_template('exchange_init.html', name=name, puid2=puid2,
                           name2=name2,
                           location2=location2, loc_id=loc2_id)


@app.route('/postnewexchange', methods=['GET', 'POST'])
def post_new_exchange():
    netid1 = auth.authenticate()
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
        loc_id = Students.get_location_name_from_netid(netid2)

        if emails_enabled:
            # send emails with the name of the other student
            send_email(student2.get_name(), netid1)
            send_email(student1.get_name(), netid2)

        html = render_template("index.html", name=name)
        response = make_response(html)
        return response
    except Exception as e:
        print("tigermealx.py error: " + str(e))
        return render_template('error404.html', name = name, loc_id=loc_id)



    
@app.route('/completeexchange', methods=['GET']) #Could be POST?
def complete_exchange():
    netid1 = request.args.get('netid1').strip().lower()
    netid2 = request.args.get('netid2').strip().lower()
    

    puid1 = Students.get_puid_from_netid(netid1)
    puid2 = Students.get_puid_from_netid(netid2)

    location_name = request.args.get('location').strip()
    time = request.args.get('time')

    location_id = Exchanges.get_loc_id_from_loc_name(location_name)

    success, msg = Exchanges.update_exchange(puid1, puid2, location_id, time)
    print(msg)

    return msg


@app.route('/searchresults', methods=['GET'])
def search_results():
    Name = request.args.get('name')
    if len(Name) > 0:
        try:
            students = Students.search_students_by_name(Name)
        except Exception as e:
            print("tigermealx.py error [100]: " + str(e))
            return render_template('errordb.html')
        html = '<div class="table-wrapper-scroll-y my-custom-scrollbar"><table class="table table-bordered table-hover"><tbody>'
        pattern = "<tr onclick=\"startexchange(%s)\"><td width='130px'>%s</td><td width='130px'>%s</td></tr>"
        for student in students:
            html += pattern%(student.get_puid(),student.get_name(),student.get_netid())
        html += '</tbody></div>'    
    # assume it's a name for now but need to also check for PUID
    else:
        html = ''
    response = make_response(html)
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
