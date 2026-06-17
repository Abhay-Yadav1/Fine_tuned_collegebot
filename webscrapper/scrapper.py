import requests
from bs4 import BeautifulSoup
url = "https://rtionline.gov.in/faq.php"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
QnA={}
container = soup.find('div', id='faq-From-div')
print(type(container))
print(container.find_all('li')[:5])