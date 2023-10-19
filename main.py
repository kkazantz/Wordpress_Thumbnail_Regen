import requests
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='regeneration_log.log')

# WordPress API credentials
wp_url = "http://vapetravellers.eu/wp-json"
username = "extsupport"
password = "zknO lNsI pdmU sSSr PC8i p3jp"

# Generate a Basic Authentication header
auth = requests.auth.HTTPBasicAuth(username, password)

# Initialize page variable
page = 1

while True:
    # Fetch media items
    media_endpoint = f"{wp_url}/wp/v2/media?page={page}&per_page=25&_fields=id,media_details&is_regeneratable=1&exclude_site_icons=1&orderby=id&order=asc"
    response = requests.get(media_endpoint, auth=auth)

    if response.status_code == 200:
        media_items = response.json()

        # Break if no more media items
        if not media_items:
            break

        for item in media_items:
            media_id = item.get("id")
            media_details = item.get("media_details", {})
            sizes = media_details.get("sizes", {})

            # Check if thumbnails are already generated
            if 'thumbnail' in sizes:
                message = f"Skipping regeneration for media ID {media_id} as thumbnails already exist."
                print(message)
                logging.info(message)
                continue

            # Regenerate thumbnail for each media item
            regenerate_endpoint = f"{wp_url}/regenerate-thumbnails/v1/regenerate/{media_id}?only_regenerate_missing_thumbnails=true&delete_unregistered_thumbnail_files=false&update_usages_in_posts=false"
            regenerate_response = requests.get(regenerate_endpoint, auth=auth)

            if regenerate_response.status_code == 200:
                message = f"Successfully regenerated thumbnail for media ID {media_id}"
                print(message)
                logging.info(message)
            else:
                message = f"Failed to regenerate thumbnail for media ID {media_id}"
                print(message)
                logging.error(message)

            # Wait for 1 seconds to avoid overwhelming the server
            time.sleep(1)

        # Increment page number for the next iteration
        page += 1

    else:
        message = f"Failed to fetch media items on page {page}."
        print(message)
        logging.error(message)
        break
