import streamlit as st

def main():
    st.title("Simple Streamlit App")

    # Text input
    user_input = st.text_input("Enter your name:", "Type here...")

    # Button
    if st.button("Submit"):
        st.success(f"Hello, {user_input}!")

if __name__ == '__main__':
    main()
