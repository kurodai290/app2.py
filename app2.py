import time
import random

def start_game():
    print("--- げぇむ『てんびん』を開始します ---")
    print("ルール: 0〜100の中から数字を選んでください。")
    print("勝者: 全員の平均値に『0.8』を掛けた値に最も近い人。")
    print("脱落: ポイントが -10 になると『秤』から水が溢れ、敗北となります。\n")

    # 初期設定
    user_name = input("あなたの名前を入力してください: ")
    bot_names = ["Bot_チシヤ", "Bot_クズリュウ", "Bot_アン"]
    
    # プレイヤーの初期化（名前: ポイント）
    players = {user_name: 0}
    for name in bot_names:
        players[name] = 0

    round_count = 1

    while len(players) > 1:
        print(f"\n========================")
        print(f"      第 {round_count} 回戦")
        print(f"========================")
        
        # 現在のポイント表示
        print("[現在のポイント]")
        for name, pt in players.items():
            print(f" {name}: {pt}pt")
        print("------------------------")

        choices = {}

        # ユーザーの入力
        while True:
            try:
                val = float(input(f"[{user_name}] 0〜100の数字を入力: "))
                if 0 <= val <= 100:
                    choices[user_name] = val
                    break
                print("範囲外です。0から100の間で入力してください。")
            except ValueError:
                print("有効な数字を入力してください。")

        # Botの入力 (戦略的思考: 平均は徐々に下がっていく傾向をシミュレート)
        for name in list(players.keys()):
            if name == user_name: continue
            
            # 回が進むごとに低い数字を狙う戦略
            if round_count == 1:
                choices[name] = random.uniform(0, 100 * 0.8)
            else:
                # 前回の平均より少し下を狙う
                choices[name] = random.uniform(0, 50) 
            
            print(f"[{name}] が数字を決定しました。")

        # 計算フェーズ
        total_val = sum(choices.values())
        average = total_val / len(choices)
        target = average * 0.8
        
        print(f"\n集計中...")
        time.sleep(1.5)
        print(f"平均値: {average:.2f}")
        print(f"設定数値 (平均×0.8): {target:.2f}")
        print("------------------------")

        # 勝者の判定（ターゲットに最も近い人）
        # 各プレイヤーのターゲットとの差を計算
        diffs = {name: abs(val - target) for name, val in choices.items()}
        winner = min(diffs, key=diffs.get)

        # 結果表示とポイント減算
        print(f"各プレイヤーの選択: { {k: round(v, 2) for k, v in choices.items()} }")
        print(f"\n勝者: {winner}！ (差: {diffs[winner]:.2f})")

        # 勝者以外は-1ポイント
        for name in list(players.keys()):
            if name != winner:
                players[name] -= 1

        # 脱落判定
        losers = [name for name, pt in players.items() if pt <= -10]
        for loser in losers:
            print(f"\n※※※ 警告 ※※※")
            print(f"{loser} の秤から水が溢れました。脱落です。")
            del players[loser]

        if user_name not in players:
            print("\n--- GAME OVER ---")
            print("あなたは死にました。")
            break

        if len(players) == 1 and user_name in players:
            print(f"\n★★★ CONGRATULATIONS ★★★")
            print(f"おめでとうございます、{user_name}。あなたは生き残りました。")
            break

        round_count += 1
        time.sleep(1)

if __name__ == "__main__":
    start_game()
