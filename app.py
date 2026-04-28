import streamlit as st
import google.generativeai as genai

st.title("APIキーの 健康診断 🩺")

# 金庫の中にそもそも何か入っているか確認
if "GEMINI_API_KEY" not in st.secrets:
    st.error("金庫（Secrets）の中に 'GEMINI_API_KEY' という名前が見当たりません。")
else:
    key = st.secrets["GEMINI_API_KEY"]
    st.write(f"金庫の中にキーは見つかりました！（長さ：{len(key)}文字）")
    
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 一番簡単なテスト
        response = model.generate_content("「OK」と言って")
        st.success("おめでとうございます！通信がつながりました！")
        st.balloons()
    except Exception as e:
        st.error("キーは見つかりましたが、Googleさんが『そのキーは使えないよ』と言っています。")
        st.info("【対策】もう一度 AI Studio で新しいキーを作り直して、貼り直してみるのが一番の近道です。")
        st.code(str(e))
