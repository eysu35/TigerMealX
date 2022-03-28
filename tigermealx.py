from flask import Flask, request, render_template
from database.exchanges import Exchanges
from database.students import Students

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def base():
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
    studentid = request.args.get('studentid')
    studentid = "123456789"
    curr_exchanges = Exchanges.get_current_exchanges('123456789')
    past_exchanges = Exchanges.get_past_exchanges('920228341')
    return render_template('exchanges.html', curr_exchanges=curr_exchanges,past_exchanges=past_exchanges)


@app.route('/about/')
def faq():
    return render_template('about.html')


@app.route('/help/')
def help_page():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
