import requests
from datetime import datetime, timedelta
import csv

# Replace with your store URL and API keys
store_url = 'https://xx.co.uk/'
consumer_key = 'xx'
consumer_secret = 'xx'

# Set the cutoff date for "old stock" (90 days ago)
cutoff_date = datetime.now() - timedelta(days=90)

# Define the API endpoint to retrieve products
endpoint = f'{store_url}/wp-json/wc/v3/products'

# Set the API parameters including authentication and product fields to retrieve
params = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'per_page': 100,  # Change this value depending on the number of products in your store
    'fields': 'id,name,stock_status,date_modified'
}

# Retrieve the list of products from the API
response = requests.get(endpoint, params=params)
products = response.json()

# Write the old stock products to a CSV file
with open('oldStock.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product ID', 'Product Name', 'Last Updated Date'])
    for product in products:
        # Check if the product is out of stock and its last updated date is older than the cutoff date
        if product['stock_status'] == 'outofstock' and datetime.fromisoformat(product['date_modified'][:-1]) < cutoff_date:
            writer.writerow([product['id'], product['name'], product['date_modified']])

# Print a message to indicate the CSV file has been created
print('oldStock.csv file created successfully.')