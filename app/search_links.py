from pathlib import Path
from urllib.parse import quote_plus
import json
import webbrowser


def load_config(project_root: Path) -> dict:
    config_file = project_root / "config" / "settings.json"
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def build_search_urls(keywords: list[str], location: str) -> list[tuple[str, str]]:
    urls = []
    for keyword in keywords:
        q = quote_plus(keyword)
        loc = quote_plus(location)

        urls.extend([
            (
                f"LinkedIn - {keyword}",
                f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}",
            ),
            (
                f"Naukri - {keyword}",
                f"https://www.naukri.com/{q.replace('+', '-')}-jobs-in-{loc.replace('+', '-')}",
            ),
            (
                f"Indeed - {keyword}",
                f"https://in.indeed.com/jobs?q={q}&l={loc}",
            ),
        ])
    return urls


def main():
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root)

    urls = build_search_urls(
        config["job_titles"],
        config["location"],
    )

    print("Opening job-search pages in your browser...")
    for name, url in urls:
        print(name)
        webbrowser.open_new_tab(url)

    print("\nReview suitable jobs and paste them into jobs/job_tracker.xlsx.")


if __name__ == "__main__":
    main()
