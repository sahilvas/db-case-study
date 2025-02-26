
# Demo Script - README

## Overview

This Python script is designed to process a list of URLs, check the status of their links, and analyze the occurrence of specified keyword sets on these URLs. The results are saved into CSV files, visualized in interactive graphs using Plotly, and logged using a customizable logging mechanism. The script also supports verbose logging for detailed debugging.

## Features

1. **URL Processing:**
   - Extracts all `href` links from each URL.
   - Filters for links that begin with `http` or `https`.
   - Checks the HTTP status (valid or invalid) for each link.
   
2. **Keyword Frequency Analysis:**
   - Analyzes each page for the occurrence of specified keyword sets.
   - Counts the frequency of each keyword set in the page content.

3. **CSV Export:**
   - Saves the valid link information (parent URL, href, and status) into a CSV file.
   - Saves the keyword frequency analysis into a CSV file.

4. **Graph Visualization:**
   - Plots bar graphs of link status statistics and keyword frequency analysis using Plotly.
   - Saves the graphs to an HTML file for visualization.

5. **Logging:**
   - Supports logging of events and errors.
   - Logs can be saved to a file and printed to the console.

6. **Command-line Arguments:**
   - Allows enabling verbose logging via a `--verbose` flag.

## Requirements

This script uses the following external Python libraries:

- `requests`: To fetch the content of the URLs and check HTTP status codes.
- `beautifulsoup4`: To parse the HTML content and extract `href` links.
- `plotly`: To create interactive graphs.
- `csv`: To save results to CSV files.
- `argparse`: To handle command-line arguments.
- `logging`: To handle logging.

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## File Structure

```
.
├── bin/
│   └── demo_script.py  # Main script to run the program
├── logs/
│   └── demo-script.log  # Log file where logs are saved
├── output/
│   ├── keyword_stats.csv  # Keyword frequency data in CSV format
│   ├── keyword_stats_graphs.html  # Graph of keyword frequency in HTML format
│   ├── valid_links.csv  # Valid link data in CSV format
│   └── valid_links_graphs.html  # Graph of link status in HTML format
├── requirements.txt  # List of required dependencies
└── utils/
    └── set_logger.py  # Helper file to configure logging
```

### **Script Explanation**

- `demo_script.py`: This is the main script that processes the URLs, extracts the valid links, analyzes the content for keyword sets, and generates the required outputs (CSV and HTML files). It also handles logging and error handling.
- `set_logger.py`: A utility script to set up logging with an option to log to both the console and a log file. It supports verbosity control.

## Usage

### Run the Script

To run the script, execute the following command:

```bash
python bin/demo_script.py
```

This will execute the script and process the URLs. By default, only essential logs will be shown.

### Enable Verbose Logging

You can enable verbose logging to get detailed logs by using the `--verbose` flag:

```bash
python bin/demo_script.py --verbose
```

This will display debug-level logs, which can be helpful for debugging or understanding the flow of the script.

### Run using docker

You can also run the script in a container by building the image and then running it
Please check the Dockerfile and update as needed

```
docker build -t demo_python_app . 
docker run --rm -t demo_python_app
```

To run it inside docker container with arguments for debugging

```
docker run --rm demo_python_app python bin/demo_script_with_async.py --verbose
```

Also, you can run it using docker-compose locally with one command

```
docker-compose up --build
```


### Generated Files

1. **Valid Links CSV**: 
   - `valid_links.csv` contains the parent URL, href link, and the HTTP status for each link.
   
2. **Keyword Frequency CSV**:
   - `keyword_stats.csv` contains the frequency of keyword sets found across all processed pages.

3. **Graphs**:
   - `valid_links_graphs.html`: A bar graph showing the total, valid, and invalid links.
   - `keyword_stats_graphs.html`: A bar graph showing the frequency of keyword sets across URLs.

Both of these HTML files can be opened in any browser to view the graphs interactively.

## Detailed Workflow

### 1. **Processing URLs and Extracting Links**

- The script processes a predefined list of URLs.
- It extracts all `href` links from the page content using BeautifulSoup and filters for those starting with `http` or `https`.
- The first 10 valid links are considered for further analysis.

### 2. **Checking Link Status**

- For each valid link, the script checks its HTTP status code by sending a GET request to the link.
- The status is recorded as either "Valid" (HTTP 200) or "Invalid" (any other status).

### 3. **Keyword Frequency Analysis**

- For each valid link, the script fetches the content and checks for the presence of predefined keyword sets.
- The frequency of each keyword set is counted and stored.

### 4. **Saving Results to CSV**

- The valid link information (URL, link, and status) is saved in `valid_links.csv`.
- The frequency of keyword sets is saved in `keyword_stats.csv`.

### 5. **Graph Generation**

- The script generates two interactive bar graphs using Plotly:
  - **Link Status Graph**: Shows the total number of links, valid links, and invalid links.
  - **Keyword Frequency Graph**: Shows the frequency of keyword sets across the processed URLs, highlighting the URLs with the highest and lowest keyword frequency.

### 6. **Logging**

- The script logs events such as the start of the script, any errors encountered, and the completion of tasks.
- Logs are saved to `demo-script.log` and printed to the console. You can enable verbose logging using the `--verbose` flag.

## Example Output

### CSV (valid_links.csv)

```
Parent URL,Href Link,Status
https://sanctionssearch.ofac.treas.gov/,https://www.treasury.gov/,Valid
https://sanctionssearch.ofac.treas.gov/,https://www.reuters.com/,Invalid
...
```

### CSV (keyword_stats.csv)

```
Parent URL,Keyword Set,Frequency
https://sanctionssearch.ofac.treas.gov/,"Sanctions, OFAC",1
https://www.treasury.gov/,"Foreign Sanctions, Balkans",0
...
```

### Graph (valid_links_graphs.html)

A bar graph showing the status of all links processed.

### Graph (keyword_stats_graphs.html)

A bar graph showing the frequency of keyword sets across the URLs.

## Error Handling

- The script logs any errors encountered while fetching URLs, checking status codes, extracting hrefs, or processing page content.
- The script will exit with a critical error if an unexpected issue occurs.

## Logging Configuration

- Logs are saved in the `logs/` directory to `demo-script.log`.
- The script uses `set_logger` from the `utils/set_logger.py` file to configure logging.
- The logging verbosity can be controlled by the `--verbose` flag.


## Future Enhancements

- **Improve Error Handling:** Implement more granular exception handling for specific request failures, such as rate limits, captchas, or blocked access.
- **Parallel Processing:** Use asynchronous requests (e.g., asyncio with aiohttp) or threading to speed up URL fetching and keyword analysis.
- **Enhanced Link Filtering:** Improve link extraction by filtering out duplicate, irrelevant, or non-informative links (e.g., navigation links, social media buttons).

## License

This project is licensed under the ...
