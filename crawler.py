# Authored by: Yat Nam
# get food item info from the web
import requests
from bs4 import BeautifulSoup


def fetch_wikipedia_description(food_name):
    url = f"https://en.wikipedia.org/wiki/{food_name.replace(' ', '_')}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return "No description available."

    soup = BeautifulSoup(response.content, 'html.parser')
    description = ""

    for paragraph in soup.find_all('p'):
        if paragraph.text.strip():
            description = paragraph.text.strip()
            break

    if not description:
        description = "No description available."

    return description

def fetch_food_storage_info():
    url = "https://www.foodsafety.gov/keep-food-safe/foodkeeper-app"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    food_storage_info = {}

    categories = soup.find_all('div', class_='field-item even')

    for category in categories:
        category_heading = category.find('h2')
        if category_heading:
            items = category.find_all('tr')
            for item in items:
                columns = item.find_all('td')
                if len(columns) >= 2:
                    food_name = columns[0].text.strip()
                    storage_time = columns[1].text.strip() if columns[1].text.strip() else "not safe"
                    food_storage_info[food_name] = storage_time

    return food_storage_info