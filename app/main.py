from pathlib import Path
from job_search import create_job_tracker
from resume_parser import find_resume, extract_resume_text
from ats_match import score_jobs_in_tracker
from cover_letter import generate_cover_letters


def main():
    project_root = Path(__file__).resolve().parent.parent

    for folder_name in [
        "resumes", "jobs", "applications", "reports", "data", "config"
    ]:
        (project_root / folder_name).mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("FINANCE AI JOB APPLICATION AGENT")
    print("=" * 60)

    tracker = create_job_tracker(project_root)
    print(f"Job tracker ready: {tracker}")

    resume_path = find_resume(project_root / "resumes")
    if not resume_path:
        print("\nACTION REQUIRED:")
        print("Copy your .docx resume into the resumes folder.")
        return

    resume_text = extract_resume_text(resume_path)
    print(f"Resume loaded: {resume_path.name}")

    score_jobs_in_tracker(project_root, resume_text)
    generate_cover_letters(project_root, resume_text)

    print("\nCompleted successfully.")
    print("Open jobs/job_tracker.xlsx to review your jobs.")


if __name__ == "__main__":
    main()
