from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
import json
import time

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def load_settings(project_root: Path) -> dict:
    path = project_root / "config" / "settings.json"
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def search_urls(keyword: str, location: str) -> dict[str, str]:
    q = quote_plus(keyword)
    loc = quote_plus(location)

    return {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}",
        "Indeed": f"https://in.indeed.com/jobs?q={q}&l={loc}",
        "Naukri": f"https://www.naukri.com/{q.replace('+', '-')}-jobs-in-{loc.replace('+', '-')}",
    }


def clean_text(value: str | None) -> str:
    return " ".join((value or "").split())


def get_text(locator, selector: str) -> str:
    try:
        return clean_text(locator.locator(selector).first.inner_text(timeout=1500))
    except Exception:
        return ""


def get_href(locator, selector: str) -> str:
    try:
        return locator.locator(selector).first.get_attribute("href", timeout=1500) or ""
    except Exception:
        return ""


def collect_linkedin(page, limit: int) -> list[dict]:
    jobs = []
    cards = page.locator(
        "div.base-card, li.jobs-search-results__list-item, div.job-search-card"
    )

    count = min(cards.count(), limit)
    for i in range(count):
        card = cards.nth(i)
        title = (
            get_text(card, "h3")
            or get_text(card, ".base-search-card__title")
            or get_text(card, "a.job-card-list__title")
        )
        company = (
            get_text(card, "h4")
            or get_text(card, ".base-search-card__subtitle")
            or get_text(card, ".job-card-container__company-name")
        )
        location = (
            get_text(card, ".job-search-card__location")
            or get_text(card, ".job-card-container__metadata-item")
        )
        link = (
            get_href(card, "a.base-card__full-link")
            or get_href(card, "a")
        )
        if title:
            jobs.append(make_row(title, company, location, "LinkedIn", link))
    return jobs


def collect_indeed(page, limit: int) -> list[dict]:
    jobs = []
    cards = page.locator(
        "div.job_seen_beacon, div.cardOutline, a.tapItem"
    )

    count = min(cards.count(), limit)
    for i in range(count):
        card = cards.nth(i)
        title = (
            get_text(card, "h2.jobTitle")
            or get_text(card, "[data-testid='job-title']")
        )
        company = (
            get_text(card, "[data-testid='company-name']")
            or get_text(card, ".companyName")
        )
        location = (
            get_text(card, "[data-testid='text-location']")
            or get_text(card, ".companyLocation")
        )
        link = get_href(card, "a")
        if link.startswith("/"):
            link = "https://in.indeed.com" + link
        if title:
            jobs.append(make_row(title, company, location, "Indeed", link))
    return jobs


def collect_naukri(page, limit: int) -> list[dict]:
    jobs = []
    cards = page.locator(
        "article.jobTuple, div.srp-jobtuple-wrapper, div.cust-job-tuple"
    )

    count = min(cards.count(), limit)
    for i in range(count):
        card = cards.nth(i)
        title = (
            get_text(card, "a.title")
            or get_text(card, ".title")
        )
        company = (
            get_text(card, "a.comp-name")
            or get_text(card, ".comp-dtls-wrap")
        )
        location = (
            get_text(card, ".locWdth")
            or get_text(card, ".location")
        )
        link = get_href(card, "a.title") or get_href(card, "a")
        if title:
            jobs.append(make_row(title, company, location, "Naukri", link))
    return jobs


def make_row(
    title: str,
    company: str,
    location: str,
    source: str,
    link: str,
) -> dict:
    return {
        "Job Title": clean_text(title),
        "Company": clean_text(company),
        "Location": clean_text(location),
        "Experience": "",
        "Source": source,
        "Job Link": link,
        "Job Description": "",
        "ATS Score": "",
        "Status": "To Review",
        "Date Found": datetime.now().strftime("%d-%m-%Y"),
        "Notes": "Collected from visible search results. Review before applying.",
    }


def append_to_tracker(project_root: Path, new_jobs: list[dict]) -> Path:
    tracker = project_root / "jobs" / "job_tracker.xlsx"
    tracker.parent.mkdir(parents=True, exist_ok=True)

    new_df = pd.DataFrame(new_jobs)

    if tracker.exists():
        existing = pd.read_excel(tracker)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    for column in ["Job Title", "Company", "Job Link"]:
        if column not in combined.columns:
            combined[column] = ""

    combined = combined.drop_duplicates(
        subset=["Job Title", "Company", "Job Link"],
        keep="last",
    )

    combined.to_excel(tracker, index=False)
    return tracker


def main():
    project_root = Path(__file__).resolve().parent.parent
    settings = load_settings(project_root)
    keywords = settings.get("job_titles", ["Finance Manager"])
    location = settings.get("location", "Bengaluru")
    max_per_site = int(settings.get("max_jobs_per_site", 20))

    collected: list[dict] = []

    print("=" * 65)
    print("FINANCE JOB COLLECTOR")
    print("=" * 65)
    print("A browser will open. Log in manually when required.")
    print("The program only reads visible job cards; it does not apply.")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        for keyword in keywords:
            print(f"\nSearching: {keyword} | {location}")

            for source, url in search_urls(keyword, location).items():
                print(f"Opening {source}...")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    print(
                        f"Review/login in the browser. Waiting 15 seconds for {source}..."
                    )
                    time.sleep(15)

                    if source == "LinkedIn":
                        jobs = collect_linkedin(page, max_per_site)
                    elif source == "Indeed":
                        jobs = collect_indeed(page, max_per_site)
                    else:
                        jobs = collect_naukri(page, max_per_site)

                    print(f"Collected {len(jobs)} visible jobs from {source}.")
                    collected.extend(jobs)

                except PlaywrightTimeoutError:
                    print(f"{source}: page timed out; skipped.")
                except Exception as exc:
                    print(f"{source}: could not collect jobs ({exc}).")

        context.close()
        browser.close()

    if not collected:
        print("\nNo visible job cards were collected.")
        print("Run app/search_links.py and add suitable jobs manually to Excel.")
        return

    tracker = append_to_tracker(project_root, collected)
    print(f"\nSaved {len(collected)} collected rows to:")
    print(tracker)
    print("\nNext run:")
    print("python app/main.py")


if __name__ == "__main__":
    main()
