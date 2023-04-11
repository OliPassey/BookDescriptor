import re
import glob
import os
import logging
import pandas as pd
import json
import argparse
from woocommerce import API

# Setup Logging
logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')

# Variables for the site URL and API credentials
site_url = 'https://xx.co.uk/'
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
    Searches the WooCommerce API for the last 1000 created products without a description
    and returns a list of their SKUs.
    """
    sku_list = []
    page = 1
    total_products_processed = 0
    products_per_page = 100
    max_products = 300

    while total_products_processed < max_products:
        # Get all products from the WooCommerce API with pagination and ordering
        response = wc_api.get('products', params={
            'per_page': products_per_page,
            'page': page,
            'order': 'desc',
            'orderby': 'date'
        })
        all_products = response.json()

        # If there are no more products, break the loop
        if not all_products:
            break

        print(f'Downloading page {page}...')  # Print the current page number

        # Loop through each product
        for product in all_products:
            total_products_processed += 1
            # If the product has no description, add its SKU to the list
            if not product['description']:
                sku_list.append(product['sku'])

            # Break the loop if total_products_processed reaches max_products
            if total_products_processed >= max_products:
                break

        # Increment the page number
        page += 1

    print(f'Total products downloaded: {total_products_processed}')
    return sku_list

def save_products_to_json(products):
    with open("products.json", "w") as f:
        json.dump(products, f)

def load_products_from_json():
    with open("products.json", "r") as f:
        sku_list = json.load(f)
    return sku_list

def save_local_output(sku_list, df):
    filtered_df = df[df['SKU'].apply(lambda x: str(x) in sku_list)]
    filtered_df.to_csv("output.csv", index=False, encoding='cp1252')

def main(load_from_local):
    # Get the latest CSV file
    print('Searching for latest CSV file...')
    csv_file = max(glob.glob('TitleDataExport_*.csv'), key=os.path.getctime)
    print(f'Found CSV file: {csv_file}')

    # Load the CSV file into a Pandas dataframe
    try:
        df = pd.read_csv(csv_file, usecols=['SKU', 'Synopsis'], encoding='cp1252')
        print(f'Loaded CSV file: {csv_file}')
    except Exception as e:
        print(f'Error loading CSV file: {e}')
        exit()

    # Get the list of SKUs that require a description
    print('Searching for products without descriptions...')
    if load_from_local:
        sku_list = load_products_from_json()
    else:
        try:
            sku_list = get_products_without_description()
            save_products_to_json(sku_list)
        except Exception as e:
            print(f'Error getting list of products without descriptions: {e}')
            exit()

    print(f'{len(sku_list)} products require a description.')
    print(f'Saving local output for manual import if required.')
    save_local_output(sku_list, df)


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
        
        print(f'Processing SKU {sku}')
        
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
            
            logging.info(f'Updating product {product_id}')
            try:
                wc_api.put(f'products/{product_id}', data={'description': synopsis})
                print(f'Successfully updated product {product_id}')
            except Exception as e:
                logging.info(f'Error updating product {product_id}: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update product descriptions from a CSV file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-download", action="store_true", help="Download products from the WooCommerce API.")
    group.add_argument("-local", action="store_true", help="Load products from a local JSON file.")
    
    args = parser.parse_args()

    main(load_from_local=args.local)
