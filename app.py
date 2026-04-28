import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 設定 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AIむげんクイズ", layout="centered")

# 音声読み上げ用
def speak(text):
    if text:
        components.html(f"""<script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = 'ja-JP';
            window.speechSynthesis.speak(msg);
        </script>""", height=0)

# AIでクイズを作る関数
def get_new_quiz():
    genre = random.choice(["どうぶつ", "きょうりゅう", "ようかい"])
    phrase = random.choice(["だーれだ？", "なーにかな？", "でしょう？"])
    prompt = f"{genre}のクイズを1問。答えと問題をひらがなのみで。形式：答え:〇〇 改行 問題:〇〇"
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        ans = lines[0].split(":")[-1].strip()
        hint = lines[1].split(":")[-1].strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "はなが ながい", "phrase": "だーれだ？"}

# --- 状態管理 ---
if 'quiz' not in st.session_state:
    st.session_state.quiz = get_new_quiz()
    st.session_state.answered = False

# --- ボタンが押された時の処理 ---
def click_next():
    st.session_state.quiz = get_new_quiz()
    st.session_state.answered = False

def click_answer():
    st.session_state.answered = True

# --- 画面表示 ---
st.title("AIむげんクイズ 🤖")

q = st.session_state.quiz
txt = f"【{q['genre']}】 {q['hint']}、{q['phrase']}"
st.subheader(txt)

# 問題の読み上げ
if not st.session_state.answered:
    speak(txt)

col1, col2 = st.columns(2)
with col1:
    st.button("こたえを みる", on_click=click_answer, use_container_width=True)
with col2:
    st.button("つぎの もんだい", on_click=click_next, use_container_width=True)

if st.session_state.answered:
    st.markdown(f"<h2 style='text-align: center; color: red;'>こたえ： {q['ans']}</h2>", unsafe_allow_html=True)
    speak(f"こたえは、{q['ans']} です！")
    st.balloons()
