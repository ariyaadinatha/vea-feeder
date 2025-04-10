import feedparser

def fetch_feed(feed_name, url, keywords):
    feed = feedparser.parse(url)
    matched_entries_list = []

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

    result_list = []

    for name, url in feed_dictionary.items():
        result = fetch_feed(name, url, keyword_list)
        result_list += result

    print(result_list)
    print(len(result_list))
        