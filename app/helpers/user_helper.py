from app.models import * 

#
#
# 
def change_contact_default_address_status(ins=None):
    if ins is not None:
        addresses = users_model.User_Address_Details.objects.filter(is_user = False, is_organisation=False, contact = ins)
        
        for addr in addresses:
            addr.default_address = False
            addr.save()

#
#
#             
def change_org_default_address_status(ins=None):
    if ins is not None:
        addresses = users_model.User_Address_Details.objects.filter(is_user = True, is_organisation = True, organisation = ins)
        
        for addr in addresses:
            addr.default_address = False
            addr.save()