import os
import random
import string
import getpass

USERS_FILE = "users.txt"
QUIZ_SCORES_FILE = "quiz_scores.txt"

# Utility to create files if missing
def ensure_files_exist():
    for filename in [USERS_FILE, QUIZ_SCORES_FILE]:
        if not os.path.exists(filename):
            open(filename, "w").close()

# Clear screen for most terminals
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Register new user
def register():
    ensure_files_exist()
    print("\n--- Register ---")
    username = input("Choose username: ").strip()
    if not username:
        print("Username can't be empty.")
        return
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.strip().split(",")[0] == username:
                print("Username already taken.")
                return
    password = getpass.getpass("Choose password: ").strip()
    if not password:
        print("Password can't be empty.")
        return
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    print("Registration successful!")

# Login user
def login():
    ensure_files_exist()
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pw = line.strip().split(",")
            if user == username and pw == password:
                print(f"Welcome back, {username}!\n")
                return username
    print("Login failed.")
    return None

# Grade Calculator
def grade_calculator(username):
    try:
        n = int(input("How many subjects? "))
        if n <= 0:
            print("Positive number please.")
            return
    except:
        print("Enter a valid integer.")
        return

    total = 0
    marks = []
    for i in range(n):
        while True:
            try:
                mark = float(input(f"Marks for subject {i+1} (0-100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    total += mark
                    break
                else:
                    print("Must be 0 to 100.")
            except:
                print("Enter a number.")

    avg = total / n
    if avg >= 90:
        grade = "A+"
    elif avg >= 80:
        grade = "A"
    elif avg >= 70:
        grade = "B"
    elif avg >= 60:
        grade = "C"
    else:
        grade = "F"

    print(f"Average: {avg:.2f}, Grade: {grade}\n")
    filename = f"grades_{username}.txt"
    with open(filename, "a") as f:
        f.write(f"Subjects:{n} Marks:{','.join(map(str, marks))} Average:{avg:.2f} Grade:{grade}\n")
    print(f"Saved results to {filename}\n")

# Quiz Game
DEFAULT_QUESTIONS = {
    "Capital of India?": "Delhi",
    "5 + 7?": "12",
    "Python is a ___ language.": "programming",
    "Sky color on clear day?": "blue",
    "Author of Harry Potter series?": "Rowling",
    "CPU stands for?": "central processing unit",
    "10 * 8?": "80",
    "Red Planet's name?": "Mars",
    "Water boiling point in Celsius?": "100",
    "Language for web pages?": "html"
}

def quiz_game(username, questions=DEFAULT_QUESTIONS, num_questions=3):
    print("\n--- Quiz ---")
    if num_questions > len(questions):
        num_questions = len(questions)
    quiz_questions = random.sample(list(questions.items()), num_questions)
    score = 0
    for q, ans in quiz_questions:
        ans_user = input(q + " ").strip()
        if ans_user.lower() == ans.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {ans}")
    print(f"Score: {score}/{num_questions}\n")
    with open(QUIZ_SCORES_FILE, "a") as f:
        f.write(f"{username},{score},{num_questions}\n")
    print(f"Quiz score saved.\n")

# Password Generator
def password_generator():
    try:
        length = int(input("Password length: "))
        if length <= 0:
            print("Positive length please.")
            return
    except:
        print("Enter an integer.")
        return

    chars = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(random.choice(chars) for _ in range(length))
    print(f"Generated password: {pwd}\n")

# View Grades
def view_my_grades(username):
    filename = f"grades_{username}.txt"
    if not os.path.exists(filename):
        print("No grades saved yet.\n")
        return
    print(f"\n--- {username}'s Grades ---")
    with open(filename) as f:
        for line in f:
            print(line.strip())
    print()

# Quiz Leaderboard
def view_quiz_leaderboard(top_n=10):
    if not os.path.exists(QUIZ_SCORES_FILE):
        print("No quiz data yet.\n")
        return
    scores = []
    with open(QUIZ_SCORES_FILE) as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                user, s, tot = parts
                try:
                    frac = int(s) / int(tot)
                except:
                    frac = 0
                scores.append((user, int(s), int(tot), frac))
    scores.sort(key=lambda x: (-x[3], -x[1]))
    print("\n--- Quiz Leaderboard ---")
    for i, (user, s, tot, frac) in enumerate(scores[:top_n], 1):
        print(f"{i}. {user} - {s}/{tot} ({frac*100:.1f}%)")
    print()

# Main Menu
def main_menu(username):
    while True:
        print("Smart Student Dashboard - Menu")
        print("1. Grade Calculator")
        print("2. Take Quiz")
        print("3. Generate Password")
        print("4. View My Grades")
        print("5. View Quiz Leaderboard")
        print("6. Logout")
        choice = input("Choose (1-6): ").strip()
        if choice == "1":
            grade_calculator(username)
        elif choice == "2":
            quiz_game(username)
        elif choice == "3":
            password_generator()
        elif choice == "4":
            view_my_grades(username)
        elif choice == "5":
            view_quiz_leaderboard()
        elif choice == "6":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice.\n")

# Start program with login or registration
def start_program():
    ensure_files_exist()
    clear_screen()
    print("Welcome to Smart Student Dashboard")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Pick (1-3): ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input.\n")

if __name__ == "__main__":
    start_program()
