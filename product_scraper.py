from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from data_preprocessing import preprocess_data
import joblib

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_product_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Scrape the name
    name_element = soup.find('h1', {'class': 'page_heading'})
    name = name_element.text.strip() if name_element else 'N/A'
    
    # Scrape the price
    price_element = soup.find('p', {'class': 'ps_sell_price'})
    price = price_element.find('span', {'class': 'price_num'}).text.strip() if price_element else 'N/A'
    
    # Scrape the rating
    rating_element = soup.find('div', {'class': 'panel-heading cp_r'})
    rating = rating_element.text.strip().split(' ')[2] if rating_element else 'N/A'
    
    # Scrape the rating distribution
    rating_distribution = {}
    rating_body = soup.find('div', {'class': 'panel-body ar-detailed'})
    if rating_body:
        rating_rows = rating_body.find_all('span', {'class': 'rc_container'})
        for row in rating_rows:
            stars = row.find_all('span', {'class': 'rating_on'})
            rating_count_text = row.find('span', {'class': 'rating_count'}).text.strip()
            rating_count = int(rating_count_text.split(' ')[0]) if rating_count_text.split(' ')[0].isdigit() else 1
            rating_distribution[len(stars)] = rating_count
    else:
        rating_distribution = {'error': 'Rating distribution not found'}
    
    # Debugging output
    print(f"Scraped data - Name: {name}, Price: {price}, Rating: {rating}, Rating Distribution: {rating_distribution}")
    
    return name, price, rating, rating_distribution

if __name__ == "__main__":
    # Read the CSV file
    df = pd.read_csv('pcgarage_cpu_data.csv')
    
    detailed_data = []
    for index, row in df.iterrows():
        print(f"Scraping product page: {row['link']}")
        name, price, rating, rating_distribution = scrape_product_page(row['link'])
        
        combined_data = {
            'title': name,
            'price': price if price else row['price'],
            'rating': rating if rating else row['rating'],
            'rating_distribution': rating_distribution,
            'link': row['link']
        }
        detailed_data.append(combined_data)
        
        # Sleep to prevent rate limiting
        time.sleep(2)  # Adjust the sleep time as needed
    
    detailed_df = pd.DataFrame(detailed_data)
    detailed_df.to_csv('detailed_cpu_data.csv', index=False)
    print("Detailed data scraped and saved to detailed_cpu_data.csv")
