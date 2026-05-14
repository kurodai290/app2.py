import random

def play_slots(balance):
    print("\n--- スロットマシン ---")
    try:
        bet = int(input(f"賭け金を入力（所持金: ${balance}）: "))
    except ValueError:
        return balance
    
    if bet <= 0 or bet > balance:
        print("無効な賭け金です。")
        return balance

    symbols = ["🍒", "🍋", "🍊", "🔔", "💎"]
    result = [random.choice(symbols) for _ in range(3)]
    print(f"結果: [ {result[0]} | {result[1]} | {result[2]} ]")

    if result[0] == result[1] == result[2]:
        payout = bet * 10 if result[0] == "💎" else bet * 5
        print(f"大当たり！ ${payout} を獲得しました！")
        return balance + payout
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        print(f"小当たり！ ${bet} を獲得しました。")
        return balance + bet
    else:
        print(f"はずれ。 ${bet} を失いました。")
        return balance - bet

def play_roulette(balance):
    print("\n--- ルーレット ---")
    try:
        bet = int(input(f"賭け金を入力（所持金: ${balance}）: "))
    except ValueError:
        return balance

    if bet <= 0 or bet > balance:
        print("無効な賭け金です。")
        return balance

    print("賭け方を選択:")
    print("1: 赤に賭ける")
    print("2: 黒に賭ける")
    choice = input("選択 (1-2): ")

    number = random.randint(0, 36)
    color = "赤" if number % 2 == 1 and number != 0 else "黒"
    if number == 0:
        color = "緑"

    print(f"出目: {number} ({color})")

    if (choice == "1" and color == "赤") or (choice == "2" and color == "黒"):
        print(f"勝ち！ ${bet} を獲得しました。")
        return balance + bet
    else:
        print(f"負け。 ${bet} を失いました。")
        return balance - bet

def main():
    balance = 100
    print("★ カジノゲームへようこそ！ ★")

    while balance > 0:
        print(f"\n現在の所持金: ${balance}")
        print("1: スロット")
        print("2: ルーレット")
        print("3: 終了する")
        
        choice = input("ゲームを選択 (1-3): ")
        if choice == "1":
            balance = play_slots(balance)
        elif choice == "2":
            balance = play_roulette(balance)
        elif choice == "3":
            print("カジノを出ます。お疲れ様でした！")
            break
        else:
            print("無効な入力です。")

    if balance <= 0:
        print("\n破産しました！ゲームオーバーです。")

if __name__ == "__main__":
    main()
