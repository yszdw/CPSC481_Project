from bs4 import BeautifulSoup

# Read the HTML content from the file
with open('test1.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract all <img> tags
img_tags = soup.find_all('img')

# Collect all SVG links
svg_links = [img['src'] for img in img_tags if img['src'].endswith('.svg')]

# Save or display the SVG links
print("Extracted SVG links:")
for link in svg_links:
    print(link)

# Optionally save to a file
with open('svg_links.txt', 'w') as file:
    for link in svg_links:
        file.write(link + '\n')
