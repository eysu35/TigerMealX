from flask import Flask, request, render_template
from keys import APP_SECRET_KEY
from database.exchanges import Exchanges
from database.students import Students

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
import auth

@app.route('/')
@app.route('/index', methods=['GET'])
def base():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)
    # assume it's a name for now but need to also check for PUID
    search_name = request.args.get('studentName')
    if search_name is None or search_name == '':
        students = []
    else:
        students = Students.search_students_by_name(search_name)
    # search_puid = Students.get_puid_from_name(search_name)

    return render_template('index.html', students=students, name=name)

@app.route('/exchanges/')
def exchanges():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)
    studentid = Students.get_puid_from_netid(netid)
    curr_exchanges = Exchanges.get_current_exchanges(studentid)
    past_exchanges = Exchanges.get_past_exchanges(studentid)
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
def exchange():
    puid = request.args.get('puid')
    student = Students.get_student_by_puid(puid)
    name = student.get_name()
    club = student.get_location()
    return render_template('exchange_init.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
