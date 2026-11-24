
import json
import os

DATA_FILE = "students.json"
ATTENDANCE_LIMIT = 75
PASS_MARK = 50

students = []


# ---------- DATA STORAGE ----------

def load_students():
    """Load saved students when the program starts."""
    global students

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                students = json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved data.")
            students = []


def save_students():
    """Save the current student list to a JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
    except OSError:
        print("Error: Student data could not be saved.")


# ---------- INPUT VALIDATION ----------

def get_number(prompt, minimum, maximum):
    """Ask for a number within the allowed range."""
    while True:
        try:
            value = float(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Enter a value from {minimum} to {maximum}.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_text(prompt):
    """Do not accept an empty name or roll number."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def find_by_roll(roll):
    """Find a student using their roll number."""
    for student in students:
        if student["roll"].lower() == roll.lower():
            return student

    return None


# ---------- STUDENT OPERATIONS ----------

def add_student():
    print("\n--- ADD STUDENT ---")

    name = get_text("Enter student name: ")
    roll = get_text("Enter roll number: ")

    if find_by_roll(roll) is not None:
        print("A student with this roll number already exists.")
        return

    attendance = get_number(
        "Enter attendance percentage: ", 0, 100
    )

    python_marks = get_number("Enter Python marks: ", 0, 100)
    maths_marks = get_number("Enter Maths marks: ", 0, 100)
    dsa_marks = get_number("Enter DSA marks: ", 0, 100)

    student = {
        "name": name,
        "roll": roll,
        "attendance": attendance,
        "python": python_marks,
        "maths": maths_marks,
        "dsa": dsa_marks
    }

    students.append(student)
    save_students()

    print(f"\nStudent {name} added successfully!")


def calculate_average(student):
    """Calculate the average of the three subject marks."""
    total = (
        student["python"]
        + student["maths"]
        + student["dsa"]
    )

    return total / 3


def show_student(student):
    """Display one student's details and analysis."""
    average = calculate_average(student)

    print("\n========== STUDENT REPORT ==========")
    print("Name:", student["name"])
    print("Roll number:", student["roll"])
    print("Attendance:", f'{student["attendance"]:.1f}%')
    print("Python:", student["python"])
    print("Maths:", student["maths"])
    print("DSA:", student["dsa"])
    print(f"Average marks: {average:.2f}%")

    if student["attendance"] < ATTENDANCE_LIMIT:
        print("Attendance status: BELOW 75%")
    else:
        print("Attendance status: Satisfactory")

    if min(
        student["python"],
        student["maths"],
        student["dsa"]
    ) < PASS_MARK:
        print("Academic status: At least one subject is below 50")
    elif average < PASS_MARK:
        print("Academic status: Average is below 50")
    else:
        print("Academic status: Satisfactory")


def view_all_students():
    """Display a short list of every student."""
    if not students:
        print("\nNo students have been added yet.")
        return

    print("\n========== ALL STUDENTS ==========")

    for student in students:
        average = calculate_average(student)

        print(
            f'{student["roll"]} | '
            f'{student["name"]} | '
            f'Attendance: {student["attendance"]:.1f}% | '
            f'Average: {average:.2f}'
        )


def search_student():
    print("\n--- SEARCH STUDENT ---")
    roll = get_text("Enter roll number: ")
    student = find_by_roll(roll)

    if student is None:
        print("Student not found.")
    else:
        show_student(student)


def analyze_student():
    print("\n--- ANALYZE STUDENT ---")
    roll = get_text("Enter roll number: ")
    student = find_by_roll(roll)

    if student is None:
        print("Student not found.")
    else:
        show_student(student)


# ---------- CLASS ANALYSIS ----------

def analyze_class():
    if not students:
        print("\nNo student data available for analysis.")
        return

    total_students = len(students)

    average_attendance = sum(
        student["attendance"] for student in students
    ) / total_students

    class_average = sum(
        calculate_average(student) for student in students
    ) / total_students

    low_attendance = [
        student for student in students
        if student["attendance"] < ATTENDANCE_LIMIT
    ]

    low_average = [
        student for student in students
        if calculate_average(student) < PASS_MARK
    ]

    print("\n========== CLASS ANALYSIS ==========")
    print("Total students:", total_students)
    print(f"Average attendance: {average_attendance:.2f}%")
    print(f"Class average marks: {class_average:.2f}")
    print("Students below 75% attendance:", len(low_attendance))
    print("Students with average below 50:", len(low_average))

    if low_attendance:
        print("\nStudents with low attendance:")
        for student in low_attendance:
            print(
                f'- {student["name"]} '
                f'({student["roll"]}): '
                f'{student["attendance"]}%'
            )

    if low_average:
        print("\nStudents with average below 50:")
        for student in low_average:
            print(
                f'- {student["name"]} '
                f'({student["roll"]}): '
                f'{calculate_average(student):.2f}'
            )


def students_needing_attention():
    needs_attention = [
        student for student in students
        if (
            student["attendance"] < ATTENDANCE_LIMIT
            or calculate_average(student) < PASS_MARK
            or min(
                student["python"],
                student["maths"],
                student["dsa"]
            ) < PASS_MARK
        )
    ]

    if not needs_attention:
        print("\nNo students currently meet these warning rules.")
        return

    print("\n======= STUDENTS NEEDING ATTENTION =======")

    for student in needs_attention:
        print()
        show_student(student)


def delete_student():
    print("\n--- DELETE STUDENT ---")
    roll = get_text("Enter roll number to delete: ")
    student = find_by_roll(roll)

    if student is None:
        print("Student not found.")
        return

    confirm = input(
        f'Delete {student["name"]} ({student["roll"]})? (yes/no): '
    ).strip().lower()

    if confirm == "yes":
        students.remove(student)
        save_students()
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


# ---------- MAIN MENU ----------

def display_menu():
    print("\n" + "=" * 42)
    print("       STUDENT PERFORMANCE ANALYZER")
    print("=" * 42)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Analyze a Student")
    print("5. Analyze the Class")
    print("6. View Students Needing Attention")
    print("7. Delete Student")
    print("8. Exit")


def main():
    load_students()

    print("\nWelcome to Student Performance Analyzer!")
    print(f"Loaded {len(students)} saved student record(s).")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            analyze_student()
        elif choice == "5":
            analyze_class()
        elif choice == "6":
            students_needing_attention()
        elif choice == "7":
            delete_student()
        elif choice == "8":
            print("\nYour data is saved. Program closed.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()