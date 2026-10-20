"""Cache openly available primary-source evidence; never overwrite existing files."""
from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "figshare_metadata.json": "https://api.figshare.com/v2/articles/24906924",
    "mohamad_2025.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11800717/",
    "sarid_lipka_2023.html": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1172771/full",
    "gormley.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6209537/",
    "lipka_2020.html": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00923/full",
    "baczewski_2022.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8992914/",
    "aas_author_appendix.html": "https://www.researchgate.net/publication/305617123_The_AAS_-_appendix",
    "kazakhstan_mental_health.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11820214/",
    "baczewski_crossref.json": "https://api.crossref.org/works/10.1089/aut.2021.0012",
}


def write_israel_table_fixture(directory: Path) -> None:
    """Keep the attributed CC BY Table 3 needed for offline transcription tests."""
    source = directory / "sarid_lipka_2023.html"
    destination = directory / "sarid_lipka_2023_table3.html"
    if not source.exists() or destination.exists():
        return
    soup = BeautifulSoup(source.read_bytes(), "html.parser")
    tables = [table for table in soup.find_all("table") if "Total Adjustment" in table.get_text(" ", strip=True)]
    if len(tables) != 1:
        raise ValueError("Cannot uniquely locate Sarid & Lipka Table 3")
    destination.write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<title>Sarid &amp; Lipka (2023), Table 3</title></head><body>\n'
        '<p>Source: Sarid, M., &amp; Lipka, O. (2023). Students with learning '
        'disabilities/attention-deficit/hyperactivity disorder in higher education '
        'dealing with remote learning: lessons learned from COVID-19 era. '
        '<a href="https://doi.org/10.3389/fpsyg.2023.1172771">'
        'Frontiers in Psychology, 14, 1172771</a>, Table 3. '
        'Copyright 2023 Sarid and Lipka. '
        '<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. '
        'Accessed 2026-10-20. This is an attributed table extract; the publisher '
        'website wrapper was removed and the table content is unchanged.</p>\n'
        + str(tables[0]) + '\n</body></html>\n'
    )


def retrieve(name: str, url: str, directory: Path) -> dict:
    path = directory / name
    row = {"name": name, "url": url, "checked_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        existed = path.exists()
        if not existed:
            with urlopen(Request(url, headers={"User-Agent": "ADHD-Research-Reanalysis/1.0"}), timeout=45) as response:
                body = response.read()
            path.write_bytes(body)
        body = path.read_bytes()
        row.update(status="cached_preexisting" if existed else "downloaded", bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        if name.endswith(".html"):
            soup = BeautifulSoup(body, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            content = soup.get_text(" ", strip=True)
            if not path.with_suffix(".txt").exists():
                path.with_suffix(".txt").write_text(content)
            row["readable_content"] = len(content) > 10000 and "Checking your browser" not in content[:1000]
        print(f"{name}: {row['status']} ({len(body):,} bytes)")
    except Exception as error:
        row.update(status="failed", error=f"{type(error).__name__}: {error}")
        print(f"{name}: {row['error']}")
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    meta = ROOT / "data" / "metadata"
    meta.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        records = list(pool.map(lambda item: retrieve(*item, meta), SOURCES.items()))
    write_israel_table_fixture(meta)
    metadata_path = meta / "figshare_metadata.json"
    if metadata_path.exists():
        article = json.loads(metadata_path.read_text())
        if article["license"]["name"] != "CC BY 4.0":
            raise ValueError("Review changed data licensing before downloading")
        for file in article["files"]:
            record = retrieve(file["name"], file["download_url"], ROOT / "data" / "raw")
            if record["status"] != "failed":
                body = (ROOT / "data" / "raw" / file["name"]).read_bytes()
                record["md5"] = hashlib.md5(body).hexdigest()
                record["matches_publisher_md5"] = record["md5"] == file["computed_md5"]
                if not record["matches_publisher_md5"]:
                    raise ValueError("Publisher MD5 validation failed")
            records.append(record)
    (meta / "retrieval_log.json").write_text(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
