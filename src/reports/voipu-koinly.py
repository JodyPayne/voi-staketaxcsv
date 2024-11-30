import pandas as pd
from datetime import datetime
import os

# Load the historical data
historical_file_path = 'voi-usd-max.csv'  # Update this path as needed
historical_data = pd.read_csv(historical_file_path)

# Convert `snapped_at` to datetime for easier matching
historical_data['snapped_at'] = pd.to_datetime(historical_data['snapped_at'])

# Load the transactions file
transactions_file_path = 'voi_XXX_koinly.csv'
transactions = pd.read_csv(transactions_file_path)

# Convert the `Date` column to datetime for easier matching
transactions['Date'] = pd.to_datetime(transactions['Date'])

# Create a dictionary for faster lookups
price_map = dict(zip(historical_data['snapped_at'].dt.date, historical_data['price']))

# Update the transactions with historical prices and net worth
prices = []
net_worths = []

for _, row in transactions.iterrows():
    transaction_date = row['Date'].date()
    price = price_map.get(transaction_date, 0)  # Default to 0 if no price is found
    if price:
        if row['Sent Amount'] > 0:  # Calculate based on Sent Amount
            net_worth = row['Sent Amount'] * price
        elif row['Received Amount'] > 0:  # Calculate based on Received Amount
            net_worth = row['Received Amount'] * price
        else:
            net_worth = 0
    else:
        net_worth = 0
    prices.append(price)
    net_worths.append(net_worth)

# Add the new columns
transactions['Price (USD)'] = prices
transactions['Net Worth Amount'] = net_worths

# Generate the output file path with "p_" prefix
directory, original_file_name = os.path.split(transactions_file_path)
new_file_name = 'pu_' + original_file_name
updated_file_path = os.path.join(directory, new_file_name)

# Save the updated transactions file
transactions.to_csv(updated_file_path, index=False)

print(f"Updated transactions saved to {updated_file_path}")
