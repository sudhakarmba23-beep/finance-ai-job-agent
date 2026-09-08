from pathlib import Path
import re
import pandas as pd


SKILLS = [
    "financial reporting",
    "general ledger",
    "gl",
    "record to report",
    "r2r",
    "procure to pay",
    "p2p",
    "order to cash",
    "o2c",
    "fp&a",
    "budgeting",
    "forecasting",
    "accounts payable",
    "accounts receivable",
    "gst",
    "tds",
    "payroll",
    "sap fi",
    "tally",
    "zoho books",
    "advanced excel",
    "month end close",
    "year end close",
    "cash flow",
    "working capital",
    "audit",
    "internal controls",
    "statutory compliance",
    "mis reporting",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def calculate_ats_score(resume_text: str, job_text: str) -> int:
    resume = normalize(resume_text)
    job = normalize(job_text)

    if not job:
        return 0

    required = [skill for skill in SKILLS if skill in job]
    if not required:
        required = [
            word for word in set(re.findall(r"[a-zA-Z&]+", job))
            if len(word) >= 5
        ][:20]

    if not required:
        return 0

    matched = sum(1 for skill in required if skill in resume)
    return round((matched / len(required)) * 100)


def score_jobs_in_tracker(project_root: Path, resume_text: str) -> None:
    tracker = project_root / "jobs" / "job_tracker.xlsx"
    if not tracker.exists():
        return

    df = pd.read_excel(tracker)

    descriptions = df.get("Job Description", pd.Series([""] * len(df))).fillna("")
    titles = df.get("Job Title", pd.Series([""] * len(df))).fillna("")

    scores = []
    for title, description in zip(titles, descriptions):
        combined = f"{title}\n{description}"
        scores.append(calculate_ats_score(resume_text, combined))

    df["ATS Score"] = scores
    df.to_excel(tracker, index=False)


if __name__ == "__main__":
    print("Run app/main.py to score the jobs in the tracker.")
