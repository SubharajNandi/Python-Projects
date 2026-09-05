import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    """Load expenses from JSON. Return an empty list if the file doesn't exist."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expenses.json. Starting with no expenses.")
        return []


def save_expenses(expenses):
    """Save expenses to JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_amount():
    while True:
        try:
            amount = float(input("Amount (₹): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def get_date():
    while True:
        date_text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()

        if not date_text:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def add_expense(expenses):
    print("\n--- Add Expense ---")

    amount = get_amount()
    category = input("Category: ").strip().title()
    description = input("Description: ").strip()
    date = get_date()

    if not category:
        category = "Other"

    if not description:
        description = "No description"

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. ₹{expense['amount']:.2f} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"{expense['date']}"
        )


def total_expenses(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal spending: ₹{total:.2f}")


def category_summary(expenses):
    print("\n--- Spending by Category ---")

    if not expenses:
        print("No expenses recorded.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{category:<15} ₹{amount:.2f}")


def biggest_expense(expenses):
    print("\n--- Biggest Expense ---")

    if not expenses:
        print("No expenses recorded.")
        return

    biggest = max(expenses, key=lambda expense: expense["amount"])

    print(f"Amount:      ₹{biggest['amount']:.2f}")
    print(f"Category:    {biggest['category']}")
    print(f"Description: {biggest['description']}")
    print(f"Date:        {biggest['date']}")


def filter_by_category(expenses):
    print("\n--- Filter by Category ---")

    if not expenses:
        print("No expenses recorded.")
        return

    category = input("Enter category: ").strip().title()

    matches = [
        expense for expense in expenses
        if expense["category"].lower() == category.lower()
    ]

    if not matches:
        print(f"No expenses found in '{category}'.")
        return

    total = 0

    for index, expense in enumerate(matches, start=1):
        total += expense["amount"]
        print(
            f"{index}. ₹{expense['amount']:.2f} | "
            f"{expense['description']} | {expense['date']}"
        )

    print(f"Category total: ₹{total:.2f}")


def monthly_summary(expenses):
    print("\n--- Monthly Summary ---")

    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    monthly = [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]

    if not monthly:
        print(f"No expenses found for {month}.")
        return

    total = sum(expense["amount"] for expense in monthly)

    category_totals = {}
    for expense in monthly:
        category = expense["category"]
        category_totals[category] = (
            category_totals.get(category, 0) + expense["amount"]
        )

    biggest = max(monthly, key=lambda expense: expense["amount"])

    print(f"\n===== {month} =====")
    print(f"Total spent: ₹{total:.2f}\n")

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{category:<15} ₹{amount:.2f}")

    print("\nBiggest expense:")
    print(f"₹{biggest['amount']:.2f} - {biggest['description']}")


def show_menu():
    print("""
================================
       PERSONAL EXPENSE TRACKER
================================
1. Add expense
2. View all expenses
3. Total spending
4. Spending by category
5. Biggest expense
6. Filter by category
7. Monthly summary
8. Exit
================================
""")


def main():
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            total_expenses(expenses)
        elif choice == "4":
            category_summary(expenses)
        elif choice == "5":
            biggest_expense(expenses)
        elif choice == "6":
            filter_by_category(expenses)
        elif choice == "7":
            monthly_summary(expenses)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Select 1-8.")


if __name__ == "__main__":
    main()
