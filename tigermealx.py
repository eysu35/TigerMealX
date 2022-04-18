from flask import Flask, request, render_template, request, make_response
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
    
    # search_puid = Students.get_puid_from_name(search_name)

    return render_template('index.html', name=name, netid=netid)

@app.route('/exchanges/')
def show_exchanges():
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
def initiate_exchange():
    netid = auth.authenticate()
    name = Students.get_first_name_from_netid(netid)
    puid2 = request.args.get('puid')
    if(puid2==None or puid2==''):
        return render_template('error.html', error_msg="missing puid")
    try:
        student2 = Students.get_student_by_puid(puid2)
    except Exception as e:
        print('tigermealx: ' + str(e))
        return render_template('error.html', error_msg="invalid puid")
    
    name2 = student2.get_name()
    location2 = Students.get_location_name_from_puid(puid2)
    return render_template('exchange_init.html',name=name, puid2=puid2,
                           name2=name2,
                           location2=location2)

@app.route('/postnewexchange')
def post_new_exchange():
    netid1 = auth.authenticate()
    puid1 = Students.get_puid_from_netid(netid1)
    puid2 = request.args.get('puid2')
    Exchanges.add_new_exchange(puid1, puid2)
    return

@app.route('/searchresults', methods=['GET'])
def search_results():
    Name = request.args.get('name')
    if len(Name) > 0:
        students = Students.search_students_by_name(Name)
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


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
