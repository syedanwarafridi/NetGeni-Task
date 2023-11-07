import pandas as pd
from bs4 import BeautifulSoup

# We also can scrap data from urls
with open("amazon_phones.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

product_names = []
prices = []
ratings = []

for product in soup.find_all('div', class_='s-result-item'):
    name = product.find('span', class_='a-text-normal')
    if name:
        product_names.append(name.text)
    else:
        product_names.append("N/A")

    price = product.find('span', class_='a-price')
    if price:
        prices.append(price.find('span', class_='a-offscreen').text)
    else:
        prices.append("N/A")

    rating = product.find('span', class_='a-icon-alt')
    if rating:
        ratings.append(rating.text)
    else:
        ratings.append("N/A")

data = {
    'Product Name': product_names,
    'Price': prices,
    'Ratings': ratings
}
df = pd.DataFrame(data)

csv_file_path = 'amazon-keyboards-bs4.csv'
df.to_csv(csv_file_path, index=False)
