# Report layout and field mapping

## Page 1 — Executive Overview

- **Cards:** `[Total Sales]`, `[Total Profit]`, `[Profit Margin]`, `[Order Count]`
- **Line chart:** Axis `DimDate[Year-Month]`; Values `[Total Sales]` and `[Total Profit]`
- **Clustered bar chart:** Axis `DimRegion[Region]`; Values `[Total Sales]`, `[Total Profit]`
- **Matrix:** Rows `DimProduct[Category]`, then `DimProduct[Sub-Category]`; Values `[Total Sales]`, `[Total Profit]`, `[Profit Margin]`
- **Slicers:** `DimDate[Year]`, `DimRegion[Region]`, `DimCustomer[Segment]`, `DimProduct[Category]`

## Page 2 — Product Performance

- **Bar chart:** Axis `DimProduct[Product Name]`; Value `[Total Profit]`. Use a visual-level Top N filter to show the top 10 products by `[Total Profit]`.
- **Scatter chart:** X-axis `[Total Sales]`; Y-axis `[Total Profit]`; Details `DimProduct[Product Name]`; Size `[Units Sold]`; Legend `DimProduct[Category]`.
- **Matrix:** Rows `DimProduct[Category]`, `DimProduct[Sub-Category]`, `DimProduct[Product Name]`; Values `[Total Sales]`, `[Total Profit]`, `[Average Discount]`, `[Product Sales Rank]`.
- Add a conditional-formatting color scale to profit so loss-making products stand out.

## Page 3 — Customer & Geography

- **Bar chart:** Axis `Orders[State]`; Values `[Total Sales]` and `[Total Profit]`.
- **Donut chart:** Legend `DimCustomer[Segment]`; Values `[Order Count]`.
- **Table:** `DimCustomer[Customer Name]`; Values `[Total Sales]`, `[Total Profit]`, `[Order Count]`. Sort by `[Total Sales]` descending and apply a Top N filter if desired.
- **Slicers:** `DimDate[Year]`, `DimRegion[Region]`, `DimProduct[Category]`.

## Formatting suggestions

- Format sales, profit and average order value as currency; margins, discounts and YoY percentages as percentages.
- Sort `DimDate[Month]` by `DimDate[Month Number]` and `DimDate[Year-Month]` by `DimDate[Year-Month Sort]`.
- Use a consistent color convention: sales in blue, profit in teal, and negative profit in red.
- Add descriptive titles and ensure visual interactions work as expected.
