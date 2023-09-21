from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)

# retrieve it by secrets.token_hex()
app.secret_key = 'f766a2a3d4aa8a52c66848e783e510d3ecf1b710c5f9b26d68b7c7fe7dffef96'
PLACEHOLDER_CODE = ("print('Welcome to Tschuppi's code image generator)\n"
                    "Please paste your code here..")


@app.route('/', methods=['GET'])
def code():
    if session.get('code') is None:
        session['code'] = PLACEHOLDER_CODE

    lines = session['code'].split('\n')

    context = {
        'message': 'Paste your Python code',
        'code': session['code'],
        'num_lines': len(lines),
        'max_char': len(max(lines, key=len)),
    }
    return render_template('code_input.html', **context)


@app.route('/save_code', methods=['POST'])
def save_code():
    session['code'] = request.form.get('code')
    return redirect(url_for('code'))


@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()
    session['code'] = PLACEHOLDER_CODE
    return redirect(url_for('code'))
