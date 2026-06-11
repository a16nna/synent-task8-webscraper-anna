import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books = []

print("Starting Book Market Intelligence Scraper...\n")

for page in range(1, 51):

    url = BASE_URL.format(page)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        all_books = soup.find_all("article", class_="product_pod")

        for book in all_books:

            title = book.h3.a["title"]

            price_text = book.find(
                "p",
                class_="price_color"
            ).text.strip()

            # Fix encoding issues like Â£51.77
            price = float(
                re.sub(r"[^\d.]", "", price_text)
            )

            rating = book.find(
                "p",
                class_="star-rating"
            )["class"][1]

            availability = (
                book.find(
                    "p",
                    class_="instock availability"
                )
                .text.strip()
            )

            books.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Availability": availability
            })

        print(f"✓ Page {page} scraped")

    except Exception as e:
        print(f"✗ Error on page {page}: {e}")

print("\nScraping Complete!")

# Create DataFrame
df = pd.DataFrame(books)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_file = f"books_data_{timestamp}.csv"
json_file = f"books_data_{timestamp}.json"
report_file = f"report_{timestamp}.txt"

# Save CSV
df.to_csv(csv_file, index=False)

# Save JSON
df.to_json(
    json_file,
    orient="records",
    indent=4
)

# Analytics

total_books = len(df)

average_price = round(
    df["Price"].mean(),
    2
)

most_expensive = df.loc[
    df["Price"].idxmax()
]

cheapest = df.loc[
    df["Price"].idxmin()
]

rating_distribution = (
    df["Rating"]
    .value_counts()
)

top_expensive = (
    df.sort_values(
        by="Price",
        ascending=False
    )
    .head(10)
)

# Generate Report

with open(report_file, "w", encoding="utf-8") as report:

    report.write(
        "BOOK MARKET INTELLIGENCE REPORT\n"
    )

    report.write("=" * 50 + "\n\n")

    report.write(
        f"Total Books Scraped: {total_books}\n"
    )

    report.write(
        f"Average Book Price: £{average_price}\n\n"
    )

    report.write(
        "MOST EXPENSIVE BOOK\n"
    )

    report.write("-" * 25 + "\n")

    report.write(
        f"Title: {most_expensive['Title']}\n"
    )

    report.write(
        f"Price: £{most_expensive['Price']}\n\n"
    )

    report.write(
        "CHEAPEST BOOK\n"
    )

    report.write("-" * 25 + "\n")

    report.write(
        f"Title: {cheapest['Title']}\n"
    )

    report.write(
        f"Price: £{cheapest['Price']}\n\n"
    )

    report.write(
        "RATING DISTRIBUTION\n"
    )

    report.write("-" * 25 + "\n")

    for rating, count in rating_distribution.items():

        report.write(
            f"{rating}: {count}\n"
        )

    report.write(
        "\nTOP 10 MOST EXPENSIVE BOOKS\n"
    )

    report.write("-" * 35 + "\n")

    for _, row in top_expensive.iterrows():

        report.write(
            f"{row['Title']} - £{row['Price']}\n"
        )

# Console Summary

print("\nANALYTICS SUMMARY")
print("=" * 30)

print(f"Total Books: {total_books}")
print(f"Average Price: £{average_price}")

print(
    f"Most Expensive Book: {most_expensive['Title']}"
)

print(
    f"Price: £{most_expensive['Price']}"
)

print(
    f"Cheapest Book: {cheapest['Title']}"
)

print(
    f"Price: £{cheapest['Price']}"
)

print("\nFiles Generated Successfully")

print(f"CSV File    : {csv_file}")
print(f"JSON File   : {json_file}")
print(f"Report File : {report_file}")