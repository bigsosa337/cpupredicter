import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_pcgarage_cpus(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    
    cpu_data = []
    page_number = 1
    
    while True:
        print(f"Scraping page {page_number}")
        response = requests.get(f"{url}pagina{page_number}/", headers=headers)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        product_boxes = soup.find_all('div', {'class': 'product_box_container'})
        
        if not product_boxes:
            break
        
        for product in product_boxes:
            # Scrape the name
            name_element = product.find('div', {'class': 'product_box_name'}).find('a')
            name = name_element.text.strip() if name_element else 'N/A'
            
            # Scrape the price
            price_element = product.find('div', {'class': 'pb-price'}).find('p', {'class': 'price'})
            price = price_element.text.strip() if price_element else 'N/A'
            
            # Scrape the link
            link = name_element['href'] if name_element else 'N/A'
            
            # Debugging output
            print(f"Scraped data - Name: {name}, Price: {price}, Link: {link}")
            
            cpu_data.append({
                'name': name,
                'price': price,
                'link': link
            })
        
        page_number += 1
        time.sleep(2)  # Sleep to prevent rate limiting
    
    return pd.DataFrame(cpu_data)

if __name__ == "__main__":
    base_url = 'https://www.pcgarage.ro/procesoare/'
    df = scrape_pcgarage_cpus(base_url)
    df.to_csv('pcgarage_cpu_data.csv', index=False)
    print("Data scraped and saved to pcgarage_cpu_data.csv")
