"""Kun Tartibi - terminalda ishlaydigan oddiy vazifalar ro'yxati."""
import argparse
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_index(tasks, number):
    if not 1 <= number <= len(tasks):
        print(f"Xato: {number}-raqamli vazifa topilmadi.")
        sys.exit(1)
    return number - 1


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Qo'shildi: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Vazifalar yo'q. Qo'shish: python main.py add \"Vazifa\"")
        return
    for i, task in enumerate(tasks, 1):
        mark = "[x]" if task["done"] else "[ ]"
        print(f"{i}. {mark} {task['title']}")


def complete_task(number):
    tasks = load_tasks()
    idx = get_index(tasks, number)
    tasks[idx]["done"] = True
    save_tasks(tasks)
    print(f"Bajarildi: {tasks[idx]['title']}")


def delete_task(number):
    tasks = load_tasks()
    idx = get_index(tasks, number)
    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"O'chirildi: {removed['title']}")


def main():
    parser = argparse.ArgumentParser(description="Kun Tartibi - vazifalar ro'yxati")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="yangi vazifa qo'shish")
    p_add.add_argument("title", help="vazifa matni")

    sub.add_parser("list", help="vazifalarni ko'rsatish")

    p_done = sub.add_parser("done", help="vazifani bajarilgan deb belgilash")
    p_done.add_argument("number", type=int)

    p_del = sub.add_parser("delete", help="vazifani o'chirish")
    p_del.add_argument("number", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.number)
    elif args.command == "delete":
        delete_task(args.number)


if __name__ == "__main__":
    main()
