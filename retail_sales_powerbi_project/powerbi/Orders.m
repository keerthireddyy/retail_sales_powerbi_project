// Power Query M for the Orders fact table.
// Before applying: update FilePath to the location of data/orders.csv on your computer.
let
    FilePath = "C:\PowerBI\RetailSalesDashboard\data\orders.csv",
    Source = Csv.Document(
        File.Contents(FilePath),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    CleanColumnNames = Table.TransformColumnNames(PromotedHeaders, Text.Trim),
    ChangedTypes = Table.TransformColumnTypes(
        CleanColumnNames,
        {
            {"Row ID", Int64.Type},
            {"Order ID", type text},
            {"Order Date", type date},
            {"Ship Date", type date},
            {"Ship Mode", type text},
            {"Customer ID", type text},
            {"Customer Name", type text},
            {"Segment", type text},
            {"Country", type text},
            {"City", type text},
            {"State", type text},
            {"Postal Code", type text},
            {"Region", type text},
            {"Product ID", type text},
            {"Category", type text},
            {"Sub-Category", type text},
            {"Product Name", type text},
            {"Sales", Currency.Type},
            {"Quantity", Int64.Type},
            {"Discount", Percentage.Type},
            {"Profit", Currency.Type}
        },
        "en-US"
    ),
    TrimmedText = Table.TransformColumns(
        ChangedTypes,
        {
            {"Order ID", each Text.Trim(_), type text},
            {"Ship Mode", each Text.Trim(_), type text},
            {"Customer ID", each Text.Trim(_), type text},
            {"Customer Name", each Text.Trim(_), type text},
            {"Segment", each Text.Trim(_), type text},
            {"Country", each Text.Trim(_), type text},
            {"City", each Text.Trim(_), type text},
            {"State", each Text.Trim(_), type text},
            {"Postal Code", each Text.Trim(_), type text},
            {"Region", each Text.Trim(_), type text},
            {"Product ID", each Text.Trim(_), type text},
            {"Category", each Text.Trim(_), type text},
            {"Sub-Category", each Text.Trim(_), type text},
            {"Product Name", each Text.Trim(_), type text}
        }
    )
in
    TrimmedText
