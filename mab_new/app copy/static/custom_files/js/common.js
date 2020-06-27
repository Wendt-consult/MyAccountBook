$(document).ready(function(){

    $("#menu li").each(function(){
      
        $("#menu li").removeClass("active");

        link_text = $(this).find("a").find("p").text();

        if(active_link === link_text){            
            $(this).addClass("active");
            return false;
        }
    });


    disabled_elems = document.querySelectorAll(".disabled_form_elements input, .disabled_form_elements select, .disabled_form_elements checkbox")

    for (var i = 0; i < disabled_elems.length; i++) {
        disabled_elems[i].disabled = !disabled_elems[i].disabled;
    }

});

//
//
//
function close_modal(elem){
    $("#wait_Modal").hide();
}


//
//
//
function edit_forms_creator(data){
    data = $.parseJSON(data);
    
    $.each(data, function(idx,value){
        $("td#form_element-"+idx).empty().append(value);
    });
}

//***********************************************************/
// Mobile & Phone Validation
//***********************************************************/

function validate_Phone(elem){
   value = $(elem).val();

   var format = /^\d{10}$/;

    if(value.length != 0){
        if (!value.match(format)) return Array(false,"*Please enter 10 digit valid mobile number");
        else return Array(true,"");
    } 
    else {
        return Array(true,"");
    }
}

//***********************************************************/
// PAN Number Validation
//***********************************************************/

function validate_PAN(elem){
    value = $(elem).val();

    var format = /[A-Z]{5}[0-9]{4}[A-Z]{1}$/;

    if(value.length != 0){
        if (!value.match(format)) return Array(false,"*Please enter valid pan card number");
        else return Array(true,"");
    } 
    else {
        return Array(true,"");
    }
}

//***********************************************************/
// GST Number Validation
//***********************************************************/

function validate_GST(elem){
    value = $(elem).val();

    var format = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;

    if(value.length != 0){
        if (!value.match(format)) return Array(false, "*Please enter valid GST number");
        else return Array(true,"");
    } 
    else {
        return Array(true,"");
    }
}

//***********************************************************/
// IFSC Number Validation
//***********************************************************/

function validate_IFSC(elem){
    value = $(elem).val();

    var format = /^[A-Za-z]{4}[a-zA-Z0-9]{7}$/;

    if(value.length != 0){
        if (!value.match(format)) return Array(false,"*Please enter valid ifsc code");
        else return Array(true,"");
    } 
    else {
        return Array(true,"");
    }    
}

//***********************************************************/
// Website/URL Validation
//***********************************************************/

function validate_URL(elem){
    value = $(elem).val();

    var format = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;

    if(value.length != 0){
        if (!value.match(format)) return Array(false,"*Please enter valid url");
        else return Array(true,"");
    }    
    else {
        return Array(true,"");
    }    
}

//***********************************************************/
// Email Validation
//***********************************************************/

function validate_Email(elem){
    value = $(elem).val();

    var format = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/

    if(value.length != 0){
        if (!value.match(format)) return Array(false,"*Please enter valid email address");
        else return Array(true,"");
    }
    else {
        return Array(true,"");
    }  
}


//***********************************************************/
// Reset Modal Forms
//***********************************************************/

$('.modal').on('hidden.bs.modal', function () {

    elem = $(this).find('form');

    $(elem).each(function(){
        $("input[type='text']").css("background-color","transparent");
    });

    $(this).find('form').trigger('reset');
});


/**************************************************************/
// Get Error Count On Form from localstorage
/**************************************************************/
function getLocalStorageValue(i_name){
    return localStorage.getItem(i_name);
}

function setLocalStorageValue(i_name, value){
    localStorage.setItem(i_name, value);
}


