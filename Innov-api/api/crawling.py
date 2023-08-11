import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import tldextract
from config import CRAWLING_THREADS_NUM, USER_AGENTS_HEADERS
from multiprocessing.dummy import Pool as ThreadPool

def access_website(main_website, timeout = 30, 
                    headers=random.choice(USER_AGENTS_HEADERS)):
    """
    Method that reformats a website for request
    :return: response
    """
    if main_website.startswith("http"):
        response = requests.get(main_website, timeout=timeout, headers=headers)
    else:
        try:
            response = requests.get('https://' + main_website, timeout=timeout, headers=headers)
        except Exception:
            try:
                response = requests.get('http://' + main_website, timeout=timeout, headers=headers)
            except Exception as e:
                raise Exception(e)
    if not (str(response.status_code).startswith("2") or str(response.status_code).startswith("3")):
        raise Exception("Invalid Status Code")
    return response

def format_link(link, split_url):
    """
    :param link:
    :param split_url:
    :return:
    """
    link = link.replace('\n', '').replace('   /', '')
    if link.startswith('#'):
        return False
    if link.endswith('/'):
        link = link[:-1]
    if link.startswith("/"):
        link = split_url.scheme + '://' + split_url.netloc + link
    elif not link.startswith("/") and not link.startswith("http"):
        link = split_url.scheme + '://' + split_url.netloc + '/' + link
    return link

def get_base_link(link):
    """
    :param link:
    :return:
    """
    return tldextract.extract(link.lower()).domain

def extract_useful_links(response,
                        keywords_in_link_to_remove,
                        keywords_in_link_to_keep,
                        max_page_number):
    """
    by providing all the a tags in a page, extract all links and keep just the useful ones for the country and the
    business units
    :param response:
    :param keywords_in_link_to_keep:
    :return: curated webpages
    """
    main_website = response.url
    soup = BeautifulSoup(response.text, features='html.parser')
    hrefs = soup.select('a[href]')
    pages = set()
    pages.add(main_website)
    split_url = urlsplit(main_website)
    for link in hrefs:
        link_text = link.text.lower()
        link = link.get('href')
        link = format_link(link=link, split_url=split_url)
        if not link:
            continue
        split_link = urlsplit(link)
        if get_base_link(split_link.netloc) != get_base_link(split_url.netloc):
            continue
        if any(ext in urlsplit(link.lower()).path for ext in keywords_in_link_to_remove):
            continue
        if not (any(ext in urlsplit(link.lower()).path or ext in link_text for ext in keywords_in_link_to_keep)):
            continue
        pages.add(link)
        if len(pages) > max_page_number:
            break
        
    return pages

def get_website_text(response):
    """
    Keeps only the interesting parts of a webpage
    :param response:
    :return:
    """
    soup = BeautifulSoup(response.text, features='html.parser')
    return str(soup)

def retrieve_all_text(url, 
                      keywords_in_link_to_remove,
                      keywords_in_link_to_keep,
                      max_page_number,
                      threads_num = CRAWLING_THREADS_NUM
                      ):
    """
    Access a website and retrieve all keywords in all its sublinks
    :return:
    html: all the html of the website
    html_page_mapping: a list of tuples (page, html) where page is the link of the page and html is the html of the page
    """
    html_list = []
    pages_list = []
    response = access_website(url)
    response.encoding = "utf-8"
    pool = ThreadPool(threads_num)
    pages = extract_useful_links(response,
                                keywords_in_link_to_remove,
                                keywords_in_link_to_keep,
                                max_page_number=max_page_number)

    outputs = pool.map(visit_page, pages)
    for output in outputs:
        html_list.append(output["html"])
        pages_list.append(output["page"])
        
    html = ' \n '.join(html_list)
    html_page_mapping = list(zip(pages_list, html_list))
    return html, html_page_mapping

def visit_page(page):
    #print(f'Visiting page: {page}')
    response = requests.get(page, headers=random.choice(USER_AGENTS_HEADERS))
    response.encoding = "utf-8"
    html = get_website_text(response)
    return {"html": html, "page" : page}
