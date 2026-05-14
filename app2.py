import streamlit as st
import random

# ページの初期設定
st.set_page_config(page_title="Python カジノゲーム", page_icon="🎰", layout="centered")

# セッション状態（所持金など）の初期化
if "balance" not in st.session_state:
    st.session_state.balance = 100
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎰 カジノゲームへようこそ！")

# 現在の所持金を表示
st.metric(label="現在の所持金", value=f"${st.session_state.balance}")

if st.session_state.balance <= 0:
    st.error("💀 破産しました！ゲームオーバーです。")
    if st.button("もう一度最初からプレイする"):
        st.session_state.balance = 100
        st.session_state.history = []
        st.rerun()
else:
    # ユーザー入力エリア
    game_type = st.selectbox("1. ゲームを選択してください", ["スロットマシン", "ルーレット (赤に賭ける)", "ルーレット (黒に賭ける)"])
    bet = st.number_input(f"2. 賭け金を入力（1〜{st.session_state.balance}）", min_value=1, max_value=st.session_state.balance, value=min(10, st.session_state.balance))

    # 勝負ボタン
    if st.button("勝負する！", type="primary"):
        # --- スロットマシンの処理 ---
        if game_type == "スロットマシン":
            symbols = ["🍒", "🍋", "🍊", "🔔", "💎"]
            res = [random.choice(symbols) for _ in range(3)]
            res_str = f"[ {res[0]} | {res[1]} | {res[2]} ]"
            
            if res[0] == res[1] == res[2]:
                payout = bet * (10 if res[0] == "💎" else 5)
                st.session_state.balance += payout
                msg = f"🎰 スロット: {res_str} ➔ 🎉 大当たり！ ${payout} 獲得！"
                st.success(msg)
            elif res[0] == res[1] or res[1] == res[2] or res[0] == res[2]:
                st.session_state.balance += bet
                msg = f"🎰 スロット: {res_str} ➔ ✨ 小当たり！ ${bet} 獲得！"
                st.info(msg)
            else:
                st.session_state.balance -= bet
                msg = f"🎰 スロット: {res_str} ➔ ❌ はずれ。 ${bet} を失いました。"
                st.error(msg)
            st.session_state.history.insert(0, msg)

        # --- ルーレットの処理 ---
        elif "ルーレット" in game_type:
            guess_color = "赤" if "赤" in game_type else "黒"
            number = random.randint(0, 36)
            color = "緑" if number == 0 else ("赤" if number % 2 == 1 else "黒")
            res_str = f"出目: {number} ({color})"
            
            if guess_color == color:
                st.session_state.balance += bet
                msg = f"🎡 ルーレット: {res_str} ➔ 💰 勝ち！ ${bet} 獲得！"
                st.success(msg)
            else:
                st.session_state.balance -= bet
                msg = f"🎡 ルーレット: {res_str} ➔ ❌ 負け。 ${bet} を失いました。"
                st.error(msg)
            st.session_state.history.insert(0, msg)
        
        # 画面を更新して所持金を反映
        st.rerun()

# 履歴の表示
if st.session_state.history:
    st.subheader("📋 ゲーム履歴")
    for log in st.session_state.history[:5]: # 直近5件を表示
        st.text(log)
