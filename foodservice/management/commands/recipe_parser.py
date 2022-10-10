from ast import Try
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json


def download_recipe_urls(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    recipe_all = soup.select('.recipe a[href]')
    return set(recipe_all)


if __name__ == '__main__':
    base_url = 'https://povar.ru/'
    recipes = {}
    all_urls = [
        'https://povar.ru/list/goryachie_bliuda/',
        'https://povar.ru/list/salad/',
        'https://povar.ru/list/zakuski/',
        'https://povar.ru/list/soup/',
        'https://povar.ru/list/vypechka/',
        'https://povar.ru/list/dessert/'
        ]
    for cat_url in all_urls:
        urls = download_recipe_urls(cat_url)
        for raw_url in set(urls):
            url = urljoin(base_url, raw_url['href'])
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.select_one('.detailed').text
            image_url = soup.select_one('.bigImgBox a img')['src']
            detailed_description = soup.select_one('.detailed_full').text.strip('\n').strip('\t')
            categorys = [category.text for category in soup.select('.detailed_tags a')]
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
                'image_url': image_url,
                'detailed_description': detailed_description,
                'categorys': categorys,
                'ingredients': ingredients,
                'steps': steps,
                'portions': portions
                }
    with open('result.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(recipes, ensure_ascii=False, indent=4))
