import streamlit as st
import google.generativeai as genai

st.title("AIむげんクイズ 🤖")

# 金庫のキーを読み込み
if "GEMINI_API_KEY" in st.secrets:
    try:
        # 1. 接続設定
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # 2. モデルの準備（models/ をつけるのが現在の正式な書き方です）
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        # 3. 通信テスト（余計な命令を消して、シンプルに送ります）
        response = model.generate_content("「つながったよ」とひらがなで言って")
        
        st.success("やったー！ついに壁を突破しました！")
        st.balloons()
        st.write("AIからのメッセージ:", response.text)
        st.info("このメッセージが出れば大成功です。クイズ画面に戻しましょう！")
        
    except Exception as e:
        # まだエラーが出る場合は、その内容を表示
        st.error("まだエラーが続いています。")
        st.code(str(e))
        
        st.write("---")
        st.write("【もう一つの方法を試します】")
        try:
            # models/ を抜いた名前でも試してみます
            model_simple = genai.GenerativeModel('gemini-1.5-flash')
            res_simple = model_simple.generate_content("「おっけー」と言って")
            st.warning("シンプルな名前で成功しました！")
            st.write(res_simple.text)
        except Exception as e2:
            st.write("どちらの方法でも届きませんでした。")
            st.code(str(e2))
else:
    st.warning("StreamlitのSecretsにキーを設定してください。")
