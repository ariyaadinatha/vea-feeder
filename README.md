# Vea - RSS News Aggregator

Vea is a Python-based RSS feed aggregator designed to fetch news articles from various sources, filter them based on keywords, and export the relevant headlines to a JSON file. It's perfect for keeping track of cybersecurity news, specific vulnerabilities, or any topics of interest from your favorite RSS feeds.

## Features

* **Configurable Feeds:** Easily add or remove RSS feed URLs via a simple JSON configuration file.
* **Keyword Filtering:** Define a list of keywords to automatically filter articles based on their titles.
* **Deduplication:** Ensures that duplicate articles (even if found across different feeds) are only stored once.
* **Structured Output:** Exports matched articles to a clear, readable JSON file, including source, title, link, and published date.
* **Logging:** Provides detailed logs of the aggregation process, making it easy to troubleshoot and monitor.
* **Flexible Output:** Stores results in a dated JSON file within a configurable output directory.

## Getting Started

Follow these steps to set up and run Vea on your system.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone git@github.com:ariyaadinatha/vea-feeder.git
    cd vea-feeder
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **On macOS (if you encounter SSL errors):**
    If you're on macOS and experience `[SSL: CERTIFICATE_VERIFY_FAILED]` errors, you might need to install Python's SSL certificates:
    ```bash
    /Applications/Python\ 3.x/Install\ Certificates.command
    ```
    (Replace `Python 3.x` with your actual Python version, e.g., `Python 3.10`).

## Configuration

Vea uses a `config.json` file to manage its settings. This file should be located in the same directory as the main script (`vea.py`).

### `config.json` Example:

```json
{
  "keywords": [
    "ransomware",
    "fortinet",
    "vulnerability",
    "exploit",
    "malware",
    "cybersecurity",
    "phishing"
  ],
  "feeds": {
    "HackerNews": "https://hnrss.org/frontpage",
    "ThreatPost": "https://threatpost.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
    "SANS Internet Storm Center": "https://isc.sans.edu/rssfeed.xml",
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/"
  },
  "output_directory": "data",
  "log_level": "INFO"
}
```

* **`keywords`**: A list of strings. Vea will search for these keywords (case-insensitive) in the article titles.
* **`feeds`**: A dictionary where each key is a human-readable feed name (e.g., "HackerNews") and its value is the RSS feed URL.
* **`output_directory`**: The name of the directory where the JSON output files will be saved. Vea will create this directory if it doesn't exist.
* **`log_level`**: The verbosity of the logging. Recommended values are `"INFO"` (for general use) or `"DEBUG"` (for detailed troubleshooting). Other standard logging levels like `"WARNING"`, `"ERROR"`, `"CRITICAL"` are also supported.

## Usage

To run Vea, simply execute the Python script from your terminal:

```bash
python3 vea.py
```

### Output

Upon successful execution, Vea will:

1.  Create an `vea.log` file in the script's directory, containing execution details.
2.  Create an `output_directory` (defaulting to `data/` if not specified in `config.json`) if it doesn't exist.
3.  Save the filtered and deduplicated news articles into a JSON file named `YYYY-MM-DD-news.json` (e.g., `2025-06-05-news.json`) within the `output_directory`.

### Example `2025-06-05-news.json` output:

```json
[
    {
        "source": "ThreatPost",
        "title": "Ransomware Attacks are on the Rise",
        "summary": "Lockbit is by far this summer’s most prolific ransomware group, trailed by two offshoots of the Conti group.",
        "link": "https://threatpost.com/ransomware-attacks-are-on-the-rise/180481/",
        "published": "2022-08-26T16:44:27"
    },
    {
        "source": "The Hacker News",
        "title": "Chaos RAT Malware Targets Windows and Linux via Fake Network Tool Downloads",
        "summary": "Threat hunters are calling attention to a new variant of a remote access trojan (RAT) called Chaos RAT that has been used in recent attacks targeting Windows and Linux systems.\nAccording to findings f",
        "link": "https://thehackernews.com/2025/06/chaos-rat-malware-targets-windows-and.html",
        "published": "2025-06-04T12:55:00"
    },
]
```

## Dependencies

Vea relies on the following Python libraries:

* `feedparser`: For parsing RSS/Atom feeds.
* `certifi`: Provides Mozilla's carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates.

## Troubleshooting

* **`[SSL: CERTIFICATE_VERIFY_FAILED]` errors:**
    * Ensure your `certifi` package is up to date: `pip install --upgrade certifi`
    * On macOS, run `Install Certificates.command` as mentioned in the Installation section.
    * If you are behind a corporate proxy, you might need to configure your environment to trust your company's CA certificates. Consult your IT department or refer to `requests` library documentation on `REQUESTS_CA_BUNDLE`.
* **No output/Empty JSON file:**
    * Check `vea.log` for any error messages or warnings.
    * Verify that your `keywords` in `config.json` are present in the titles of the articles you expect to see.
    * Ensure the RSS feed URLs in `config.json` are correct and accessible.