import os
import requests
from bs4 import BeautifulSoup

# Step 1: Extract SVG and PNG links from the HTML file
def extract_image_links(html_file):
    with open(html_file, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    # Extract SVG and PNG links
    svg_links = [img['src'] for img in img_tags if img['src'].endswith('.svg')]
    png_links = [img['src'] for img in img_tags if img['src'].endswith('.png')]

    return svg_links, png_links, soup

# Step 2: Download images to specific directories
def download_images(links, save_directory):
    os.makedirs(save_directory, exist_ok=True)

    for link in links:
        try:
            file_name = os.path.basename(link)
            save_path = os.path.join(save_directory, file_name)

            # Send a GET request to fetch the image file
            response = requests.get(link)
            response.raise_for_status()  # Raise an error for bad HTTP responses

            # Write the image content to a file
            with open(save_path, 'wb') as file:
                file.write(response.content)

            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {link}: {e}")

# Step 3: Replace image paths in the HTML content
def replace_image_paths(soup, svg_directory, png_directory):
    img_tags = soup.find_all('img')

    for img in img_tags:
        src = img.get('src', '')
        if src.endswith('.svg'):  # Update SVG paths
            file_name = os.path.basename(src)
            img['src'] = os.path.join(svg_directory, file_name)
        elif src.endswith('.png'):  # Update PNG paths
            file_name = os.path.basename(src)
            img['src'] = os.path.join(png_directory, file_name)

        # Remove any custom attributes like `anima-src`
        if 'anima-src' in img.attrs:
            del img.attrs['anima-src']

    return soup.prettify()

# Main workflow
def main(html_file, svg_save_directory, png_save_directory, output_html_file):
    # Step 1: Extract links
    svg_links, png_links, soup = extract_image_links(html_file)

    # Step 2: Download SVG and PNG images
    download_images(svg_links, svg_save_directory)
    download_images(png_links, png_save_directory)

    # Step 3: Replace paths in the HTML
    updated_html = replace_image_paths(soup, svg_save_directory, png_save_directory)

    # Save the updated HTML
    with open(output_html_file, 'w') as file:
        file.write(updated_html)

    print(f"Updated HTML saved to {output_html_file}")

# Usage
html_file = 'test1.html'
svg_save_directory = './svgs/'
png_save_directory = './pngs/'
output_html_file = 'updated.html'

main(html_file, svg_save_directory, png_save_directory, output_html_file)
