import streamlit as st

st.set_page_config(page_title="カジノロビー", page_icon="🏦", layout="centered")

# 全ページ共通の所持金システム
if "balance" not in st.session_state:
    st.session_state.balance = 100
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🏦 ネットカジノ・ロビー")
st.write("左側のメニューから遊びたいゲームのページを選んでください。")

st.markdown("---")
st.metric(label="現在の総資産", value=f"${st.session_state.balance}")

if st.session_state.balance <= 0:
    st.error("💀 破産しました！")
    if st.button("手元金を$100に戻す"):
        st.session_state.balance = 100
        st.session_state.history = []
        st.rerun()

# 履歴表示
if st.session_state.history:
    st.subheader("📋 全ゲーム総合履歴")
    for log in st.session_state.history[:5]:
        st.text(log)
