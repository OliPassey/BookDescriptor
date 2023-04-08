import re
import glob
import os
import logging
import pandas as pd
from woocommerce import API

# Setup Logging
logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')

# Variables for the site URL and API credentials
site_url = 'https://yourshop.co.uk'
client_key = 'xx'
client_secret = 'xx'

# Create a connection to the WooCommerce API
wc_api = API(
    url=site_url,
    consumer_key=client_key,
    consumer_secret=client_secret,
    version='wc/v3',
    timeout=30
)

def get_products_without_description():
    """
    Searches the WooCommerce API for products without a description
    and returns a list of their SKUs.
    """
    sku_list = []
    page = 1
    
    while True:
        # Get products from the WooCommerce API
        products = wc_api.get('products', params={'per_page': 100, 'page': page}).json()
        
        # Break the loop if there are no more products
        if not products:
            break
        
        # Loop through each product
        for product in products:
            # If the product has no description, add its SKU to the list
            if not product['description']:
                sku_list.append(product['sku'])
        
        # Increment the page number to fetch the next page of products
        page += 1
    print(f'Products found: {sku_list}')
    return sku_list
    


# Get the latest CSV file
print('Searching for latest CSV file...')
csv_file = max(glob.glob('TitleDataExport_*.csv'), key=os.path.getctime)
print(f'Found CSV file: {csv_file}')

# Load the CSV file into a Pandas dataframe
print(f'Loading CSV file: {csv_file}...')
try:
    df = pd.read_csv(csv_file, usecols=['SKU', 'Synopsis'], encoding='cp1252')
    print(f'Loaded CSV file: {csv_file}')
except Exception as e:
    print(f'Error loading CSV file: {e}')
    exit()

# Get the list of SKUs that require a description
print('Searching for products without descriptions...')
try:
    sku_list = get_products_without_description()
    print(f'{len(sku_list)} products require a description.')
except Exception as e:
    print(f'Error getting list of products without descriptions: {e}')
    exit()

# prints the first 10 rows of the dataframe, can be commented out in normal operation
#print(df.head(10))  

# Loop through each row in the dataframe
for index, row in df.iterrows():
    # Get the SKU and synopsis from the dataframe
    sku = str(row['SKU'])  # Convert the SKU to a string
    synopsis = row['Synopsis']
    
    logging.info(f'Checking SKU {sku}...')  # Debugging print statement
    
    # If the SKU is not in the list of SKUs that require a description, skip to next row
    logging.info(f'Checking SKU {sku} (type: {type(sku)})...')  # Debugging print statement
    logging.info(f'sku_list: {sku_list}')

    if sku not in sku_list:
        logging.info(f'SKU {sku} not in the list of products requiring a description.')  # Debugging print statement
        continue
    
    print(f'Processing SKU {sku} with synopsis "{synopsis}"...')
    
    if pd.isna(synopsis):
        print(f'No synopsis found for product with SKU {sku} - skipping.')
        continue
    
    # Get the current product from the WooCommerce API
    logging.info(f'Fetching product with SKU {sku} from the WooCommerce API...')  # Debugging print statement
    product = wc_api.get(f'products?sku={sku}').json()
    
    # If no product found, skip to next row
    if not product:
        logging.info(f'No product found with SKU {sku}.')
        continue
    
    # Get the first product in the search results
    product_id = product[0]['id']
    
    # If the product has no description, update it with the synopsis from the CSV file
    if not product[0]['description']:
        # Check if the synopsis contains HTML tags
        if not re.search('<.*?>', synopsis):
            synopsis = f'<p>{synopsis}</p>'
        
        logging.info(f'Updating product {product_id} with new description: {synopsis}')
        try:
            wc_api.put(f'products/{product_id}', data={'description': synopsis})
            print(f'Successfully updated product {product_id} with new description: {synopsis}')
        except Exception as e:
            logging.info(f'Error updating product {product_id}: {e}')
