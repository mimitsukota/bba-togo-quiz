import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.title("AIむげんクイズ 🤖")

# 金庫のキーを読み込み
if "GEMINI_API_KEY" in st.secrets:
    try:
        # 1. 接続設定（APIのバージョンを正式版 'v1' に強制固定します）
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # 2. モデルの準備
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. 通信テスト（エラーが出やすいv1betaを避け、正式版URLで送る指示）
        response = model.generate_content(
            "「つながったよ」とはなして",
            request_options=RequestOptions(api_version='v1')
        )
        
        st.success("やったー！ついに壁を突破しました！")
        st.balloons()
        st.write("AIのメッセージ:", response.text)
        st.info("このメッセージが出れば、もう大丈夫です。クイズ画面に戻せます！")
        
    except Exception as e:
        # まだエラーが出る場合は、詳しい内容を表示
        st.error("まだエラーが続いています。もう少しだけ詳しく見てみましょう。")
        st.code(str(e))
        
        # もし「404」が出るなら、モデル名を究極にシンプルにしてみます
        st.write("---")
        st.write("予備の接続を試します...")
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            res_alt = model_alt.generate_content("「おっけー」と言って")
            st.warning("予備の接続で成功しました！")
            st.write(res_alt.text)
        except:
            st.write("予備も届きませんでした。")

else:
    st.warning("StreamlitのSecretsにキーを設定してください。")
