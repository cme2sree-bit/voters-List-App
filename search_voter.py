from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
DATA_FILE = 'Book1.xlsx'

def get_data():
    return pd.read_excel(DATA_FILE)

@app.route('/')
def home():
    return render_template('home.html')

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
        query = request.form['query']
        results = df[df['Name'].str.contains(query, na=False, case=False)].to_dict('records')
    return render_template('search.html', results=results)
