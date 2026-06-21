from dotenv import load_dotenv
from composio import Composio
import pandas as pd
import yagmail
from datetime import datetime

load_dotenv()

# ----------------------------
# COMPOSIO SETUP
# ----------------------------
client = Composio(
    toolkit_versions={"googlesheets": "20260616_00"}
)

USER_ID = "pg-test-c6ddba40-aabe-425c-8873-03689febc536"

SPREADSHEET_ID = "1btS29Kk-PSHuYs_lIvcPyr0c6FKdA-QfUzGLKox_alA"


# ----------------------------
# FILTER FUNCTION
# ----------------------------
def is_valid_job(title):
    title = title.lower()

    priority_keywords = [
        "sales assistant",
        "retail assistant",
        "customer service",
        "call centre",
        "call center",
        "collections",
        "remote customer support"
    ]

    secondary_keywords = [
        "floor assistant",
        "stock controller",
        "waiter",
        "retail"
    ]

    for word in priority_keywords:
        if word in title:
            return True

    for word in secondary_keywords:
        if word in title:
            return True

    return False


# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("jobs.csv")

values = [["Job Title", "Company", "Link"]]

seen_jobs = set()


# ----------------------------
# PROCESS JOBS
# ----------------------------
for _, row in df.iterrows():
    job_text = row["Job Info"]

    parts = job_text.split("\n")

    title = parts[0] if len(parts) > 0 else ""
    company = parts[1] if len(parts) > 1 else ""
    link = parts[2] if len(parts) > 2 else ""

    # FILTER JOBS
    if not is_valid_job(title):
        continue

    # REMOVE DUPLICATES
    unique_key = f"{title}-{company}-{link}"

    if unique_key in seen_jobs:
        continue

    seen_jobs.add(unique_key)

    values.append([title, company, link])


# ----------------------------
# SEND TO GOOGLE SHEETS
# ----------------------------
result = client.tools.execute(
    user_id=USER_ID,
    slug="GOOGLESHEETS_BATCH_UPDATE",
    arguments={
        "spreadsheet_id": SPREADSHEET_ID,
        "sheet_name": "Sheet1",
        "first_cell_location": "A1",
        "value_input_option": "USER_ENTERED",
        "values": values
    }
)

print(result)