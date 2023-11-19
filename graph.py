from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Replace these credentials with your own
USERNAME = 'charan'
PASSWORD_HASH = bcrypt.generate_password_hash('123').decode('utf-8')

# Flag to check if the user is logged in
logged_in = False

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and bcrypt.check_password_hash(PASSWORD_HASH, password):
            logged_in = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

@app.route('/')
def index():
    global logged_in
    if not logged_in:
        return redirect(url_for('login'))

    # Read CSV file
    df = pd.read_csv('emotion_data.csv')

    # Create line graph
    line_graph = create_line_graph(df)

    # Create bar graph
    bar_graph, dominant_emotion = create_bar_graph(df)

    return render_template('index.html', line_graph=line_graph, bar_graph=bar_graph, dominant_emotion=dominant_emotion)

def create_line_graph(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['Emotion'], marker='o')
    plt.title('Emotion vs Timestamp')
    plt.xlabel('Timestamp')
    plt.ylabel('Emotion')
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert the plot to base64 for embedding in HTML
    line_graph = base64.b64encode(img.getvalue()).decode()

    return line_graph

def create_bar_graph(df):
    plt.figure(figsize=(10, 6))
    emotion_counts = df['Emotion'].value_counts()
    dominant_emotion = emotion_counts.idxmax()
    plt.bar(emotion_counts.index, emotion_counts.values)
    plt.title('Emotion Counts vs Timestamp')
    plt.xlabel('Emotion')
    plt.ylabel('Count')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert the plot to base64 for embedding in HTML
    bar_graph = base64.b64encode(img.getvalue()).decode()

    return bar_graph, dominant_emotion

if __name__ == '__main__':
    app.run(debug=True)
