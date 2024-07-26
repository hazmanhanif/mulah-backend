# import requests
# from bs4 import BeautifulSoup
# import csv
# from datetime import datetime

# # URL to scrape
# url = "https://www.wired.com/"

# # Send request to the website
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find the containers for headlines
# headline_containers = soup.find_all(['h3', 'div'], class_='SummaryItemHedBase-hiFYpQ')

# # CSV file setup
# csv_file = "headlines.csv"

# # Open CSV file for writing
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Title', 'Link', 'Date'])

#     # Iterate through containers and extract data
#     for container in headline_containers:
#         title = container.get_text(strip=True)
#         link = container.find_parent('a')['href'] if container.find_parent('a') else None
#         if link:
#             full_link = f"https://www.wired.com{link}"
#             # For simplicity, assume the current date for the article date
#             date = datetime.now().strftime('%Y-%m-%d')
#             writer.writerow([title, full_link, date])

# print(f"Data scraped and saved to {csv_file}")

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Function to extract the date from an article page
def extract_date_from_article(article_url):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the publication date in the article page
        date_tag = soup.find('time')  # Adjust the tag or class if needed
        if date_tag:
            date_str = date_tag.get_text(strip=True)
            # Convert the date string to the desired format (dd/mm/yyyy)
            try:
                date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                date = 'Unknown'
        else:
            date = 'Unknown'
    except Exception as e:
        print(f"Error extracting date from {article_url}: {e}")
        date = 'Unknown'
    
    return date

# URL to scrape
url = "https://www.wired.com/"

# Send request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the containers for headlines
headline_containers = soup.find_all(['h3', 'div'], class_='SummaryItemHedBase-hiFYpQ')

# CSV file setup
csv_file = "headlines.csv"

# Open CSV file for writing
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Date'])

    # Iterate through containers and extract data
    for container in headline_containers:
        title = container.get_text(strip=True)
        link = container.find_parent('a')['href'] if container.find_parent('a') else None
        if link:
            full_link = f"https://www.wired.com{link}"
            
            # Extract the date from the article page
            article_date = extract_date_from_article(full_link)
            
            writer.writerow([title, full_link, article_date])
            
            # Optional: Delay between requests to avoid hitting the server too hard
            time.sleep(1)

print(f"Data scraped and saved to {csv_file}")
