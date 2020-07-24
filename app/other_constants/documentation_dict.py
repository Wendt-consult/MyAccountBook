
from app.other_constants import *

#====================================================================
# CUSTOMER TYPE
#====================================================================
customer_type = []

for record in user_constants.CUSTOMER_TYPE:
    customer_type.append("<li>{} - {}</li>".format(record[0], record[1]))

customer_type = ''.join(customer_type)

#====================================================================
# SALUTATION
#====================================================================
salutation = []

for record in user_constants.SALUTATIONS:
    salutation.append("<li>{} - {}</li>".format(record[0], record[1]))

salutation = ''.join(salutation)

#====================================================================
# SUB CUSTOMER
#====================================================================
is_sub_customer = []

for record in user_constants.IS_SUB_CUSTOMER:
    is_sub_customer.append("<li>{} - {}</li>".format(record[0], record[1]))

is_sub_customer = ''.join(is_sub_customer)

#====================================================================
# COUNTRY
#====================================================================
country = []

for record in country_list.COUNTRIES_LIST_CHOICES:
    country.append("<li>{} - {}</li>".format(record[0], record[1]))

country = ''.join(country)

#====================================================================
# BILLING/INVOICE TERMS
#====================================================================
billing_terms = []

for record in payment_constants.PAYMENT_DAYS:
    billing_terms.append("<li>{} - {}</li>".format(record[0], record[1]))

billing_terms = ''.join(billing_terms)

#====================================================================
# PREFERRED DELIVERY TERMS
#====================================================================
preferred_delivery = []

for record in payment_constants.PREFERRED_DELIVERY:
    preferred_delivery.append("<li>{} - {}</li>".format(record[0], record[1]))

preferred_delivery = ''.join(preferred_delivery)

#====================================================================
# PREFERRED CURRENCY
#====================================================================
preferred_currency = []

for record in currency_list.CURRENCY_CHOICES:
    preferred_currency.append("<li>{} - {}</li>".format(record[0], record[1]))

preferred_currency = ''.join(preferred_currency)

#====================================================================
# ORGANIZATION TYPE
#====================================================================
organisation_type = []

for record in user_constants.ORGANIZATION_TYPE:
    organisation_type.append("<li>{} - {}</li>".format(record[0], record[1]))

organisation_type = ''.join(organisation_type)

#====================================================================
# GST REGISTERATION TYPE
#====================================================================
gst_reg_type = []

for record in user_constants.GST_REG_TYPE:
    gst_reg_type.append("<li>{} - {}</li>".format(record[0], record[1]))

gst_reg_type = ''.join(gst_reg_type)




#====================================================================
# CSV IMPORT DICTIONARY
#====================================================================

CSV_IMPORT_DICT = {
    "Contact Basic Details" : {
        "is_parent_record" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "<p>This states that the record is the master record for each contact.</p>",
        },
        "app_id" :{
            "value" : "Example : App-xyz",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : """
                <p>Application Id of the contact if provide. This will always update the 
                contact record if found in your contacts list.</p> 
                <p>If app_id is incorrect then the record will be skipped 
                along with its child records containing address, accounts, tax details,etc.</p>
            """,
        },
        "customer_type" :{
            "value" : "<ul>"+customer_type+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "Contact Type",
        },	
        "salutation" :{
            "value" : "<ul>"+salutation+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "YES",
            "description" : "",
        },
        "contact_name" :{
            "value" : "Example : xxx",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "Best if unique value is used.",
        },	
        "display_name" :{
            "value" : "Example : yyy",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "<p>This will be displayed on the Invoice, if blank then contact name will be used</p>",
        },	
        "use_app_user_details" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : """
                <p>This will map the user to your contacts</p>.
                <p>To add existing user to your contact list, set value to TRUE, else it will be set as a normal contact</br>
                If set TRUE and if you do not provide address, accounts, tax details then they will be used from the user's profile</p>
            """,
        },	
        "is_sub_customer" :{
            "value" : "<ul>"+is_sub_customer+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "",
        },
        "organisation_type" :{
            "value" : "<ul>"+organisation_type+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "Specify the type of Organization",
        },	
        "organisation_name" :{
            "value" : "Example : Ford Inc.",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Name of the organisation.",
        },	
        "is_msme_reg" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "Is MSME Registered",
        },	
        "email" :{
            "value" : "Example : james@gnail.com",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "Email Address for notifications and alerts",
        },	
        "phone" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "Landline/Mobile",
        },	
        "website" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Website Link",
        },	
        "facebook" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Facebook Account Link",
        },	
        "twitter" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Twitter Account Link",
        },	
    },
    "Address Details" : {	
        "is_contact_address" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : """ 
                <p>If TRUE, the record or row containing address details will be inserted</p>
                <p>Else, the details will be skipped</p>
            """,
        },	
        "contact_person" :{
            "value" : "Example : Richard Smith",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Name of the person to contact on the address",
        },	
        "flat_door_no" :{
            "value" : "Example : Oscar Villa",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Flat/Office/Shop",
        },	
        "street" :{
            "value" : "Example : MG Road",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Street/Locality",
        },	
        "city" :{
            "value" : "Example : Mumbai",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "City/Village",
        },	
        "pincode" :{
            "value" : "Example : 100001",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Pin/Zip Code",
        },	
        "state" :{
            "value" : "Example : Maharastra",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "State/Province",
        },
        "country" :{
            "value" : "<ul>"+country+"</ul>",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "<p>Use abbreviation.</p><p>Optional if no address details are provided</p>",
        },	
        "is_billing_address" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "<p>Sets the Address as Billing Address of the contact</p>",
        },	
        "is_shipping_address" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : "<p>Sets the Address as Shipping Address of the contact</p>",
        },
    },
    "Account Details" : {	
        "is_contact_account_details" :{
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : """ 
                <p>If TRUE, the record or row containing account details will be inserted</p>
                <p>Else, the details will be skipped</p>
            """,
        },	
        "account_holder_name" :{
            "value" : "Example : XXXX",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Name of the account holder",
        },	
        "account_number" :{
            "value" : "Example : 1111111111",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Account Numeber",
        },	
        "ifsc_code" :{
            "value" : "Example : IFSC00001",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Bank IFSC Code",
        },	
        "bank_name" :{
            "value" : "Example : ICICI",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Name of the bank",
        },	
        "branch_name" :{
            "value" : "Example : Mumbai",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Bank Branch Name",
        },	
    },
    "Tax Details" : {
        "is_contact_tax_details" : {
            "value" : "TRUE/FALSE",
            "datatype" : "TEXT",
            "optional" : "NO",
            "description" : """<p>If TRUE, then tax details will be inserted</p>
                <p>Else, the details will be skipped</p>""",
        },
        "pan" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "PAN Number",
        },
        "gstin" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "GSTIN Number",
        },	
        "gst_reg_type" :{
            "value" : "<ul>"+gst_reg_type+"</ul>",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "GST Registeration Number",
        },	
        "business_reg_no" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Business Registeration Number",
        },	
        "tax_reg_no" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Tax Registeration Number",
        },	
        "cst_reg_no" :{
            "value" : "",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "CGST Registeration Number",
        },	
        "tds" :{
            "value" : "Example : 10.2",
            "datatype" : "INTEGER/DECIMAL",
            "optional" : "YES",
            "description" : "TDS Percent",
        },
        "opening_balance" :{
            "value" : "Example : 10000.50",
            "datatype" : "INTEGER/DECIMAL",
            "optional" : "YES",
            "description" : "Opening Balance",
        },
        "as_of" :{
            "value" : "2019-12-23",
            "datatype" : "DATE",
            "optional" : "YES",
            "description" : "Opening Balance Date",
        },
        "preferred_currency" :{
            "value" : "<ul>"+preferred_currency+"</ul>",
            "datatype" : "TEXT",
            "optional" : "YES",
            "description" : "Preferred currency for pay and collect.<p>Use abbreviation.</p>",
        },	
        "preferred_delivery" :{
            "value" : "<ul>"+preferred_delivery+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "Delivery Terms and preferrence",
        },	
        "invoice_terms" :{
            "value" : "<ul>"+billing_terms+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "Terms for Invoice",
        },	
        "billing_terms" :{
            "value" : "<ul>"+billing_terms+"</ul>",
            "datatype" : "INTEGER",
            "optional" : "NO",
            "description" : "Terms for Billing",
        },
    }
    
}
