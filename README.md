# BookDescriptor

1. **Connects to the WooCommerce website** using the provided credentials.
2. **Finds the latest CSV file** containing product information, such as SKUs and descriptions, in the script's directory.
3. **Loads the CSV file** and extracts the necessary product information.
4. **Retrieves a list of products** from the website that are missing descriptions.
5. **Goes through each product in the CSV file**, checks if it needs a description, and updates the product on the website accordingly.
6. **Logs relevant information** for tracking and debugging purposes in a simple, easy-to-read format.

The script helps streamline the process of updating product descriptions on the website, making it more convenient for website administrators to manage product information.

The script is capable of downloading 1000 products per minute, if you have 25k products expect the download to take 25 minutes. Also think about how many API calls you are likely to make. In my first run i had 8k titles to fix and after 4k (many hours) it crashed Apache or SQL (not sure which).

Please test this script on a dev site before letting loose on production, i am not responsible for what this script does to your site, even though i have used and tested it extensively.

## Installation & Usage
-Clone the repo locally (run on your PC, not the webserver)<br />
-Create API Key & Secret in WooCommerce (do not share these with anyone)<br />
-Add your site URL & API Credentials to config.json<br />
-Install Python3 if not already installed<br />
-pip install woocommerce<br />
-pip install pandas<br />
-pip install tk<br />
-pip install pillow<br />

Usage <br />
-Place a csv output of ISBN, Synopsis in the same folder as gui.py<br />
-python ./gui.py<br />

Example Output:<br />
PS C:\BookDescriptor> .\script.py<br />
Searching for latest CSV file...<br />
Found CSV file: TitleDataExport_2023041122.csv<br />
Loaded CSV file: TitleDataExport_2023041122.csv<br />
Searching for products without descriptions...<br />
Downloading page 1...<br />
Downloading page 2...<br />
Downloading page 3...<br />
Downloading page 4...<br />
Downloading page 5...<br />
Downloading page 6...<br />
Downloading page 7...<br />
Downloading page 8...<br />
Downloading page 9...<br />
Downloading page 10...<br />
Total products downloaded: 1000<br />
264 products require a description.<br />
Total rows in DataFrame: 1000<br />
Processing SKU 9781905847518<br />
Successfully updated product 407<br />
Processing SKU 9781741047226<br />
Successfully updated product 409<br />
Processing SKU 9780571280421<br />
Successfully updated product 411<br />
Processing SKU 9780007137312<br />
Successfully updated product 413<br />
