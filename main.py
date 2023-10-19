import requests
import time

# WordPress API credentials
wp_url = "http://your_wordpress_site.com/wp-json"
username = "your_username"
password = "your_password"

# Generate a Basic Authentication header
auth = requests.auth.HTTPBasicAuth(username, password)

# Fetch media items
media_endpoint = f"{wp_url}/wp/v2/media?page=1&per_page=25&_fields=id&is_regeneratable=1&exclude_site_icons=1&orderby=id&order=asc"
response = requests.get(media_endpoint, auth=auth)

if response.status_code == 200:
    media_items = response.json()
    for item in media_items:
        media_id = item.get("id")

        # Regenerate thumbnail for each media item
        regenerate_endpoint = f"{wp_url}/regenerate-thumbnails/v1/regenerate/{media_id}?only_regenerate_missing_thumbnails=true&delete_unregistered_thumbnail_files=false&update_usages_in_posts=false"
        regenerate_response = requests.get(regenerate_endpoint, auth=auth)

        if regenerate_response.status_code == 200:
            print(f"Successfully regenerated thumbnail for media ID {media_id}")
        else:
            print(f"Failed to regenerate thumbnail for media ID {media_id}")

        # Wait for 2 seconds to avoid overwhelming the server
        time.sleep(2)
else:
    print("Failed to fetch media items.")

