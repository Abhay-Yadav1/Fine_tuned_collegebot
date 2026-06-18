import requests
from bs4 import BeautifulSoup
import csv
url = "https://rtionline.gov.in/faq.php"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

QnA = {}
container = soup.find('div', id='faq-From-div')

for item in container.find_all('li'):
    a_tag = item.find('a')
    question = a_tag.get_text(strip=True)

    answer_div = item.find('div', id='Answer')
    answer = answer_div.get_text(strip=True)

    QnA[question] = answer

with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Key', 'Value'])  # Header
    for key, value in QnA.items():
        writer.writerow([key, value])

