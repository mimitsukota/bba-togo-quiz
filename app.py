import streamlit as st
import random
from gtts import gTTS
import os
import pandas as pd

# --- 1. クイズリストを読み込む関数 ---
def get_mimitsuko_quiz():
    try:
        df = pd.read_csv('quiz_data.csv')
        quiz_dict = df.sample(n=1).iloc[0].to_dict()
        return quiz_dict
    except Exception as e:
        backup_quizzes = [
            {"genre": "きょうりゅう", "q": "つのが さんぼんあって、かおの まわりに フリルが あるのは？", "a": "とりけらとぷす", "img": "🦖"},
            {"genre": "ようかい", "q": "あたまに おさらが あって、きゅうりが だいすきなのは？", "a": "かっぱ", "img": "🥒"},
            {"genre": "ようかい", "q": "ふるい ちょうちんが ばけもので、ぺろっと したを だしているのは？", "a": "ちょうちんおばけ", "img": "🏮"}
        ]
        return random.choice(backup_quizzes)

# --- 2. 状態の初期化 ---
if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_mimitsuko_quiz()
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'play_audio' not in st.session_state:
    st.session_state.play_audio = None

st.title("🎓 とうごはかせの てんさいクイズ 🦖")

# --- つぎのもんだい ボタン（上） ---
if st.button("🌟 つぎの もんだい", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.session_state.play_audio = "q.mp3"
    st.rerun()

# --- クイズ表示エリア ---
q = st.session_state.my_quiz
st.divider()

# ジャンルを大きく太字で表示
st.markdown(f"## 🏷️ **{q['genre']}**")
# 問題文を表示
st.write(f"### {q['q']}")

# --- こたえをみる ボタン ---
if not st.session_state.show_answer:
    if st.button("💡 こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        a_text = f"せいかいは、{q['a']} だよ。"
        tts = gTTS(a_text, lang='ja')
        tts.save("a.mp3")
        st.session_state.play_audio = "a.mp3"
        st.rerun()

# --- 答えの表示 ---
if st.session_state.show_answer:
    st.success(f"### せいかい！\n# 「{q['a']}」だよ！")
    
    # 画像の表示
    if 'url' in q and pd.notnull(q['url']):
        st.image(q['url'], caption=f"ほんものの {q['a']}", use_container_width=True)
    
    st.write(f"つぎの もんだいも がんばろう！")

# --- 音声再生の実行 ---
if st.session_state.play_audio:
    st.audio(st.session_state.play_audio, autoplay=True)
    st.session_state.play_audio = None

# --- 画面の一番下にも「つぎのもんだい」ボタンを追加 ---
if st.session_state.show_answer:
    st.divider()
    if st.button("🌟 つぎの もんだいへ！", key="bottom_button", use_container_width=True):
        st.session_state.my_quiz = get_mimitsuko_quiz()
        st.session_state.show_answer = False
        tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
        tts.save("q.mp3")
        st.session_state.play_audio = "q.mp3"
        st.rerun()
