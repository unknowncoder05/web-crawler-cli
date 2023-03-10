import argparse
import json
import requests
from bs4 import BeautifulSoup


def extract_images_from_page(url):
    """
    Extracts image URLs from a given webpage.
    :param url: The URL of the webpage to extract images from.
    :return: A list of image URLs found on the webpage.
    """
    images = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    for img in img_tags:
        src = img.get('src')
        if src and (src.endswith('.jpg') or src.endswith('.jpeg') or src.endswith('.png')):
            images.append(src)
    return images


def get_links_from_page(url):
    """
    Extracts links from a given webpage.
    :param url: The URL of the webpage to extract links from.
    :return: A list of links found on the webpage.
    """
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
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
    while urls_to_crawl:
        url, current_depth = urls_to_crawl.pop(0)
        if current_depth > depth:
            break
        if url in visited:
            continue
        visited.add(url)
        images = extract_images_from_page(url)
        for image in images:
            results.append({
                'image_url': image,
                'source_url': url,
                'depth': current_depth
            })
        links = get_links_from_page(url)
        for link in links:
            if link not in visited:
                urls_to_crawl.append((link, current_depth + 1))
    save_results_to_file(results, output_file)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web Crawler CLI')
    parser.add_argument('start_url', type=str, help='Starting URL')
    parser.add_argument('depth', type=int, help='Crawling Depth')
    args = parser.parse_args()

    # Crawl the webpage and save results to a JSON file
    crawl_webpage(args.start_url, args.depth)