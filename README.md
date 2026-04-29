YouTube Search Automation

This tool lets you automate YouTube searches and grab video metadata, all while keeping an eye on real-time network latency. When it finishes, you’ll get a clean CSV file with all the results.

Overview

Everything runs through a real Chrome browser session, thanks to undetected-chromedriver—so you won’t get tripped up by YouTube’s bot detection. While your search runs, a background thread keeps pinging youtube.com, tracking latency as it happens. The tool dumps all collected metadata into a CSV file once the run wraps up.

Features

- Automated YouTube search — launches Chrome for you, enters your search, then waits for results
- Metadata extraction — pulls the video’s title, video URL, uploader’s channel name, channel URL, view count, and upload time right off each result
- Real-time latency monitoring — a dedicated ping thread tracks the lowest, average, and highest ping to youtube.com during the whole session; throws a warning in the console if anything goes over 300ms
- CSV export — writes all the data into youtube_results.csv, with clean headers
- Error-safe threading — the ping thread shuts down cleanly no matter what happens, thanks to a finally block

Requirements

- Python 3.8 or above
- Google Chrome (must be installed)
- ChromeDriver that matches your Chrome version (handled automatically)
Install dependencies with:

pip install undetected-chromedriver selenium ping3

Usage

Here’s how to use it:

video1 = YTVIDSEARCH("your search query")
video1.main()

Example:

video1 = YTVIDSEARCH("python programming")
video1.main()

Output

Everything ends up in youtube_results.csv in your current directory. The file has these columns:

| Column         | Description                     |
|---------------|---------------------------------|
| Title         | Video title                     |
| Video Link    | Full URL to the video           |
| Channel       | Channel display name            |
| Channel Link  | Full URL to the channel         |
| Views         | View count shown on YouTube     |
| Uploaded Time | Upload time as seen on YouTube  |

Console Output

While searching, the script prints a summary for every video it finds. When it’s done, it shows the full latency report:

Lowest Latency: 12.34 ms
Average Latency: 18.72 ms
Highest Latency: 45.10 ms

Notes

- Set version_main=147 when setting up the Chrome driver to match your installed Chrome’s major version
- YouTube sometimes changes its DOM, so if scraping suddenly fails, you might need to update the CSS selectors