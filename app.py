import streamlit as st
from Function.UserDao_file import UserDao
from keras.models import load_model
from Function.User_file import User
import numpy as np
from Function import datapreprocessing as pre
from Function.datapreprocessing import DataPreprocessing 

# Creat Corpus
dp=DataPreprocessing("./data/mobile_feedback/Cleaned_Train.csv")
# Create object userdao
userdao=UserDao()
# Function to predict sentiment
def predict_sentiment(comment):
    model = load_model("./model/model_sentiment_lstm.h5")
    result = model.predict(comment)
    label_index = np.argmax(result, axis=1)
    predicted_label = dp.label_encoder.inverse_transform(label_index)
    return predicted_label

# Streamlit app for sentiment analysis
def sentiment_analysis(username):
    st.title("Vietnamese Sentiment Analysis")
    user=User(username)
    if userdao.get_user_id(user)==1:
        st.write("Hello, admin")
        if st.button("Predict"):
            comment_of_user= userdao.get_comment_by_user()
            for comment in comment_of_user:
                processed_comment = dp.fit_transform(comment[0].lower())
                full_name=userdao.get_full_name(comment[0])
                print(comment[0])
                prediction = predict_sentiment(processed_comment)
                prediction = dp.Standardization(prediction)
                st.write(f"Hello {full_name},! This is the result of analyzing the results of the comment")
                st.write(f"'{comment[0]}'")
                st.write("Sentiment:", prediction)
    else:
        comment = st.text_area("Enter your comment:")
        st.write(f"Hello, {username}")
        if st.button("Enter comment"):
            userdao.insert_comment(user, comment)
            st.success("Comment posted successfully!")
# Streamlit app for login page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username:", key="username_input")
    password = st.text_input("Password:", type="password", key="password_input")
    user=User(username,password)
    
    if st.button("Login"):
        login_success = userdao.check_login(user)
        if login_success==1:
            st.session_state.page = "sentiment_analysis"
            st.session_state.username = username
        else:
            st.error("Invalid username or password.")
    else:
        st.info("Please login to access the sentiment analysis page.")

# Run the Streamlit app
if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "username" not in st.session_state:
        st.session_state.username = ""
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "sentiment_analysis":
        sentiment_analysis(st.session_state.username)
