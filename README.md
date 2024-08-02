# Amazon Product Scraper

## Overview
A Python script that scrapes product details from Amazon category pages and sends the data to an external service via POST requests.

## Features
- Scrapes product details from Amazon category pages
- Handles rate limiting by Amazon
- Sends product data to an external service via POST requests

## Prerequisites
- Python 3.x
- requests library
- beautifulsoup4 library
- tabulate library

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/FezekaMabece/NerdsThinkCode_

2. Change into the project directory
   ```sh
   cd NerdsThinkCode_

3. Install required libraries:
   ```sh
   pip install requests beautifulsoup4 tabulate
   pip install beautifulsoup4
   pip install tabulate
   
3. The script will scrape product details from the selected category and send the data to the external service.

## Notes
- The script uses a simple user-agent rotation to avoid being blocked by Amazon.
- The script handles rate limiting by Amazon by waiting for a random time before retrying.
- The script sends product data to an external service via POST requests.

## Acknowledgments
- Amazon for providing the product data
- The `requests` and `beautifulsoup4` libraries for making web scraping easier

## Team: NerdsThinkCode_
Team Leader: Lebang Nong (lebangnong@gmail.com)
Back-end Developer: Katlego Barayi (katlegobarayi07@gmail.com)
Front-end Developer: Fezeka Mabece (fmabece@gmail.com)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
