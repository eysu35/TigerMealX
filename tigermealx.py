from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('index.html')


@app.route('/exchanges/')
def exchanges():
    return render_template('exchanges.html')


@app.route('/faq/')
def faq():
    return render_template('faq.html')


@app.route('/help/')
def help_page():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)  # auto restart
