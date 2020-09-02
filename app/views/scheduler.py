from app.models import *
from datetime import datetime,date

def test_fun():
    invoice = invoice_model.InvoiceModel.objects.all()
    count = len(invoice)
    for i in range(0,count):
        # if statement for one time invoice
        if(invoice[i].invoice_type_new == 'on'):
            invoice_due_date = invoice[i].invoice_new_due_date
            current_date = date.today()
            if(invoice[i].invoice_status == 0):
                if(invoice_due_date < current_date):
                    delta = (current_date - invoice_due_date).days
                    invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(invoice_status = 1,inovice_over_due_count = delta)
            elif(invoice[i].invoice_status == 1):
                delta = (current_date - invoice_due_date).days
                invoice_model.InvoiceModel.objects.filter(pk = invoice[i].id).update(inovice_over_due_count = delta)
                # invoice for recurring type
        elif(invoice[i].invoice_type_recurring == 'on'):
            frequency = invoice[i].invoice_type_recurring
            repeat = invoice[i].invoice_recurring_repeat
            count = invoice[i].invoice_recurring_count
            current_date = date.today()
            if(repeat != count):
                if(frequency == 'Weekly'):
                    if(count == 0):
                        pass
                    #     if(invoice[0].invoice_recurring_start_date <= current_date):

                    # invoice_date
                elif(frequency == 'Monthly'):
                    pass
                elif(frequency == 'Quarterly'):
                    pass
                elif(frequency == 'Half yearly'):
                    pass
                elif(frequency == 'Yearly'):
                    pass

    print("running")
    data = "data"
    return data