import requests

from bs4 import BeautifulSoup

QUALIFICATION_KEYWORDS = [
    "team", "role", "responsibilities", "qualifications",
    "skills", "you will", "thrive", "looking for",
    "background", "responsible", "nice to have",
    "good fit", "may also have", "technologies"
]


def retreive_qualification(url: str) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    qualifications = {}

    for ul in soup.find_all("ul"):
        list_items = ul.find_all("li")

        if not list_items:
            continue

        heading = ul.find_previous(["h2", "h3", "h4", "p"])

        if heading is None:
            continue

        if heading.name == "p":
            bold_text = heading.find(["strong", "b"])

            if bold_text is None:
                continue

            heading_text = bold_text.get_text(" ", strip=True)

        else:
            heading_text = heading.get_text(" ", strip=True)

        heading_lower = heading_text.lower()

        if not any(
            keyword in heading_lower
            for keyword in QUALIFICATION_KEYWORDS
        ):
            continue

        qualifications[heading_text] = [
            item.get_text(" ", strip=True)
            for item in list_items
        ]

    return qualifications