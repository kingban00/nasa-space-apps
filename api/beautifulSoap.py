import requests
from bs4 import BeautifulSoup
import certifi
import json

# verify=certifi.where()

def extract_elements_for_anchor(base_url, anchor):
    url = f'{base_url}/{anchor}'
    
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        article_data = {
            'title': '',
            'url': url,
            'description': '',
            'images': [],
            'links': [],
            'text2jax-process': [],  # Initialize as an empty list
            'views_row': [],         # Initialize as an empty list
            'content': {
                'paragraphs': [],
                'additional_info': []
            }
        }

        title_elements = soup.find_all('h3')
        for title_element in title_elements:
            article_data['title'] = title_element.get_text().strip()
            break  # Assuming you only want the first h1 element

        description_element = soup.find('div', class_='description')
        if description_element:
            article_data['description'] = description_element.get_text().strip()

        img_elements = soup.find_all('img')
        for img in img_elements:
            image_url = img.get('src')
            alt_text = img.get('alt', '')
            if image_url:
                article_data['images'].append({
                    'url': image_url,
                    'alt_text': alt_text
                })

        p_elements = soup.find_all('p')
        for p in p_elements:
            article_data['content']['paragraphs'].append(p.get_text().strip())

        text2jax_elements = soup.find_all('div', class_="text2jax_elements")
        for text2jax in text2jax_elements:
            article_data['text2jax-process'].append(text2jax.get_text())

        views_rows = soup.find_all('div', class_="views-row")
        for views_row in views_rows:
            article_data['views_row'].append(views_row.get_text())

        a_elements = soup.find_all('a', href=True)
        for a in a_elements:
            link_url = a['href']
            link_text = a.get_text().strip()
            article_data['links'].append({
                'url': link_url,
                'text': link_text
            })

        article_content = soup.find('div', class_='field-text-with-media')
        if article_content:
            paragraphs = article_content.find_all('p')
            for p in paragraphs:
                article_data['content']['paragraphs'].append(p.get_text().strip())

        additional_info_elements = soup.find_all('div', class_='additional-info')
        for info_element in additional_info_elements:
            info_text = info_element.get_text().strip()
            if info_text:
                article_data['content']['additional_info'].append(info_text)

        return article_data
    else:
        print(f"Failed to retrieve the webpage for anchor '{anchor}'. Status code:", response.status_code)
        return None

def main():
    base_url = "https://www.usgs.gov/science/science-explorer/climate/impacts-on-plants-and-animals"

    anchors_to_visit = ['overview', 'publications', 'science', 'data-and-more', 'news']

    articles_data = {}

    for anchor in anchors_to_visit:
        article_data = extract_elements_for_anchor(base_url, anchor)
        articles_data[anchor] = article_data

    json_data = json.dumps(articles_data, indent=4)
    
    print(json_data)

if __name__ == "__main__":
    main()