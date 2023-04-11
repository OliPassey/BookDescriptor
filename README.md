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

The script is capable of downloading 1000 products per minute, if you have 25k products expect the download to take 25 minutes. Also think about how many API calls you are likely to make. In my first run i had 8k titles to fix and after 4k (many hours) it crashed Apache or SQL (not sure which).

Other parts of this repo: <br />
-script.py works. - use this in the fist instance. <br />
-bookDescriptor.py in progress, will allow for parts of the script to be run on-demand, and makes it easier to dump out the info the script is processing. <br />
-gui.py work in progress towards an executable one file version of the script. <br />
-logged output, working towards dumping out a list of SKUs it couldn't find a synopsis for so you can potentially search elsewhere for them. <br />
-old stock, start on work to identify dead stock and remove it from the site.

Please test this script on a dev site before letting loose on production, i am not responsible for what this script does to your site, even though i have used and tested it extensively.

Usage of bookDescriptor.py <br />
./bookDescriptor.py --download  <br />
./bookDescriptor.py --local <br />

Usage of script.py <br />
./script.py
