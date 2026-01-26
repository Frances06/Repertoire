from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/redirect')
def redirect_to_home():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)