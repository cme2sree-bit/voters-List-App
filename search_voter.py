<h2>Search Voter</h2>
<form method="POST">
  <input type="text" name="serial" placeholder="Serial No">
  <input type="text" name="name" placeholder="Name">
  <input type="text" name="house" placeholder="House Name">
  <input type="text" name="party" placeholder="Political Party (LDF/UDF/NDA)">
  <input type="submit" value="Search">
</form>
{% if results %}
  <table border=1>
    <tr>
      {% for col in results[0].keys() %}<th>{{ col }}</th>{% endfor %}
    </tr>
    {% for v in results %}
      <tr>
        {% for c in v.values() %}<td>{{ c }}</td>{% endfor %}
      </tr>
    {% endfor %}
  </table>
{% endif %}
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'change_this_secret'  # Change for production

ADMIN_PASSWORD = 'admin123'  # Change this to a strong password!

# Admin login-required decorator
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Admin login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('home'))
        else:
            return "Wrong password! <a href='/login'>Try again</a>"
    return '''
        <form method="POST">
            Admin Password: <input type="password" name="password"/>
            <input type="submit" value="Login"/>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))
@app.route("/add", methods=['GET', 'POST'])
@admin_required
def add():
    ...
    
@app.route("/edit/<serial_no>", methods=['GET', 'POST'])
@admin_required
def edit(serial_no):
    ...

@app.route("/delete/<serial_no>")
@admin_required
def delete(serial_no):
    ...


