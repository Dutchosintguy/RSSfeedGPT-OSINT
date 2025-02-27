# RSSfeedGPT-OSINT
RSS Feed Summarizer with OpenAI GPT - OSINT

# RSS Feed Summarizer with OpenAI GPT

This script fetches articles from multiple RSS feeds, merges similar articles using OpenAI embeddings, and summarizes them concisely using OpenAI's GPT-4-turbo. The output is saved as an intelligence briefing report txt file.

## Features
- Fetches RSS feeds from multiple sources.
- Limits each feed to a maximum of **3** articles.
- Uses **OpenAI embeddings** to detect and merge similar articles, reducing redundant summarization requests.
- Summarizes articles with **shorter prompts** to save API costs.
- Outputs a structured **intelligence briefing report**.

## Installation
### Prerequisites
- Python 3.8+
- An OpenAI API key

### Install Required Packages
Clone the repository and install dependencies:

```bash
# Clone the repository
git clone [https://github.com/Dutchosintguy/RSSfeedGPT-OSINT.git]
cd RSSfeedGPT-OSINT

# Install dependencies
pip install -r requirements.txt
```

## Usage
Update your OpenAI API key in `rss_summarizer.py` by replacing `"YOUR_OPENAI_API_KEY"` with your actual key.

Run the script:

```bash
python3 RSSfeedGPT-OSINT.py
```

The script will:
1. Fetch articles from predefined RSS feeds.
2. Merge similar articles using OpenAI embeddings.
3. Summarize the merged content using GPT-4-turbo.
4. Generate an **intelligence briefing report** as `intelligence_briefing.txt`.

## Configuration
### Adding or Removing RSS Feeds
Modify the `RSS_FEEDS` list in `rss_summarizer.py` to add or remove feeds:

```python
RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    # Add or remove feeds as needed
]
```

### Adjusting the Similarity Threshold
To fine-tune how aggressively similar articles are merged, modify the `threshold` parameter in `find_similar_articles()`:

```python
def find_similar_articles(articles, threshold=0.85):
```

Increasing the value (e.g., `0.90`) makes the merging stricter, while decreasing it (e.g., `0.80`) makes it more lenient.

## License
This project is licensed under the MIT License.

## Contributions
Pull requests are welcome! If you find a bug or want to improve performance, feel free to contribute.

## Contact
For any inquiries or issues, open an issue on [GitHub](https://github.com/yourusername/rss-feed-summarizer/issues).

