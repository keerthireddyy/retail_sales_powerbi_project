# Retail Sales & Profitability Dashboard — Power BI project

A complete, reproducible portfolio project using fictional retail orders. The package includes a data generator, a ready-to-load CSV, Power Query M, DAX model tables and measures, and a three-page report plan.

## Project question

Which products, customers, regions, and discounts are driving revenue and profit—and where are sales unprofitable?

## Files

- `generate_data.py` — creates deterministic synthetic data using only the Python standard library.
- `data/orders.csv` — generated dataset (about 5,000–6,000 order lines across 2022–2025).
- `powerbi/Orders.m` — Power Query query for importing and cleaning the CSV.
- `powerbi/ModelTables.dax` — DAX for the calendar, product, customer, and region tables.
- `powerbi/Measures.dax` — sales, profit, customer, YoY, YTD, and ranking measures.
- `powerbi/ReportLayout.md` — visual-by-visual report build guide.

## Requirements

- Power BI Desktop (Windows) to build and save the `.pbix` report.
- Python 3.9+ only if you want to regenerate the sample CSV. No Python packages are required.

## Quick start

1. Unzip the project folder somewhere convenient.
2. Open `generate_data.py` from a terminal and run:

   ```bash
   python generate_data.py
   ```

   This creates or replaces `data/orders.csv`.
3. Open Power BI Desktop and choose **Transform data > New source > Blank query**.
4. Open **Advanced Editor**, paste the contents of `powerbi/Orders.m`, and change its `FilePath` value to the full path of your `data/orders.csv` file. For example:

   ```text
   C:\Users\YourName\Documents\retail_sales_powerbi_project\data\orders.csv
   ```

   Name the query `Orders`, then select **Close & Apply**.
5. In Power BI, create the tables from `powerbi/ModelTables.dax`. Use **Modeling > New table** and paste one table definition at a time: `DimDate`, `DimProduct`, `DimCustomer`, and `DimRegion`.
6. Create these relationships in **Model view** (one-to-many, single direction from dimension to Orders):
   - `DimDate[Date]` → `Orders[Order Date]`
   - `DimProduct[Product ID]` → `Orders[Product ID]`
   - `DimCustomer[Customer ID]` → `Orders[Customer ID]`
   - `DimRegion[Region]` → `Orders[Region]`
7. Select `DimDate`, choose **Mark as date table**, and select `DimDate[Date]`. Sort `DimDate[Month]` by `DimDate[Month Number]` and `DimDate[Year-Month]` by `DimDate[Year-Month Sort]`.
8. Create the measures in `powerbi/Measures.dax` one at a time using **Modeling > New measure**. For best formatting, set currency measures to currency and ratio measures to percentage.
9. Build the pages using `powerbi/ReportLayout.md`.
10. Save the finished report as `Retail_Sales_Profitability.pbix`.

## Data notes

- All data is fictional and generated with a fixed random seed, so regenerating it produces the same dataset.
- `Sales` is net of the line discount. `Profit` is net sales minus estimated product cost; larger discounts can result in negative profit.
- An order can have multiple product rows. Use `DISTINCTCOUNT(Orders[Order ID])` for order count rather than counting rows.
- The data spans four calendar years so year-over-year measures have prior-year data to compare.

## What to discuss in a portfolio walkthrough

1. Which region and category combination has the strongest profit margin?
2. Which products sell well but have negative profit?
3. How do discount levels relate to profit?
4. How did sales and profit change year over year?
5. What practical pricing or product-mix action would you recommend?

Power BI report visuals are configured in Power BI Desktop; this source bundle provides the dataset and complete Power Query/DAX code, but does not contain a prebuilt `.pbix` file.
