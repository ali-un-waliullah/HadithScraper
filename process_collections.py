from bs4 import BeautifulSoup
import json
import re


with open('search.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Open file for reading
# Read and parse the file
# Create json objects in /collections with the following format:
# {
#     "bookName": "ibnmajah",
#     "hadithNumber": "1",
#     "hadithText": "The Book of the Sunnah",
#     "hadithReference": "English reference : Vol. 1, Book 1, Hadith 1",
#     "hadithNarrated": "Narrated"
# }
# Save the json objects in a file named ibnmajah1.json


def read_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_name: str, content: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_file(file_name: str) -> BeautifulSoup:
    return BeautifulSoup(read_file(file_name), 'html.parser')


def get_book_name(soup: BeautifulSoup) -> str:
    div_tag_book_name = soup.find('div', class_="actualHadithContainer")
    a_tag = div_tag_book_name.find('a')

    if a_tag:
        pattern = r'/(?P<book>\w+)(?P<number>[:/\d]+)'
        match = re.search(pattern, a_tag['href'])
        if match:
            return match[1]
    return "Unknown"


def get_hadith_number(soup: BeautifulSoup) -> str:
    div_tag_book_name = soup.find('div', class_="actualHadithContainer")
    a_tag = div_tag_book_name.find('a')

    if a_tag:
        pattern = r'/(?P<book>\w+)(?P<number>[:/\d]+)'
        match = re.search(pattern, a_tag['href'])
        if match:
            return match[2]
    return "Unknown"


def get_hadith_text(soup: BeautifulSoup) -> str:
    text_details_div = soup.find('div', class_='text_details')
    if text_details_div:
        return text_details_div.text.strip()
    return "Unknown"


def get_hadith_reference(soup: BeautifulSoup) -> str:
    hadith_reference_div = soup.find('div', class_='hadith_reference_sticky')
    if hadith_reference_div:
        return hadith_reference_div.text.strip()
    return "Unknown"


def get_hadith_narrated(soup: BeautifulSoup) -> str:
    hadith_narrated_div = soup.find('div', class_='hadith_narrated')
    if hadith_narrated_div:
        return hadith_narrated_div.text.strip()
    return "Unknown"


def get_hadith(soup: BeautifulSoup) -> dict:
    return {
        "bookName": get_book_name(soup),
        "hadithNumber": get_hadith_number(soup),
        "hadithText": get_hadith_text(soup),
        "hadithReference": get_hadith_reference(soup),
        "hadithNarrated": get_hadith_narrated(soup)
    }


def get_hadiths(soup: BeautifulSoup) -> list:
    output_list = []
    boh_divs = soup.find_all('div', class_='boh')
    for boh_div in boh_divs:
        output_list.append(get_hadith(boh_div))
    return output_list


results = soup.find_all('div', class_='actualHadithContainer')
output_list = []
boh_divs = soup.find_all('div', class_='boh')
for boh_div in boh_divs:
    output = {}
    # Extract bookName and hadithNumber
    div_tag_book_name = boh_div.find('div', class_="actualHadithContainer")
    a_tag = div_tag_book_name.find('a')

    if a_tag:
        pattern = r'/(?P<book>\w+)(?P<number>[:/\d]+)'
        match = re.search(pattern, a_tag['href'])
        if match:
            output['bookName'] = match[1]
            output['hadithNumber'] = match[2]
        else:
            output['bookName'] = "Unknown"
            output['hadithNumber'] = "Unknown"

    # Extract hadithText
    text_details_div = boh_div.find('div', class_='text_details')
    if text_details_div:
        output['hadithText'] = text_details_div.text.strip()

    # Extract hadithReference
    hadith_reference_div = boh_div.find(
        'div', class_='hadith_reference_sticky')
    if hadith_reference_div:
        output['hadithReference'] = hadith_reference_div.text.strip()

    # Extract hadithNarrated
    hadith_narrated_div = boh_div.find('div', class_='hadith_narrated')
    if hadith_narrated_div:
        output['hadithNarrated'] = hadith_narrated_div.text.strip()

    output_list.append(output)

print(json.dumps(output_list, indent=4, ensure_ascii=False))
