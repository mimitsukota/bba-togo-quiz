import streamlit as st
import random
from gtts import gTTS
import os

# --- 1. クイズリスト（すべて ひらがな） ---
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

# --- 2. 状態の初期化 ---
if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_mimitsuko_quiz()
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'play_audio' not in st.session_state:
    st.session_state.play_audio = None

# タイトルを「とうごはかせのてんさいクイズ」に変更！
st.title("🎓 とうごはかせの てんさいクイズ 🦖")

# --- つぎのもんだい ボタン ---
if st.button("🌟 つぎの もんだい", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.session_state.play_audio = "q.mp3"
    st.rerun()

# --- クイズ表示 ---
q = st.session_state.my_quiz
st.divider()
st.info(f"じゃんる：{q['genre']}")
st.write(f"## {q['q']}")

# --- こたえをみる ボタン ---
if not st.session_state.show_answer:
    if st.button("💡 こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        a_text = f"せいかいは、{q['a']} だよ！ さすが とうごはかせ！"
        tts = gTTS(a_text, lang='ja')
        tts.save("a.mp3")
        st.session_state.play_audio = "a.mp3"
        st.rerun()

# --- 答えの表示 ---
if st.session_state.show_answer:
    st.balloons()
    # メッセージも博士向けに
    st.success(f"### せいかい！\n# 「{q['a']}」だよ！ {q['img']}\n\nさすが とうごはかせだね！")

# --- 音声再生 ---
if st.session_state.play_audio:
    st.audio(st.session_state.play_audio, autoplay=True)
    st.session_state.play_audio = None
