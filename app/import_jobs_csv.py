from pathlib import Path
from datetime import datetime
import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_file = project_root / "data" / "jobs_import.csv"
    tracker = project_root / "jobs" / "job_tracker.xlsx"

    if not csv_file.exists():
        print(f"CSV not found: {csv_file}")
        return

    imported = pd.read_csv(csv_file)

    required_defaults = {
        "Job Title": "",
        "Company": "",
        "Location": "Bengaluru",
        "Experience": "",
        "Source": "CSV Import",
        "Job Link": "",
        "Job Description": "",
        "ATS Score": "",
        "Status": "To Review",
        "Date Found": datetime.now().strftime("%d-%m-%Y"),
        "Notes": "",
    }

    for column, default in required_defaults.items():
        if column not in imported.columns:
            imported[column] = default

    if tracker.exists():
        existing = pd.read_excel(tracker)
        combined = pd.concat([existing, imported], ignore_index=True)
    else:
        combined = imported

    combined = combined.drop_duplicates(
        subset=["Job Title", "Company", "Job Link"],
        keep="last",
    )

    combined.to_excel(tracker, index=False)
    print(f"Imported {len(imported)} job(s) into {tracker}")


if __name__ == "__main__":
    main()
