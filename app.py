import streamlit as st
import random
from gtts import gTTS

# --- 1. ばあば特選！クイズリスト ---
def get_mimitsuko_quiz():
    quizzes = [
        {"genre": "きょうりゅう", "q": "つのが 3ぼんあって、かおの まわりに フリルがあるのは？", "a": "とりけらとぷす", "img": "🦖"},
        {"genre": "きょうりゅう", "q": "きょうりゅうの 王さまで、手が とっても ちいさいのは？", "a": "てぃらのさうるす", "img": "👑"},
        {"genre": "きょうりゅう", "q": "せなかに 板（いた）が たくさん 並んでいるのは？", "a": "すてごさうるす", "img": "🛡️"},
        {"genre": "きょうりゅう", "q": "頭（あたま）が とっても かたくて、ずつきが とくいなのは？", "a": "ぱきけふぁろさうるす", "img": "👷"},
        {"genre": "きょうりゅう", "q": "よろい みたいな 体で、しっぽに ハンマーが ついているのは？", "a": "あんきろさうるす", "img": "🔨"},
        {"genre": "どうぶつ", "q": "おはなが ながーくて、お耳がパタパタ。だーれだ？", "a": "ぞう", "img": "🐘"},
        {"genre": "どうぶつ", "q": "笹（ささ）を むしゃむしゃ 食べる、白と黒の くまさんは？", "a": "ぱんだ", "img": "🐼"},
        {"genre": "ようかい", "q": "頭におさらがあって、きゅうりが 大すきなのは？", "a": "かっぱ", "img": "🥒"},
    ]
    return random.choice(quizzes)

# --- 2. アプリの表示設定 ---
st.title("🦖 ばあばの 特製クイズ 🎁")

# 状態の初期化
if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_mimitsuko_quiz()
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# --- ボタン配置 ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🌟 つぎの もんだい"):
        st.session_state.my_quiz = get_mimitsuko_quiz()
        st.session_state.show_answer = False
        st.rerun()

with col2:
    if st.button("🔊 もんだいを きく"):
        tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
        tts.save("q.mp3")
        st.audio("q.mp3", autoplay=True)

# --- クイズ表示 ---
q = st.session_state.my_quiz
st.divider()
st.info(f"ジャンル：{q['genre']}")
st.write(f"## {q['q']}")
st.divider()

# --- 答えを見るボタン ---
if not st.session_state.show_answer:
    if st.button("💡 こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()

# --- 答えの表示 ---
if st.session_state.show_answer:
    st.balloons()
    st.success(f"### せいかいは・・・\n# 「{q['a']}」だよ！ {q['img']}")
    
    # 答えの音声も流すと、より盛り上がります
    if st.button("🔊 せいかいを きく"):
        tts_a = gTTS(f"せいかいは、{q['a']}だよ！", lang='ja')
        tts_a.save("a.mp3")
        st.audio("a.mp3", autoplay=True)
