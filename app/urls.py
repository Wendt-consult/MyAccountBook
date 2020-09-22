from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app.views import dashboard, contacts, base, invoice, collections, \
    products, inventory, common_views, creditnotes, accounts_ledger, system_settings, \
    profile, purchase_order, expense, reports, purchasentry, journal_entry,scheduler, \
    payment_made,debit_note



# Authorization
urlpatterns = [
    path('', dashboard.index, name = 'home'),
    path('login/', auth_views.LoginView.as_view(template_name = 'app/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/registration/logout.html'), name = 'logout'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('unauthorized/', login_required(base.UnAuthorized.as_view()), name = 'unauthorized'),
    path('signup/', base.signup, name='signup'),
]

# System - Only On if User is Admin
urlpatterns += [
    path('system/config/', never_cache(login_required(system_settings.SettingsView.as_view())), name = 'settings_view'),
    path('system/config/db_operations/', never_cache(login_required(system_settings.DatabaseOperations.as_view())), name = 'settings_load_initial_data'),
    path('system/config/load_initial_data/', never_cache(login_required(system_settings.load_initial_data)), name = 'load_initial_data'),
]

# Dashboard
urlpatterns += [
    path('dashboard/', never_cache(login_required(dashboard.Dashboard.as_view())), name = 'dashboard'),
]

# Contacts
urlpatterns += [
    path('contacts/<int:ins>/', never_cache(login_required(contacts.ContactsView.as_view())), name = 'contacts'),
    path('contacts/add/', never_cache(login_required(contacts.add_contacts)), name = 'add-contacts'),
    path('contacts/add_address/', never_cache(login_required(contacts.add_address_details_form)), name = 'add_address_details_form'),
    path('contacts/add_accounts/', never_cache(login_required(contacts.add_accounts_details_form)), name = 'add_accounts_details_form'),
    path('contacts/edit/<int:ins>/', never_cache(login_required(contacts.edit_contact)), name = 'edit-contact'),
    
    path('contacts/check_appid/', never_cache(login_required(contacts.check_app_id)), name='check-appid'),
    path('contacts/user_exists_in_list/', never_cache(login_required(contacts.user_exists_in_list)), name='check-appid-user-exist'),
    path('contacts/upload/<str:a>/', never_cache(login_required(contacts.ContactsFileUploadView.as_view())), name='contacts-upload'),
    path('contacts/status_change/<slug:slug>/<int:ins>/', never_cache(login_required(contacts.status_change)), name='contact-status-change'),
    path('contacts/delete/<int:ins>/', never_cache(login_required(contacts.delete_contact)), name='contact-delete'),

    path('contacts/edit_contact_details_form/', never_cache(login_required(contacts.edit_contact_details_form)), name = 'edit_contact_details_form'),
    path('contacts/edit_tax_details_form/', never_cache(login_required(contacts.edit_tax_details_form)), name = 'edit_tax_details_form'),
    path('contacts/edit_other_details_form/', never_cache(login_required(contacts.edit_other_details_form)), name = 'edit_other_details_form'),
    path('contacts/edit_address_details_form/', never_cache(login_required(contacts.edit_address_details_form)), name = 'edit_address_details_form'),
    path('contacts/edit_accounts_details_form/', never_cache(login_required(contacts.edit_accounts_details_form)), name = 'edit_accounts_details_form'),
    path('contacts/edit_social_details_form/', never_cache(login_required(contacts.edit_social_details_form)), name = 'edit_social_details_form'),

    path('contacts/delete_address/<int:ins>/', never_cache(login_required(contacts.delete_contact_address)), name = 'delete_contact_address'),
    path('contacts/delete_accounts/<int:ins>/', never_cache(login_required(contacts.delete_accounts_details)), name = 'delete_accounts_details'),

]

# Invoice
urlpatterns += [
    # codded by akhil
    # path('invoice/', never_cache(login_required(invoice.Invoice.as_view())), name = 'invoice'),
    # path('invoice/invoice_designer/', never_cache(login_required(invoice.InvoiceDesigner.as_view())), name = 'invoice-designer'),
    # path('invoice/invoice_designer/manage/', never_cache(login_required(invoice.manage_invoice_designs)), name = 'manage-invoice-designs'),
    # path('invoice/create_invoice/', never_cache(login_required(invoice.CreateInvoice.as_view())), name = 'create-invoice'),
    # path('invoice/view_invoice/<int:ins>/', never_cache(login_required(invoice.ViewInvoice.as_view())), name = 'view-invoice'),
    # path('invoice/create_invoice/contacts/<int:ins>/', never_cache(login_required(invoice.CreateContactInvoice.as_view())), name = 'create-contact-invoice'),
    # path('invoice/create_invoice/collections/<int:ins>/', never_cache(login_required(invoice.CreateCollectionInvoice.as_view())), name = 'create-collection-invoice'),

    # codded by roshan
    path('invoice/', never_cache(login_required(invoice.Invoice.as_view())), name = 'invoice'),
    path('invoice/add/<slug:slug>/', never_cache(login_required(invoice.add_invoice)), name = 'add_invoice'),
    path('invoice/org_address_state/', never_cache(login_required(invoice.org_address_state)), name = 'org_address_state'),
    path('invoice/save_invoice/', never_cache(login_required(invoice.save_invoice)), name = 'save_invoice'),
    path('invoice/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(invoice.unique_invoice_number)), name = 'unique_invoice_number'),
    path('invoice/edit_invoice/<int:ins>/', never_cache(login_required(invoice.EditInvoice.as_view())), name = 'edit_invoice'),
    path('send_invoice/<int:ins>/', never_cache(login_required(invoice.send_invoice)), name = 'send_invoice'),
    path('invoice/print/<int:ins>/', never_cache(login_required(invoice.print_invoice)), name = 'print_invoice'),
    path('invoice/delete/<int:ins>/', never_cache(login_required(invoice.delete_invoice)), name = 'delete_invoice'),
    path('invoice/search_engin/', never_cache(login_required(invoice.search_engin_product)), name = 'search_engin_product'),
    path('invoice/check_invoice_terms/<int:ins>/', never_cache(login_required(invoice.check_invoice_terms)), name = 'check_invoice_terms'),
    path('invoice/clone_invoice/<int:ins>/', never_cache(login_required(invoice.CloneInvoice.as_view())), name = 'clone_invoice'),
    path('invoice/paid/<int:ins>/', never_cache(login_required(invoice.paid_invoice)), name = 'paid_invoice'),
    path('invoice/customer_gst/<int:ins>/', never_cache(login_required(invoice.customer_gst)), name = 'customer_gst'),
    path('invoice/delete/<int:ins>/', never_cache(login_required(invoice.delete_invoice)), name = 'delete_invoice'),
]

# urlpatterns +=[
#     path('invoice/get_pdf/<int:ins>/', never_cache(login_required(invoice.get_pdf)), name = 'get_pdf'),
    
# ] 

# Collections
urlpatterns += [
    path('collections/', never_cache(login_required(collections.view_collections)), name = 'collections'),
    path('collections/contact/<int:ins>/', never_cache(login_required(collections.view_contact_collections)), name = 'contact-collections'),
    path('collections/add_collections/', never_cache(login_required(collections.AddCollections.as_view())), name = 'add-collections'),
    path('collections/add_collections/partial/<int:ins>/', never_cache(login_required(collections.AddPartialCollection.as_view())), name = 'add-partial-collections'),
    path('collections/edit/<int:ins>/', never_cache(login_required(collections.Edit_Collection.as_view())), name = 'edit_collections'),
    path('collections/edit_partial/<int:ins>/<int:obj>/', never_cache(login_required(collections.Edit_PartialCollection.as_view())), name = 'edit_partial_collection'),
]

# Products
urlpatterns += [
    path('products/<int:ins>/', never_cache(login_required(products.view_products)), name = 'view_products'),
    path('products/add/', never_cache(login_required(products.AddProducts.as_view())), name = 'add_products'),
    path('products/edit/<int:ins>/', never_cache(login_required(products.EditProducts.as_view())), name = 'edit_product'),
    path('products/delete/<int:ins>/', never_cache(login_required(products.delete_product)), name='product-delete'),
    path('products/status_change/<slug:slug>/<int:ins>/', never_cache(login_required(products.status_change)), name='product-status-change'),
    # BUNDLE ADDED BY ROSHAN
    path('prducts/bundle/',never_cache(login_required(products.bundle)),name='bundle'),    
    path('products/clone/<int:ins>/', never_cache(login_required(products.CloneProduct.as_view())), name='product-clone'),
]

# Inventory
urlpatterns += [
    path('inventory/', never_cache(login_required(inventory.view_inventory)), name = 'view_inventory'),
    path('inventory/add/', never_cache(login_required(inventory.AddInventory.as_view())), name = 'add_inventory'),
    path('inventory/products/<int:ins>/', never_cache(login_required(inventory.InventoryProducts.as_view())), name = 'view_inventory_products'),
    path('inventory/products/delete/<int:ins>/', never_cache(login_required(inventory.delete_inventory_product)), name = 'delete_inventory_product'),
    path('inventory/get_edit_inventory_product_form/', never_cache(login_required(inventory.get_edit_inventory_product_form)), name = 'get_edit_inventory_product_form'),
    path('inventory/edit_inventory_product/', never_cache(login_required(inventory.edit_inventory_product)), name = 'edit_inventory_product'),
]

# AJAX or Direct
urlpatterns += [
    path('fetch_contact_addresses/<int:ins>/', never_cache(login_required(common_views.fetch_contact_addresses)), name='fetch_contact_addresses'),
    path('fetch_product_details/<int:ins>/', never_cache(login_required(common_views.fetch_product_details)), name='fetch_product_details'),
    path('ajax_add_product/', never_cache(login_required(products.ajax_add_product)), name='ajax_add_product'),
    path('fetch_products_dropdown/', never_cache(login_required(common_views.fetch_products_dropdown)), name='fetch_products_dropdown'),
    path('add_contact_or_employee/', never_cache(login_required(common_views.add_contact_or_employee)), name='add_contact_or_employee'),
    path('get_contacts_dropdown/', never_cache(login_required(common_views.get_contacts_dropdown)), name='get_contacts_dropdown'),
    path('add_edit_address/<int:ins>/', never_cache(login_required(common_views.add_edit_address)), name='add_edit_address'),
    path('add_edit_address/<int:ins>/<int:obj>/', never_cache(login_required(common_views.add_edit_address)), name='add_edit_address'),
    path('delete_bundle_product/<int:ins>/<int:obj>/',never_cache(login_required(products.delete_bundle_product)),name='delete-bundle-product'),
    path('edit_bundle_product_form/',never_cache(login_required(products.edit_bundle_product_form)),name='edit_bundle_product_form'),
    path('add_bundle_product_form/',never_cache(login_required(products.add_bundle_product_form)),name='add_bundle_product_form'),
    path('delete_product_image/<int:pid>/<int:img_id>/',never_cache(login_required(products.delete_product_image)),name='delete_product_image'),
    path('check_existing_product/',never_cache(login_required(products.check_existing_product)),name='check_existing_product'),
    path('get_predefined_groups/', never_cache(login_required(accounts_ledger.get_predefined_groups)), name = 'get_predefined_groups'),
    path('add_ledger_group/', never_cache(login_required(accounts_ledger.add_ledger_group)), name = 'add_ledger_group'),
    path('add_ledger_group/<slug:ins>/<str:strs>/', never_cache(login_required(accounts_ledger.acc_ledger_info)), name = 'acc_ledger_info'),
    path('add_ledger_group/unique/<slug:ins>/<str:strs>', never_cache(login_required(accounts_ledger.unique)), name = 'unique'),
    path('add_ledger_group/unique2/<slug:ins>/<str:strs>/', never_cache(login_required(accounts_ledger.unique2)), name = 'unique2'),
    path('send_creditnote/<int:ins>/', never_cache(login_required(creditnotes.send_creditnote)), name = 'send_creditnote'),
    path('check_gst_existing/', never_cache(login_required(profile.check_gst_existing)), name = 'check_gst_existing'),
    path('get_gst/', never_cache(login_required(profile.get_gst)), name = 'get_gst'),
    path('get_state_gst/', never_cache(login_required(profile.get_state_gst)), name = 'get_state_gst'), 
    path('org/gst_state_code/', never_cache(login_required(profile.gst_state_code)), name = 'gst_state_code'), 
    # CUSTOMIZE VIEW  
    path('customize_view/<int:ins>/', never_cache(login_required(common_views.customize_view_list)), name = 'customize_view_list'),  
    path('gst_number/', never_cache(login_required(common_views.get_gst_number)), name = 'get_gst_number'),
]

# Credit Notes
urlpatterns += [
    path('creditnotes/', never_cache(login_required(creditnotes.CreditView.as_view())), name = 'credit_note'),
    path('creditnotes/add/<slug:slug>', never_cache(login_required(creditnotes.add_creditnote)), name = 'add_credit_note'),
    path('creditnote/contact/<slug:slug>', never_cache(login_required(creditnotes.fetch_contact)), name = 'creditnote_contact'),
    path('creditnote/product/<slug:slug>', never_cache(login_required(creditnotes.fetch_product)), name = 'creditnote_product'),
    path('creditnote/save/', never_cache(login_required(creditnotes.save_credit_note)), name = 'save_credit_note'),
    path('creditnote/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(creditnotes.unique_credit_number)), name = 'unique_creditnote_number'),
    path('creditnote/product_fetch/', never_cache(login_required(creditnotes.last_product_fetch)), name = 'last_product_fetch'),
    path('creditnote/contact_fetch/', never_cache(login_required(creditnotes.last_contact_fetch)), name = 'last_contact_fetch'),
    path('creditnote/edit/<int:ins>/', never_cache(login_required(creditnotes.EditCreditnote.as_view())), name = 'edit_credit_note'),
    path('creditnote/clone/<int:ins>/', never_cache(login_required(creditnotes.CloneCreditnote.as_view())), name = 'clone_credit_note'),
    path('creditnote/state_compare/', never_cache(login_required(creditnotes.state_compare)), name = 'creditnote_state_compare'),
    path('creditnote/print/<int:ins>/', never_cache(login_required(creditnotes.print_credit_note)), name = 'print_credit_note'),
    path('creditnote/delete/<int:ins>/', never_cache(login_required(creditnotes.delete_credit_note)), name = 'delete_credit_note'),
    
]

# Accounts Ledger
urlpatterns += [
    path('ledger/add/', never_cache(login_required(accounts_ledger.AccLedger.as_view())), name = 'add_accounts'),
]


#
# Profile Manager
#
urlpatterns += [
    path('profile/', never_cache(login_required(profile.Profile.as_view())), name = 'profile'),
    path('profile/add_organisation_contact/', never_cache(login_required(profile.add_organisation_contact)), name = 'add_organisation_contact'),
    path('profile/add_organisation_addres/', never_cache(login_required(profile.add_organisation_addres)), name = 'add_organisation_addres'),
    path('profile/edit_address_details_form/<int:ins>/', never_cache(login_required(profile.edit_org_address_details_form)), name = 'edit_org_address_details_form'),
    path('profile/edit_account_details_form/<int:ins>/', never_cache(login_required(profile.edit_org_account_details_form)), name = 'edit_org_account_details_form'),
    path('profile/delete_account/<int:ins>/', never_cache(login_required(profile.delete_org_account)), name = 'delete_org_account'),
    path('profile/blank/', never_cache(login_required(profile.blank)), name = 'blank'),
    path('profile/gst_settings/', never_cache(login_required(profile.GSTSettingsView.as_view())), name = 'gst_settings'),
    path('profile/delete_gst_settings/<int:ins>/', never_cache(login_required(profile.delete_gst_settings)), name = 'delete_gst_settings'),
    path('profile/delete_composite_gst_settings/<int:ins>/', never_cache(login_required(profile.delete_composite_gst_settings)), name = 'delete_composite_gst_settings'),
    path('profile/edit_gst_settings/', never_cache(login_required(profile.edit_gst_settings)), name = 'edit_gst_settings'),
    path('profile/edit_composite_gst_settings/', never_cache(login_required(profile.edit_composite_gst_settings)), name = 'edit_composite_gst_settings'),
    path('profile/gst_configuration/', never_cache(login_required(profile.GSTConfigurationView.as_view())), name = 'gst_configuration'),
    path('profile/gst_composite_setting/', never_cache(login_required(profile.gst_composite_setting)), name = 'gst_composite_setting'),
    path('profile/org_address_active/<int:ins>/', never_cache(login_required(profile.org_address_active)), name = 'org_address_active'),
    path('profile/org_address_inactive/<int:ins>/', never_cache(login_required(profile.org_address_inactive)), name = 'org_address_inactive'),
    path('profile/org_address_check/', never_cache(login_required(profile.org_address_check)), name = 'org_address_check'),
    path('profile/org_address_inactive_check/', never_cache(login_required(profile.org_address_inactive_check)), name = 'org_address_inactive_check'),
    path('profile/add_organisation_bank_account/', never_cache(login_required(profile.add_organisation_bank_account)), name = 'add_organisation_bank_account'),
    path('profile/edit_organisation_bank_account/<int:ins>/', never_cache(login_required(profile.edit_organisation_bank_account)), name = 'edit_organisation_bank_account'),
    path('profile/delete_org_bank_account/<int:ins>/', never_cache(login_required(profile.delete_org_bank_account)), name = 'delete_org_bank_account'),
]

# Purchase Order
urlpatterns += [
    path('view_purchase_order/', never_cache(login_required(purchase_order.PurchaseOrderView.as_view())), name = 'purchase_order'),
    path('purchase_order/add_purchase_order/<slug:slug>/', never_cache(login_required(purchase_order.add_purchase_order)), name = 'add_purchase_order'),
    path('purchase/product/<slug:slug>', never_cache(login_required(purchase_order.fetch_purchase_product)), name = 'purchase_order_product'),
    path('purchase_order/address/<slug:slug>/', never_cache(login_required(purchase_order.org_contact_address)), name = 'org_contact_address'),
    path('purchase_order/last_address/', never_cache(login_required(purchase_order.last_address_fetch)), name = 'last_address_fetch'),
    path('purchase_order/account_group_fetch/', never_cache(login_required(purchase_order.last_acc_group_fetch)), name = 'last_acc_group_fetch'),
    path('purchase_order/save_order/', never_cache(login_required(purchase_order.save_purchase_order)), name = 'save_purchase_order'),
    path('purchase_order/edit_order/<int:ins>/', never_cache(login_required(purchase_order.EditPurchaseOrder.as_view())), name = 'edit_purchase_order'),
    path('purchase_order/clone_order/<int:ins>/', never_cache(login_required(purchase_order.ClonePurchaseOrder.as_view())), name = 'clone_purchase_order'),
    path('purchase_order/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(purchase_order.unique_purchase_number)), name = 'unique_purchase_number'),
    path('purchase_order/vendor_state/<int:ins>/', never_cache(login_required(purchase_order.vendor_state)), name = 'vendor_state'),
    path('purchase_order/print/<int:ins>/', never_cache(login_required(purchase_order.print_purchase_order)), name = 'print_purchase_order'),
    path('purchase_order/delete/<int:ins>/', never_cache(login_required(purchase_order.delete_purchase_order)), name = 'delete_purchase_order'),
    path('purchase_order/vendor_details/<int:ins>/', never_cache(login_required(purchase_order.vendor_details)), name = 'vendor_details'),
    path('purchase_order/void/<int:ins>/', never_cache(login_required(purchase_order.void_purchase)), name = 'void_purchase'),
    path('purchase_order/vendor_gst_save/', never_cache(login_required(purchase_order.vendor_gst_save)), name = 'vendor_gst_save'),
]

# Expense
urlpatterns += [
    path('expense/', expense.ExpenseView.as_view(), name='view_expenses'),
	path('add-expense/', expense.AddExpense.as_view(), name='add_expense'),
	path('edit-expense/<int:pk>/', expense.AddExpense.as_view(), name='edit_expense'),
	path('clone-expense/<int:pk>/<str:clone>/', expense.AddExpense.as_view(), name='clone_expense'),
	path('delete-expense/<int:pk>/', expense.DeleteExpense.as_view(), name='delete_expense'),
	path('pdf/<int:pk>/', expense.generate_pdf_view, name='generate_pdf'),
    path('expense/vendor_state/<int:ins>/', never_cache(login_required(expense.expenss_vendor_state)), name = 'expense_vendor_state'),

	#Ajax Request
	path('add-payment-method', expense.add_payment_method_view, name='add_payment_method'),
	path('check-expense-number/', expense.check_expense_number_view, name='check_expense_number'),
	path('product-details/', expense.get_product_details_view, name='get_product_details'),
]

# Reports
urlpatterns += [
    path('reports/gst_ledger/', reports.GSTLedgerReportsView.as_view(), name='gst_ledger_reports'),
    path('reports/get_reports_pdf/', reports.get_reports_pdf, name='get_reports_pdf'),
    path('reports/email/', reports.send_email, name='send_reports_email'),
]

# Purchase Entry
urlpatterns += [
    path('view_purchase_entry/', never_cache(login_required(purchasentry.PurchaseEntry.as_view())), name = 'Purchase_entry'),
    path('purchase_entry/add_purchase_entry/<int:ins>/<slug:slug>/', never_cache(login_required(purchasentry.add_purchase_entry)), name = 'add_purchase_entry'),
    path('purchase_entry/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(purchasentry.unique_entry_number)), name = 'unique_entry_number'),
    path('purchase_entry/save_purchase_entry/', never_cache(login_required(purchasentry.save_purchase_entry)), name = 'save_purchase_entry'),
    path('purchase_entry/delete/<int:ins>/', never_cache(login_required(purchasentry.delete_purchase_entry)), name = 'delete_purchase_entry'),
    path('purchase_entry/edit_purchase_entry/<int:ins>/', never_cache(login_required(purchasentry.EditPurchaseEntry.as_view())), name = 'edit_purchase_entry'),
]

# Journal_entry
urlpatterns += [
    path('journalentry/', never_cache(login_required(journal_entry.view_journalentry)), name = 'view_journalentry'),
    path('journalentry/add_journalentry/<int:ins>/', never_cache(login_required(journal_entry.JournalEntry)), name = 'add_journalentry'),
    path('journalentry/save_journalentry/', never_cache(login_required(journal_entry.SaveJournalEntry)), name = 'SaveJournalEntry'),
    path('journalentry/edit_journalentry/<int:ins>/', never_cache(login_required(journal_entry.EditJournal.as_view())), name = 'edit_journalentry'),
    path('journalentry/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(journal_entry.unique_journal_number)), name = 'unique_journal_number'),
    path('journalentry/delete/<int:ins>/', never_cache(login_required(journal_entry.journalentry_delete)), name = 'journalentry_delete'),
    path('journalentry/print/<int:ins>/', never_cache(login_required(journal_entry.print_jounal_entry)), name = 'print_jounal_entry'),
]
#

#
# Payment Made
#
urlpatterns += [
    path('paymentmade/', never_cache(login_required(payment_made.PaymentMade.as_view())), name = 'payment_made'),
    path('paymentmade/make_payment/<slug:slug>/', never_cache(login_required(payment_made.makePayment)), name = 'make_payment'),
    path('paymentmade/add_make_payment/', never_cache(login_required(payment_made.addMakePayment.as_view())), name = 'add_make_payment'),
    path('paymentmade/unique_number/<int:ins>/<slug:number>/', never_cache(login_required(payment_made.unique_payment_number)), name = 'unique_payment_number'),
]

#
# Debit Note
#
urlpatterns += [
    path('debitnote/', never_cache(login_required(debit_note.DebitNoteView.as_view())), name = 'view_debit_note'),
    path('debitnote/add_debit_note/', never_cache(login_required(debit_note.add_debit_note)), name = 'add_debit_note'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()



