
#****************************************************************************
#   ACCOUNTS LEDGER - MAJOR HEADS
#****************************************************************************
LEDGER_ACCOUNT_DICT = {
    0 : "Income",
    1 : "Expense",
    2 : "Assets",
    3 : "Liabilities",
    4 : "Equity",
}

LEDGER_ACCOUNT_CHOICES = (
    (0, "Income"),
    (1, "Expense"),
    (2, "Assets"),
    (3, "Liabilities"),
    (4, "Equity"),
)

#****************************************************************************
#   ACCOUNTS LEDGER - MAJOR HEADS GROUPS
#****************************************************************************

ACCOUNTS_LEDGER_GROUPS_DICT = {
    0 : {
        "0_0" : "Other Income",
        "0_1" : "Discount",
        "0_2" : "General Income",
        "0_3" : "Sales",
        "0_4" : "Intrest Income",
        "0_5" : "Late fees Income",
        "0_6" : "Other Charges",
        "0_7" : "Shipping Charges",
    },
    1 : {  
        "1_0" : "Advertising and Marketing/Promotion",
        "1_1" : "Automobile Expense",
        "1_2" : "Bad Debit",
        "1_3" : "Bank Fees and Charges",
        "1_4" : "Consultant Expense",
        "1_5" : "Charitable Contributions",
        "1_6" : "Contract Assets",
        "1_7" : "Credit Card Charges",
        "1_8" : "Depreciation Expense",
        "1_9" : "IT and Internet Expenses",
        "1_10" : "Janitorial Expenses",
        "1_11" : "Lodging",
        "1_12" : "Meals and Entertainment",
        "1_13" : "Merchandise",
        "1_14" : "Office Supplies",
        "1_15" : "Other Expenses",
        "1_16" : "Postage",
        "1_17" : "Printing and Stationery",
        "1_18" : "Raw Materials and Consumables",
        "1_19" : "Repairs and Maintenance",
        "1_20" : "Salaries and Employee Wages",
        "1_21" : "Telephone Expenses",
        "1_22" : "Transportation Expenses",
        "1_23" : "Travel Expenses",
    },
    2 : {
        "2_0" : "Fix Assets",
        "2_1" : "Other Current Asset",
    },
    3 : {
        "3_0" : "Current Liabilities",
        "3_1" : "Credit Card",
        "3_2" : "Bank Over Drafts",
        "3_3" : "Non- Current Liabilities",
        "3_4" : "Loans",
        "3_5" : "Account Payables",
        "3_6" : "GST Payables",
        "3_7" : "Customer Advances",
        "3_8" : "Professional Tax Payable",
    },
    4 : {
        "4_0" : "Share Capital",
        "4_1" : "Retained Earnings",
    },
}

