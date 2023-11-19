import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def create_line_graph(df):
    fig = px.line(df, x='Timestamp', y='Emotion', markers=True, title='Emotion vs Timestamp')
    return fig

@st.cache_data
def create_bar_graph(df):
    emotion_counts = df['Emotion'].value_counts().reset_index()
    emotion_counts.columns = ['Emotion', 'Count']

    fig = px.bar(emotion_counts, x='Emotion', y='Count', title='Emotion Counts vs Timestamp',
                 labels={'Emotion': 'Emotion', 'Count': 'Count'})
    
    dominant_emotion = emotion_counts['Emotion'].iloc[0]  # Assuming you want the emotion with the highest count

    return fig, dominant_emotion

def main():
    st.title("Graph Page")
    
    # Read CSV file
    df = pd.read_csv('emotion_data.csv')

    # Create line graph
    line_graph = create_line_graph(df)

    # Create bar graph
    bar_graph, dominant_emotion = create_bar_graph(df)

    # Display graphs
    st.markdown("## Emotion vs Timestamp")
    st.plotly_chart(line_graph, use_container_width=True)

    st.markdown("## Emotion Counts vs Timestamp")
    st.plotly_chart(bar_graph, use_container_width=True)

    st.markdown(f"**Dominant Emotion:** {dominant_emotion}")

    # Display DataFrame
    st.markdown("## Emotion Data Table")
    st.dataframe(df)

if __name__ == "__main__":
    main()
