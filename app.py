
import streamlit as st
import random
from gtts import gTTS
import os
import pandas as pd

# --- 1. クイズリストを読み込む関数 ---
def get_mimitsuko_quiz():
    try:
        # GitHubにアップロードした quiz_data.csv を読み込みます
        df = pd.read_csv('quiz_data.csv')
        # ランダムに1行選んで辞書形式にします
        quiz_dict = df.sample(n=1).iloc[0].to_dict()
        return quiz_dict
    except Exception as e:
        # 万が一CSVが読み込めなかった時のための「保険」のリスト
        # mimitsukoさんの最新の修正（削除と修正）を反映済みです
        backup_quizzes = [
            {"genre": "きょうりゅう", "q": "つのが さんぼんあって、かおの まわりに フリルが あるのは？", "a": "とりけらとぷす", "img": "🦖"},
            {"genre": "きょうりゅう", "q": "きょうりゅうの おうさまで、てが とっても ちいさいのは？", "a": "てぃらのさうるす", "img": "👑"},
            {"genre": "どうぶつ", "q": "おはなが ながーくて、おみみが パタパタ。だーれだ？", "a": "ぞう", "img": "🐘"},
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

# --- 答えの表示（画像対応の準備もしておきました） ---
if st.session_state.show_answer:
    st.balloons()
    st.success(f"### せいかい！\n# 「{q['a']}」だよ！")
    
    # 明日の画像作業のために、表示する仕組みだけ作っておきました
    if 'url' in q and pd.notnull(q['url']):
        # CSVのurl列にファイル名が入っていれば表示されます
        st.image(q['url'], caption=f"ほんものの {q['a']}", use_container_width=True)
    
    st.write(f"さすが とうごはかせだね！")

# --- 音声再生の実行 ---
if st.session_state.play_audio:
    st.audio(st.session_state.play_audio, autoplay=True)
    st.session_state.play_audio = None
