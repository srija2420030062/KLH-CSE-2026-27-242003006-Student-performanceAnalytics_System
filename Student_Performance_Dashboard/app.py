
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page settings
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Dashboard title
st.title("🎓 Student Performance Analytics Dashboard")
st.write("Analyze student marks, study time, and academic performance.")

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("DATASET/student-mat.csv", sep=";")
    return data

df = load_data()

# Basic data cleaning
df = df.drop_duplicates()
df = df.dropna(subset=["G1", "G2", "G3", "studytime", "absences", "sex"])

# Create pass/fail result
df["Result"] = df["G3"].apply(
    lambda mark: "Pass" if mark >= 10 else "Fail"
)

# Sidebar filters
st.sidebar.header("Filter Students")

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["sex"].unique(),
    default=df["sex"].unique()
)

study_time = st.sidebar.multiselect(
    "Select Study Time",
    options=sorted(df["studytime"].unique()),
    default=sorted(df["studytime"].unique())
)

filtered_df = df[
    (df["sex"].isin(gender)) &
    (df["studytime"].isin(study_time))
]

if filtered_df.empty:
    st.warning("No students found for the selected filters.")
    st.stop()

# KPI metrics
st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(filtered_df))
col2.metric("Average Final Grade", round(filtered_df["G3"].mean(), 2))
col3.metric("Highest Grade", filtered_df["G3"].max())

pass_percentage = (
    (filtered_df["Result"] == "Pass").mean() * 100
)

col4.metric("Pass Percentage", f"{pass_percentage:.2f}%")

st.divider()

# Grade distribution
st.subheader("1. Grade Distribution")

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["G3"], bins=10, kde=True, ax=ax1)
ax1.set_xlabel("Final Grade (G3)")
ax1.set_ylabel("Number of Students")
st.pyplot(fig1)
plt.close(fig1)

# Study time vs marks
st.subheader("2. Study Time vs Average Marks")

study_avg = filtered_df.groupby("studytime")["G3"].mean()

fig2, ax2 = plt.subplots()
study_avg.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Study Time")
ax2.set_ylabel("Average Final Grade")
ax2.set_title("Study Time vs Average Grade")
st.pyplot(fig2)
plt.close(fig2)

# Absences vs marks
st.subheader("3. Absences vs Final Grade")

fig3, ax3 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="absences",
    y="G3",
    hue="sex",
    ax=ax3
)
ax3.set_title("Absences and Student Performance")
st.pyplot(fig3)
plt.close(fig3)

# Gender analysis
st.subheader("4. Gender-wise Performance")

gender_avg = filtered_df.groupby("sex")["G3"].mean()

fig4, ax4 = plt.subplots()
gender_avg.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Gender")
ax4.set_ylabel("Average Final Grade")
st.pyplot(fig4)
plt.close(fig4)

# Pass and fail analysis
st.subheader("5. Pass and Fail Analysis")

result_count = filtered_df["Result"].value_counts()

fig5, ax5 = plt.subplots()
result_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax5
)
ax5.set_ylabel("")
st.pyplot(fig5)
plt.close(fig5)

# Correlation heatmap
st.subheader("6. Subject Marks Correlation")

fig6, ax6 = plt.subplots()
sns.heatmap(
    filtered_df[["G1", "G2", "G3"]].corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax6
)
st.pyplot(fig6)
plt.close(fig6)

# Student data table
st.subheader("7. Student Records")

st.dataframe(filtered_df, use_container_width=True)

# Download filtered data
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Student Data",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
