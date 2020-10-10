from django.contrib import admin
from app.models.creditnote_model import *
from app.models.accounts_model import *
from app.models.products_model import *
from app.models.contacts_model import *
from app.models.users_model import *
from app.models.purchase_model import *
from app.models.customize_model import *
from app.models.invoice_model import *
from app.models.expense_model import *
from app.models.purchasentry_model import *
from app.models.payment_made_model import *
from app.models.journalentry_model import *
from app.models.debit_note_model import *
from app.models.quotation_model import *
from app.models import *

#
#
@admin.register(users_model.Profile)
class Profile(admin.ModelAdmin):
    model = users_model.Profile

#
#
@admin.register(users_model.User_Account_Details)
class User_Account_Details(admin.ModelAdmin):
    model = users_model.User_Account_Details 

#
#
@admin.register(users_model.User_Address_Details)
class User_Address_Details(admin.ModelAdmin):
    model = users_model.User_Address_Details 

@admin.register(users_model.User_Tax_Details)
class User_Tax_Details(admin.ModelAdmin):
    model = users_model.User_Tax_Details 
#
#
@admin.register(accounts_model.MajorHeads)
class MajorHeads_Details(admin.ModelAdmin):
    model = accounts_model.MajorHeads
    
    list_display = ('major_head_name', 'is_active',)

#
#  
@admin.register(accounts_model.AccGroups)
class AccGroups_Details(admin.ModelAdmin):
    model = accounts_model.AccGroups
    
    list_display = ( 'is_standard', 'group_name', 'group_info', 'major_head', 'user', 'is_active',)
    
    
@admin.register(CreditNode)
class CreditNode(admin.ModelAdmin):
    model = CreditNode    

@admin.register(AccLedger)
class AccLedger(admin.ModelAdmin):
    model = AccLedger  
    

@admin.register(creditnote_Items)
class creditnote_Items(admin.ModelAdmin):
    model = creditnote_Items  

@admin.register(ProductsModel)
class ProductsModel(admin.ModelAdmin):
    model = ProductsModel 

@admin.register(BundleProducts)
class BundleProducts(admin.ModelAdmin):
    model = BundleProducts

@admin.register(Organisations)
class Organisations(admin.ModelAdmin):
    model = Organisations 

@admin.register(Organisation_Contact)
class Organisation_Contact(admin.ModelAdmin):
    model = Organisation_Contact

@admin.register(Contacts)
class Contacts(admin.ModelAdmin):
    model = Contacts

@admin.register(ProductPhotos)
class ProductPhotos(admin.ModelAdmin):
    model = ProductPhotos   

@admin.register(PurchaseOrder)
class PurchaseOrder(admin.ModelAdmin):
    model = PurchaseOrder 

@admin.register(Purchase_Items)
class Purchase_Items(admin.ModelAdmin):
    model = Purchase_Items

@admin.register(CustomizeModuleName)
class CustomizeModuleName(admin.ModelAdmin):
    model = CustomizeModuleName

@admin.register(CustomizeContactView)
class CustomizeContactView(admin.ModelAdmin):
    model = CustomizeContactView

@admin.register(CustomizeProductView)
class CustomizeProductView(admin.ModelAdmin):
    model = CustomizeProductView

@admin.register(CustomizeCreditView)
class CustomizeCreditView(admin.ModelAdmin):
    model = CustomizeCreditView

@admin.register(CustomizePurchaseView)
class CustomizePurchaseView(admin.ModelAdmin):
    model = CustomizePurchaseView

@admin.register(CustomizeExpenseView)
class CustomizeExpenseView(admin.ModelAdmin):
    model = CustomizeExpenseView

@admin.register(CustomizeInvoiceView)
class CustomizeInvoiceView(admin.ModelAdmin):
    model = CustomizeInvoiceView

@admin.register(InvoiceModel)
class InvoiceModel(admin.ModelAdmin):
    model = InvoiceModel

@admin.register(Invoice_Line_Items)
class Invoice_Line_Items(admin.ModelAdmin):
    model = Invoice_Line_Items

@admin.register(Expense)
class Expense(admin.ModelAdmin):
    model = Expense

@admin.register(PurchaseEntry)
class PurchaseEntry(admin.ModelAdmin):
    model = PurchaseEntry

@admin.register(PurchaseEntryItems)
class PurchaseEntryItems(admin.ModelAdmin):
    model = PurchaseEntryItems

@admin.register(JournalEntry)
class JournalEntry(admin.ModelAdmin):
    model = JournalEntry

@admin.register(PurchasePayment)
class PurchasePayment(admin.ModelAdmin):
    model = PurchasePayment

@admin.register(DebitNote)
class DebitNote(admin.ModelAdmin):
    model = DebitNote

@admin.register(DebitNoteItems)
class DebitNoteItems(admin.ModelAdmin):
    model = DebitNote

@admin.register(QuotationModel)
class QuotationModel(admin.ModelAdmin):
    model = QuotationModel

@admin.register(Quotation_Items)
class Quotation_Items(admin.ModelAdmin):
    model = Quotation_Items