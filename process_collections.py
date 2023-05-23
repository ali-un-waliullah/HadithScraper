from bs4 import BeautifulSoup
import json
import re
from fetch_collections import fetch_page


def read_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_name: str, content: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_file(file_name: str) -> BeautifulSoup:
    """
    Parses HTML file and returns a soup object
    """
    return BeautifulSoup(read_file(file_name), 'html.parser')


def get_book_name(soup: BeautifulSoup) -> str:
    """
    Returns the book name from the soup object
    """
    div_tag_book_name = soup.find('div', class_="actualHadithContainer")
    a_tag = div_tag_book_name.find('a')

    if a_tag:
        pattern = r'/(?P<book>\w+)(?P<number>[:/\d]+)'
        match = re.search(pattern, a_tag['href'])
        if match:
            return match[1]
    return "Unknown"


def get_hadith_number(soup: BeautifulSoup) -> str:
    """
    Returns the hadith number from the soup object
    """
    div_tag_book_name = soup.find('div', class_="actualHadithContainer")
    a_tag = div_tag_book_name.find('a')

    if a_tag:
        pattern = r'/(?P<book>\w+)(?P<number>[:/\d]+)'
        match = re.search(pattern, a_tag['href'])
        if match:
            return match[2]
    return "Unknown"


def get_hadith_text(soup: BeautifulSoup) -> str:
    """
    Returns the hadith text from the soup object
    """
    text_details_div = soup.find('div', class_='text_details')
    if text_details_div:
        return text_details_div.text.strip()
    return "Unknown"


def get_hadith_reference(soup: BeautifulSoup) -> str:
    """
    Returns the hadith reference from the soup object
    """
    hadith_reference_div = soup.find('div', class_='hadith_reference_sticky')
    if hadith_reference_div:
        return hadith_reference_div.text.strip()
    return "Unknown"


def get_hadith_narrated(soup: BeautifulSoup) -> str:
    """
    Returns the hadith narrated from the soup object
    """
    hadith_narrated_div = soup.find('div', class_='hadith_narrated')
    if hadith_narrated_div:
        return hadith_narrated_div.text.strip()
    return "Unknown"


def get_hadith(soup: BeautifulSoup) -> dict:
    """
    Returns a Hadith object
    """
    return {
        "bookName": get_book_name(soup),
        "hadithNumber": get_hadith_number(soup),
        "hadithText": get_hadith_text(soup),
        "hadithReference": get_hadith_reference(soup),
        "hadithNarrated": get_hadith_narrated(soup)
    }


def check_pages(soup: BeautifulSoup) -> list:
    """
    Checks if pagination exists and returns the lists of pages to fetch
    """
    pagination_div = soup.find('ul', class_='yiiPager')
    links = []
    if pagination_div:
        page_links = pagination_div.find_all('a')
        for page_link in page_links:
            links.append("https://sunnah.com"+page_link['href'])
        links.pop(0)
        links.pop(-1)
    return links


def get_hadiths(soup: BeautifulSoup) -> list:
    """
    Returns a list of Hadith objects.
    """
    output_list = []
    boh_divs = soup.find_all('div', class_='boh')
    for boh_div in boh_divs:
        output_list.append(get_hadith(boh_div))
    return json.dumps(output_list, indent=4)


if __name__ == "__main__":
    homepage = parse_file('./pages/search.html')
    pages = check_pages(homepage)
    print(pages)
    if pages:
        for page in range(0, len(pages)):
            fetch_page(pages[page], f"page{page+1}.html")

    print(get_hadiths(homepage))
