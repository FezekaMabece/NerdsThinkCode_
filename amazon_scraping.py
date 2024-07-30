import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime
import time
import random

def scrape_amazon_products(url):
    max_retries = 5
    retries = 0
    
    while retries < max_retries:
        try:
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            soup = BeautifulSoup(response.content, 'html.parser')
            product_elements = soup.select(".a-column.a-span12.a-text-center._cDEzb_grid-column_2hIsc")

            products = []
            scrape_date = datetime.now().strftime("%Y-%m-%d")

            for item in product_elements:
                product_name = item.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1").text.strip() if item.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1") else "N/A"
                product_image = item.find("img")['src'] if item.find("img") else "N/A"
                product_url = item.find("a")['href'] if item.find("a") else "N/A"
                product_url = "https://www.amazon.com" + product_url if product_url != "N/A" else "N/A"
                product_price = item.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay").text.strip() if item.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay") else "N/A"

                products.append({
                    "Name": product_name,
                    "Image": product_image,
                    "URL": product_url,
                    "Price": product_price,
                    "Scraped Date": scrape_date
                })

            return products

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("Too many requests. Retrying...")
                time.sleep(random.uniform(5, 15))  # Wait for a random time before retrying
                retries += 1
            else:
                print("An error occurred:", e)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None

if __name__ == "__main__":
    amazon_categories = {
        "Kitchen": {"url": "https://www.amazon.com/gp/bestsellers/kitchen"},
        "Fashion": {"url": "https://www.amazon.com/gp/bestsellers/fashion"},
        "Electronics": {"url": "https://www.amazon.com/gp/bestsellers/electronics"},
        "Grocery": {"url": "https://www.amazon.com/gp/bestsellers/grocery"},
        "Wireless": {"url": "https://www.amazon.com/gp/bestsellers/wireless"},
        "Applications": {"url": "https://www.amazon.com/gp/bestsellers/appliances"}
    }

    user_input = input("Please choose the category you want to search:\n1. Kitchen\n2. Fashion\n3. Electronics\n4. Grocery\n5. Wireless\n6. Applications\nEnter the number: ")

    if user_input.isdigit() and 1 <= int(user_input) <= 6:
        category_keys = list(amazon_categories.keys())
        selected_category = category_keys[int(user_input) - 1]
        print(f"Scraping products from the {selected_category} category...")
        products = scrape_amazon_products(amazon_categories[selected_category]["url"])
        if products:
            print(tabulate(products, headers="keys", tablefmt="grid"))
    else:
        print("Invalid input. Please enter a number between 1 and 6.")
