# import requests

# from pytrends.request import TrendReq
# import time
# import random

# import pandas as pd
# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)

# from pytrends.exceptions import TooManyRequestsError
# # from requests_proxy import ProxySession

# def get_timeframe():
#     """Get the timeframe from the user"""
#     print("Select a timeframe:")
#     print("1. Everything (all)")
#     print("2. Specific dates (YYYY-MM-DD YYYY-MM-DD)")
#     print("3. Specific datetimes (YYYY-MM-DDTHH YYYY-MM-DDTHH)")
#     print("4. Current Time Minus Time Pattern:")
#     print("  a. By Month (today #-m)")
#     print("  b. Daily (now #-d)")
#     print("  c. Hourly (now #-H)")
    
#     choice = input("Enter your choice (1/2/3/4): ")
    
#     if choice == "1":
#         return "all"
#     elif choice == "2":
#         start_date = input("Enter start date (YYYY-MM-DD): ")
#         end_date = input("Enter end date (YYYY-MM-DD): ")
#         return f"{start_date} {end_date}"
#     elif choice == "3":
#         start_datetime = input("Enter start datetime (YYYY-MM-DDTHH): ")
#         end_datetime = input("Enter end datetime (YYYY-MM-DDTHH): ")
#         return f"{start_datetime} {end_datetime}"
#     elif choice == "4":
#         print("Select a time pattern:")
#         print("a. By Month (today #-m)")
#         print("b. Daily (now #-d)")
#         print("c. Hourly (now #-H)")
        
#         pattern_choice = input("Enter your choice (a/b/c): ")
        
#         if pattern_choice == "a":
#             months = input("Enter number of months (1/3/12): ")
#             return f"today {months}-m"
#         elif pattern_choice == "b":
#             days = input("Enter number of days (1/7): ")
#             return f"now {days}-d"
#         elif pattern_choice == "c":
#             hours = input("Enter number of hours (1/4): ")
#             return f"now {hours}-H"
#     else:
#         print("Invalid choice. Defaulting to 'all'.")
#         return "all"

# def get_keywords():
#     """Get the keywords from the user"""
#     kw_list = input("Enter keywords (comma separated): ")
#     return [keyword.strip() for keyword in kw_list.split(",")]

# def get_gprop():
#     """Get the Google property filter from the user"""
#     print("Select a Google property filter:")
#     print("1. Web searches (default)")
#     print("2. Images")
#     print("3. News")
#     print("4. YouTube")
#     print("5. Froogle (Google Shopping results)")
    
#     choice = input("Enter your choice (1/2/3/4/5): ")
    
#     if choice == "1":
#         return ""
#     elif choice == "2":
#         return "images"
#     elif choice == "3":
#         return "news"
#     elif choice == "4":
#         return "youtube"
#     elif choice == "5":
#         return "froogle"
#     else:
#         print("Invalid choice. Defaulting to web searches.")
#         return ""

# def get_geo():
#     """Get the country from the user"""
#     country = input("Enter country (two letter abbreviation, e.g. US): ")
#     return country


# def main():


#     pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
#     timeframe = get_timeframe()
#     keyword = get_keywords()
#     gprop = get_gprop()
#     geo = get_geo()

#     # Add a delay before making the request
#     delay = random.uniform(1, 5)  # Random delay between 1 and 5 seconds
#     time.sleep(delay)
#     pytrends.build_payload(keyword, cat=0, timeframe=timeframe, geo=geo, gprop=gprop)

#     try:
#         iot = pytrends.interest_over_time()
#         iot.plot()
#     except requests.exceptions.RetryError as e:
#         print(f"Too many requests error: {e}")
#         # You could add additional logic here to handle the error, such as waiting for a longer period of time before retrying
#         time.sleep(60)  # Wait for 1 minute before retrying
#         main()  # Retry the request

# if __name__ == "__main__":

#     main()

from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd

# Connect to Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# Build payload
kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# Get Interest Over Time data
interest_over_time_df = pytrends.interest_over_time()

# Get Interest by Region data
interest_by_region_df = pytrends.interest_by_region()

# Get Related Queries data
related_queries_df = pytrends.related_queries()

# Get Related Topics data
related_topics_df = pytrends.related_topics()

# Combine data into a single table
data = [
    {
        'title': 'Interest Over Time',
        'url': pytrends.get_url(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': interest_over_time_df
    },
    {
        'title': 'Interest by Region',
        'url': pytrends.get_url(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': interest_by_region_df
    },
    {
        'title': 'Related Queries',
        'url': pytrends.get_url(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': related_queries_df
    },
    {
        'title': 'Related Topics',
        'url': pytrends.get_url(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': related_topics_df
    }
]

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
