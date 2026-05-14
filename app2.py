<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python カジノゲーム</title>
    <!-- PyScriptの読み込み -->
    <link rel="stylesheet" href="pyscript.net">
    <script type="module" src="pyscript.net"></script>
    <style>
        body { font-family: sans-serif; background: #222; color: #fff; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: 0 auto; background: #333; padding: 20px; border-radius: 10px; }
        input, button, select { padding: 10px; margin: 10px 5px; font-size: 16px; border-radius: 5px; border: none; }
        button { background: #28a745; color: white; cursor: pointer; }
        button:hover { background: #218838; }
        #log { background: #111; padding: 15px; border-radius: 5px; text-align: left; height: 200px; overflow-y: auto; font-family: monospace; white-space: pre-wrap; }
    </style>
</head>
<body>

<div class="container">
    <h2>🎰 カジノゲーム 🎰</h2>
    <div>現在の所持金: <span id="balance_display" style="color: #ffc107; font-weight: bold; font-size: 20px;">$100</span></div>
    
    <hr style="border-color: #444;">

    <div>
        <label>1. ゲーム選択: </label>
        <select id="game_type">
            <option value="slots">スロットマシン</option>
            <option value="roulette_red">ルーレット (赤に賭ける)</option>
            <option value="roulette_black">ルーレット (黒に賭ける)</option>
        </select>
    </div>

    <div>
        <label>2. 賭け金を入力: </label>
        <input type="number" id="bet_input" value="10" min="1" style="width: 80px;">
    </div>

    <button id="play_btn">勝負する！</button>

    <h3>📋 ゲーム履歴</h3>
    <div id="log">カジノへようこそ！ゲームを選んで「勝負する！」を押してください。</div>
</div>

<!-- Pythonロジックの埋め込み -->
<script type="py">
import random
from pyscript import document

# グローバル変数で所持金を管理
balance = 100

def update_ui(msg):
    global balance
    document.querySelector("#balance_display").innerText = f"${balance}"
    log_div = document.querySelector("#log")
    log_div.innerText = msg + "\n" + log_div.innerText

def play_game(event):
    global balance
    if balance <= 0:
        update_ui("【ゲームオーバー】破産しています。ページを再読み込みしてください。")
        return

    # 入力値の取得
    try:
        bet = int(document.querySelector("#bet_input").value)
    except ValueError:
        update_ui("【エラー】有効な賭け金を入力してください。")
        return

    if bet <= 0 or bet > balance:
        update_ui(f"【エラー】無効な賭け金です（所持金: ${balance}）")
        return

    game_type = document.querySelector("#game_type").value

    # --- スロットマシンの処理 ---
    if game_type == "slots":
        symbols = ["🍒", "🍋", "🍊", "🔔", "💎"]
        res = [random.choice(symbols) for _ in range(3)]
        res_str = f"[ {res[0]} | {res[1]} | {res[2]} ]"
        
        if res[0] == res[1] == res[2]:
            payout = bet * 10 if res[0] == "💎" else bet * 5
            balance += payout
            msg = f"🎰 スロット: {res_str}\n🎉 大当たり！ ${payout} を獲得しました！"
        elif res[0] == res[1] or res[1] == res[2] or res[0] == res[2]:
            balance += bet
            msg = f"🎰 スロット: {res_str}\n✨ 小当たり！ ${bet} を獲得しました。"
        else:
            balance -= bet
            msg = f"🎰 スロット: {res_str}\n❌ はずれ。 ${bet} を失いました。"

    # --- ルーレットの処理 ---
    elif "roulette" in game_type:
        guess_color = "赤" if "red" in game_type else "黒"
        number = random.randint(0, 36)
        color = "緑" if number == 0 else ("赤" if number % 2 == 1 else "黒")
        
        res_str = f"出目: {number} ({color})"
        if guess_color == color:
            balance += bet
            msg = f"🎡 ルーレット: {res_str}\n💰 勝ち！ ${bet} を獲得しました。"
        else:
            balance -= bet
            msg = f"🎡 ルーレット: {res_str}\n❌ 負け。 ${bet} を失いました。"

    if balance <= 0:
        msg += "\n💀 破産しました！ゲームオーバーです。"

    update_ui(msg)

# ボタンにPython関数を紐付け
document.querySelector("#play_btn").onclick = play_game
</script>

</body>
</html>
