import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from streamlit.hashing import generate_password_hash, verify_password

# Replace these credentials with your own
USERNAME = 'your_username'
PASSWORD_HASH = generate_password_hash('your_password')

# Flag to check if the user is logged in
logged_in = False

@st.cache
def read_data():
    # Read CSV file
    df = pd.read_csv('emotion_data.csv')
    return df

def login():
    global logged_in
    if st.button("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if username == USERNAME and verify_password(password, PASSWORD_HASH):
            logged_in = True
            st.success("Logged in successfully!")

    return logged_in

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

    # Convert the plot to base64 for embedding in Streamlit
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

    # Convert the plot to base64 for embedding in Streamlit
    bar_graph = base64.b64encode(img.getvalue()).decode()

    return bar_graph, dominant_emotion

def main():
    global logged_in
    st.title("Emotion Analysis App")

    if not logged_in:
        logged_in = login()

    if logged_in:
        df = read_data()

        # Create line graph
        line_graph = create_line_graph(df)

        # Create bar graph
        bar_graph, dominant_emotion = create_bar_graph(df)

        # Display graphs
        st.markdown("## Emotion vs Timestamp")
        st.image(line_graph, use_column_width=True)

        st.markdown("## Emotion Counts vs Timestamp")
        st.image(bar_graph, use_column_width=True)

        st.markdown(f"**Dominant Emotion:** {dominant_emotion}")

if __name__ == "__main__":
    main()
