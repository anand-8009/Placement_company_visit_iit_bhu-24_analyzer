import streamlit as st
import pandas as pd
import math

# Load your cleaned dataset
df = pd.read_csv("placement_iit_bhu_refined_csv4.csv")
st.set_page_config(page_title="Placement Insights", layout="wide")
st.info("💡 This app looks best in **Light Theme**. Please switch from settings (top-right corner).")

# App title
st.title("🎓 Placement Insights'24 - Company Search")

# Search bar
search_query = st.text_input("🔍 Search for a company", placeholder="Enter company name...")
LAKH = 100_000  # 1 Lakh in rupees
def to_lpa(val):
    return f"{val/LAKH:.1f} LPA" if pd.notna(val) else "N/A"
if search_query:
    # Normalize query
    search_query_lower = search_query.strip().lower()

    # Case-insensitive search
    filtered_df = df[df['company_name'].str.lower().str.contains(search_query_lower, na=False)]

    if not filtered_df.empty:
        st.success(f"Found {len(filtered_df)} result(s) for **'{search_query}'** ✅")

        # Show results as styled cards
        for _, row in filtered_df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color:#f9f9f9;
                                padding:20px;
                                margin-bottom:15px;
                                border-radius:12px;
                                box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h3 style="color:#2C3E50;">🏢 {row['company_name']}</h3>
                        <p><b>📌 Profile:</b> {row.get('company_profile', 'N/A')}</p>
                        <p><b>🎯 CGPA Cutoff:</b> {row.get('cgpa', 'N/A')}</p>
                        <p><b>💰 CTC (B.Tech):</b> {to_lpa(row.get('ctc_btech'))} | <b>Base:</b> {to_lpa(row.get('base_btech'))}</p>
                    <p><b>💰 CTC (IDD):</b> {to_lpa(row.get('ctc_idd'))} | <b>Base:</b> {to_lpa(row.get('base_idd'))}</p>
                        <p><b>📚 Eligible Courses:</b> {row.get('courses', 'N/A')}</p>
                        <p><b>🏫 Eligible Departments:</b> {row.get('dept_eligible', 'N/A')}</p>
                        <p><b>⌚ Last updated_time:</b> {row.get('updated_time', 'N/A')}</p>
                        <p><b>🏢 Location:</b> {row.get('location', 'N/A')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:
        st.warning(f"No company found matching **'{search_query}'**")
else:
    st.info("Please enter a company name to search.")



# App title
st.title("🎓 Placement Insights - Advanced Filters")


# ---------------- PROFILE FILTER ----------------
profile_options = [
    "Software/Quant Developer",
    "Core_Engineering",
    "Other",
    "Business/Product Analyst",
    "Data Science/AI",
    "Teaching/Academic",
    "Supply_chain/R&D"
]

selected_profile = st.selectbox("📌 Select Profile", ["-- Select a Profile --"] + profile_options)

# ---------------- SALARY RANGE OPTIONS ----------------
salary_ranges_lakh = {
    "-- All Salaries --": (0, float("inf")),
    "1 - 10 Lakh": (1, 10),
    "10 - 15 Lakh": (10, 15),
    "15 - 20 Lakh": (15, 20),
    "20 - 25 Lakh": (20, 25),
    "25 - 30 Lakh": (25, 30),
    "30 - 40 Lakh": (30, 40),
    "Above 40 Lakh": (40, float("inf")),
}

LAKH = 100_000  # 1 Lakh in rupees

def lakh_range_to_rupees(tup):
    lo_lakh, hi_lakh = tup
    lo = lo_lakh * LAKH
    hi = math.inf if math.isinf(hi_lakh) else hi_lakh * LAKH
    return lo, hi

# ---------------- SALARY FILTER ----------------
st.subheader("💰 Salary Filter")

col1, col2 = st.columns(2)

with col1:
    salary_columns = {
    "CTC (B.Tech)": "ctc_btech",
    "Base (B.Tech)": "base_btech",
    "CTC (IDD)": "ctc_idd",
    "Base (IDD)": "base_idd"
}

    selected_salary_col_label = st.selectbox("Select Salary Type", list(salary_columns.keys()))
    selected_salary_col = salary_columns[selected_salary_col_label]
    
    selected_range_label = st.selectbox("Select Salary Range", list(salary_ranges_lakh.keys()), index=0)
    salary_min_rs, salary_max_rs = lakh_range_to_rupees(salary_ranges_lakh[selected_range_label])

with col2:
    # New Greater Than or Equal To filter
    salary_gte_options = {
        "-- No Minimum --": 0,
        "≥ 10 Lakh": 10,
        "≥ 15 Lakh": 15,
        "≥ 20 Lakh": 20,
        "≥ 25 Lakh": 25,
        "≥ 30 Lakh": 30,
        "≥ 35 Lakh": 35,
        "≥ 40 Lakh": 40
    }
    
    selected_gte_label = st.selectbox("Salary Greater Than or Equal To", list(salary_gte_options.keys()))
    salary_gte_value = salary_gte_options[selected_gte_label] * LAKH

# ---------------- CGPA FILTER ----------------
st.subheader("🎯 CGPA Filter")
cgpa_options = [0.0, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]

col1, col2 = st.columns(2)
with col1:
    selected_cgpa_min = st.selectbox("Minimum CGPA:", options=cgpa_options, index=0)
with col2:
    selected_cgpa_max = st.selectbox("Maximum CGPA:", options=cgpa_options, index=len(cgpa_options)-1)

# ---------------- COURSE FILTER ----------------
st.subheader("📚 Course Filter")

course_options = [
    "-- All Courses --",
    "B.Tech only",
    "IDD only",
    "B.Tech + IDD"
]

selected_course_filter = st.selectbox("Eligible Courses", course_options)

# ---------------- DATE FILTER ----------------
st.subheader("📅 Date Filter(Based on last updated time on tpo)")

# Month filter
month_options = ["-- All Months --", "Dec", "Jan", "Feb", "Nov", "March", "April", "May", "Oct", "June"]
selected_month = st.selectbox("Select Month", month_options)

# Year filter
year_options = ["-- All Years --", 2024, 2025]
selected_year = st.selectbox("Select Year", year_options)

# Day filter
day_options = ["-- All Days --", "1 - 15", "16 - 31"]
selected_day_range = st.selectbox("Select Day Range", day_options)

# ---------------- FILTERING LOGIC ----------------
filtered_df = df.copy()

# Profile filter
if selected_profile != "-- Select a Profile --":
    filtered_df = filtered_df[filtered_df["profile"] == selected_profile]

# Ensure salary column is numeric (in rupees)
filtered_df[selected_salary_col] = pd.to_numeric(filtered_df[selected_salary_col], errors="coerce")

# Apply salary filter only if not "All"
if selected_range_label != "-- All Salaries --":
    filtered_df = filtered_df[
        (filtered_df[selected_salary_col] >= salary_min_rs) &
        (filtered_df[selected_salary_col] <= salary_max_rs)
    ]

if selected_gte_label != "-- No Minimum --":
    filtered_df = filtered_df[filtered_df[selected_salary_col] >= salary_gte_value]

# Apply CGPA filter (between min and max)
filtered_df["cgpa"] = pd.to_numeric(filtered_df["cgpa"], errors="coerce")
if not math.isinf(selected_cgpa_max):
    filtered_df = filtered_df[(filtered_df["cgpa"] >= selected_cgpa_min) & (filtered_df["cgpa"] <= selected_cgpa_max)]
else:
    filtered_df = filtered_df[filtered_df["cgpa"] >= selected_cgpa_min]

# Apply course filter
if selected_course_filter == "B.Tech only":
    filtered_df = filtered_df[filtered_df["courses_list"].astype(str) == "['btech']"]
elif selected_course_filter == "IDD only":
    filtered_df = filtered_df[filtered_df["courses_list"].astype(str) == "['idd']"]
elif selected_course_filter == "B.Tech + IDD":
    filtered_df = filtered_df[filtered_df["courses_list"].astype(str) == "['btech', 'idd']"]

# Apply month filter
if selected_month != "-- All Months --":
    filtered_df = filtered_df[filtered_df["month"] == selected_month]

# Apply year filter
if selected_year != "-- All Years --":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

# Apply day filter
if selected_day_range == "1 - 15":
    filtered_df = filtered_df[filtered_df["date"].between(1, 15)]
elif selected_day_range == "16 - 31":
    filtered_df = filtered_df[filtered_df["date"].between(16, 31)]

# Sort by the selected salary column (highest first)
filtered_df = filtered_df.sort_values(by=selected_salary_col, ascending=False)

# ---------------- DISPLAY RESULTS ----------------
def to_lpa(val):
    return f"{val/LAKH:.1f} LPA" if pd.notna(val) else "N/A"

if not filtered_df.empty:
    st.success(f"✅ Found {len(filtered_df)} companies matching filters")

    for _, row in filtered_df.iterrows():
        with st.expander(f"🏢 {row['company_name']}"):
            st.markdown(
                f"""
                <div style="background-color:#f9f9f9;
                            padding:15px;
                            margin-bottom:10px;
                            border-radius:10px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p><b>📌 Profile:</b> {row.get('company_profile', row.get('profile', 'N/A'))}</p>
                    <p><b>🎯 CGPA Cutoff:</b> {row.get('cgpa', 'N/A')}</p>
                    <p><b>💰 CTC (B.Tech):</b> {to_lpa(row.get('ctc_btech'))} | <b>Base:</b> {to_lpa(row.get('base_btech'))}</p>
                    <p><b>💰 CTC (IDD):</b> {to_lpa(row.get('ctc_idd'))} | <b>Base:</b> {to_lpa(row.get('base_idd'))}</p>
                    <p><b>📚 Eligible Courses:</b> {row.get('courses_list', 'N/A')}</p>
                    <p><b>🏫 Eligible Departments:</b> {row.get('dept_eligible', 'N/A')}</p>
                    <p><b>⌚ Last updated_time:</b> {row.get('updated_time', 'N/A')}</p>
                     <p><b>🏢 Location:</b> {row.get('location', 'N/A')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("🚫 No companies found for selected filters")
