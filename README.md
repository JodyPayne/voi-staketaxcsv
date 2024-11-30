# VOI CSV Exporter

## Overview

The **VOI CSV Exporter** is a tool designed to export transaction data from the VOI ecosystem into various CSV formats, such as **Koinly** and **CryptoTax**, for tax reporting and portfolio analysis.

This project is a **GitFork** of the open-source **staketaxcsv** framework, customized specifically for VOI transactions.

## Tools Used
- **Python**
- **ChatGPT**
- **GitBash**

### Current Status
The primary and tested format is **Koinly**, as this project was built with compatibility for Koinly tax software in mind.

---

## Instructions

### All-in-One Command Workflow

Follow the six steps below to generate a VOI CSV with historical VOI USD prices:

# 1. Navigate to the src directory and run the VOI exporter script with your wallet address:
py voi_exporter.py --format koinly --wallet <wallet_address>

# 2. Locate the exported wallet .csv file:
# It will be saved in the following directory:
# voi-staketaxcsv/src/reports

# 3. Download VOI historical data from CoinGecko:
# Visit https://www.coingecko.com/en/coins/voi-network/historical_data
# Save the historical price file in the directory:
# voi-staketaxcsv/src/reports

# 4. Open the voipu-koinly.py script in an editor (e.g., Notepad):
# Replace 'voi_XXX_koinly.csv' in line 13 with your exported CSV file name:
# transactions_file_path = 'voi_XXX_koinly.csv'

# 5. Run the voipu-koinly.py script to process the file:
py voipu-koinly.py

# 6. The new CSV file with historical VOI prices will be created:
# The output file will be prefixed with 'pu_' and saved in the same directory:
# voi-staketaxcsv/src/reports
