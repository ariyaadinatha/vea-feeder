from datetime import datetime
import feedparser
import logging

def fetch_feed(feed_name, url, keywords):
    logging.info(f"Fetching RSS from {feed_name}")

    feed = feedparser.parse(url)
    matched_entries_list = []
    logging.info(f"Total feed fetched: {len(feed.entries)}")
    
    logging.info(f"Processing feed from {feed_name}")
    for entry in feed.entries:
        title = entry.get('title')
        summary = entry.get('summary')
        link = entry.get('link')
        published = entry.get('published')
        
        for keyword in keywords:
            if keyword in title.lower():
                matched_entries_list.append({
                    'source': feed_name,
                    'title': title,
                    'link': link,
                    'published': published,
                })

    return matched_entries_list

def vea():
    result_list = []

    for name, url in feed_dictionary.items():
        result = fetch_feed(name, url, keyword_list)
        result_list += result

    return result_list


if __name__ == "__main__":
    # keywords to filter
    keyword_list = ['ransomware', 'fortinet']

    # Dictionary of feeds
    feed_dictionary = {
        "HackerNews": "https://hnrss.org/frontpage",
        "ThreatPost": "https://threatpost.com/feed/",
        "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
        "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
    }

    # Logging file initialization
    logging.basicConfig(filename='vea.log',
                    format='[%(asctime)s-%(levelname)s-%(funcName)s-%(lineno)d]: %(message)s', level=logging.INFO)

    logging.info("=============== Starting Vea ===============")
    result = vea()
    print(result)
    logging.info(f"Total result: {len(result)}")
    logging.info("=============== Successfully running Vea ===============")        