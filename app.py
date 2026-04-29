import streamlit as st
import random
from gtts import gTTS
import os
import pandas as pd

# --- 1. エクセル(CSV)からクイズを読み込む設定に変更！ ---
def get_mimitsuko_quiz():
    try:
        # ここで、アップロードした quiz_data.csv を読み込みます
        df = pd.read_csv('quiz_data.csv')
        # その中からランダムに1行選んでクイズにします
        quiz_dict = df.sample(n=1).iloc[0].to_dict()
        return quiz_dict
    except Exception as e:
        # もし読み込みに失敗した時のための予備（保険です）
        return {"genre": "きょうりゅう", "q": "つのが さんぼんあるのは？", "a": "とりけらとぷす", "img": "🦖"}

# --- 2. 状態の初期化 ---
if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_mimitsuko_quiz()
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'play_audio' not in st.session_state:
    st.session_state.play_audio = None

st.title("🎓 とうごはかせの てんさいクイズ 🦖")

# --- つぎのもんだい ボタン ---
if st.button("🌟 つぎの もんだい", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    # 問題の音声を作成
    tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.session_state.play_audio = "q.mp3"
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
        # 答えの音声を作成
        a_text = f"せいかいは、{q['a']} だよ！ さすが とうごはかせ！"
        tts = gTTS(a_text, lang='ja')
        tts.save("a.mp3")
        st.session_state.play_audio = "a.mp3"
        st.rerun()

# --- 答えの表示 ---
if st.session_state.show_answer:
    st.balloons()
    st.success(f"### せいかい！\n# 「{q['a']}」だよ！ {q['img']}\n\nさすが とうごはかせだね！")

# --- 音声再生の実行 ---
if st.session_state.play_audio:
    st.audio(st.session_state.play_audio, autoplay=True)
    st.session_state.play_audio = None
