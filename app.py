import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- セキュリティ設定 ---
# Streamlit CloudのSecretsからAPIキーを読み込む設定です
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("APIキーの設定を確認してください。")
    st.stop()

st.set_page_config(page_title="AIむげんクイズ", layout="centered")

# 音声読み上げ用のJavaScript
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
    
    prompt = f"""
    5歳児向けのクイズを1問作ってください。
    ジャンル: {genre}
    ルール：
    1. 答えは子供が知っている有名なもの。
    2. 全てひらがなとカタカナのみ。
    3. 特徴を1行で。
    出力形式：
    答え:（ここに答え）
    問題:（ここに特徴）
    """
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        ans = lines[0].replace("答え:", "").replace("こたえ:", "").strip()
        hint = lines[1].replace("問題:", "").replace("もんだい:", "").strip()
        return {"genre": genre, "ans": ans, "hint": hint, "phrase": phrase}
    except:
        return {"genre": "どうぶつ", "ans": "ぞう", "hint": "おなかが ながくて おおきい", "phrase": "だーれだ？"}

# 状態管理
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = generate_quiz()
    st.session_state.show_answer = False

# 画面表示
st.title("AIむげんクイズ 🤖")
st.write("5さいの おともだちへ！")

quiz = st.session_state.current_quiz
question_full = f"【{quiz['genre']}】 {quiz['hint']}、{quiz['phrase']}"

st.subheader(question_full)

# 読み上げ（未回答の時だけ自動読み上げ）
if not st.session_state.show_answer:
    speak(question_full)

col1, col2 = st.columns(2)

with col1:
    if st.button("こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        speak(f"こたえは、{quiz['ans']} です！")

with col2:
    if st.button("つぎの もんだい", use_container_width=True):
        # 次の問題を生成してリセット
        st.session_state.current_quiz = generate_quiz()
        st.session_state.show_answer = False
        st.rerun()

if st.session_state.show_answer:
    st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>こたえ： {quiz['ans']}</h2>", unsafe_allow_html=True)
    st.balloons()
