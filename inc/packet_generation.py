import random
import requests
from requests.exceptions import RequestException

# --- Configuration Constants ---
# Use constants for easier modification and readability.
NUM_REQUESTS = 500

# --------------------------------------------------------------------------------------------------------------------
#                                     Post Lab Exercise
#
# Replace the value stored in Doh_Packet_Percentage below from 50 to the values indicated in your lab manual and
# rerun the lab
# --------------------------------------------------------------------------------------------------------------------
# Set the probability of a request being DoH (e.g., 70 means 70%).
DOH_PROBABILITY_PERCENT = 50

# List of DoH servers, structured to handle different API requirements.
DOH_SERVERS = [
    {
        "url": "https://dns.google/resolve",
        "headers": None,
        "params": lambda domain: {"name": domain, "type": "A"},
    },
    {
        "url": "https://cloudflare-dns.com/dns-query",
        "headers": {"accept": "application/dns-json"},
        "params": lambda domain: {"name": domain, "type": "A"},
    },
]

# Cleaned list of websites. Avoid prefixes like 'www.' or 'http://'
# to ensure they work correctly with both DoH queries and browser navigation.
WEBSITES = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "amazon.com",
    "twitter.com",
    "instagram.com",
    "linkedin.com",
    "pinterest.com",
    "reddit.com",
    "wikipedia.org",
    "netflix.com",
    "microsoft.com",
    "ebay.com",
    "nike.com",
    "apple.com",
    "yahoo.com",
    "twitch.tv",
    "vimeo.com",
    "dropbox.com",
    "airbnb.com",
    "spotify.com",
    "snapchat.com",
    "hulu.com",
    "walmart.com",
    "github.com",
    "slack.com",
    "medium.com",
    "canva.com",
    "shopify.com",
    "zillow.com",
    "fandom.com",
    "paypal.com",
    "cnn.com",
    "bbc.com",
    "espn.com",
    "forbes.com",
    "cnbc.com",
    "nytimes.com",
    "huffpost.com",
    "buzzfeed.com",
    "nationalgeographic.com",
    "stackoverflow.com",
    "theguardian.com",
    "mashable.com",
    "indeed.com",
    "engadget.com",
    "wired.com",
    "cnet.com",
]

# --- Function Definitions ---


def perform_doh_lookup(website):
    """
    Performs a DoH lookup for a given website using a randomly chosen DoH server.
    """
    print(f"Performing DoH lookup for: {website}")
    try:
        server_config = random.choice(DOH_SERVERS)
        params = server_config["params"](website)

        response = requests.get(
            server_config["url"],
            params=params,
            headers=server_config["headers"],
            timeout=10,  # Add a timeout to prevent hanging
        )
        response.raise_for_status()
        print("Response Content:")
        print(response.content)
    except RequestException as e:
        print(f"DoH lookup failed: {e}")


def perform_nondoh_lookup(website):
    """
    Performs a non-DoH lookup by navigating to the website using Selenium,
    which triggers a standard system DNS lookup.
    """
    print(f"Performing non-DoH lookup for: {website}")
    try:
        response = requests.get(
            f"https://{website}",
            timeout=10,
        )
        response.raise_for_status()
        print("Response Content:")
        print(response.content)
    except RequestException as e:
        print(f"Non- DoH lookup failed: {e}")


# --- Main Execution Block ---=
def main():
    """
    Main function to set up the driver and run the traffic generation loop.
    """
    driver = None  # Initialize driver to None
    try:
        for i in range(NUM_REQUESTS):
            website = random.choice(WEBSITES)

            if random.uniform(0, 100) < DOH_PROBABILITY_PERCENT:
                perform_doh_lookup(website)
            else:
                perform_nondoh_lookup(website)

    finally:
        if driver:
            print("\nShutting down the Chrome driver.")
            driver.quit()
        print("Script finished.")


if __name__ == "__main__":
    main()
