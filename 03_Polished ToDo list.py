# Day 2 - 30th August 2026
# Mini Project 2i - Little Polished ToDo list

ToDo = []

print("===== To-Do LIST =====")

while True: 
    task = input("\nEnter a task (or type 'done to Fininh): ")

    if task.lower() == "done":
        break

    ToDo.append(task)

print("\n===== Your To-Do LIST =====")

for i, task in enumerate(ToDo, start=1):
    print(f"{i} {task}")
