PRODUCT_TYPE = (
    (0, 'GOODS'),
    (1, 'SERVICES'),
    (2, 'BUNDLE'),
)

PRODUCT_TYPE_DICT = {
    0: 'GOODS',
    1: 'SERVICES',
    2: 'BUNDLE',
}
    
Currency = (
    (0,'₹'),
    (1,'$'),
    (2,'CA$'),
    (3,'€'),
    (4,'Kč'),
    (5,'AU$'),
)


UNITS = (
    (0, 'KG'),
    (1, 'G'),
    (2, 'OZ'),
    (3, 'LB'),
    (4, 'T'),
    (5, 'MT'),
    (6, 'CT'),
    (7, 'FURLONG'),
    (8, 'IN'),
    (9, 'FT'),
    (10, 'YD'),
    (11, 'MI'),
    (12, 'M'),
    (13, 'ML'),
    (14, 'SF'),
    (15, 'SQ'),
    (16, 'CM'),
    (17, 'BKT'),
    (18, 'BAG'),
    (19, 'BOWL'),
    (20, 'BX'),
    (21, 'CARD'),
    (22, 'CASE'),
    (23, 'CARTON'),
    (24, 'DZ'),
    (25, 'EA'),
    (26, 'GAL'),
    (27, 'GS'),
    (28, 'KIT'),
    (29, 'SET'),
    (30, 'SHT'),
    (31, 'TUBE'),
    (32, 'PK'),
    (31, 'TB'),
    (33, 'TSP'),
    (34, 'C'),
    (35, 'PT'),
    (36, 'QT'),
    (37, 'ML'),
    (38, 'L'),
)

PRODUCT_STOCK_NOTIFICATION_TRIGGERS = (
    (0, '5 DAYS AGO'),
    (1, '1 WEEK AGO'),
    (2, '10 DAYS AGO'),
    (3, '2 WEEKS AGO'),
    (4, '1 MONTH AGO'),
    (5, '45 DAYS AGO'),
    (6, '2 MONTHS AGO'),
    (7, '3 MONTHS AGO'),
    (8, '6 MONTHS AGO'),
    (9, '1 YEAR AGO'),
)


#****************************************************************************
#   INVOICE FREQUENCY
#****************************************************************************
INVOICE_FREQUENCY = (
    (0, 'WEEKLY'),
    (1, 'MONTHLY'),
    (2, 'QUARTERLY'),
    (2, 'HALF-YEARLY'),
    (2, 'YEARLY'),
)

#****************************************************************************
#   INVOICE TYPE
#****************************************************************************
INVOICE_TYPE = (
    (0, 'One Time'), 
    (1, 'Recurring'),
)


#****************************************************************************
#   SALES ACCOUNT 
#****************************************************************************
SALES_ACCOUNT_DICT = {
    0:"Discount",
    1:"General Income",
    2:"Interest Income",
    3:"Late Fee Income",
    4:"Other Charges",
    5:"Sales",
    6:"Shipping Charges",
}

SALES_ACCOUNT_CHOICES = (
    ("Income",(
            (0, "Discount"),
            (1, "General Income"),
            (2, "Interest Income"),
            (3, "Late Fee Income"),
            (4, "Other Charges"),
            (5, "Sales"),
            (6, "Shipping Charges"),
        ),
    ),
)

PURCHASE_ACCOUNT_CHOICES = (
    ("Expense",(
            (0,'Advertising and Marketing/Promotion'),
            (1,'Automobile Expense'),
            (2,'Bad Debit'),
            (3,'Bank Fees and Charges'),
            (4,'Consultant Expense'),
            (5,'Charitable Contributions'),
            (6,'Contract Assets'),
            (7,'Credit Card Charges'),
            (8,'Depreciation Expense'),
            (9,'IT and Internet Expenses'),
            (10,'Janitorial Expenses'),
            (11,'Meals and Entertainment'),
            (12,'Merchandise'),
            (13,'Office Supplies'),
            (14,'Other Expenses'),
            (15,'Postage'),
            (16,'Printing and Stationery'),
            (17,'Raw Materials and Consumables'),
            (18,'Repairs and Maintenance'),
            (19,'Salaries and Employee Wages'),
            (20,'Telephone Expenses'),
            (21,'Transportation Expenses'),
            (22,'Travel Expenses'),
            (23,'Cost Of Goods Sold'),
            (24,'Accounting Fee'),
            (25,'Annual Maintenance Charges'),
            (26,'Depreciation'),
            (27,'Refund From Vendors'),
            (28,'Dues & Subscription'),
            (29,'Education & Training'),
            (30,'Fuel'),
            (31,'Interest Expense'),

        ),
    ),
)