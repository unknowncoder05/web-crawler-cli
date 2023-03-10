import argparse
import json
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('web_crawler')
logger.setLevel(logging.DEBUG)

# Set up the stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Set up the log message format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Add the stream handler to the logger
logger.addHandler(stream_handler)

def extract_images_from_page(soup):
    """
    Extracts image URLs from a given webpage.
    :param url: The URL of the webpage to extract images from.
    :return: A list of image URLs found on the webpage.
    """
    images = []    
    img_tags = soup.find_all('img')
    for img in img_tags:
        src = img.get('src')
        if src and (src.endswith('.jpg') or src.endswith('.jpeg') or src.endswith('.png')):
            images.append(src)
    return images


def get_links_from_page(url, soup):
    """
    Extracts links from a given webpage.
    :param url: The URL of the webpage to extract links from.
    :return: A list of links found on the webpage.
    """
    links = []
    a_tags = soup.find_all('a')
    for a in a_tags:
        href = a.get('href')
        if href and not href.startswith('javascript'):
            if href.startswith('/'):
                href = url + href
            elif not href.startswith('http'):
                href = url + '/' + href
            links.append(href)
    return links


def save_results_to_file(results, output_file):
    """
    Saves the results to a JSON file.
    :param results: A list of dictionaries containing the results.
    :param output_file: The output file name.
    """
    with open(output_file, 'w') as f:
        json.dump({'results': results}, f, indent=4)


def crawl_webpage(start_url, depth, output_file='results.json'):
    """
    Crawls a webpage and all the links it contains up to the specified depth, and saves the results in a JSON file.
    :param start_url: The starting URL to crawl from.
    :param depth: The maximum depth to crawl to.
    :param output_file: The name of the output file to save the results to.
    """
    results = []
    visited = set()
    urls_to_crawl = [(start_url, 0)]

    if depth < 0:
        logger.error("depth must be a positive integer")
        return

    while urls_to_crawl:
        url, current_depth = urls_to_crawl.pop(0)
        if current_depth > depth:
            break
        if url in visited:
            continue
        visited.add(url)
        logger.debug(f"Extracting images from {url}")
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logger.warning(f"could not retrieve {url}. {e}")
            continue
        if response.status_code != 200:
            logger.warning(
                f"Error: could not retrieve {url}. Response code {response.status_code}")
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        images = extract_images_from_page(soup)
        if not images:
            continue
        for image in images:
            results.append({
                'image_url': image,
                'source_url': url,
                'depth': current_depth
            })
        logger.debug(f"Extracting links from {url}")
        links = get_links_from_page(url, soup)
        for link in links:
            if link not in visited:
                urls_to_crawl.append((link, current_depth + 1))
        logger.debug(f"Found {len(links)} links on {url}")
    save_results_to_file(results, output_file)
    logger.info(f"Saved {len(results)} results to {output_file}")


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web Crawler CLI')
    parser.add_argument('start_url', type=str, help='Starting URL')
    parser.add_argument('depth', type=int, help='Crawling Depth')
    args = parser.parse_args()

    # Crawl the webpage and save results to a JSON file
    crawl_webpage(args.start_url, args.depth)
