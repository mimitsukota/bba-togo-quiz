import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 初期設定 ---
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
    # AIに「ランダムな数値」を渡して、毎回違う答えを強制する
    prompt = f"乱数{random.randint(1,999)}: 5歳児向けの{genre}クイズを1問。答えと問題をひらがなのみで。形式：答え:〇〇 改行 問題:〇〇"
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        ans = lines[0].split(":")[-1].strip()
        hint = lines[1].split(":")[-1].strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "はなが ながい", "phrase": "だーれだ？"}

# --- アプリのメイン処理 ---

# 1. 最初の問題を準備
if 'quiz' not in st.session_state:
    st.session_state.quiz = get_new_quiz()
    st.session_state.answered = False

st.title("AIむげんクイズ 🤖")

q = st.session_state.quiz
txt = f"【{q['genre']}】 {q['hint']}、{q['phrase']}"
st.subheader(txt)

# 問題の読み上げ（答えが出ていない時だけ）
if not st.session_state.answered:
    speak(txt)

# 2. ボタンの処理
col1, col2 = st.columns(2)

with col1:
    # 答えを見るボタン
    if st.button("こたえを みる", use_container_width=True):
        st.session_state.answered = True
        st.rerun() # 画面を強制的に書き換えて答えを出す

with col2:
    # つぎの問題ボタン
    if st.button("つぎの もんだい", use_container_width=True):
        st.session_state.quiz = get_new_quiz() # 新しい問題をAIに作らせる
        st.session_state.answered = False     # 答えを隠す
        st.rerun() # 画面を強制的に書き換えて新しい問題を出す

# 3. 答えの表示
if st.session_state.answered:
    st.markdown(f"<h1 style='text-align: center; color: red;'>こたえ： {q['ans']}</h1>", unsafe_allow_html=True)
    speak(f"こたえは、{q['ans']} です！")
    st.balloons()
