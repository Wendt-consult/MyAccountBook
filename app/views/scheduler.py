from app.models import *
from datetime import datetime,date
import datetime
def test_fun():
    invoice = invoice_model.InvoiceModel.objects.filter(invoice_delete_status = 0)
    count = len(invoice)
    current_date = date.today()
    for i in range(0,count):
        # if statement for one time invoice
        if(invoice[i].invoice_type_new == 'on'):
            invoice_due_date = invoice[i].invoice_new_due_date
            if(invoice[i].invoice_status == 0):
                if(invoice_due_date < current_date):
                    delta = (current_date - invoice_due_date).days
                    invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(invoice_status = 1,inovice_over_due_count = delta)
            elif(invoice[i].invoice_status == 1):
                delta = (current_date - invoice_due_date).days
                invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(inovice_over_due_count = delta)
                # invoice for recurring type
        elif(invoice[i].invoice_type_recurring == 'on'):     
            invoice_recurr_date = invoice[i].invoice_date
            invoice_recurr_pay_temrs = invoice[i].invoice_recurring_pay
            check_date = None
            if(invoice_recurr_pay_temrs == 'On Due Date'):
                check_date = invoice_recurr_date
            elif(invoice_recurr_pay_temrs == '10 Days'):
                check_date = invoice_recurr_date + datetime.timedelta(days=10)
            elif(invoice_recurr_pay_temrs == '20 Days'):
                check_date = invoice_recurr_date + datetime.timedelta(days=20)
            elif(invoice_recurr_pay_temrs == '30 Days'):
                check_date = invoice_recurr_date + datetime.timedelta(days=30)
            elif(invoice_recurr_pay_temrs == '60 Days'):
                check_date = invoice_recurr_date + datetime.timedelta(days=60)
            elif(invoice_recurr_pay_temrs == '90 Days'):
                check_date = invoice_recurr_date + datetime.timedelta(days=90)

            if(invoice[i].invoice_status == 0):
                if(check_date < current_date):
                    delta = (current_date - check_date).days
                    invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(invoice_status = 1,inovice_over_due_count = delta)
            elif(invoice[i].invoice_status == 1):
                delta = (current_date - check_date).days
                invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(inovice_over_due_count = delta)

            # recurring invoice to create one new invoice
            frequency = invoice[i].invoice_recurring_frequency
            repeat = invoice[i].invoice_recurring_repeat
            count = invoice[i].invoice_recurring_count
            recurr_start_date = invoice[i].invoice_recurring_start_date
            recurr_advance = invoice[i].invoice_recurring_advance

            new_date = None
            new_invoice_date = None
            new_invoice_pay_terms = invoice_recurr_pay_temrs
            new_due_date = None
            new_count = None
            if(repeat != count):

                if(frequency == 'Weekly'):
                    if(count == 0):
                        new_invoice_date = recurr_start_date    
                        if(recurr_advance is not None):
                            new_date = recurr_start_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = recurr_start_date
                    else:
                        a = (7 * count)
                        new_invoice_date = recurr_start_date + datetime.timedelta(days=int(a))
                        if(recurr_advance != ''):
                            new_date = new_invoice_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = new_invoice_date
                    new_count = count + 1
                elif(frequency == 'Monthly'):
                    if(count == 0):
                        new_invoice_date = recurr_start_date
                        if(recurr_advance != ''):
                            new_date = recurr_start_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = recurr_start_date
                    else:
                        a = (31 * count)
                        new_invoice_date = recurr_start_date + datetime.timedelta(days=int(a))
                        if(recurr_advance != ''):
                            new_date = new_invoice_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = new_invoice_date
                    new_count = count + 1
                elif(frequency == 'Quarterly'):
                    if(count == 0):
                        new_invoice_date = recurr_start_date
                        if(recurr_advance != ''):
                            new_date = recurr_start_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = recurr_start_date
                    else:
                        a = (84 * count)
                        new_invoice_date = recurr_start_date + datetime.timedelta(days=int(a))
                        if(recurr_advance != ''):
                            new_date = new_invoice_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = new_invoice_date
                    new_count = count + 1
                elif(frequency == 'Half yearly'):
                    if(count == 0):
                        new_invoice_date = recurr_start_date
                        if(recurr_advance != ''):
                            new_date = recurr_start_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = recurr_start_date
                    else:
                        a = (180 * count)
                        new_invoice_date = recurr_start_date + datetime.timedelta(days=int(a))
                        if(recurr_advance != ''):
                            new_date = new_invoice_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = new_invoice_date
                    new_count = count + 1
                elif(frequency == 'Yearly'):
                    if(count == 0):
                        new_invoice_date = recurr_start_date
                        if(recurr_advance != ''):
                            new_date = recurr_start_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = recurr_start_date
                    else:
                        a = (180 * count)
                        new_invoice_date = recurr_start_date + datetime.timedelta(days=int(a))
                        if(recurr_advance != ''):
                            new_date = new_invoice_date - datetime.timedelta(days=int(recurr_advance))
                        else:
                            new_date = new_invoice_date
                    new_count = count + 1

                    
                if(invoice_recurr_pay_temrs == 'On Due Date'):
                    new_due_date = new_invoice_date
                elif(invoice_recurr_pay_temrs == '10 Days'):
                    new_due_date = new_invoice_date + datetime.timedelta(days=10)
                elif(invoice_recurr_pay_temrs == '20 Days'):
                    new_due_date = new_invoice_date + datetime.timedelta(days=20)
                elif(invoice_recurr_pay_temrs == '30 Days'):
                    new_due_date = new_invoice_date + datetime.timedelta(days=30)
                elif(invoice_recurr_pay_temrs == '60 Days'):
                    new_due_date = new_invoice_date + datetime.timedelta(days=60)
                elif(invoice_recurr_pay_temrs == '90 Days'):
                    new_due_date = new_invoice_date + datetime.timedelta(days=90)

                if(new_date <= current_date):
                    invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(invoice_recurring_count = new_count)

                    b = invoice_model.InvoiceModel.objects.filter(user = invoice[i].user).count()
                    data_count = 'IN-000'+str(int(b)+1)
                    invoice_newone = invoice_model.InvoiceModel(
                        user = invoice[i].user, 
                        invoice_customer = invoice[i].invoice_customer, 
                        email = invoice[i].email,
                        cc_email = invoice[i].cc_email, 
                        purchase_order_number = invoice[i].purchase_order_number,
                        invoice_number = data_count,
                        invoice_check = 'on',
                        save_type=2,
                        invoice_date = new_invoice_date,
                        invoice_type_new = 'on',
                        invoice_new_pay_terms = new_invoice_pay_terms,
                        invoice_recurring_count = new_count,
                        invoice_new_due_date = new_due_date,
                        invoice_type_recurring = 'off', 
                        invoice_salesperson = invoice[i].invoice_salesperson,
                        invoice_state_supply = invoice[i].invoice_state_supply,
                        terms_and_condition = invoice[i].terms_and_condition, 
                        Note = invoice[i].Note,
                        attachements=invoice[i].attachements,
                        sub_total = invoice[i].sub_total,
                        total_discount = invoice[i].total_discount,
                        total_amount = invoice[i].total_amount,
                        shipping_charges = invoice[i].shipping_charges,     
                        cgst = invoice[i].cgst,
                        sgst = invoice[i].sgst,
                        igst = invoice[i].igst,
                        invoice_org_gst_num = invoice[i].invoice_org_gst_num,
                        invoice_org_gst_type = invoice[i].invoice_org_gst_type,
                        invoice_org_gst_state = invoice[i].invoice_org_gst_state,
                    )
                    if(invoice[i].cgst != '' or invoice[i].sgst != ''):
                        invoice_newone.is_cs_gst = True
                    else:
                        invoice_newone.is_cs_gst = False
                    invoice_newone.save()

                    new_items = invoice_model.Invoice_Line_Items.objects.filter(invoice_item_list = invoice[i])
                    for j in range(0,len(new_items)):
                        a = new_items[j]
                        a.pk = None
                        a.invoice_item_list = None
                        a.invoice_item_list = invoice_newone
                        a.save()

    purchase_entry = purchase_entry.PurchaseEntry.objects.exclude(entry_status = 3,save_type = 2)
    entry_count = len(purchase_entry)
    for j in range(0,entry_count):
        entry_due_date = purchase_entry[0].purchase_entry_due_date
        if(purchase_entry[0].entry_status == 0):
            if(entry_due_date < current_date):
                remaining_date = (current_date - entry_due_date).days
                purchase_entry.PurchaseEntry.objects.filter(pk = purchase_entry[i].id).update(entry_status = 1,entry_date_count = delta)
        elif(purchase_entry[0].entry_status == 1 or purchase_entry[0].entry_status == 4):
            if(entry_due_date > current_date):
                remaining_date = (current_date - current_date).days
                purchase_entry.PurchaseEntry.objects.filter(pk = purchase_entry[i].id).update(entry_status = 1,entry_date_count = remaining_date)

    data = "data"
    return data