import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 初期設定 ---
# 秘密のキーを読み込み
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("APIキーが 設定されていません。")
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

# AIでクイズを作る（キャッシュしないように工夫）
def get_new_quiz():
    genre = random.choice(["どうぶつ", "きょうりゅう", "ようかい"])
    phrase = random.choice(["だーれだ？", "なーにかな？", "でしょう？"])
    # 毎回違う指示にするための魔法の数字
    seed = random.randint(1, 10000)
    prompt = f"命令{seed}: 5歳児向けの{genre}クイズを1問。答えと問題をひらがなのみで。形式：答え:〇〇 改行 問題:〇〇"
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        ans = lines[0].split(":")[-1].strip()
        hint = lines[1].split(":")[-1].strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "はなが ながい", "phrase": "だーれだ？"}

# --- 画面の表示管理 ---
# ここで「今の問題」をしっかり保存します
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = get_new_quiz()
    st.session_state.is_answered = False

st.title("AIむげんクイズ 🤖")

q = st.session_state.quiz_data
full_question = f"【{q['genre']}】 {q['hint']}、{q['phrase']}"

st.subheader(full_question)

# 問題の読み上げ（答えが出ていない時だけ）
if not st.session_state.is_answered:
    speak(full_question)

# --- ボタン ---
col1, col2 = st.columns(2)

with col1:
    # 答えを見るボタン：押すと answered を True にして再描画
    if st.button("こたえを みる", use_container_width=True, key="ans_btn"):
        st.session_state.is_answered = True
        st.rerun()

with col2:
    # つぎの問題ボタン：押すと 新しい問題を生成して再描画
    if st.button("つぎの もんだい", use_container_width=True, key="next_btn"):
        st.session_state.quiz_data = get_new_quiz()
        st.session_state.is_answered = False
        st.rerun()

# --- 答えの表示 ---
if st.session_state.is_answered:
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>こたえ： {q['ans']}</h1>", unsafe_allow_html=True)
    speak(f"こたえは、{q['ans']} です！")
    st.balloons()
