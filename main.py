from datetime import datetime
import feedparser
import logging
import json
import time
import os # Import os module for path operations

# --- Configuration Loading Function ---
def load_config(config_path='config.json'):
    """
    Loads configuration from a JSON file.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: A dictionary containing the loaded configuration.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file is malformed JSON.
    """
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found at: {config_path}")
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from config file {config_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading config: {e}")
        raise


def fetch_feed(feed_name, url, keywords):
    """
    Fetches an RSS feed, parses it, and filters entries based on keywords.

    Args:
        feed_name (str): The name of the feed (e.g., "HackerNews").
        url (str): The URL of the RSS feed.
        keywords (list): A list of keywords to filter titles by.

    Returns:
        list: A list of dictionaries, each representing a matched entry.
    """
    logging.info(f"Fetching RSS from {feed_name} ({url})")
    matched_entries_list = []

    try:
        feed = feedparser.parse(url)

        # Check for parsing errors reported by feedparser's bozo attribute
        if hasattr(feed, 'bozo') and feed.bozo == 1:
            logging.warning(f"Malformed feed detected for {feed_name}: {feed.bozo_exception}")

        # CRITICAL FIX: Check if feed.entries exists and is iterable
        if not hasattr(feed, 'entries') or not isinstance(feed.entries, list):
            logging.warning(f"Feed '{feed_name}' has no usable 'entries' attribute or it's not a list. Skipping processing this feed.")
            return []

        logging.info(f"Total entries found in {feed_name}: {len(feed.entries)}")

        logging.info(f"Processing feed from {feed_name}")
        for entry in feed.entries:
            title = entry.get('title')
            link = entry.get('link')
            published_raw = entry.get('published')

            # --- SAFELY HANDLE SUMMARY ---
            raw_summary = entry.get('summary')
            processed_summary = None # Initialize to None

            if raw_summary:
                # feedparser can return summary as a dict, e.g., {'type': 'text/html', 'value': '...'}
                if isinstance(raw_summary, dict) and 'value' in raw_summary:
                    processed_summary = raw_summary['value']
                elif isinstance(raw_summary, str):
                    processed_summary = raw_summary
                
                # if processed_summary is a string, slice it
                if processed_summary:
                    processed_summary = processed_summary[:200]
                else:
                    processed_summary = None # Ensure it's None if parsing failed

            # Ensure title and link exist before processing
            if not title or not link:
                logging.debug(f"Skipping entry from {feed_name} due to missing title or link: {entry}")
                continue

            title_lower = title.lower()
            
            # Convert published date to ISO 8601 format
            published_iso = None
            if published_raw:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_iso = datetime(*entry.published_parsed[:6]).isoformat()
                except Exception as e:
                    logging.warning(f"Could not parse published date '{published_raw}' for entry '{title}': {e}")
            
            # Check if any keyword is present in the title
            if any(keyword in title_lower for keyword in keywords):
                matched_entries_list.append({
                    'source': feed_name,
                    'title': title,
                    'summary': processed_summary, # Use the safely processed summary
                    'link': link,
                    'published': published_iso,
                })

    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching/processing {feed_name} ({url}): '{e}'")

    return matched_entries_list

def vea(feed_dictionary, keyword_list):
    """
    Aggregates news from multiple RSS feeds, filters them, and deduplicates.

    Args:
        feed_dictionary (dict): A dictionary of feed names to URLs.
        keyword_list (list): A list of keywords to filter by.

    Returns:
        list: A list of unique matched entries.
    """
    logging.info("Starting Vea aggregation process.")
    all_matched_entries = []
    seen_links = set() # To store unique links for deduplication

    for name, url in feed_dictionary.items():
        # Fetch entries for the current feed
        current_feed_entries = fetch_feed(name, url, keyword_list)
        
        # Deduplicate and add to the main list
        for entry in current_feed_entries:
            if entry['link'] not in seen_links:
                all_matched_entries.append(entry)
                seen_links.add(entry['link'])
            else:
                logging.debug(f"Duplicate entry found and skipped: {entry['link']}")

    logging.info(f"Aggregation complete. Total unique results: {len(all_matched_entries)}")
    return all_matched_entries

def export_data(data, output_dir="."):
    """
    Exports the collected data to a JSON file.

    Args:
        data (list): The list of dictionaries to export.
        output_dir (str): The directory to save the JSON file. Defaults to current directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")

    file_name = f"{datetime.today().date()}-news.json"
    file_path = os.path.join(output_dir, file_name)

    logging.info(f"Exporting data to {file_path}")
    try:
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info(f"Data successfully exported to {file_path}")
    except IOError as e:
        logging.error(f"Error exporting data to {file_path}: {e}")

if __name__ == "__main__":
    # --- Logging Initialization (Moved to the very top) ---
    # We'll set an initial log level (e.g., INFO or DEBUG) here.
    # It can be updated later with the config's log_level, if successfully loaded.
    initial_log_level = logging.INFO # Use INFO as a sensible default
    
    logging.basicConfig(filename='vea.log',
                        format='[%(asctime)s-%(levelname)s-%(funcName)s-%(lineno)d]: %(message)s',
                        level=initial_log_level,
                        encoding='utf-8')
    logging.info("Vea script started. Logging initialized.")

    # --- Configuration Loading ---
    config_file_path = 'config.json'
    try:
        config = load_config(config_file_path)

        # If config loads successfully, update log level from config
        log_level_str = config.get('log_level', 'INFO').upper()
        numeric_log_level = getattr(logging, log_level_str, logging.INFO)
        if not isinstance(numeric_log_level, int):
            numeric_log_level = logging.INFO
            logging.warning(f"Invalid log_level '{log_level_str}' in config. Defaulting to INFO.")
        
        # Set the root logger level (which basicConfig applies to)
        logging.getLogger().setLevel(numeric_log_level)
        logging.info(f"Log level updated to: {logging.getLevelName(numeric_log_level)}")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Now this critical message will go to vea.log because basicConfig has run
        logging.critical(f"Failed to load configuration from {config_file_path}: {e}. Exiting.")
        exit(1) # Exit the script if config loading fails

    # --- Proceed with script execution only if config loaded successfully ---
    keyword_list = config.get('keywords', [])
    feed_dictionary = config.get('feeds', {})
    output_directory = config.get('output_directory', 'data')

    logging.info("=============== Starting Vea News Aggregator ===============")
    
    start_time = time.time()
    
    result = vea(feed_dictionary, keyword_list)
    export_data(result, output_directory)

    end_time = time.time()
    duration = end_time - start_time

    logging.info(f"Total unique articles collected: {len(result)}")
    logging.info(f"Vea operation completed in {duration:.2f} seconds.")
    logging.info("=============== Vea News Aggregator Finished ===============")