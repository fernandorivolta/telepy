from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime

app = Flask(__name__, template_folder='html/')
@app.route('/')
def index():
    return render_template('index.html', last_updated=datetime.now(tz=None))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.run(host='0.0.0.0', debug=True) 