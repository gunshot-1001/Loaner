import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URLs for different loan types
urls = {
    "Home Loan": "https://www.bankbazaar.com/home-loan-interest-rate.html",
    "Car Loan": "https://www.bankbazaar.com/car-loan-interest-rate.html",
    "Personal Loan": "https://www.bankbazaar.com/personal-loan-interest-rate.html"
}

# Path to save CSV
save_dir = r"C:\Users\Durvank\Loaner\backend\data\raw"
os.makedirs(save_dir, exist_ok=True)
csv_path = os.path.join(save_dir, "loan_interest_rates.csv")

data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

for loan_type, url in urls.items():
    print(f"Scraping {loan_type} data...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        print(f"⚠️ No table found for {loan_type}")
        continue

    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            bank_name = cols[0].get_text(strip=True)
            interest_rate = cols[1].get_text(strip=True)
            data.append({
                "Loan Type": loan_type,
                "Bank": bank_name,
                "Interest Rate": interest_rate,
                "Link": url
            })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"✅ Data saved to {csv_path}")
print(df.head())
