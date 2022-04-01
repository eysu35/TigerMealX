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
    # assume it's a name for now but need to also check for PUID
    # search_name = request.args.get('studentName')
    # if search_name is None or search_name == '':
    #     students = []
    # else:
    #     students = Students.search_students_by_name(search_name)
    # search_puid = Students.get_puid_from_name(search_name)
    name = Students.get_name_from_netid(netid)
    return render_template('navbar.html', name=name)

@app.route('/search')
def search():
    username = auth.authenticate()
    # assume it's a name for now but need to also check for PUID
    search_name = request.args.get('studentName')
    if search_name is None or search_name == '':
        students = []
    else:
        students = Students.search_students_by_name(search_name)
    # search_puid = Students.get_puid_from_name(search_name)

    return render_template('index.html', students=students)


@app.route('/exchanges/')
def exchanges():
    username = auth.authenticate()

    studentid = request.args.get('studentid')
    studentid = "123456789"
    curr_exchanges = Exchanges.get_current_exchanges('123456789')
    past_exchanges = Exchanges.get_past_exchanges('920228341')
    return render_template('exchanges.html', curr_exchanges=curr_exchanges,past_exchanges=past_exchanges)


@app.route('/about/')
def faq():
    username = auth.authenticate()

    return render_template('about.html')


@app.route('/help/')
def help_page():
    username = auth.authenticate()
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
