from bs4 import BeautifulSoup
import requests

base_site = 'https://www.atlasobscura.com'  # Base site

url = 'https://www.atlasobscura.com/things-to-do/uganda/places'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

card_bodies = soup.find_all('a', class_='Card')

for card_body in card_bodies:
    href = card_body['href']
    full_url = base_site + href

    # Visit each linked page and extract data
    linked_response = requests.get(full_url)
    
    if linked_response.status_code == 200:
        linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
        
        # Extract content from the linked page
        # Adjust the tags and attributes according to the structure of the linked page
        title = linked_soup.find('h1').text.strip()
        description = linked_soup.find('h3', class_='DDPage__header-dek' ).text.strip()
        content = linked_soup.find('div',class_='DDP__body-copy').text.strip()
        # description = linked_soup.find('div', class_='description').text.strip()
        
        # Process and use the extracted data
        print("Title:", title)
        print("Description:", description)
        print("Content:", content)  
        print("----------------------------------------")
    else:
        print(f"Failed to retrieve data from {full_url}")

