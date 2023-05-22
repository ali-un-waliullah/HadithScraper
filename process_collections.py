from bs4 import BeautifulSoup
import json
import re


with open('search.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

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
