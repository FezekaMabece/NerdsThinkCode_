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
                #The class to find the price!!!
                # <span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">37<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span>
                products.append({
                    "product_name": product_name,
                    "product_image": product_image,
                    "product_url": product_url,
                    "product_price": product_price,
                    "scrape_date": scrape_date
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
        
def getting_post_request(product_name,product_image,product_url,product_price,scrape_date):

   url = 'https://nerd-biz-bot.vercel.app/products'
   # Data to be sent in the request
   if product_price == 'N/A':
       product_price = 0
   data = {'product_name': product_name, 'image_url': product_image, 'price': product_price, 'source': product_url, 'date_scraped': scrape_date}
   print(data)

   # Send POST request
   response = requests.post(url, json=data)  # Use json= if sending JSON data

   # Check if the request was successful
   if response.status_code == 200:
       print('Data submitted successfully!')
       # Optionally, get the response data
       response_data = response.json()
       print(response_data)
   else:
       print(f"Request failed with status code {response.status_code}")

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
        # if products:
        #     print(tabulate(products, headers="keys", tablefmt="grid"))
        
        for product in products:
            getting_post_request(product["product_name"], product["product_image"], product["product_url"], product["product_price"], product["scrape_date"])
    else:
        print("Invalid input. Please enter a number between 1 and 6.")
