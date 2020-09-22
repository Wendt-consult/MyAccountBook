/********************************************************************/
// INPUT TYPE NUMBER SROLL HIDE
/********************************************************************/
// Disable Mouse scrolling
$('input[type=number]').on('mousewheel',function(e){ $(this).blur(); });
// Disable keyboard scrolling
$('input[type=number]').on('keydown',function(e) {
    var key = e.charCode || e.keyCode;
    // Disable Up and Down Arrows on Keyboard
    if(key == 38 || key == 40 || key == 69 || key == 189) {
	e.preventDefault();
    } else {
	return;
    }

});
/*code: 48-57 Numbers 8  - Backspace, 35 - home key, 36 - End key 37-40: Arrow keys, 46 - Delete key*/
    function restrictAlphabets(e){
		var x=e.which||e.keycode;
		if((x>=48 && x<=57) || x==8 ||
			(x>=35 && x<=40)|| x==46)
			return true;
		else
			return false;
   }
/********************************************************************/
// decimal point
/********************************************************************/
function float_value(event, elem) { 
    // var $this = $(this);
    
    if ((event.which != 46 || $(elem).val().indexOf('.') != -1) &&
       ((event.which < 48 || event.which > 57) &&
       (event.which != 0 && event.which != 8))) {
           event.preventDefault();
    }

    var text = $(elem).val();
    if ((event.which == 46) && (text.indexOf('.') == -1)) {
        setTimeout(function() {
            if ($(elem).val().substring($(elem).val().indexOf('.')).length > 3) {
                $(elem).val($this.val().substring(0, $(elem).val().indexOf('.') + 3));
            }
        }, 1);
    }

    if ((text.indexOf('.') != -1) &&
        (text.substring(text.indexOf('.')).length > 2) &&
        (event.which != 0 && event.which != 8) &&
        ($(elem)[0].selectionStart >= text.length - 2)) {
            event.preventDefault();
    }      
};

/********************************************************************/
// Before saving check entry amount
/********************************************************************/

function check_amount(model_id){
    var enter_value = $('#expensePaymentModel-'+model_id).find('#pay_amount-'+model_id).val()
    var balance = $('#expensePaymentModel-'+model_id).find('#entry_balance-'+model_id).val()
    if(parseFloat(enter_value) == 0.00 || parseFloat(enter_value) > parseFloat(balance)){
        alert("Please enter valid amount")
        $('#expensePaymentModel-'+model_id).find('#pay_amount-'+model_id).focus()
        return false
    }else{
        return true
    }
}

/********************************************************************/
// Date Picker
/********************************************************************/

$(".pay_date,#make_payment_date").datepicker({dateFormat: 'dd-mm-yy'}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");

$('.pay_date,#make_payment_date').keypress(function(event) {
    event.preventDefault();
});

/********************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG  VANDOR NAME
/********************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#make_payment_vendor").select2();
      });
    });
$(document).on('click','#select2-make_payment_vendor-container',function(){

    var a = $('#addcontact').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact()" id="addcontact" data-target="#ContactModal" style="margin-left: -8%;">+ Add Contact</button>');
        }
        });
function add_contact(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#make_payment_vendor").select2();
          });
        });

        $('#id_customer_type').remove()
        var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
        html +='<option value="2" selected>VENDOR</option>'
        html +='<option value="4">CUSTOMER AND VENDOR</option></select>'
       $('#con_type').append(html)

       $('#add_contact_type').remove()
       var button = '<button class="btn btn-sm btn-success save_button " name="purchase_contact" id="add_contact_type" style="margin-top:16px;background-color: #598ebb;" onclick="return entry_contact_form()">Save</button>'
       $( button ).insertBefore("#contact_type_add");
    }


/********************************************************************/
// PUCHASE LINE ITEMS(ACCOUNT) SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $("#make_payment_account").select2();
        // $('.select2-container--default').css('padding-bottom','16px')
      });
});

$(document).on('click','#select2-make_payment_account-container',function(){
    var a = $('#account_assest').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link" data-toggle="modal" id="account_assest" onclick="account_assest()" data-target="#addGroupModal" style="margin-left: -8%;">+ Add New</button>');
            // $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact()" id="addcontact" data-target="#ContactModal" style="margin-left: -8%;">+ Add Contact</button>');
        }
});

function account_assest(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#make_payment_account").select2();
          });
        });
}


/********************************************************************/
// PURCHASE_OREDR CONTACT MODEL SAVE USING AJAX
/********************************************************************/
function entry_contact_form(){
  
    event.preventDefault()

    // if($('#id_contact_name').val() == ''){
    //     alert('Contact name is requried')
    //     $('#id_contact_name').focus()
    //     return false
    // }else if($('#id_organization_type option').filter(':selected').val() != '1' & $('#id_organization_name').val() == ''){
    //     alert('Organization name is requried')
    //     $('#id_organization_name').focus()
    //     return false
    // }else if($('#id_user_address_details_set-0-city').val() == ''){
    //     alert('City is requried')
    //     $('#id_user_address_details_set-0-city').focus()
    //     return false
    // }else if($('#id_user_address_details_set-0-state').val() == ''){
    //     alert('State is requried')
    //     $('#id_user_address_details_set-1-state').focus()
    //     return false
    // }else if($('#id_user_address_details_set-0-country').val() == ''){
    //     alert('Country is requried')
    //     $('#id_user_address_details_set-0-country').focus()
    //     return false
    // }

    // if($('.address_is_billing_diff').is(':checked')){
    //     if($('#id_user_address_details_set-1-city').val() == ''){
    //         alert('City is requried')
    //         $('#id_user_address_details_set-1-city').focus()
    //         return false
    //     }else if($('#id_user_address_details_set-1-state').val() == ''){
    //         alert('State is requried')
    //         $('#id_user_address_details_set-1-state').focus()
    //         return false
    //     }else if($('#id_user_address_details_set-1-country').val() == ''){
    //         alert('Country is requried')
    //         $('#id_user_address_details_set-1-country').focus()
    //         return false
    //     }
    // }
    
    $.post("/contacts/add/",$("#add_payment_contact_form").serialize(), function(data){
        if(data != '0'){
            
            $.get("/creditnote/contact_fetch/",function(data){
                
                    $("#make_payment_vendor").each(function(){
                        $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                    });
                    $('#make_payment_vendor').val(data.ids).change(); 
                
            });
            $("#ContactModal").modal('hide');
        }  
    });
}

/********************************************************************/
// PURCHASE_OREDR ACCOUNT_LEDGER(GROUP) MODEL SAVE USING AJAX
/********************************************************************/
function purchase_accoun_ledger_form(save_type){
  
    event.preventDefault()

    if($('#id_group_name').val() == ''){
        alert('group name is requried')
        $('#id_group_name').focus()
        return false
    }

    $.post("/add_ledger_group/",$("#add_group_form").serialize(), function(data){
    if(data != '0'){
        
        $.get("/purchase_order/account_group_fetch/",function(data){

            $("#make_payment_account").each(function(){
                $('<option/>').val(data.ids).html(data.group_name).appendTo($(this));
            });
            $('#make_payment_account').val(data.ids).change(); 
            
        });
        $("#addGroupModal").modal('hide');
    }
  
});
}

/*********************************************************************** */
// DEFUALT PURCHASE_OREDER AND CHECK PURCHASE_OREDER NUMBER IS UNIQUE
/*********************************************************************** */
$("#auto_payment_number").click(function(){
    if($(this).is(':checked')){
        var ins = 0
        var slug = 'a'
        $.ajax({
            type:"GET",
            url: "/paymentmade/unique_number/"+ins+"/"+slug+"/",
            dataType: "json",
            success: function(data){
                $('#make_pyament_number').val(data.payment_number)
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }else{
        $('#make_pyament_number').val('')
    }  
});

$("#make_pyament_number").focusout(function(){
    $("#auto_payment_number").prop('checked',false);
    var ins = 1
    var payment_number = $("#make_pyament_number").val()
    $.ajax({
        type:"GET",
        url: "/paymentmade/unique_number/"+ins+"/"+payment_number+"/",
        dataType: "json",
        success: function(data){
            if(data.unique != 0){
                alert('This payment number is already exits. Please enter the different payment number.')
                $('#make_pyament_number').focus();
                $('#make_pyament_number').val('')
            }
            
        },
    });
  });

/*********************************************************************** */
// MOUSE HOVER
/*********************************************************************** */
vendor_info()
function vendor_info(){
    var ins = $('#make_payment_vendor').val()
    if(ins != ''){
        $.get("/purchase_order/vendor_details/"+ins+"/",function(data){
            var name 
            var organization
            var mail
            var number
            var address
        
            if(data.name == null){
                name = ''
            }
            else if(data.name != null){
                name = data.name
            }

            if(data.oganization_name == null){
                organization = ''
            }
            else if(data.oganization_name != null){
                organization = data.oganization_name
            }
            if(data.mail == null){
                mail = ''
            }
            else if(data.mail != null){
                mail = data.mail
            }
            if(data.number == null){
                number = ''
            }
            else if(data.number != null){
                number = data.number   
            }

            if(data.address == null){
                address = ''
            }
            else if(data.address != null){
                address = data.address
            }
                
            if(data.gstin == null){
                gstin = ''
            }
            else if(data.gstin != null){
                gstin = data.gstin
            }
            if(data.gst_type == null){
                gst_type = ''
            }
            else if(data.gst_type != null){
                gst_type = data.gst_type
            }
            // var html2 = ''
            
            // html2 +='Name:- '+name+''+'\n'+ 'Organisation Name:-'+'\n'+organization+''+'\n'+'Email:-'+mail+''+'\n'+'Number:-'+number+''+'\n'+'Address:-'+address+'';
            
            $("#v_info").find('#v_name').text(name)
            $("#v_info").find('#v_org').text(organization)
            // $("#v_info").find('#v_mail').text(mail)
            // $("#v_info").find('#v_num').text(number)
            $("#v_info").find('#v_addr').text(address)
            $("#v_info").find('#v_gst_type').text(gst_type)
            $("#v_info").find('#v_gstin').text(gstin)
            $("#v_info").show()
            $('#v_question').hide()
            // $('#contact_gst_change').find('#vendor_gst_type').text(gst_type)
            $("#contact_gst_change option:contains("+gst_type+")").attr('selected', true);
            $('#contact_gst_change').find('#vendor_gst').val(gstin)
            $('#vendor_ids').val(ins)
            // attr('data-tip', html2);
        });
    }else{
        // $("#vendor_details").append('')
        $("#v_info").hide()
        $('#v_question').show()
        $("#v_info").find('#v_name').text('')
        $("#v_info").find('#v_org').text('')
        // $("#v_info").find('#v_mail').text('')
        // $("#v_info").find('#v_num').text('')
        $("#v_info").find('#v_addr').text('')
        $("#v_info").find('#v_gst_type').text('')
        $("#v_info").find('#v_gstin').text('')
        $('#contact_gst_change').find('#vendor_gst_type').val(0).change()
        $('#contact_gst_change').find('#vendor_gst').val('')
        // attr('data-tip', '');
    }
}
