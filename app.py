import streamlit as st
import random
from gtts import gTTS
import os

# --- 1. ばあば特選！クイズリスト（ぜんぶ ひらがな） ---
def get_mimitsuko_quiz():
    quizzes = [
        {"genre": "きょうりゅう", "q": "つのが さんぼんあって、かおの まわりに フリルが あるのは？", "a": "とりけらとぷす", "img": "🦖"},
        {"genre": "きょうりゅう", "q": "きょうりゅうの おうさまで、てが とっても ちいさいのは？", "a": "てぃらのさうるす", "img": "👑"},
        {"genre": "きょうりゅう", "q": "せなかに いたが たくさん ならんでいるのは？", "a": "すてごさうるす", "img": "🛡️"},
        {"genre": "きょうりゅう", "q": "あたまが とっても かたくて、ずつきが とくいなのは？", "a": "ぱきけふぁろさうるす", "img": "👷"},
        {"genre": "きょうりゅう", "q": "よろい みたいな からだで、しっぽに はんまーが ついているのは？", "a": "あんきろさうるす", "img": "🔨"},
        {"genre": "きょうりゅう", "q": "くびが とーっても ながくて、からだが おおきいのは？", "a": "ぶらきおさうるす", "img": "🦒"},
        {"genre": "どうぶつ", "q": "おはなが ながーくて、おみみが パタパタ。だーれだ？", "a": "ぞう", "img": "🐘"},
        {"genre": "どうぶつ", "q": "ささを むしゃむしゃ たべる、しろと くろの くまさんは？", "a": "ぱんだ", "img": "🐼"},
        {"genre": "ようかい", "q": "あたまに おさらが あって、きゅうりが だいすきなのは？", "a": "かっぱ", "img": "🥒"},
    ]
    return random.choice(quizzes)

# 音声ファイル作成関数
def speak(text, filename):
    tts = gTTS(text, lang='ja')
    tts.save(filename)
    return filename

# --- 2. アプリの表示設定 ---
st.title("🦖 ばあばの 特製クイズ 🎁")

# 状態の初期化
if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_mimitsuko_quiz()
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# --- つぎのもんだい ボタン ---
if st.button("🌟 つぎの もんだい", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    # 問題の音声を作成して再生
    q_file = speak(st.session_state.my_quiz['q'], "q.mp3")
    st.audio(q_file, autoplay=True)
    st.rerun()

# --- クイズ表示エリア ---
q = st.session_state.my_quiz
st.divider()
st.info(f"じゃんる：{q['genre']}")
st.write(f"## {q['q']}")

# --- こたえをみる ボタン ---
if not st.session_state.show_answer:
    if st.button("💡 こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        # 答えの音声を作成して再生
        a_text = f"せいかいは、{q['a']} だよ！"
        a_file = speak(a_text, "a.mp3")
        st.audio(a_file, autoplay=True)
        st.rerun()

# --- 答えの表示 ---
if st.session_state.show_answer:
    st.balloons()
    st.success(f"### せいかいは・・・\n# 「{q['a']}」だよ！ {q['img']}")
    # 答えが表示されている間、もう一度音声を聴けるボタン
    if st.button("🔊 もういちど きく"):
        st.audio("a.mp3", autoplay=True)
