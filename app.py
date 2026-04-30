import streamlit as st
import random
from gtts import gTTS
import os
import pandas as pd

# --- 1. クイズリストを読み込む関数 ---
def get_mimitsuko_quiz():
    try:
        # CSVを読み込む（5つの項目：genre,q,a,img,url）
        df = pd.read_csv('quiz_data.csv')
        # ランダムに1問選んで辞書形式にする
        quiz_dict = df.sample(n=1).iloc[0].to_dict()
        return quiz_dict
    except Exception as e:
        # もし読み込みに失敗した時のバックアップ
        backup_quizzes = [
            {"genre": "きょうりゅう", "q": "つのが さんぼんあって、かおの まわりに フリルが あるのは？", "a": "とりけらとぷす", "img": "🦖", "url": "1-27529180.jpg"},
            {"genre": "ようかい", "q": "あたまに おさらが あって、きゅうりが だいすきなのは？", "a": "かっぱ", "img": "🥒", "url": "41.JPG"},
            {"genre": "ようかい", "q": "ふるい ちょうちんが ばけもので、ぺろっと したを だしているのは？", "a": "ちょうちんおばけ", "img": "🏮", "url": "59.JPG"}
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

# --- つぎのもんだい ボタン ---
if st.button("🌟 つぎの もんだい", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    # 問題の音声を生成
    tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.session_state.play_audio = "q.mp3"
    st.rerun()

# --- クイズ表示エリア ---
q = st.session_state.my_quiz
st.divider()

# ジャンルの表示
st.markdown(f"## 🏷️ **{q['genre']}**") 

# 問題文の表示（1回だけにしました！）
st.write(f"### {q['q']}")

# --- こたえをみる ボタン ---
if not st.session_state.show_answer:
    if st.button("💡 こたえを みる", use_container_width=True):
        st.session_state.show_answer = True
        # 音声を生成
        a_text = f"せいかいは、{q['a']} だよ。"
        tts = gTTS(a_text, lang='ja')
        tts.save("a.mp3")
        st.session_state.play_audio = "a.mp3"
        st.rerun()

# --- 答えと写真の表示 ---
if st.session_state.show_answer:
    st.success(f"### せいかい！\n# 「{q['a']}」だよ！")
    
    # 画像（url）を表示する設定
    if 'url' in q and pd.notnull(q['url']):
        # GitHub上の画像ファイルを読み込んで表示
        st.image(q['url'], caption=f"ほんものの {q['a']}", use_container_width=True)
    
    st.write(f"つぎの もんだいも がんばろう！")

# --- 音声再生の実行 ---
if st.session_state.play_audio:
    st.audio(st.session_state.play_audio, autoplay=True)
    st.session_state.play_audio = None

# --- 画面の下にもボタンを追加 ---
st.divider()
if st.button("🌟 つぎの もんだいへ！", key="bottom_button", use_container_width=True):
    st.session_state.my_quiz = get_mimitsuko_quiz()
    st.session_state.show_answer = False
    tts = gTTS(st.session_state.my_quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.session_state.play_audio = "q.mp3"
    st.rerun()
