from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from app.models import *
from django.contrib.auth.models import User

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

# use Library
register = template.Library()


#*************************************************************************
#   LOADER COMPONENT - MODAL 
#*************************************************************************
@register.simple_tag
def loader_component():
    htm = '''<div class="modal" id="wait_Modal"  tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="background-color: hsla(0, 4%, 26%, 0.87) !important;">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title pull-left">Processing.. Please Wait</h4>
                        <button type="button" onclick="close_modal($(this))" class="close" data-dismiss="modal">&times;</button>
                    </div>
                    <div class="modal-body">                
                        <div id="loader_container" class="loader-custom"></div>
                        <div id="svg_container" class="hide">
                            <svg id="failure_svg" class="checkmark hide" style="box-shadow: inset 0px 0px 0px #FF0000; animation: fill_red .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" style="stroke: #FF0000;" />
                                <path class="checkmark__check" fill="none" d="M16 16 36 36 M36 16 16 36" />
                            </svg>
                            <svg id="success_svg" class="checkmark hide" style="box-shadow: inset 0px 0px 0px #7ac142; animation: fill_green .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" style="stroke: #7ac142;" />
                                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                            </svg>
                        </div> 
                        <div id="modal-text" class="text-center"></div>            
                    </div>
                </div>
            </div>
        </div>'''

    return safestring.mark_safe(htm)