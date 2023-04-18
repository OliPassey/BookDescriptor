from tkinter import ttk
from urllib.request import urlopen
from PIL import Image, ImageTk
import re
import glob
import os
import logging
import pandas as pd
from woocommerce import API
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
import threading
import json

# Setup Logging
logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Variables for the site URL and API credentials
site_url = config['site_url']
client_key = config['client_key']
client_secret = config['client_secret']

# Create a connection to the WooCommerce API
wc_api = API(
    url=site_url,
    consumer_key=client_key,
    consumer_secret=client_secret,
    version='wc/v3',
    timeout=30
)

def main():
    def get_products_without_description():
        """
        Searches the WooCommerce API for the last 1000 created products without a description
        and returns a list of their SKUs.
        """
        sku_list = []
        
        page = 1
        total_products_processed = 0
        products_per_page = 100
        max_products = 100

        print(f'Connecting to {site_url}')
        logging.info(f'Connecting to {site_url}')
        print(f'Downloading the latest {max_products} products.')
        logging.info(f'Downloading the latest {max_products} products.')
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
            logging.info(f'Downloading page {page}...')
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
        logging.info(f'Total products downloaded: {total_products_processed}')
        return sku_list

    # Get the latest CSV file
    print('Searching for latest CSV file...')
    csv_file = max(glob.glob('TitleDataExport_*.csv'), key=os.path.getctime)
    print(f'Found CSV file: {csv_file}')
    skus_missing_synopsis = []
    # Load the CSV file into a Pandas dataframe
    try:
        df = pd.read_csv(csv_file, usecols=['SKU', 'Synopsis'], encoding='cp1252')
        print(f'Loaded CSV file: {csv_file}')
        logging.info(f'Loaded CSV file: {csv_file}')
        # prints the first 10 rows of the dataframe, can be commented out in normal operation
        #print(df.head(10))  
        print(f'Total rows loaded in DataFrame: {len(df)}')
        logging.info(f'Total rows loaded in DataFrame: {len(df)}')
    except Exception as e:
        print(f'Error loading CSV file: {e}')
        logging.info(f'Error loading CSV file: {e}')
        exit()

    # Get the list of SKUs that require a description
    print('Searching for products without descriptions...')
    try:
        sku_list = get_products_without_description()
        print(f'{len(sku_list)} products require a description.')
        logging.info(f'{len(sku_list)} products require a description.')
    except Exception as e:
        print(f'Error getting list of products without descriptions: {e}')
        logging.info(f'Error getting list of products without descriptions: {e}')
        exit()
    


    # Set the index of the DataFrame to the 'SKU' column and convert it to string
    df['SKU'] = df['SKU'].astype(str)
    df.set_index('SKU', inplace=True)


        # Loop through each SKU in the sku_list
    for sku in sku_list:
        print(f'Checking SKU {sku}...')
        logging.info(f'Checking SKU {sku}...')
        
        # Check if the SKU exists in the DataFrame
        if sku in df.index:
            synopsis = df.loc[sku]['Synopsis']
            
            if pd.isna(synopsis):
                print(f'No synopsis for SKU {sku} exists from Batch - skipping.')
                logging.info(f'No synopsis for SKU {sku} exists from Batch - skipping.')
                skus_missing_synopsis.append(sku)
                continue

            
            # Get the current product from the WooCommerce API
            print(f'Fetching product with SKU {sku} from the WooCommerce API...')
            logging.info(f'Fetching product with SKU {sku} from the WooCommerce API...')
            product = wc_api.get(f'products?sku={sku}').json()

            # If no product found, skip to next row
            if not product:
                print(f'No product found with SKU {sku}.')
                logging.info(f'No product found with SKU {sku}.')
                continue

            # Get the first product in the search results
            product_id = product[0]['id']

            # If the product has no description, update it with the synopsis from the CSV file
            if not product[0]['description']:
                # Check if the synopsis contains HTML tags
                if not re.search('<.*?>', synopsis):
                    synopsis = f'<p>{synopsis}</p>'

                print(f'Updating product {sku}')
                logging.info(f'Updating product {sku}')
                try:
                    wc_api.put(f'products/{product_id}', data={'description': synopsis})
                    print(f'Successfully updated product {sku}')
                    logging.info(f'Successfully updated product {sku}')
                except Exception as e:
                    print(f'Error updating product {sku}: {e}')
                    logging.info(f'Error updating product {sku}: {e}')

    print(f'Process complete.')
    print("\nSKUs with missing synopses, you may want to update these manually:")
    print(skus_missing_synopsis)
    logging.info(f'Process Complete')
    logging.info("\nSKUs with missing synopses, you may want to update these manually:")
    logging.info(skus_missing_synopsis)

if __name__ == '__main__':
    # Create a function to redirect console output to the GUI
    def redirector(input_str):
        console.insert(tk.END, input_str)
        console.see(tk.END)  # Automatically scroll to the end of the console output

    sys.stdout.write = redirector

    # Create the GUI window
    root = tk.Tk()
    root.title("PTS-BookDescriptor")
    root.geometry("800x600")

    # Create a console output
    console = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    console.grid(column=0, row=0, pady=(10, 0))

    # Create a Start button
    def start_button_click():
        console.delete('1.0', tk.END)
        threading.Thread(target=main).start()

    start_button = tk.Button(root, text="Start", command=start_button_click)
    start_button.grid(column=0, row=1, pady=10)

    # Create an exit button
    def exit_button_click():
        root.destroy()

    exit_button = tk.Button(root, text="Exit", command=exit_button_click)
    exit_button.grid(column=0, row=2, pady=10)

    # Run the GUI
    root.mainloop()
