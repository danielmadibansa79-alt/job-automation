import streamlit as st
import pandas as pd

# ----------------------------
# PAGE CONFIG (SAAS LOOK)
# ----------------------------
st.set_page_config(
    page_title="AI Job Control Panel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# DARK UI STYLE
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main {
    background-color: #0e1117;
}

.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #161b22;
    margin-bottom: 10px;
    border: 1px solid #2a2f3a;
}

.big-title {
    font-size: 28px;
    font-weight: bold;
    color: #58a6ff;
}

.small-text {
    color: #8b949e;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("jobs.csv")

def parse_job(text):
    parts = str(text).split("\n")
    title = parts[0] if len(parts) > 0 else ""
    company = parts[1] if len(parts) > 1 else ""
    link = parts[2] if len(parts) > 2 else ""
    return title, company, link

jobs = []
for _, row in df.iterrows():
    t, c, l = parse_job(row["Job Info"])
    jobs.append([t, c, l])

jobs_df = pd.DataFrame(jobs, columns=["Title", "Company", "Link"])

# ----------------------------
# AI SCORE ENGINE
# ----------------------------
def score_job(title, company):
    text = (title + " " + company).lower()
    score = 0

    if any(x in text for x in ["sales", "customer", "retail", "call"]):
        score += 40
    if "entry" in text or "junior" in text:
        score += 25
    if "remote" in text:
        score += 20
    if "cape town" in text:
        score += 10
    if any(x in text for x in ["mlm", "crypto", "investment"]):
        score -= 100

    return score

jobs_df["Score"] = jobs_df.apply(lambda x: score_job(x["Title"], x["Company"]), axis=1)
jobs_df = jobs_df.sort_values(by="Score", ascending=False)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Control Panel")

search = st.sidebar.text_input("Search Jobs")

min_score = st.sidebar.slider("Minimum Score", 0, 100, 50)

filtered_df = jobs_df[jobs_df["Score"] >= min_score]

if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.lower().str.contains(search.lower())
    ]

# ----------------------------
# HEADER
# ----------------------------
st.markdown('<div class="big-title">🚀 AI Job Control Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="small-text">Live ranked job system with AI filtering</div>', unsafe_allow_html=True)

# ----------------------------
# METRICS CARDS
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(jobs_df))
col2.metric("Best Score", jobs_df["Score"].max())
col3.metric("Filtered Jobs", len(filtered_df))

# ----------------------------
# TABS UI
# ----------------------------
tab1, tab2, tab3 = st.tabs(["🔥 Top Jobs", "📊 All Jobs", "🎯 Best Only"])

# ----------------------------
# TAB 1
# ----------------------------
with tab1:
    st.subheader("Top Ranked Jobs")

    for _, row in jobs_df.head(10).iterrows():
        st.markdown(f"""
        <div class="card">
        <b>{row['Title']}</b><br>
        {row['Company']}<br>
        Score: <b>{row['Score']}</b><br>
        <a href="{row['Link']}" target="_blank">Open Job</a>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# TAB 2
# ----------------------------
with tab2:
    st.subheader("All Jobs")
    st.dataframe(jobs_df, use_container_width=True)

# ----------------------------
# TAB 3
# ----------------------------
with tab3:
    st.subheader("Best Jobs Only")

    best = filtered_df[filtered_df["Score"] > 60]

    st.dataframe(best, use_container_width=True)

    st.download_button(
        "⬇ Download Best Jobs",
        best.to_csv(index=False),
        "best_jobs.csv"
    )