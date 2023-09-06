import requests
from bs4 import BeautifulSoup

def get_icbc_gbp_rate():
    url = "https://www.kylc.com/huilv/d-icbc-gbp.html"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rate_data = soup.find('span', {'id': 'td_rate_1'}).text
        
        return float(rate_data)
    else:
        return 9.2

