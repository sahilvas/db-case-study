import requests
from bs4 import BeautifulSoup
import csv
import plotly.graph_objects as go
from collections import Counter
import time
import logging
import argparse
import sys, os

# Get the directory where bin/utils is located
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(f"Base directory: {base_dir}")

# Add the root project directory to the Python path so that it can find the 'utils' directory
sys.path.append(base_dir)

from utils.set_logger import set_logger


# Timeout settings
TIMEOUT = 20  # seconds

# List of URLs (List 1)
urls = [
    "https://sanctionssearch.ofac.treas.gov/",
    "https://home.treasury.gov/",
    "https://www.thomsonreuters.com/",
    "https://verafin.com/solution/",
    "https://www.swift.com/",
    "https://anti-fraud.ec.europa.eu/index_en",
    "https://www.kroll.com/",
    "https://learn.seon.io/"
]

# List of Keyword Sets (List 2)
keyword_sets = [
    {"Sanctions"}, {"OFAC"},
    {"Foreign Sanctions"}, {"Balkans"},
    {"ESG trends"}, {"Corporate income tax"},
    {"European Parliament"}, {"customs fraud"},
    {"Cybersecurity"}, {"OLAF"},
    {"Device Fingerprinting"}
]


# Set default paths
logs_directory = os.path.join(base_dir, "logs")
output_directory = os.path.join(base_dir, "output")

# Global constants
script_log_identifier = "demo_script"
valid_links_csv_filename = output_directory + "/valid_links.csv"
keyword_stats_csv_filename = output_directory + "/keyword_stats.csv"
valid_links_html_filename = output_directory + "/valid_links_graphs.html"
keyword_stats_html_filename = output_directory + "/keyword_stats_graphs.html"

# Call set_logger with default settings (check directories and use default script identifier)
logger = set_logger()

def check_http_status(url):
    """Checks the HTTP status of a URL."""
    try:
        logger.debug(f"Checking status for URL: {url}")
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def get_hrefs(url):
    """Extracts href links from a URL and filters for http/https links."""
    try:
        logger.debug(f"Extracting hrefs from: {url}")
        response = requests.get(url, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")
        href_links = [a['href'] for a in soup.find_all('a', href=True)]
        # Filter for links starting with http or https
        valid_links = [link for link in href_links if link.startswith("http")]
        logger.debug(f"Found {len(valid_links)} valid links in {url}")
        return valid_links[:10]  # Get first 10 links
    except Exception as e:
        logger.error(f"Error extracting links from {url}: {e}")
        return []


def check_keywords_in_page(content, keyword_sets):
    """Checks for individual keywords on a given page."""
    content = content.lower()
    keyword_set_counts = Counter()

    for keyword_set in keyword_sets:
        for keyword in keyword_set:
            keyword_lower = keyword.lower()
            if keyword_lower in content:
                keyword_set_counts[tuple(keyword_set)] += 1

    return keyword_set_counts


def save_valid_links_to_csv(valid_links_info):
    """Saves the valid link information to a CSV file."""
    logger.info("Saving valid links to CSV...")
    with open(valid_links_csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Parent URL", "Href Link", "Status"])
        for row in valid_links_info:
            writer.writerow(row)
    logger.info(f"Valid links saved to {valid_links_csv_filename}")


def plot_link_status_graph(valid_links_info):
    """Plots a bar graph of link status statistics (total, valid, invalid)."""
    total_links = len(valid_links_info)
    valid_links = len([x for x in valid_links_info if x[2] == "Valid"])
    invalid_links = len([x for x in valid_links_info if x[2] == "Invalid"])

    fig = go.Figure(data=[
        go.Bar(x=["Total", "Valid", "Invalid"], y=[total_links, valid_links, invalid_links])
    ])

    fig.update_layout(
        title="Link Status Statistics",
        xaxis_title="Link Status",
        yaxis_title="Number of Links"
    )
    logger.info("Displaying link status graph.")
    fig.show()

    return fig


def save_keyword_frequencies_to_csv(keyword_freq_per_link):
    """Saves the keyword frequencies to a CSV file."""
    logger.info("Saving keyword frequencies to CSV...")
    with open(keyword_stats_csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Parent URL", "Keyword Set", "Frequency"])
        for url, keyword_counts in keyword_freq_per_link.items():
            for keyword_set, count in keyword_counts.items():
                writer.writerow([url, ', '.join(keyword_set), count])
    logger.info(f"Keyword frequencies saved to {keyword_stats_csv_filename}")


def plot_keyword_frequency_graph(keyword_freq_per_link):
    """Plots a bar graph of keyword frequencies across valid links."""
    url_keyword_freq = [(url, sum(keyword_counts.values())) for url, keyword_counts in keyword_freq_per_link.items()]
    urls_sorted = sorted(url_keyword_freq, key=lambda x: x[1], reverse=True)
    sorted_urls = [x[0] for x in urls_sorted]
    sorted_freqs = [x[1] for x in urls_sorted]
    # Identify the highest and lowest frequency links
    max_url = sorted_urls[0]
    min_url = sorted_urls[-1]

    # Highlight the highest and lowest frequency
    fig = go.Figure(data=[
        go.Bar(
            x=sorted_freqs,
            y=sorted_urls,
            orientation='h',
            marker_color=['red' if url == sorted_urls[0] else ('green' if url == sorted_urls[-1] else 'blue') for url in sorted_urls]  # Highlight highest in red, lowest in green
        )
    ])

    fig.update_layout(
        title="Keyword Frequency in Valid Links",
        xaxis_title="Keyword Frequency",
        yaxis_title="URLs",
    )

    # Highlight the URL with the highest and lowest frequency
    fig.add_annotation(
        x=max_url, y=max(sorted_freqs),
        text=f"Highest: {max_url}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1
    )

    fig.add_annotation(
        x=min_url, y=min(sorted_freqs),
        text=f"Lowest: {min_url}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1
    )
    logger.info("Displaying keyword frequency graph.")
    fig.show()

    return fig


def process_links_and_keywords(urls, keyword_sets):
    """Main processing function for extracting links, checking validity, and analyzing keywords."""
    valid_links_info = []
    keyword_set_counts_per_link = {}

    for url in urls:
        logger.info(f"Processing URL: {url}")
        valid_links = get_hrefs(url)
        total_keyword_set_count = Counter()

        for link in valid_links:
            status_code = check_http_status(link)
            status = "Valid" if status_code == 200 else "Invalid"
            valid_links_info.append([url, link, status])

            if status == "Valid":
                # If valid, check for keyword sets in the link's page
                response = requests.get(link, timeout=TIMEOUT)
                page_content = response.text.lower()
                keyword_set_counts = check_keywords_in_page(page_content, keyword_sets)
                total_keyword_set_count.update(keyword_set_counts)

        # Store the total keyword set count for the main URL (including sub-links)
        keyword_set_counts_per_link[url] = total_keyword_set_count

    return valid_links_info, keyword_set_counts_per_link


def main():
    """Main function to execute the full script."""

    try:
        # Start time
        start_time = time.time()
        
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Process URLs and analyze keywords.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
        args = parser.parse_args()

        # Enable verbose logging if the flag is set
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.info("Verbose logging enabled.")
        else:
            logger.setLevel(logging.INFO)

        logger.info("Script Started.")

        # Process links and keywords
        try:
            valid_links_info, keyword_set_counts_per_link = process_links_and_keywords(urls, keyword_sets)
        except Exception as e:
            logger.error(f"Error processing links and keywords: {str(e)}")
            raise

        # Save valid link information to CSV
        try:
            save_valid_links_to_csv(valid_links_info)
        except Exception as e:
            logger.error(f"Error saving valid links to CSV: {str(e)}")
            raise

        # Plot link status graph
        try:
            link_status_fig = plot_link_status_graph(valid_links_info)
        except Exception as e:
            logger.error(f"Error plotting link status graph: {str(e)}")
            raise

        # Save keyword frequencies to CSV
        try:
            save_keyword_frequencies_to_csv(keyword_set_counts_per_link)
        except Exception as e:
            logger.error(f"Error saving keyword frequencies to CSV: {str(e)}")
            raise

        # Plot keyword frequency graph
        try:
            keyword_frequency_fig = plot_keyword_frequency_graph(keyword_set_counts_per_link)
        except Exception as e:
            logger.error(f"Error plotting keyword frequency graph: {str(e)}")
            raise

        # Save graphs to HTML files
        try:
            link_status_fig.write_html(valid_links_html_filename)
            keyword_frequency_fig.write_html(keyword_stats_html_filename)
            logger.info(f"Graphs saved to {valid_links_html_filename} and {keyword_stats_html_filename}")
        except Exception as e:
            logger.error(f"Error saving graphs to HTML: {str(e)}")
            raise

        # Time taken calculation
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Script execution completed successfully in {execution_time:.2f} seconds.")

    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}")
        logger.critical("Script execution failed")
        exit(103)

if __name__ == "__main__":
    main()
