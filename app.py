import streamlit as st
import sqlite3
from datetime import date, timedelta
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="My Habit Tracker",
    page_icon="🔥",
    layout="centered"
)

# Database connection function
def get_connection():
    return sqlite3.connect("habits.db")

# Show messages
if "message" in st.session_state:
    st.success(st.session_state["message"])
    del st.session_state["message"]

# CSS styling
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #F8F5FF;
}

/* Main title */
h1 {
    color: #6A35B5;
    font-weight: 800;
}

/* Section headings */
h2, h3 {
    color: #7541B8;
}

/* Buttons */
.stButton > button {
    background-color: #7541B8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #54258F;
    color: white;
    border: none;
}

/* Dashboard metrics */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E5D8FA;
    border-left: 5px solid #7541B8;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(106, 53, 181, 0.10);
}

div[data-testid="stMetricLabel"] {
    color: #7541B8;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    color: #4B267D;
    font-weight: 800;
}

/* Input boxes */
.stTextInput input {
    border: 1px solid #C7A9ED;
    border-radius: 8px;
}

/* Progress bar */
.stProgress > div > div > div {
    background-color: #7541B8;
}
/* Habit cards */
.habit-card {
    background-color: white;
    border: 1px solid #E5D8FA;
    border-left: 5px solid #7541B8;
    border-radius: 14px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 4px 10px rgba(106, 53, 181, 0.10);
}

/* Habit name */
.habit-name {
    color: #54258F;
    font-size: 20px;
    font-weight: 700;
}
/* Purple theme for all buttons */
.stButton > button {
    background-color: #7541B8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    transition: 0.3s;
}

/* Button hover effect */
.stButton > button:hover {
    background-color: #54258F;
    color: white;
    border: 1px solid #54258F;
}
/* Dashboard metric cards */
[data-testid="stMetric"] {
    background-color: #F3ECFC;
    border: 1px solid #E1D2F5;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0 3px 8px rgba(84, 37, 143, 0.10);
}

/* Dashboard metric labels */
[data-testid="stMetricLabel"] {
    color: #54258F;
    font-weight: 600;
}

/* Dashboard metric values */
[data-testid="stMetricValue"] {
    color: #54258F;
    font-weight: 700;
}
/* Purple progress bar */
.stProgress > div > div > div > div {
    background-color: #7541B8;
}

.stProgress > div > div {
    background-color: #E5D8F5;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# Create database tables
connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    streak INTEGER DEFAULT 0,
    last_done TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS habit_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    completed_date TEXT
)
""")

connection.commit()
connection.close()


# Main heading
st.title("🔥 My Habit Tracker")
st.write("Track your daily habits and build your streak!")
st.write(f"Today: {date.today()}")


# Add Habit
st.subheader("➕ Add New Habit")

habit = st.text_input("Enter your habit:")

if st.button("Add Habit"):

    if habit.strip():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO habits (name) VALUES (?)",
            (habit.strip(),)
        )

        connection.commit()
        connection.close()

        st.success("Habit added successfully!")
        st.rerun()

    else:
        st.warning("Please enter a habit.")


# Fetch habits
connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    "SELECT id, name, streak, last_done FROM habits"
)

habits = cursor.fetchall()

connection.close()


# Dashboard
st.subheader("📊 Dashboard")

total_habits = len(habits)

today = date.today()

completed_habits = sum(
    1 for h in habits
    if h[3] == str(today)
)

current_streak = max(
    [h[2] for h in habits],
    default=0
)

if total_habits > 0:
    progress = completed_habits / total_habits
else:
    progress = 0

col1, col2, col3 = st.columns(3)

col1.metric("📋 Total Habits", total_habits)
col2.metric("✅ Completed Today", completed_habits)
col3.metric("🔥 Best Streak", current_streak)

st.write(
    f"📊 Today's Progress: {completed_habits} / {total_habits} habits completed"
)

st.progress(progress)

st.write(f"Completion: {progress * 100:.0f}%")
import streamlit as st
import sqlite3
from datetime import date

# Page configuration
st.set_page_config(
    page_title="My Habit Tracker",
    page_icon="🔥",
    layout="centered"
)

# Database connection function
def get_connection():
    return sqlite3.connect("habits.db")

# Show messages
if "message" in st.session_state:
    st.success(st.session_state["message"])
    del st.session_state["message"]

# CSS styling
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #F8F5FF;
}

/* Main title */
h1 {
    color: #6A35B5;
    font-weight: 800;
}

/* Section headings */
h2, h3 {
    color: #7541B8;
}

/* Buttons */
.stButton > button {
    background-color: #7541B8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #54258F;
    color: white;
    border: none;
}

/* Dashboard metrics */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E5D8FA;
    border-left: 5px solid #7541B8;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(106, 53, 181, 0.10);
}

div[data-testid="stMetricLabel"] {
    color: #7541B8;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    color: #4B267D;
    font-weight: 800;
}

/* Input boxes */
.stTextInput input {
    border: 1px solid #C7A9ED;
    border-radius: 8px;
}

/* Progress bar */
.stProgress > div > div > div {
    background-color: #7541B8;
}
/* Habit cards */
.habit-card {
    background-color: white;
    border: 1px solid #E5D8FA;
    border-left: 5px solid #7541B8;
    border-radius: 14px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 4px 10px rgba(106, 53, 181, 0.10);
}

/* Habit name */
.habit-name {
    color: #54258F;
    font-size: 20px;
    font-weight: 700;
}
/* Purple theme for all buttons */
.stButton > button {
    background-color: #7541B8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    transition: 0.3s;
}

/* Button hover effect */
.stButton > button:hover {
    background-color: #54258F;
    color: white;
    border: 1px solid #54258F;
}
/* Dashboard metric cards */
[data-testid="stMetric"] {
    background-color: #F3ECFC;
    border: 1px solid #E1D2F5;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0 3px 8px rgba(84, 37, 143, 0.10);
}

/* Dashboard metric labels */
[data-testid="stMetricLabel"] {
    color: #54258F;
    font-weight: 600;
}

/* Dashboard metric values */
[data-testid="stMetricValue"] {
    color: #54258F;
    font-weight: 700;
}
/* Purple progress bar */
.stProgress > div > div > div > div {
    background-color: #7541B8;
}

.stProgress > div > div {
    background-color: #E5D8F5;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# Create database tables
connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    streak INTEGER DEFAULT 0,
    last_done TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS habit_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    completed_date TEXT
)
""")

connection.commit()
connection.close()


# Main heading
st.title("🔥 My Habit Tracker")
st.write("Track your daily habits and build your streak!")
st.write(f"Today: {date.today()}")


# Add Habit
st.subheader("➕ Add New Habit")

habit = st.text_input("Enter your habit:",
key="add_habit_input")

if st.button("Add Habit",key="add_habit_button"):

    if habit.strip():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO habits (name) VALUES (?)",
            (habit.strip(),)
        )

        connection.commit()
        connection.close()

        st.success("Habit added successfully!")
        st.rerun()

    else:
        st.warning("Please enter a habit.")


# Fetch habits
connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    "SELECT id, name, streak, last_done FROM habits"
)

habits = cursor.fetchall()

connection.close()


# Dashboard
st.subheader("📊 Dashboard")

total_habits = len(habits)

today = date.today()

completed_habits = sum(
    1 for h in habits
    if h[3] == str(today)
)

current_streak = max(
    [h[2] for h in habits],
    default=0
)

if total_habits > 0:
    progress = completed_habits / total_habits
else:
    progress = 0

col1, col2, col3 = st.columns(3)

col1.metric("📋 Total Habits", total_habits)
col2.metric("✅ Completed Today", completed_habits)
col3.metric("🔥 Best Streak", current_streak)

st.write(
    f"📊 Today's Progress: {completed_habits} / {total_habits} habits completed"
)

st.progress(progress)

st.write(f"Completion: {progress * 100:.0f}%")
# Weekly Progress Summary
st.subheader("📅 Weekly Progress")

today = date.today()
week_start = today - timedelta(days=6)

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT completed_date, COUNT(*)
    FROM habit_history
    WHERE completed_date >= ? AND completed_date <= ?
    GROUP BY completed_date
""", (str(week_start), str(today)))

records = cursor.fetchall()
connection.close()

weekly_data = {
    (week_start + timedelta(days=i)).strftime("%a"): 0
    for i in range(7)
}

for completed_date, count in records:
    day = date.fromisoformat(completed_date).strftime("%a")
    weekly_data[day] = count

st.metric("Total completions this week", sum(weekly_data.values()))
st.bar_chart(weekly_data)

# Search Habit
st.subheader("🔎 Search Habits")

search = st.text_input(
    "Search Habit",
    placeholder="Type a habit name..."
)

if search:
    displayed_habits = [
        h for h in habits
        if search.lower() in h[1].lower()
    ]
else:
    displayed_habits = habits


# Display Habits
st.subheader("📋 My Habits")

if displayed_habits:

    for habit_id, name, streak, last_done in displayed_habits:

        st.markdown(
            f'<div class="habit-card">'
            f'<div class="habit-name">🔥 {name}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.write(f"🔥 Streak: {streak} day(s)")

        # Mark Done Today
        if st.button(
            "🟩 Mark Done Today",
            key=f"done_{habit_id}"
        ):

            today = date.today()

            if last_done == str(today):

                st.warning("⚠️ Already completed today!")

            else:

                if last_done is None:
                    new_streak = 1

                else:
                    previous_date = date.fromisoformat(last_done)
                    gap = (today - previous_date).days

                    if gap == 1:
                        new_streak = streak + 1
                    else:
                        new_streak = 1

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE habits
                    SET streak = ?, last_done = ?
                    WHERE id = ?
                """, (new_streak, str(today), habit_id))

                cursor.execute("""
                    SELECT 1 FROM habit_history
                    WHERE habit_id = ? AND completed_date = ?
                """, (habit_id, str(today)))

                if cursor.fetchone() is None:

                    cursor.execute("""
                        INSERT INTO habit_history
                        (habit_id, completed_date)
                        VALUES (?, ?)
                    """, (habit_id, str(today)))

                connection.commit()
                connection.close()

                st.session_state["message"] = (
                    "Habit completed successfully! 🎉"
                )

                st.rerun()


        # Edit Habit
        if st.button(
            "✏️ Edit",
            key=f"edit_{habit_id}"
        ):

            st.session_state[f"editing_{habit_id}"] = True

        if st.session_state.get(
            f"editing_{habit_id}", False
        ):

            new_name = st.text_input(
                "Enter new habit name",
                value=name,
                key=f"input_{habit_id}"
            )

            if st.button(
                "💾 Save",
                key=f"save_{habit_id}"
            ):

                if new_name.strip():

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute("""
                        UPDATE habits
                        SET name = ?
                        WHERE id = ?
                    """, (new_name.strip(), habit_id))

                    connection.commit()
                    connection.close()

                    st.session_state[f"editing_{habit_id}"] = False
                    st.session_state["message"] = "Habit updated successfully!"
                    st.rerun()

                else:
                    st.warning("Habit name cannot be empty.")


        # Delete Habit
        if st.button(
            "🗑️ Delete",
            key=f"delete_{habit_id}"
        ):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM habits WHERE id = ?",
                (habit_id,)
            )

            connection.commit()
            connection.close()

            st.session_state["message"] = "Habit deleted successfully!"
            st.rerun()

else:

    st.info("No habits found. Add a new habit!")

# Clear Habit History
if st.button("🗑️ Clear All Habit History"):

    st.session_state["confirm_clear_history"] = True

if st.session_state.get("confirm_clear_history", False):

    st.warning("Are you sure you want to delete all habit history logs?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Clear All History"):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM habit_history")

            connection.commit()
            connection.close()

            st.session_state["confirm_clear_history"] = False
            st.session_state["message"] = "All habit history cleared!"
            st.rerun()

    with col2:
        if st.button("Cancel"):

            st.session_state["confirm_clear_history"] = False
            st.rerun()
# Habit History
st.header("📋 Habit History")

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT habit_history.completed_date, habits.name
    FROM habit_history
    JOIN habits
    ON habit_history.habit_id = habits.id
    ORDER BY habit_history.completed_date DESC
""")

history = cursor.fetchall()

connection.close()

if history:

    for completed_date, name in history:

        st.write(f"✅ {name} - {completed_date}")

else:

    st.info("No history yet.")


# Search Habit
st.subheader("🔎 Search Habits")

search = st.text_input(
    "Search Habit",
    placeholder="Type a habit name...",
    key="search_habit_input"
)

if search:
    displayed_habits = [
        h for h in habits
        if search.lower() in h[1].lower()
    ]
else:
    displayed_habits = habits


# Display Habits
st.subheader("📋 My Habits")

if displayed_habits:

    for habit_id, name, streak, last_done in displayed_habits:

        st.markdown(
            f'<div class="habit-card">'
            f'<div class="habit-name">🔥 {name}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.write(f"🔥 Streak: {streak} day(s)")

        # Mark Done Today
        if st.button(
            "🟩 Mark Done Today",
            key=f"search_done_{habit_id}"
        ):

            today = date.today()

            if last_done == str(today):

                st.warning("⚠️ Already completed today!")

            else:

                if last_done is None:
                    new_streak = 1

                else:
                    previous_date = date.fromisoformat(last_done)
                    gap = (today - previous_date).days

                    if gap == 1:
                        new_streak = streak + 1
                    else:
                        new_streak = 1

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE habits
                    SET streak = ?, last_done = ?
                    WHERE id = ?
                """, (new_streak, str(today), habit_id))

                cursor.execute("""
                    SELECT 1 FROM habit_history
                    WHERE habit_id = ? AND completed_date = ?
                """, (habit_id, str(today)))

                if cursor.fetchone() is None:

                    cursor.execute("""
                        INSERT INTO habit_history
                        (habit_id, completed_date)
                        VALUES (?, ?)
                    """, (habit_id, str(today)))

                connection.commit()
                connection.close()

                st.session_state["message"] = (
                    "Habit completed successfully! 🎉"
                )

                st.rerun()


        # Edit Habit
        if st.button(
            "✏️ Edit",
            key=f"search_edit_{habit_id}"
        ):

            st.session_state[f"editing_{habit_id}"] = True

        if st.session_state.get(
            f"editing_{habit_id}", False
        ):

            new_name = st.text_input(
                "Enter new habit name",
                value=name,
                key=f"input_{habit_id}"
            )

            if st.button(
                "💾 Save",
                key=f"save_{habit_id}"
            ):

                if new_name.strip():

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute("""
                        UPDATE habits
                        SET name = ?
                        WHERE id = ?
                    """, (new_name.strip(), habit_id))

                    connection.commit()
                    connection.close()

                    st.session_state[f"editing_{habit_id}"] = False
                    st.session_state["message"] = "Habit updated successfully!"
                    st.rerun()

                else:
                    st.warning("Habit name cannot be empty.")


        # Delete Habit
        if st.button(
            "🗑️ Delete",
            key=f"search_delete_{habit_id}"
        ):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM habits WHERE id = ?",
                (habit_id,)
            )

            connection.commit()
            connection.close()

            st.session_state["message"] = "Habit deleted successfully!"
            st.rerun()

else:

    st.info("No habits found. Add a new habit!")

# Clear Habit History
if st.button("🗑️ Clear All Habit History",key="clear_all_history_button"):

    st.session_state["confirm_clear_history"] = True

if st.session_state.get("confirm_clear_history", False):

    st.warning("Are you sure you want to delete all habit history logs?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Clear All History"):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM habit_history")

            connection.commit()
            connection.close()

            st.session_state["confirm_clear_history"] = False
            st.session_state["message"] = "All habit history cleared!"
            st.rerun()

    with col2:
        if st.button("Cancel"):

            st.session_state["confirm_clear_history"] = False
            st.rerun()
# Habit History
st.header("📋 Habit History")

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT habit_history.completed_date, habits.name
    FROM habit_history
    JOIN habits
    ON habit_history.habit_id = habits.id
    ORDER BY habit_history.completed_date DESC
""")

history = cursor.fetchall()

connection.close()

if history:

    for completed_date, name in history:

        st.write(f"✅ {name} - {completed_date}")

else:

    st.info("No history yet.")

# MONTHLY PROGRESS DASHBOARD

st.markdown("---")
st.header("📅 Monthly Progress Dashboard")

today = date.today()
current_month = today.strftime("%Y-%m")

monthly_connection = get_connection()
monthly_cursor = monthly_connection.cursor()

monthly_cursor.execute("""
    SELECT COUNT(*)
    FROM habit_history
    WHERE strftime('%Y-%m', completed_date) = ?
""", (current_month,))

monthly_total = monthly_cursor.fetchone()[0]

monthly_cursor.execute("""
    SELECT COUNT(*)
    FROM habits
""")

total_habits = monthly_cursor.fetchone()[0]

monthly_cursor.execute("""
    SELECT habits.name, COUNT(*) AS total
    FROM habit_history
    JOIN habits ON habit_history.habit_id = habits.id
    WHERE strftime('%Y-%m', habit_history.completed_date) = ?
    GROUP BY habits.name
    ORDER BY total DESC
    LIMIT 1
""", (current_month,))

best_habit = monthly_cursor.fetchone()

monthly_cursor.execute("""
    SELECT completed_date, COUNT(*)
    FROM habit_history
    WHERE strftime('%Y-%m', completed_date) = ?
    GROUP BY completed_date
    ORDER BY completed_date
""", (current_month,))

daily_progress = monthly_cursor.fetchall()

monthly_connection.close()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Monthly Completions", monthly_total)

with col2:
    st.metric("Total Habits", total_habits)

with col3:
    st.metric(
        "Best Habit",
        best_habit[0] if best_habit else "Not yet"
    )

st.subheader("📊 Monthly Daily Progress")

if daily_progress:
    daily_counts = {
    str(day): count
    for day, count in daily_progress
}

    days = pd.date_range(
    start=f"{current_month}-01",
    end=today
)

    chart_data = pd.DataFrame({
    "Completions": [
        daily_counts.get(day.strftime("%Y-%m-%d"), 0)
        for day in days
    ]
}, index=days.strftime("%d %b"))

    st.bar_chart(chart_data)


      
else:
    st.info("No completions recorded this month yet.")