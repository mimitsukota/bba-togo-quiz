import streamlit as st
import google.generativeai as genai

st.title("AIむげんクイズ 🤖")

try:
    # 新しいキーで接続
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AIに一言喋らせてみる
    response = model.generate_content("「やっとつながったね」とひらがなで言って")
    st.success("通信成功！")
    st.write("AIのメッセージ:", response.text)
except Exception as e:
    st.error("まだエラーが出ています...")
    st.code(str(e))
