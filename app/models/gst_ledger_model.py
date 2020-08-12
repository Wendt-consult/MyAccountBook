from django.db import models
from django.contrib.auth.models import User
from app.models import invoice_model, creditnote_model, expense_model, purchase_model
from app.other_constants import *
from django.db.models.signals import post_save
from django.dispatch import receiver
  
#=====================================================================
# MULTIPLE COLLECTION METHODS
#=====================================================================
class GST_Ledger(models.Model):
    user = models.ForeignKey(
        User,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    is_invoice = models.BooleanField(
        default = False,
        db_index = True,
    )

    is_creditnote = models.BooleanField(
        default = False,
        db_index = True,
    )

    is_purchase_order = models.BooleanField(
        default = False,
        db_index = True,
    )

    is_expense = models.BooleanField(
        default = False,
        db_index = True,
    )

    invoice = models.ForeignKey(
        invoice_model.InvoiceModel,
        blank = True,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
    )

    creditnote = models.ForeignKey(
        creditnote_model.CreditNode,
        blank = True,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
    )

    expense = models.ForeignKey(
        expense_model.Expense,
        blank = True,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
    )

    purchase_order = models.ForeignKey(
        purchase_model.PurchaseOrder,
        blank = True,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
    )

    gst_number = models.CharField(
        max_length=50,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_amount = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_amount = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_amount = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    total_tax = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
    )

    input_tab = models.BooleanField(
        default = False,
        db_index = True,
    )


#==================================================================
# Create instances on Invoice Creation
#==================================================================
#

@receiver(post_save, sender=invoice_model.InvoiceModel)
def create_gstlegder_invoice(sender, instance, created, **kwargs):

    if created:
        gst_ledger = GST_Ledger.objects.create(invoice=instance)
    

        invoice = invoice_model.InvoiceModel.objects.get(pk = instance.pk)

        igst_amount = float(invoice.igst) if invoice.igst !="" else 0
        cgst_amount = float(invoice.cgst) if invoice.cgst !="" else 0
        sgst_amount = float(invoice.sgst) if invoice.sgst !="" else 0
        #print(igst, cgst, sgst)

        gst_ledger.gst_number = invoice.invoice_org_gst_num
        gst_ledger.cgst_amount = cgst_amount
        gst_ledger.sgst_amount = sgst_amount
        gst_ledger.igst_amount = igst_amount
        gst_ledger.is_invoice = True
        gst_ledger.total_tax = gst_ledger.cgst_amount + gst_ledger.sgst_amount + gst_ledger.igst_amount

        gst_ledger.user = invoice.user

        gst_ledger.save()

    else:
        pass


#==================================================================
# Create instances on Credit Creation
#==================================================================
#


@receiver(post_save, sender=creditnote_model.CreditNode)
def create_gstlegder_creditnote(sender, instance, created, **kwargs):
    if created:
        gst_ledger = GST_Ledger.objects.create(creditnote=instance)
        
        ins = creditnote_model.CreditNode.objects.get(pk = instance.pk)

        igst_amount = list(filter(None, [ins.igst_5, ins.igst_12, ins.igst_18, ins.igst_28, ins.igst_other]))
        cgst_amount = list(filter(None, [ins.cgst_5, ins.cgst_12, ins.cgst_18, ins.cgst_28, ins.cgst_other]))
        sgst_amount = list(filter(None, [ins.sgst_5, ins.sgst_12, ins.sgst_18, ins.sgst_28, ins.sgst_other]))
        #print(igst, cgst, sgst)


        gst_ledger.gst_number = ins.creditnote_org_gst_num
        gst_ledger.cgst_amount = sum([float(i) for i in cgst_amount]) if len(cgst_amount) > 0  else 0
        gst_ledger.sgst_amount = sum([float(i) for i in sgst_amount]) if len(sgst_amount) > 0  else 0
        gst_ledger.igst_amount = sum([float(i) for i in igst_amount]) if len(igst_amount) > 0  else 0
        gst_ledger.is_creditnote = True
        gst_ledger.input_tab = True
        gst_ledger.total_tax = gst_ledger.cgst_amount + gst_ledger.sgst_amount + gst_ledger.igst_amount
        gst_ledger.user = ins.user

        gst_ledger.save()

    else:
        pass  
#==================================================================
# Create instances on Expense Creation
#==================================================================
#


@receiver(post_save, sender=expense_model.Expense)
def create_gstlegder_expense(sender, instance, created, **kwargs):
    if created:
        gst_ledger = GST_Ledger.objects.create(expense=instance)
        
        ins = expense_model.Expense.objects.get(pk = instance.pk)

        igst_amount = list(filter(None, [ins.igst_5, ins.igst_12, ins.igst_18, ins.igst_28]))
        cgst_amount = list(filter(None, [ins.cgst_5, ins.cgst_12, ins.cgst_18, ins.cgst_28]))
        sgst_amount = list(filter(None, [ins.sgst_5, ins.sgst_12, ins.sgst_18, ins.sgst_28]))
        #print(igst, cgst, sgst)

        gst_ledger.cgst_amount = sum([float(i) for i in cgst_amount]) if len(cgst_amount) > 0  else 0
        gst_ledger.sgst_amount = sum([float(i) for i in sgst_amount]) if len(sgst_amount) > 0  else 0
        gst_ledger.igst_amount = sum([float(i) for i in igst_amount]) if len(igst_amount) > 0  else 0
        gst_ledger.is_expense = True
        gst_ledger.input_tab = True
        gst_ledger.total_tax = gst_ledger.cgst_amount + gst_ledger.sgst_amount + gst_ledger.igst_amount
        gst_ledger.user = ins.user
        gst_ledger.save()

    else:
        pass  
#==================================================================
# Create instances on Purchase Order Creation
#==================================================================
#
"""
@receiver(post_save, sender=purchase_model.PurchaseOrder)
def create_gstlegder_purchaseorder(sender, instance, created, **kwargs):
    if created:
        gst_ledger = GST_Ledger.objects.create(purchase_order = instance)
        
        ins = purchase_model.PurchaseOrder.objects.get(pk = instance.pk)

        igst_amount = list(filter(None, [ins.igst_5, ins.igst_12, ins.igst_18, ins.igst_28, ins.igst_other]))
        cgst_amount = list(filter(None, [ins.cgst_5, ins.cgst_12, ins.cgst_18, ins.cgst_28, ins.cgst_other]))
        sgst_amount = list(filter(None, [ins.sgst_5, ins.sgst_12, ins.sgst_18, ins.sgst_28, ins.sgst_other]))
        #print(igst, cgst, sgst)

        gst_ledger.cgst_amount = sum([float(i) for i in cgst_amount]) if len(cgst_amount) > 0  else 0
        gst_ledger.sgst_amount = sum([float(i) for i in sgst_amount]) if len(sgst_amount) > 0  else 0
        gst_ledger.igst_amount = sum([float(i) for i in igst_amount]) if len(igst_amount) > 0  else 0
        gst_ledger.is_purchase_order = True
        gst_ledger.input_tab = True
        gst_ledger.total_tax = gst_ledger.cgst_amount + gst_ledger.sgst_amount + gst_ledger.igst_amount
        gst_ledger.save()

    else:
        pass        
"""


