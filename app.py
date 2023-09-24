from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles


app = Flask(__name__)

# retrieve it by secrets.token_hex()
app.secret_key = 'f766a2a3d4aa8a52c66848e783e510d3ecf1b710c5f9b26d68b7c7fe7dffef96'
PLACEHOLDER_CODE = ("print('Welcome to Tschuppis code image generator')\n"
                    "print('Please paste your code here..')")
DEFAULT_STYLE = 'monokai'


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


@app.route('/style', methods=['GET'])
def style():
    if session['style'] is None:
        session['style'] = DEFAULT_STYLE

    formatter = HtmlFormatter(style=session['style'])
    context = {
        'message': 'Select Your Style 🎨',
        'style_definitions': formatter.get_style_defs(),
        'styles': list(get_all_styles()),
        'style_bg_color': formatter.style.background_color,
        'highlighted_code': highlight(
            session['code'], Python3Lexer(), formatter
        ),
    }
    return render_template("style_selection.html", **context)


@app.route('/save_style', methods=['POST'])
def save_style():
    if request.form.get('style') is not None:
        session['style'] = request.form.get('style')
    if request.form.get('code') is not None:
        session['code'] = request.form.get('code')
    return redirect(url_for('style'))
