# BookDescriptor
This script automates the process of updating missing product descriptions on a WooCommerce website from a local csv source. The code was written for a specific book shop struggling with legally licensed Synopsis information being provided in a separate outdated format. You may need to remove or change some of these restraints to use UTF8 encoding on the csv file for example. The csv file needs to have a SKU & Synopsis column at the minimum, and match the current naming structure. 

The script is likely inefficient, but by design will have to make less and less changes over time if used as designed. The use case is to mop up a large amount of missing descriptions with high quality replacements from a local source.

1. **Connects to the WooCommerce website** using the provided credentials.
2. **Finds the latest CSV file** containing product information, such as SKUs and descriptions, in the script's directory.
3. **Loads the CSV file** and extracts the necessary product information.
4. **Retrieves a list of products** from the website that are missing descriptions.
5. **Goes through each product in the CSV file**, checks if it needs a description, and updates the product on the website accordingly.
6. **Logs relevant information** for tracking and debugging purposes in a simple, easy-to-read format.

The script helps streamline the process of updating product descriptions on the website, making it more convenient for website administrators to manage product information.
