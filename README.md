# Web Crawler CLI

This is a command-line tool written in Python that crawls a given website and saves information about any images found to a JSON file.


## Usage

To use the web crawler, run the crawler.py script with the following command-line arguments:

```sh
python crawler.py <start_url> <depth>
```

- start_url: The URL of the website to crawl.
- depth: The maximum depth to crawl. A depth of 0 means only the start URL will be crawled. A depth of 1 means the start URL and all pages linked from the start URL will be crawled, and so on.

Example usage:

```sh
python crawler.py https://www.google.com 2
```

This will crawl https://www.google.com and any pages linked from that page up to a maximum depth of 2, and save the results to a file called results.json.


# Dependencies

This tool requires the following Python packages:

- requests
- beautifulsoup4

You can install these packages using pip:

```sh
pip install requests beautifulsoup4
```

# Future Improvements

Some potential improvements to this tool include:

- Throttling: Currently, the tool does not have any throttling mechanism, which means that it could potentially overload a server with requests. Throttling could be added to limit the rate of requests and avoid overloading servers.
- Multithreading: Currently, the tool is single-threaded, which means that it can only crawl one page at a time. Multithreading could be used to crawl multiple pages concurrently, which would make the crawling process faster.
- User agent: Currently, the tool does not specify a user agent when making requests. Some websites might block requests from certain user agents, so it would be a good idea to specify a user agent to avoid being blocked.
