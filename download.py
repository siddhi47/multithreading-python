import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor


os.makedirs("dog_image", exist_ok=True)


def download_image_from_url(url):
    try:
        response = requests.get(url, timeout=1)
        if response.status_code == 200:
            with open(os.path.join("dog_image", url.split("/")[-1]), "wb") as f:
                f.write(response.content)
    except Exception as e:
        print(f"Failed to download image from {url}. Exception: {e}")


url = "https://raw.githubusercontent.com/iblh/not-cat/refs/heads/master/urls/not-cat/dog-urls.txt"
response = requests.get(url)
if response.status_code == 200:
    image_url_list = response.text.split("\n")
    image_url_list = [url for url in image_url_list if url]

else:
    print(f"Failed to fetch file. Status code: {response.status_code}")

    print(image_url_list)
print(f"Number of images to download: {len(image_url_list)}")


# without multithreading
start_time = time.time()
for url in image_url_list:
    download_image_from_url(url)
print(f"Time taken without multithreading: {time.time() - start_time}")

# Using multithreading to download images
start_time = time.time()
max_workers = os.cpu_count()
print(f"Number of CPUs: {max_workers}")
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(download_image_from_url, image_url_list)

print(f"Time taken with multithreading: {time.time() - start_time}")
