#
# Author : Lawrence Gandhar
# Module : Emailer
#

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from app.models import * 

class Email_Helper():

    def __init__(self, to=[], from_add=None, cc=[], bcc=[], subject=None, message=None, attachment=[]):
        self.to = to
        self.cc = cc
        self.subject = subject
        self.message = message
        self.attachement = attachment
        self.from_add = from_add if from_add is None else settings.EMAIL_HOST_USER
        
        #
        self.email_config = ""
        self.errors = []
    #
    # Check mandatory fields "email_add" and "subject"
    #
    def mail_validate(self):
        
        if self.to is None or len(self.to) == 0:
            return False
        return True
        
    #
    # 
    #
    def mail_send(self):
    
        if not self.mail_validate():
            return False
        
        email_draft = EmailMultiAlternatives(self.subject, self.message, self.from_add, self.to, cc=self.cc)
        
        if self.attachement is not None and len(self.attachement) > 0:
            for file_path in self.attachement:
                email_draft.attach_file(file_path)
        
        email_draft.attach_alternative(self.message, "text/html")
        
        if email_draft.send():
            print("Email sent")
                
            
        
        
        
        
        
        
        