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
    profile, purchase_order, expense



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
    path('contacts/', never_cache(login_required(contacts.ContactsView.as_view())), name = 'contacts'),
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
    path('invoice/', never_cache(login_required(invoice.Invoice.as_view())), name = 'invoice'),
    path('invoice/invoice_designer/', never_cache(login_required(invoice.InvoiceDesigner.as_view())), name = 'invoice-designer'),
    path('invoice/invoice_designer/manage/', never_cache(login_required(invoice.manage_invoice_designs)), name = 'manage-invoice-designs'),
    path('invoice/create_invoice/', never_cache(login_required(invoice.CreateInvoice.as_view())), name = 'create-invoice'),
    path('invoice/view_invoice/<int:ins>/', never_cache(login_required(invoice.ViewInvoice.as_view())), name = 'view-invoice'),
    path('invoice/create_invoice/contacts/<int:ins>/', never_cache(login_required(invoice.CreateContactInvoice.as_view())), name = 'create-contact-invoice'),
    path('invoice/create_invoice/collections/<int:ins>/', never_cache(login_required(invoice.CreateCollectionInvoice.as_view())), name = 'create-collection-invoice'),
]

urlpatterns +=[
    path('invoice/get_pdf/<int:ins>/', never_cache(login_required(invoice.get_pdf)), name = 'get_pdf'),
    
] 

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
    path('products/', never_cache(login_required(products.view_products)), name = 'view_products'),
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
    # CUSTOMIZE VIEW  
    path('customize_view/<int:ins>/', never_cache(login_required(common_views.customize_view_list)), name = 'customize_view_list'),  
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
]

# Expense
urlpatterns += [
    path('expense/', expense.ExpenseView.as_view(), name='view_expenses'),
	path('add-expense/', expense.AddExpense.as_view(), name='add_expense'),
	path('edit-expense/<int:pk>/', expense.AddExpense.as_view(), name='edit_expense'),
	path('clone-expense/<int:pk>/<str:clone>/', expense.AddExpense.as_view(), name='clone_expense'),
	path('delete-expense/<int:pk>/', expense.DeleteExpense.as_view(), name='delete_expense'),
	path('pdf/<int:pk>/', expense.generate_pdf_view, name='generate_pdf'),

	#Ajax Request
	path('add-payment-method', expense.add_payment_method_view, name='add_payment_method'),
	path('check-expense-number/', expense.check_expense_number_view, name='check_expense_number'),
	path('product-details/', expense.get_product_details_view, name='get_product_details'),
]

#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()



