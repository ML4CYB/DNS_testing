import random
import subprocess
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests

#-------------------------------------------------------------------------------------------------------------------
# This Python script is designed to generate both doH and non-doH traffic. It employs Chromium, a headless
# version of Google Chrome, along with the Selenium and Requests libraries to perform the lookups. The script
# maintains a list of 50 different websites. For doH lookups, the script utilizes two servers: Google's DNS
# server and Cloudflare's DNS server. The process begins by randomly selecting a website and then determining
# if the lookup will be doH or non-doH through a random true or false decision. For non-doH lookups, the driver
# simply performs a regular lookup of the website. In case of a doH lookup, the script selects one of the
# two doH servers and employs the Requests library to perform the lookup through that server. This approach
# facilitates the tagging of traffic as doH due to the ability to identify the server's IP address. The process
# repeats 500 times or until sufficient packets are captured by the tcpdump.
#-------------------------------------------------------------------------------------------------------------------
# DoH servers


doh_servers = [
    "https://dns.google/resolve",
    "https://cloudflare-dns.com/dns-query"
]
# Websites
websites = [
    "www.google.com",
    "www.youtube.com",
    "www.facebook.com",
    "www.amazon.com",
    "www.twitter.com",
    "www.instagram.com",
    "www.linkedin.com",
    "www.pinterest.com",
    "www.reddit.com",
    "www.wikipedia.org",
    "www.netflix.com",
    "www.microsoft.com",
    "www.ebay.com",
    "www.nike.com",
    "www.apple.com",
    "www.yahoo.com",
    "www.twitch.tv",
    "www.vimeo.com",
    "www.dropbox.com",
    "www.airbnb.com",
    "www.spotify.com",
    "www.snapchat.com",
    "www.hulu.com",
    "www.walmart.com",
    "www.github.com",
    "www.slack.com",
    "www.medium.com",
    "www.canva.com",
    "www.shopify.com",
    "www.zillow.com",
    "www.fandom.com",
    "www.homedepot.com",
    "www.paypal.com",
    "www.cnn.com",
    "www.bbc.com",
    "www.espn.com",
    "www.forbes.com",
    "www.cnbc.com",
    "www.nytimes.com",
    "www.huffpost.com",
    "www.buzzfeed.com",
    "www.nationalgeographic.com",
    "www.stackoverflow.com",
    "www.theguardian.com",
    "www.mashable.com",
    "www.indeed.com",
    "www.engadget.com",
    "www.wired.com",
    "www.cnet.com"
    
]

# Configure Chrome options running in headless mode
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')

# Configures service and sets up the driver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Loops though 500 different times to generate pacets
for i in range(500):

    # Picks a random website from the list
    ran_website = random.choice(websites)

    # Randomizes the choice between doH and non-doH lookups does 70% doH and 30% non-doH
    doh = random.randint(1,10)
    if doh <= 7 :
        print("Performing DoH lookup:", ran_website)
        # Chooses a random DoH server from the list
        doh_serv = random.choice(doh_servers)

        # Checks if the server is google's, forms the url, and preforms the lookup
        if doh_serv == "https://dns.google/resolve":
            query_url = f"{doh_serv}?name={ran_website}&type=a&do=1"
            response = requests.get(query_url)

        # If the servers is cloudflares it sets the header and params to the correct values
        # and preforms the lookup
        else:
            header = {"accept": "application/dns-json"}
            params = {    "name": ran_website, "type": "AAAA"}
            response = requests.get(doh_serv, params= params, headers= header)
            
        
        try:

            #-------------------------------------------------------------------------------------------------------
              # This is used for error checking. If the request was successful it will print out the
              # information received, if there is an request error it will print out the status_code for that error
            #-------------------------------------------------------------------------------------------------------

             if response.status_code == 200:
                   print("Response Content:")
                   print (response.content)
            
            # If encounters an error prints out the status code
             else:
              print(f"Request failed with status code: {response.status_code}")

     #-------------------------------------------------------------------------------------------------------
      # Again this is used for error checking if there is an error during the lookup process it will output
      # the error
     #------------------------------------------------------------------------------------------------------
        except Exception as error:
            print("DoH lookup err:", error)

    else:
        print("Performing non-DoH lookup:", ran_website)

        try:
            # Preforms the non-doH lookup
            driver.get("https://" + ran_website)
            print("Non-DoH title:", driver.title)
        
        # Will show the error if one occurs
        except Exception as e:
            print("Non-DoH lookup err:", e)


# Close the Chrome driver
driver.quit()