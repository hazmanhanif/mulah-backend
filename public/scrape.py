import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

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
            # For simplicity, assume the current date for the article date
            date = datetime.now().strftime('%Y-%m-%d')
            writer.writerow([title, full_link, date])

print(f"Data scraped and saved to {csv_file}")
