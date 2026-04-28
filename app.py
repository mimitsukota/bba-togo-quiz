import streamlit as st
import google.generativeai as genai

st.title("AIむげんクイズ 🤖")

# 最新の「正式な」設定方法で接続します
if "GEMINI_API_KEY" in st.secrets:
    try:
        # 窓口を正式版（v1）に固定するおまじない
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # モデル名の指定を一番確実なものに
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 通信テスト
        response = model.generate_content("「やったね」とひらがなで言って")
        
        st.success("やったー！通信がつながりました！")
        st.balloons()
        st.write("AIからのメッセージ:", response.text)
        st.write("これでクイズ画面に戻る準備ができました。")
        
    except Exception as e:
        st.error("新しいキーでもまだエラーが出ています...")
        st.code(str(e))
else:
    st.warning("金庫にキーを設定してください。")
