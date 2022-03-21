from flask import Flask, redirect, url_for, request, render_template
from exchanges import Exchange
from students import Students

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def base():
    # assume it's a name for now but need to also check for PUID
    search_name = request.args.get('studentName')
    # search_puid = Students.get_puid_from_name(search_name)

    students = Students.search_students_by_name(search_name)
    return render_template('index.html', students=students)


@app.route('/exchanges/')
def exchanges():
    curr_exchanges = []
    curr_exchanges.append(Exchange("Floyd","Ivy","Lunch","Complete","11/04/2000"))
    past_exchanges = []
    past_exchanges.append(Exchange("Chloe","Ivy","Lunch","Complete","11/04/2000"))
    return render_template('exchanges.html', curr_exchanges=curr_exchanges, past_exchanges=past_exchanges)


@app.route('/faq/')
def faq():
    return render_template('faq.html')


@app.route('/help/')
def help_page():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
