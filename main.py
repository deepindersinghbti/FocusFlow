import json

print("Welcome to FocusFlow!")


def get_choice():
    print("1. Add new task", "2. Mark task(s) as done", "3. Modify existing task",
          "4. View task list", "5. Delete task(s)", "6. Exit", sep='\n')
    while True:
        try:
            choice = int(input("Choose an option (1/2/3/4/5/6): "))
            if 1 <= choice <= 6:
                break
            else:
                print("Invalid input. Please enter an integer from 1 to 6.")
        except ValueError:
            print("Invalid input. Please enter an integer from 1 to 6.")
    return choice


def add_task():
    while True:
        task_name = input("Enter task name: ")
        if 3 <= len(task_name) <= 100:
            break
        else:
            print("Length of the task name must be from 3 to 100 characters.")

    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    new_task = {"title": task_name, "done": False}
    tasks.append(new_task)

    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print("Task added successfully!")


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks_dicts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks_dicts = []
    return tasks_dicts


def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


def mark_as_done():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to mark as done.")
        return

    print("\nYour currently due tasks:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} [{status}]")

    try:
        done_task_nums = list(
            map(int, input("\nEnter task number(s) to mark as done (e.g. 1 2 3): ").split()))
        for num in done_task_nums:
            index = num - 1
            if 0 <= index < len(tasks):
                tasks[index]["done"] = True
            else:
                print(f"Task #{num} is invalid.")
        save_tasks(tasks)
        print("Selected task(s) marked as done.")
    except ValueError:
        print("Invalid input. Please enter task numbers separated by space.")

def modify_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to modify.")
        return

    # Filter only pending tasks
    pending_tasks = [task for task in tasks if not task["done"]]

    if not pending_tasks:
        print("All tasks are already completed. No pending tasks to modify. ✅")
        return

    while True:
        # Show pending tasks
        print("\nPending tasks:")
        for i, task in enumerate(pending_tasks, start=1):
            print(f"{i}. {task['title']} [❌]")

        try:
            task_num = int(input("\nEnter the task number to modify: "))
            index = task_num - 1

            if 0 <= index < len(pending_tasks):
                # Valid task number, now get new title
                while True:
                    new_title = input("Enter the new task name: ")
                    if 3 <= len(new_title) <= 100:
                        break
                    else:
                        print("Task name must be between 3 and 100 characters.")

                # Find and update the task in the full task list
                original_title = pending_tasks[index]['title']
                for task in tasks:
                    if task['title'] == original_title and not task['done']:
                        task['title'] = new_title
                        break

                save_tasks(tasks)
                print("Task modified successfully!")
                break  # Exit loop after successful modification
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def view_list():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    print("\nYour task list:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} [{status}]")


def delete_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks to delete.")
        return

    print("\nYour task list:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} [{status}]")

    try:
        nums_to_delete = list(
            map(int, input("\nEnter task number(s) to delete (e.g. 1 2 3): ").split()))
        # sort in reverse to avoid index shifting
        nums_to_delete = sorted(set(nums_to_delete), reverse=True)

        for num in nums_to_delete:
            index = num - 1
            if 0 <= index < len(tasks):
                removed = tasks.pop(index)
                print(f"Deleted: {removed['title']}")
            else:
                print(f"Task #{num} is invalid.")

        save_tasks(tasks)
        print("Selected task(s) deleted.")

    except ValueError:
        print("Invalid input. Please enter task numbers separated by space.")


    
if __name__ == '__main__':
    choice = get_choice()

    match choice:
        case 1:
            add_task()
        case 2:
            mark_as_done()
        case 3:
            modify_task()
        case 4:
            view_list()
        case 5:
            delete_tasks()
        case 6:
            print("Thank you for using FocusFlow!")