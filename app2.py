import streamlit as st
import pandas as pd

st.set_page_config(page_title="ローカル対戦：0.8倍サバイバル", page_icon="⚖️")

# --- セッション状態の初期化 ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False,
        'players': [],
        'round': 1,
        'submitted_count': 0,
        'current_inputs': {}, # {名前: 数値}
        'history': []
    })

# --- ゲーム管理関数 ---
def start_game(names):
    st.session_state.players = [{"name": name.strip(), "points": 0} for name in names if name.strip()]
    st.session_state.game_active = True
    st.session_state.round = 1
    st.session_state.current_inputs = {}
    st.session_state.submitted_count = 0

# --- メインUI ---
st.title("⚖️ 0.8倍狙い！ローカル対戦")

if not st.session_state.game_active:
    st.subheader("プレイヤー登録")
    player_names = st.text_area("参加者の名前を改行して入力してください", "プレイヤー1\nプレイヤー2\nプレイヤー3")
    if st.button("ゲーム開始"):
        start_game(player_names.split('\n'))
        st.rerun()

else:
    # サイドバー：現在のスコア
    st.sidebar.header("現在のスコア")
    for p in st.session_state.players:
        st.sidebar.write(f"{p['name']}: {p['points']} pt")
    if st.sidebar.button("タイトルに戻る"):
        st.session_state.game_active = False
        st.rerun()

    st.subheader(f"第 {st.session_state.round} ラウンド")
    
    # 順番に入力
    current_player_idx = st.session_state.submitted_count
    
    if current_player_idx < len(st.session_state.players):
        current_player = st.session_state.players[current_player_idx]["name"]
        
        with st.form(key=f"input_form_{current_player_idx}"):
            st.write(f"👉 **{current_player}** さんの番です")
            # 秘密の入力（type="password"で数字を隠す）
            val = st.number_input("自分の数字を入力 (0.0 - 100.0)", 0.0, 100.0, step=0.1, key=f"in_{current_player}")
            st.caption("※入力中、他の人は画面を見ないでください！")
            
            if st.form_submit_button("数値を確定して次の人へ"):
                st.session_state.current_inputs[current_player] = val
                st.session_state.submitted_count += 1
                st.rerun()
    else:
        # --- 全員の入力完了後の結果計算 ---
        st.success("全員の入力が完了しました！")
        if st.button("結果を見る"):
            results = st.session_state.current_inputs
            vals = list(results.values())
            avg = sum(vals) / len(vals)
            target = avg * 0.8
            
            # 勝者判定
            # 重複チェック
            counts = {v: vals.count(v) for v in set(vals)}
            
            summary = []
            valid_players = []
            for name, val in results.items():
                p_ref = next(p for p in st.session_state.players if p["name"] == name)
                if counts[val] > 1:
                    p_ref["points"] -= 2
                    summary.append({"名前": name, "数値": val, "判定": "❌ 被り(-2pt)"})
                else:
                    valid_players.append({"name": name, "val": val, "player": p_ref})
            
            winner_name = "なし"
            if valid_players:
                # 0と100の特殊ルール
                has_zero = any(d["val"] == 0 for d in valid_players)
                has_hundred = any(d["val"] == 100 for d in valid_players)
                
                if has_zero and has_hundred:
                    winner_data = random.choice([d for d in valid_players if d["val"] == 100])
                elif has_zero:
                    winner_data = random.choice([d for d in valid_players if d["val"] == 0])
                else:
                    winner_data = min(valid_players, key=lambda x: abs(x["val"] - target))
                
                winner_name = winner_data["name"]
                for d in valid_players:
                    if d["name"] == winner_name:
                        summary.append({"名前": d["name"], "数値": d["val"], "判定": "🏆 勝利！"})
                    else:
                        d["player"]["points"] -= 1
                        summary.append({"名前": d["name"], "数値": d["val"], "判定": "敗北(-1pt)"})
            
            # 結果表示
            st.divider()
            st.info(f"平均: {avg:.2f}  →  **ターゲット(×0.8): {target:.2f}**")
            st.table(pd.DataFrame(summary))
            
            if any(p["points"] <= -5 for p in st.session_state.players):
                st.error("🏁 誰かのポイントが-5に達したため、ゲーム終了です！")
                if st.button("もう一度遊ぶ"):
                    st.session_state.game_active = False
                    st.rerun()
            else:
                if st.button("次のラウンドへ"):
                    st.session_state.round += 1
                    st.session_state.submitted_count = 0
                    st.session_state.current_inputs = {}
                    st.rerun()
      
