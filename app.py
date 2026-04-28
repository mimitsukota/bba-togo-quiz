import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 初期設定 ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # モデル名を「gemini-pro」という、より汎用的な名前に変更します
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("APIキーの設定を確認してください。")
    st.stop()

st.set_page_config(page_title="AIむげんクイズ", layout="centered")

# 音声読み上げ
def speak(text):
    if text:
        components.html(f"""<script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = 'ja-JP';
            window.speechSynthesis.speak(msg);
        </script>""", height=0)

# AIでクイズを作る
def get_new_quiz():
    genre = random.choice(["どうぶつ", "きょうりゅう", "ようかい"])
    phrase = random.choice(["だーれだ？", "なーにかな？", "でしょう？"])
    
    # AIへの命令
    prompt = f"5歳児向けの{genre}クイズを1問作ってください。答えと問題文はひらがなとカタカナのみ。形式：答え:〇〇 改行 問題:〇〇"
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        ans = "？"
        hint = "もういちど してみてね"
        for line in lines:
            if "答え" in line or "こたえ" in line:
                ans = line.split(":")[-1].strip()
            if "問題" in line or "もんだい" in line:
                hint = line.split(":")[-1].strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except Exception as e:
        # 万が一エラーが出た場合、その内容を表示します
        return {"genre": "エラー", "ans": "再試行してください", "hint": str(e), "phrase": "？"}

# --- 画面の管理 ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = get_new_quiz()
    st.session_state.is_answered = False

st.title("AIむげんクイズ 🤖")

q = st.session_state.quiz_data
full_question = f"【{q['genre']}】 {q['hint']}、{q['phrase']}"

st.subheader(full_question)

if not st.session_state.is_answered:
    speak(full_question)

col1, col2 = st.columns(2)

with col1:
    if st.button("こたえを みる", use_container_width=True, key="ans_btn"):
        st.session_state.is_answered = True
        st.rerun()

with col2:
    if st.button("つぎの もんだい", use_container_width=True, key="next_btn"):
        st.session_state.quiz_data = get_new_quiz()
        st.session_state.is_answered = False
        st.rerun()

# 答えの表示
if st.session_state.is_answered:
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>こたえ： {q['ans']}</h1>", unsafe_allow_html=True)
    speak(f"こたえは、{q['ans']} です！")
    st.balloons()
