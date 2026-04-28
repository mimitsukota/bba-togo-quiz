import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components
import time

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

# AIでクイズを作る関数（ループ防止を強化）
def get_new_quiz():
    genre = random.choice(["どうぶつ", "きょうりゅう", "ようかい"])
    phrase = random.choice(["だーれだ？", "なーにかな？", "でしょう？"])
    
    # 毎回違う結果にするために、ランダムな数字をプロンプトに混ぜます
    seed = random.randint(1, 1000)
    prompt = f"""
    番号{seed}: 5歳児向けの{genre}クイズを1問だけ作成してください。
    さっきとは違う、新しい問題にしてください。
    答えと問題文は「ひらがな」と「カタカナ」のみ。
    形式：
    答え:〇〇
    問題:〇〇
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        lines = text.split('\n')
        # 答えと問題を抽出（より柔軟に）
        ans = "？？？"
        hint = "もんだい作成中..."
        for line in lines:
            if "答え" in line or "こたえ" in line:
                ans = line.split(":")[-1].strip()
            if "問題" in line or "もんだい" in line:
                hint = line.split(":")[-1].strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "はなが ながい", "phrase": "だーれだ？"}

# --- 状態管理 ---
if 'quiz' not in st.session_state:
    st.session_state.quiz = get_new_quiz()
    st.session_state.answered = False

# --- ボタン処理 ---
def click_next():
    # 状態をリセットしてから新しい問題をセット
    st.session_state.answered = False
    st.session_state.quiz = get_new_quiz()

def click_answer():
    st.session_state.answered = True

# --- 画面表示 ---
st.title("AIむげんクイズ 🤖")

q = st.session_state.quiz
txt = f"【{q['genre']}】 {q['hint']}、{q['phrase']}"
st.subheader(txt)

if not st.session_state.answered:
    speak(txt)

col1, col2 = st.columns(2)
with col1:
    st.button("こたえを みる", on_click=click_answer, use_container_width=True)
with col2:
    # ここを押すと強制的に click_next が走ります
    st.button("つぎの もんだい", on_click=click_next, use_container_width=True)

if st.session_state.answered:
    st.markdown(f"<h2 style='text-align: center; color: red;'>こたえ： {q['ans']}</h2>", unsafe_allow_html=True)
    speak(f"こたえは、{q['ans']} です！")
    st.balloons()
