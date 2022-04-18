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
    name = Students.get_first_name_from_netid(netid)
    
    # search_puid = Students.get_puid_from_name(search_name)

    return render_template('index.html', name=name, netid=netid)

@app.route('/exchanges/')
def show_exchanges():
    netid = auth.authenticate()
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
                           past_exchanges=past_exchanges, name=name)


@app.route('/about/')
def faq():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)

    return render_template('about.html', name=name)


@app.route('/help/')
def help_page():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)

    return render_template('help.html', name=name)

@app.route('/exchangeportal')
def initiate_exchange():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)
    puid2 = request.args.get('puid')
    if puid2 is None or puid2 == '':
        return render_template('error404.html')
    try:
        student2 = Students.get_student_by_puid(puid2)
    except Exception as e:
        print("tigermealx.py error [62]: " + str(e))
        return render_template('error404.html')
    
    name2 = student2.get_name()
    location2 = Students.get_location_name_from_puid(puid2)
    return render_template('exchange_init.html',name=name, puid2=puid2,
                           name2=name2,
                           location2=location2)

@app.route('/postnewexchange', methods=['GET', 'POST'])
def post_new_exchange():
    netid1 = auth.authenticate()
    if request.method == 'POST':
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
                send_email(student1.get_name(), netid2)

            html = render_template("index.html", name=name)
            response = make_response(html)
            return response
        except Exception as e:
            print("tigermealx.py error [88]: " + str(e))
            return render_template('error404.html')

    

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
    app.logger.exception(err)
    return render_template('error404.html')


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
