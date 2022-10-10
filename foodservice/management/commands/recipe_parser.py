import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from pathvalidate import sanitize_filename


def download_recipe_urls(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    recipe_all = soup.select('.recipe a[href]')
    return set(recipe_all)

def download_image(url, filename, folder='media/'):
    """Функция для скачивания картинок.
    Args:
        url (str): Cсылка на картинку, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    """
    home = Path().resolve()
    path = Path(home, folder)
    Path(path).mkdir(parents=True, exist_ok=True)
    named_path = f'{path}/{sanitize_filename(filename)}'
    response = requests.get(url)
    response.raise_for_status()
    with open(named_path, 'wb') as file:
        file.write(response.content)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_data()
        except Exception as exc:
            raise


def load_data():
    base_url = 'https://povar.ru/'
    recipes = {}
    all_urls = [
        ('https://povar.ru/list/goryachie_bliuda/', 'Обед'),
        ('https://povar.ru/list/salad/', 'Ужин'),
        ('https://povar.ru/list/zakuski/', 'Ужин'),
        ('https://povar.ru/list/soup/', 'Обед'),
        ('https://povar.ru/list/vypechka/', 'Завтрак'),
        ('https://povar.ru/list/dessert/', 'Десерт')
        ]
    for cat_url, menu_category in all_urls:
        urls = download_recipe_urls(cat_url)
        for raw_url in set(urls):
            url = urljoin(base_url, raw_url['href'])
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.select_one('.detailed').text
            image_url = soup.select_one('.bigImgBox a img')['src']
            image_name = urlsplit(image_url)[2].split('/')[-1]
            download_image(image_url, filename=image_name)
            detailed_description = soup.select_one('.detailed_full').text.strip('\n').strip('\t')
            categorys = menu_category
            ingredients = [ingredient.text.replace(u'\xa0', u'').split('                                —') for ingredient in soup.select('.detailed_ingredients li')]
            for ingredient in ingredients:
                try:
                    product, raw_amount = ingredient
                    match = re.match(r'([0-9]{0,}-?,?[0-9]{1,}?)([а-яА-Я]{0,} ?[а-яА-Я]{0,})', raw_amount, re.I)
                    if match:
                        amount, measur = match.groups()
                        ingredient[1] = amount
                        ingredient.append(measur)      
                    steps = [step.text for step in soup.select('.detailed_step_description_big')]
                    portions = soup.select('.detailed_full')[-1].text.split(' ')[-1]
                except ValueError:
                    pass
            if len(portions) > 1:
                portions = portions[-1]
            recipes[title] = {
                'image_url': f'media/{image_name}',
                'detailed_description': detailed_description,
                'categorys': categorys,
                'ingredients': ingredients,
                'steps': steps,
                'portions': portions
                }
    with open('result.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(recipes, ensure_ascii=False, indent=4))
