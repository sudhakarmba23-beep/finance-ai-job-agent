from datetime import datetime
from pathlib import Path
import pandas as pd


COLUMNS = [
    "Job Title",
    "Company",
    "Location",
    "Experience",
    "Source",
    "Job Link",
    "Job Description",
    "ATS Score",
    "Status",
    "Date Found",
    "Notes",
]


def create_job_tracker(project_root: Path | None = None) -> Path:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent

    jobs_folder = project_root / "jobs"
    jobs_folder.mkdir(parents=True, exist_ok=True)
    output = jobs_folder / "job_tracker.xlsx"

    if output.exists():
        return output

    starter_jobs = [
        {
            "Job Title": "Finance Manager",
            "Company": "",
            "Location": "Bengaluru",
            "Experience": "10-15 Years",
            "Source": "Manual",
            "Job Link": "",
            "Job Description": "",
            "ATS Score": "",
            "Status": "To Review",
            "Date Found": datetime.now().strftime("%d-%m-%Y"),
            "Notes": "Replace this sample row with a real job.",
        },
        {
            "Job Title": "Accounts Manager",
            "Company": "",
            "Location": "Bengaluru",
            "Experience": "10-15 Years",
            "Source": "Manual",
            "Job Link": "",
            "Job Description": "",
            "ATS Score": "",
            "Status": "To Review",
            "Date Found": datetime.now().strftime("%d-%m-%Y"),
            "Notes": "Replace this sample row with a real job.",
        },
    ]

    pd.DataFrame(starter_jobs, columns=COLUMNS).to_excel(output, index=False)
    return output


if __name__ == "__main__":
    path = create_job_tracker()
    print("=" * 50)
    print("JOB TRACKER CREATED SUCCESSFULLY")
    print("=" * 50)
    print(f"Saved to: {path}")
