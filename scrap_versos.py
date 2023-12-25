import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = 'https://www.versos.cat/poemes'

def extract_poem_data(poem_url):
    response = requests.get(poem_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        author_tag = soup.find('span', class_='autor-poema')
        title_tag = soup.find('h1', class_='titol-poema')
        poem_div = soup.find('div', id='el-poema')

        author = author_tag.get_text(strip=True) if author_tag else 'Unknown Author'
        title = title_tag.get_text(strip=True) if title_tag else 'Unknown Title'
        poem_text = '\n'.join(segment for segment in poem_div.stripped_strings) if poem_div else 'Poem text not found'

        return author, title, poem_text
    else:
        return 'Failed to retrieve', 'Failed to retrieve', 'Failed to retrieve'
    
with open('poems.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Author', 'Title', 'Text'])

    # Start with the first page
    page_number = 1
    total_pages = 116  # If you know the total number of pages

    # Start time measurement
    start_time = time.time()

    for page in range(total_pages):
        # Construct the URL for the current page
        page_url = f'{base_url}?page={page_number}'  # Adjust this based on the actual URL pattern

        # Send a GET request to the URL
        response = requests.get(page_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all poem links on the current page
            poem_links = soup.find_all('article', class_='capsa-poema')
            for link_tag in poem_links:
                poem_link = link_tag.find('a', class_='llegir-mes').get('href')
                author, title, poem = extract_poem_data(poem_link)
                writer.writerow([author, title, poem])

            # Increment the page number to get the next page on the next iteration
            page_number += 1

            # Add a delay to be polite
            time.sleep(1)

        else:
            print(f'Failed to retrieve page {page_number}')
            break  # Exit the loop if a page fails to load

    # End time measurement
    end_time = time.time()
    elapsed_time = end_time - start_time

print(f'Scraping complete. Time taken: {elapsed_time:.2f} seconds.')