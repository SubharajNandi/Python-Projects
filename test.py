# Day 2 - 30th August 2026
# Mini Project 2 - Simple Text-Based To-Do List

ToDo = []

for i in range(5):
    task = input(f"Enter task {i + 1}: ")
    ToDo.append(task)

print("\nYour To-Do List:")

#for i, task in enumerate(ToDo, start=1):
 #   print(f"{i}. {task}")