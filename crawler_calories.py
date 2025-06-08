# Authored by: Yat Nam
# Get calorie info from food items from the web
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.calories.info"


def fetch_category_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories_section = soup.find_all('div', {'class': 'MuiBox-root css-10ib5jr'})
    category_links = [BASE_URL + a['href'] for div in categories_section for a in div.find_all('a') if 'food' in a['href']]
    return category_links


def fetch_calorie_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    table_rows = soup.select('table tr')
    for row in table_rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            try:
                food_name = cols[0].text.strip()

                serving_size = re.sub(r'\D', '', cols[1].text.strip())
                calories = re.sub(r'\D', '', cols[2].text.strip())
                data.append((food_name, serving_size, calories))
            except IndexError:
                print(f"Error processing row: {row}")
                continue
    return data


def save_to_file(data):
    with open('calories.txt', 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"{item[0]},{item[1]},{item[2]}\n")


def main():
    all_data = []
    category_links = fetch_category_links()
    for url in category_links:
        print(f"Fetching data from: {url}")
        data = fetch_calorie_info(url)
        all_data.extend(data)
    save_to_file(all_data)
    print(f"Data fetched and saved for {len(category_links)} categories.")

if __name__ == "__main__":
    main()












