from bs4 import BeautifulSoup
import os

# Your HTML content
with open('test1.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Directory for the relative SVG path
relative_path = "./svgs/"

# Find all <img> tags
img_tags = soup.find_all('img')

for img in img_tags:
    src = img.get('src', '')
    if src.endswith('.svg'):  # Check if the `src` points to an SVG
        # Extract the file name
        file_name = os.path.basename(src)
        # Replace with the relative path
        img['src'] = os.path.join(relative_path, file_name)

    # Remove the `anima-src` attribute if it exists
    if 'anima-src' in img.attrs:
        del img.attrs['anima-src']

# Get the updated HTML as a string
updated_html = soup.prettify()

# Output the updated HTML
print("Updated HTML:")
print(updated_html)

# Optionally save the updated HTML to a file
with open("updated.html", "w") as file:
    file.write(updated_html)
