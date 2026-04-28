import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- セキュリティ設定 ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("APIキーの設定を確認してください。")
    st.stop()

st.set_page_config(page_title="AIむげんクイズ", layout="centered")

# 音声読み上げ用
def speak(text):
    if text:
        components.html(f"""
            <script>
                var msg = new SpeechSynthesisUtterance('{text}');
                msg.lang = 'ja-JP';
                window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

# AIに問題を頼む関数
def generate_quiz():
    genre = random.choice(["どうぶつ", "きょうりゅう", "ようかい"])
    phrase = random.choice(["だーれだ？", "なーにかな？", "でしょう？"])
    
    prompt = f"{genre}のクイズを1問。答えと問題をひらがなのみで。出力形式：答え:〇〇 改行 問題:〇〇"
    
    try:
        # 「考え中」の表示を出すためにスピンを入れる
        with st.spinner('AIが もんだいを かんがえ中...'):
            response = model.generate_content(prompt)
            lines = response.text.strip().split('\n')
            ans = lines[0].replace("答え:", "").replace("こたえ:", "").strip()
            hint = lines[1].replace("問題:", "").replace("もんだい:", "").strip()
            return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "はなが ながい", "phrase": "だーれだ？"}

# 状態管理
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = generate_quiz()
    st.session_state.show_answer = False

st.title("AIむげんクイズ 🤖")

quiz = st.session_state.current_quiz
question_full = f"【{quiz['genre']}】 {quiz['hint']}、{quiz['phrase']}"

st.subheader(question_full)

# 読み上げ（答えが出ていない時だけ）
if not st.session_state.show_answer:
    speak(question_full)

col1, col2 = st.columns(2)

with col1:
    if st.button("こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()

with col2:
    if st.button("つぎの もんだい", use_container_width=True):
        # ここで新しい問題を生成
        st.session_state.current_quiz = generate_quiz()
        st.session_state.show_answer = False
        st.rerun()

if st.session_state.show_answer:
    st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>こたえ： {quiz['ans']}</h2>", unsafe_allow_html=True)
    speak(f"こたえは、{quiz['ans']} です！")
    st.balloons()
