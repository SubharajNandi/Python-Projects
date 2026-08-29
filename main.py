# Day 1 - 29th August 2026
# Mini Project 1 - Text Based slot machine Program

import random

symbols = ["🍒", "🍋", "💲"]

balance = 100

while balance > 0:

    print("\n==================")
    print("SLOT MACHINE")
    print("==================")

    print(f"Balance: ${balance}")

    try:
        bet = int(input("Enter your Bet: $"))
    except ValueError:
        print("Plese enter a valid Number.")
        continue

    if bet <= 0:
        print("Bet must be greater than 0.")
        continue

    if bet > balance:
        print("Insufficient Balance.")
        continue

    balance -= bet
    
    result = []

    for _ in range(3):
        result.append(random.choice(symbols))

    print("\nSpinning...")
    print("| " + " | ".join(result) + " |")

    if result[0] == result[1] == result[2]:
        winnings = bet * 3
        balance += winnings

        print(f"fJACKPOT! You Won ${winnings}!")

    else:
        print(f"You lost ${bet}.")

    if balance == 0:
        print("\nYou ran out of money!")
        break

    play_again = input("\nPlay again? (Y/n): ")

    if play_again.upper() != "Y":
        break

    print(f"\nFinal balace: ${balance}")
    print("Thanks for Playing!")