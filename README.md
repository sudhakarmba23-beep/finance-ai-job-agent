# Finance AI Job Application Agent

A Windows-friendly, semi-automated job-search assistant for finance and accounting roles.

## What it does

- Creates and maintains an Excel job tracker.
- Opens LinkedIn, Naukri and Indeed search pages.
- Reads a DOCX resume.
- Calculates a simple ATS match score.
- Generates tailored cover-letter drafts.
- Imports jobs from CSV.

## Important

This project does not automatically submit applications or bypass website controls. You review every job and submit each application yourself.

## Setup

1. Open this folder in VS Code.
2. Put your DOCX resume inside the `resumes` folder.
3. Open a VS Code terminal.
4. Run:

```powershell
python -m pip install -r requirements.txt
python app/main.py
```

## Open job searches

```powershell
python app/search_links.py
```

This opens job-search pages in your normal web browser.

## Add real jobs

Open:

```text
jobs/job_tracker.xlsx
```

Add the job title, company, link and job description.

Then run:

```powershell
python app/main.py
```

The program updates ATS scores and creates cover letters inside:

```text
applications/cover_letters
```

## Import multiple jobs from CSV

Edit:

```text
data/jobs_import.csv
```

Then run:

```powershell
python app/import_jobs_csv.py
python app/main.py
```

## Suggested workflow

1. Run `python app/search_links.py`.
2. Review jobs in the browser.
3. Copy suitable jobs into `jobs/job_tracker.xlsx`.
4. Run `python app/main.py`.
5. Review ATS scores and cover-letter drafts.
6. Apply manually after checking all information.


## Module 1: Browser-assisted job collection

Run:

```powershell
python app/job_collector.py
```

A Chromium browser opens and searches LinkedIn, Indeed and Naukri for the roles in `config/settings.json`.

Important:
- Log in manually when a site asks.
- The script reads only visible job cards.
- It does not submit applications.
- Site layouts can change. When a site blocks collection, use `python app/search_links.py` and add jobs manually.

After collection, run:

```powershell
python app/main.py
```

This updates ATS scores and cover letters.
