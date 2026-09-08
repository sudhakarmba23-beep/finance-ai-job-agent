from pathlib import Path
import re
import pandas as pd


def safe_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(value).strip())
    return value.strip("_") or "job"


def build_cover_letter(job_title: str, company: str, resume_text: str) -> str:
    company_name = company.strip() or "your organization"

    return f"""Dear Hiring Manager,

I am writing to apply for the {job_title} position at {company_name}. I bring more than 15 years of experience in finance and accounting, including financial reporting, general ledger, R2R, P2P, O2C, budgeting, forecasting, accounts payable, accounts receivable, GST, TDS, payroll, audit coordination, cash-flow management, and statutory compliance.

My experience includes managing finance operations for an organization with annual turnover of approximately ₹20 crore, improving vendor-payment processing time by 50%, improving receivable collections by 50%, processing payroll, strengthening internal controls, and supporting management through timely MIS and financial analysis. I am also experienced with SAP FI, Tally ERP, Zoho Books, and Advanced Microsoft Excel.

I would welcome the opportunity to discuss how my finance leadership, process-improvement experience, and hands-on accounting knowledge can contribute to {company_name}.

Sincerely,
Sudhakar Nalla
Bengaluru
"""

def generate_cover_letters(project_root: Path, resume_text: str) -> None:
    tracker = project_root / "jobs" / "job_tracker.xlsx"
    output_folder = project_root / "applications" / "cover_letters"
    output_folder.mkdir(parents=True, exist_ok=True)

    if not tracker.exists():
        return

    df = pd.read_excel(tracker)

    for index, row in df.iterrows():
        title = str(row.get("Job Title", "")).strip()
        company = str(row.get("Company", "")).strip()

        if not title:
            continue

        filename = (
            f"{index + 1:03d}_"
            f"{safe_filename(company)}_"
            f"{safe_filename(title)}.txt"
        )

        letter = build_cover_letter(title, company, resume_text)
        (output_folder / filename).write_text(letter, encoding="utf-8")


if __name__ == "__main__":
    print("Run app/main.py to generate cover letters.")
