
import streamlit as st
import pandas as pd
import main as core

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Student Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

core.load_students()

# ---------- STYLING ----------
st.markdown("""
<style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 650 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        letter-spacing: -0.4px;
    }

    div[data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        padding: 16px;
        border-radius: 12px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.7rem;
    }

    .subtitle {
        color: #64748b;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .status-good {
        color: #15803d;
        font-weight: 600;
    }

    .status-bad {
        color: #dc2626;
        font-weight: 600;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 42px;
    }

    div[data-testid="stForm"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 2rem 0.8rem;
        }

        h1 {
            font-size: 1.65rem !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.35rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------- HELPER FUNCTIONS ----------

def average(student):
    return core.calculate_average(student)


def get_status(student):
    attendance_ok = (
        student["attendance"] >= core.ATTENDANCE_LIMIT
    )

    marks_ok = (
        min(
            student["python"],
            student["maths"],
            student["dsa"]
        ) >= core.PASS_MARK
        and average(student) >= core.PASS_MARK
    )

    if attendance_ok and marks_ok:
        return "Satisfactory"

    return "Needs Attention"


def student_dataframe(data):
    rows = []

    for s in data:
        rows.append({
            "Roll No.": s["roll"],
            "Name": s["name"],
            "Attendance": f'{s["attendance"]:.1f}%',
            "Python": s["python"],
            "Maths": s["maths"],
            "DSA": s["dsa"],
            "Average": round(average(s), 2),
            "Status": get_status(s)
        })

    return pd.DataFrame(rows)


# ---------- HEADER ----------

st.title("Student Performance Analyzer")
st.markdown(
    '<p class="subtitle">Manage students. Track performance. Identify progress.</p>',
    unsafe_allow_html=True
)

# ---------- NAVIGATION ----------

page = st.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Add Student",
        "All Students",
        "Student Report",
        "Class Analysis",
        "Needs Attention",
        "Delete Student"
    ]
)

st.divider()


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.subheader("Dashboard")
    st.caption("Overview of student performance")

    total = len(core.students)

    if total == 0:
        st.info("No student records yet. Start by adding a student.")
    else:
        avg_attendance = sum(
            s["attendance"] for s in core.students
        ) / total

        class_average = sum(
            average(s) for s in core.students
        ) / total

        low_attendance = sum(
            s["attendance"] < core.ATTENDANCE_LIMIT
            for s in core.students
        )

        needs_attention = sum(
            get_status(s) == "Needs Attention"
            for s in core.students
        )

        c1, c2 = st.columns(2)
        c1.metric("Total Students", total)
        c2.metric("Class Average", f"{class_average:.1f}%")

        c3, c4 = st.columns(2)
        c3.metric("Avg. Attendance", f"{avg_attendance:.1f}%")
        c4.metric("Needs Attention", needs_attention)

        st.divider()

        st.subheader("Recent Student Records")

        df = student_dataframe(core.students)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Performance Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.caption("Attendance")
            st.progress(
                min(avg_attendance / 100, 1.0)
            )
            st.write(f"{avg_attendance:.1f}%")

        with col2:
            st.caption("Class Average")
            st.progress(
                min(class_average / 100, 1.0)
            )
            st.write(f"{class_average:.1f}%")


# ==================================================
# ADD STUDENT
# ==================================================

elif page == "Add Student":

    st.subheader("Add New Student")
    st.caption("Enter student details and academic marks.")

    with st.form("add_student_form"):

        name = st.text_input("Student Name")
        roll = st.text_input("Roll Number")

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0
        )

        st.markdown("**Subject Marks**")

        c1, c2, c3 = st.columns(3)

        with c1:
            python_marks = st.number_input(
                "Python",
                0.0, 100.0, 50.0
            )

        with c2:
            maths_marks = st.number_input(
                "Maths",
                0.0, 100.0, 50.0
            )

        with c3:
            dsa_marks = st.number_input(
                "DSA",
                0.0, 100.0, 50.0
            )

        submitted = st.form_submit_button(
            "Add Student",
            use_container_width=True
        )

        if submitted:

            if not name.strip() or not roll.strip():
                st.error("Please enter both name and roll number.")

            elif core.find_by_roll(roll.strip()):
                st.error("This roll number already exists.")

            else:
                student = {
                    "name": name.strip(),
                    "roll": roll.strip(),
                    "attendance": attendance,
                    "python": python_marks,
                    "maths": maths_marks,
                    "dsa": dsa_marks
                }

                core.students.append(student)
                core.save_students()

                st.success(f"{name} added successfully!")
                st.rerun()


# ==================================================
# ALL STUDENTS
# ==================================================

elif page == "All Students":

    st.subheader("All Students")

    if not core.students:
        st.info("No students available.")
    else:
        search = st.text_input(
            "Search by name or roll number",
            placeholder="Enter student name or roll number..."
        )

        filtered = [
            s for s in core.students
            if search.lower() in s["name"].lower()
            or search.lower() in s["roll"].lower()
        ]

        st.caption(f"{len(filtered)} student record(s)")

        st.dataframe(
            student_dataframe(filtered),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# STUDENT REPORT
# ==================================================

elif page == "Student Report":

    st.subheader("Student Report")

    if not core.students:
        st.info("No student records available.")
    else:
        selected_roll = st.selectbox(
            "Select Student",
            [s["roll"] for s in core.students],
            format_func=lambda r: next(
                s["name"] + " (" + s["roll"] + ")"
                for s in core.students if s["roll"] == r
            )
        )

        student = core.find_by_roll(selected_roll)

        if student:
            st.divider()

            st.markdown(f"### {student['name']}")
            st.caption(f"Roll Number: {student['roll']}")

            a, b = st.columns(2)
            a.metric(
                "Average Marks",
                f"{average(student):.2f}%"
            )
            b.metric(
                "Attendance",
                f"{student['attendance']:.1f}%"
            )

            st.divider()

            st.markdown("**Subject Performance**")

            for subject in ["python", "maths", "dsa"]:
                value = student[subject]

                st.write(f"{subject.upper()} — {value:.1f}/100")
                st.progress(value / 100)

            st.divider()

            if student["attendance"] < core.ATTENDANCE_LIMIT:
                st.warning("Attendance is below 75%.")
            else:
                st.success("Attendance is satisfactory.")

            failed = [
                subject.upper()
                for subject in ["python", "maths", "dsa"]
                if student[subject] < core.PASS_MARK
            ]

            if failed:
                st.warning(
                    "Below passing marks: " + ", ".join(failed)
                )
            elif average(student) < core.PASS_MARK:
                st.warning("Overall average is below 50.")
            else:
                st.success("Academic performance is satisfactory.")


# ==================================================
# CLASS ANALYSIS
# ==================================================

elif page == "Class Analysis":

    st.subheader("Class Analysis")

    if not core.students:
        st.info("No student data available.")
    else:
        total = len(core.students)

        avg_attendance = sum(
            s["attendance"] for s in core.students
        ) / total

        class_average = sum(
            average(s) for s in core.students
        ) / total

        low_attendance = [
            s for s in core.students
            if s["attendance"] < core.ATTENDANCE_LIMIT
        ]

        low_average = [
            s for s in core.students
            if average(s) < core.PASS_MARK
        ]

        c1, c2 = st.columns(2)
        c1.metric("Total Students", total)
        c2.metric("Class Average", f"{class_average:.2f}")

        c3, c4 = st.columns(2)
        c3.metric("Average Attendance", f"{avg_attendance:.2f}%")
        c4.metric("Low Attendance", len(low_attendance))

        st.divider()

        st.markdown("**Students Below Attendance Limit**")

        if low_attendance:
            st.dataframe(
                student_dataframe(low_attendance),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No students below attendance limit.")

        st.markdown("**Students With Average Below 50**")

        if low_average:
            st.dataframe(
                student_dataframe(low_average),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No students with an average below 50.")


# ==================================================
# NEEDS ATTENTION
# ==================================================

elif page == "Needs Attention":

    st.subheader("Students Needing Attention")
    st.caption(
        "Students with low attendance or unsatisfactory academic performance."
    )

    needs_attention = [
        s for s in core.students
        if get_status(s) == "Needs Attention"
    ]

    if not needs_attention:
        st.success("All students currently meet the performance rules.")
    else:
        st.warning(
            f"{len(needs_attention)} student(s) need attention."
        )

        st.dataframe(
            student_dataframe(needs_attention),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# DELETE STUDENT
# ==================================================

elif page == "Delete Student":

    st.subheader("Delete Student")

    if not core.students:
        st.info("No students available to delete.")
    else:
        selected_roll = st.selectbox(
            "Select student to delete",
            [s["roll"] for s in core.students],
            format_func=lambda r: next(
                s["name"] + " (" + s["roll"] + ")"
                for s in core.students if s["roll"] == r
            )
        )

        student = core.find_by_roll(selected_roll)

        if student:
            st.warning(
                f"You are about to delete {student['name']} "
                f"({student['roll']})."
            )

            if st.button(
                "Delete Student",
                type="primary",
                use_container_width=True
            ):
                core.students.remove(student)
                core.save_students()
                st.success("Student deleted successfully.")
                st.rerun()


# ---------- FOOTER ----------

st.divider()

st.caption(
    "Student Performance Analyzer · Built with Python and Streamlit"
)
