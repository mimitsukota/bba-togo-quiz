import streamlit as st
import google.generativeai as genai

# 設定
st.title("エラーチェック中...")

try:
    key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # テストで一言AIに喋らせる
    response = model.generate_content("「こんにちは」とだけ言ってください")
    st.success("AIとの通信に成功しました！")
    st.write("AIからの返事:", response.text)
    
except Exception as e:
    st.error("AIとの通信に失敗しました。原因は以下の通りです：")
    st.code(str(e)) # ここにエラーの原因が表示されます

st.write("---")
st.write("この画面に表示された内容を、そのまま私に教えてください。")
