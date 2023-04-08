# BookDescriptor
This script automates the process of updating missing product descriptions on a WooCommerce website from a local csv source.

1. **Connects to the WooCommerce website** using the provided credentials.
2. **Finds the latest CSV file** containing product information, such as SKUs and descriptions, in the script's directory.
3. **Loads the CSV file** and extracts the necessary product information.
4. **Retrieves a list of products** from the website that are missing descriptions.
5. **Goes through each product in the CSV file**, checks if it needs a description, and updates the product on the website accordingly.
6. **Logs relevant information** for tracking and debugging purposes in a simple, easy-to-read format.

The script helps streamline the process of updating product descriptions on the website, making it more convenient for website administrators to manage product information.
