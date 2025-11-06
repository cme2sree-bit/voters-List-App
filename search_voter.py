from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from functools import wraps

app = Flask(__name__)
app.secret_key = 'change_this_secret'  # Change to a strong secret in production

ADMIN_PASSWORD = 'admin123'  # Change to a strong password
DATA_FILE = 'sec.kerala.gov.csv'

def get_data():
    df = pd.read_csv(DATA_FILE)
    return df

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    df = get_data()
    parties = ['LDF', 'UDF', 'NDA']
    party_count = {p: int((df['Political Party'] == p).sum()) for p in parties}
    party_count['Others'] = int((~df['Political Party'].isin(parties)).sum())
    return render_template('home.html', party_count=party_count)

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

@app.route('/voters')
def voters():
    df = get_data()
    voters_list = df.to_dict('records')
    return render_template('voters.html', voters=voters_list)

@app.route('/search', methods=['GET', 'POST'])
def search():
    df = get_data()
    results = []
    if request.method == 'POST':
        serial = request.form.get('serial', '').strip()
        name = request.form.get('name', '').strip()
        house = request.form.get('house', '').strip()
        party = request.form.get('party', '').strip()
        filt = pd.Series([True] * len(df))
        if serial:
            filt &= df['Serial No'].astype(str).str.contains(serial, na=False, case=False)
        if name:
            filt &= df['Name'].str.contains(name, na=False, case=False)
        if house:
            filt &= df['House Name'].str.contains(house, na=False, case=False)
        if party:
            filt &= df['Political Party'].str.contains(party, na=False, case=False)
        results = df[filt].to_dict('records')
    return render_template('search.html', results=results)

@app.route('/add', methods=['GET','POST'])
@admin_required
def add():
    if request.method == 'POST':
        df = get_data()
        new_row = {
            'Serial No': request.form['serial'],
            'Name': request.form['name'],
            "Guardian's Name": request.form.get("guardian", ""),
            'OldWard No/ House No.': request.form.get("oldward", ""),
            'House Name': request.form['house'],
            'Political Party': request.form['party']
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return redirect(url_for('voters'))
    return render_template('add.html')

@app.route('/edit/<serial_no>', methods=['GET','POST'])
@admin_required
def edit(serial_no):
    df = get_data()
    row = df[df['Serial No'].astype(str) == serial_no]
    if row.empty:
        return "Voter Not Found"
    if request.method == 'POST':
        ix = row.index[0]
        df.at[ix,'Name'] = request.form['name']
        df.at[ix,"Guardian's Name"] = request.form['guardian']
        df.at[ix,'OldWard No/ House No.'] = request.form['oldward']
        df.at[ix,'House Name'] = request.form['house']
        df.at[ix,'Political Party'] = request.form['party']
        df.to_csv(DATA_FILE, index=False)
        return redirect(url_for('voters'))
    v = row.iloc[0].to_dict()
    return render_template('edit.html', v=v)

@app.route('/delete/<serial_no>')
@admin_required
def delete(serial_no):
    df = get_data()
    df = df[df['Serial No'].astype(str) != serial_no]
    df.to_csv(DATA_FILE, index=False)
    return redirect(url_for('voters'))

if __name__ == '__main__':
    app.run(debug=True)
