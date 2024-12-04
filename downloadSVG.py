import os
import requests

# Read SVG links from the file
with open('svg_links.txt', 'r') as file:
    svg_links = [line.strip() for line in file if line.strip()]

# Directory to save downloaded SVGs
save_directory = "svgs"

# Create the directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Download each SVG
for link in svg_links:
    try:
        # Extract the file name from the link
        file_name = os.path.basename(link)
        save_path = os.path.join(save_directory, file_name)

        # Send a GET request to fetch the SVG file
        response = requests.get(link)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Write the SVG content to a file
        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {file_name}")
    except Exception as e:
        print(f"Failed to download {link}: {e}")

print("All downloads completed!")
