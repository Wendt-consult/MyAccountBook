$(document).ready(function(){
    $('input[type="file"]').hide();
});

//******************************************************************
// LABEL CLICK
//******************************************************************

$('label#custom-file-upload').on("click", function(){
	$('#id_logo').click();
});


//******************************************************************
// DELETE ENTRIES
//******************************************************************

function del_all_entries(ids){
    if(ids == 0){
        $("span#title_head").empty().text(" Organisation Contact Details");
    }else{
        $("span#title_head").empty().text(" Account Details");
    }

    $("#del_all_modal").modal("show");
}

/************************************************************/
//   IMAGE VALIDATION DELETE
/************************************************************/

// Code by Lawrence Gandhar
$('#id_logo').on("change", function(){
	if (this.files && this.files[0]) {
		var img = document.querySelector('img');  // $('img')[0]
		img.src = URL.createObjectURL(this.files[0]); // set src to blob url       
	}
});


/********************************************************************/
// delete contact
/********************************************************************/
function delete_org_account(ids){    
    $.get("/profile/delete_account/"+ids+"/", function(data){
        if(data == '1') location.reload();
        else alert("Unauthorized Access");
    });
} 

/********************************************************************/
// check gst state code
/********************************************************************/

// $("#id_state").on("change",function(){

// 	id_state = $(this).val();
	
// 	if(id_state !=""){
// 		$.post("/check_gst_existing/",{"state_id":id_state, "organisation_id":organisation_id, 'csrfmiddlewaretoken':csrf_token},
// 			function(data){
// 				if(parseInt(data)>0){
// 					$("tr.gst_tr").hide();
// 				}else{
// 					$("tr.gst_tr").show();
// 				}
// 		});
// 	}
// });

/******************************************************************/
// STATE SELECT - SET GST
/******************************************************************/

var modal_id = ''
function check_gst(forloop,address_id,state){
	// elem = $(this);
	// ids = $(elem).closest(".modal").attr("id");
	modal_id = "#editAddressModal-"+forloop
	if(state !=""){
		$.post("/get_state_gst/",{'state_id':state, 'organisation_id':organisation_id,'address_id':address_id, 'csrfmiddlewaretoken':csrf_token},function(data){
			
			// $("#"+ids).find("#id_gstin").val(data.gstin);
			// $("#"+ids).find("#gst_reg").val(data.gst_reg_type);
			$("#editAddressModal-"+forloop).find(".tax_id_input").val(data.tax_id);
			$("#editAddressModal-"+forloop).find("#id_gstin").val(data.gstin);
            $("#editAddressModal-"+forloop).find("#gst_reg").val(data.gst_reg_type);
			$("#editAddressModal-"+forloop).find("#org_address_ids").val(address_id);
			$("#editAddressModal-"+forloop).find("#org_address_state").val(data.state);
			if(data.is_deafult == 'yes'){
				$("#editAddressModal-"+forloop).find("#default_tax").prop('checked',true);
			}else{
				$("#editAddressModal-"+forloop).find("#default_tax").prop('checked',false);
			}
			$("#editAddressModal-"+forloop).modal('show')
			if(data.gstin !="" && data.gstin != null && data.count == 'yes'){ 
				alert("Already a GST Number is registered in this state");
			}
		});
	}
};

/******************************************************************/
// gst configuration
/******************************************************************/
//  is register
$('#is_orginsation_register').click(function(){

    if($('#is_orginsation_register').is(':checked')){
        $('#no_orginsation_register').prop('checked',false)
        $('#gst_multiple').show()
    }
});

$('#no_orginsation_register').click(function(){
    
    if($('#no_orginsation_register').is(':checked')){
        $('#is_orginsation_register').prop('checked', false)
		$('#gst_multiple').hide()
		$('#gst_configuration_setting').hide()
		$('.single_gst_field').hide()
		$('#is_single_gst').prop('checked', false)
		$('#is_multiple_gst').prop('checked', false)
    }
});

// multiple gst

$('#is_multiple_gst').click(function(){
    
    if($('#is_multiple_gst').is(':checked')){
        $('#is_single_gst').prop('checked', false)
		$('#gst_configuration_setting').show()
		$('.single_gst_field').hide()
    }
});

$('#is_single_gst').click(function(){
    
    if($('#is_single_gst').is(':checked')){
        $('#is_multiple_gst').prop('checked', false)
		$('#gst_configuration_setting').hide()
		$('.single_gst_field').show()
    }
});
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
// GST STATE ADDRESS CHECK
/********************************************************************/

function gst_state_code(elem){
	if($('#error_field').text() == '' & $(elem).val() != ''){
		var str = $(elem).val()
		str = str.substring(0,2)
		if($("#single_gst_code option[value="+str+"]").length > 0){
			var state = $("#single_gst_code option[value="+str+"]").text()
			var org_id = $('#org_id').val()
			$.post("/org/gst_state_code/",{'state':state, 'org_id':org_id,'csrfmiddlewaretoken':csrf_token},function(data){
				if(data == 0){
					$('#error_field').text('GST state code not matching with existing address state') 
					$('#org_single_gst_save').prop('disabled', true)
				}else{
					$('#gst_state').val($("#single_gst_code option[value="+str+"]").text())
				}
			});
		}else{
			$('#error_field').text('GST state code not matching with existing address state') 
			$('#org_single_gst_save').prop('disabled', true)
		}
	}
}

function multiple_state_code(elem){
	if(($('.error_field').text() == '' || $('.error_field').text() == 'GST state code not matching with existing address state' ) & $(elem).val() != ''){
		var str = $(elem).val()
		str = str.substring(0,2)
		if($("#single_gst_code option[value="+str+"]").length > 0){
			var state = $("#single_gst_code option[value="+str+"]").text()
			var ids = $(modal_id).find("#org_address_state").val();
			if(state != ids){
				$('.error_field').text('GST state code not matching with existing address state') 
				$('.multiple_update').prop('disabled', true)
			}
			
		}else{
			$('.error_field').text('GST state code not matching with existing address state') 
			$('.multiple_update').prop('disabled', true)
		}
	}
}

$('.mul_cancel_gst').click(function(){
	$('.error_field').text('') 
	$('.multiple_update').prop('disabled', false)
})

/********************************************************************/
// SET DEFAULT GST
/********************************************************************/

function set_default_tax(elem){
	
	if($(elem).prop("checked")){
		c_box = confirm('Do you really want to set this gst as a default');
	
		if(c_box){

			$(elem).prop("checked",true);
		}else{
			$(elem).prop("checked",false);
		}
	}else{
		c_box = confirm('Do you really want to remove this gst from default');
		if(c_box){
			$(elem).prop("checked",false);
					
		}else{
			$(elem).prop("checked",true);
		}
	}
}
/********************************************************************/
// hide and show table active and inactive row
/********************************************************************/

function show_table_row(category){
	if(category == 'show_inactive'){
		$('.org_address_table_active').hide()
		$('.org_address_table_inactive').show()
		$('#active_row').show()
		$('#inactive_row').hide()
		// for table hide active
		$('#org_active_address_length').hide()
		$('#org_active_address_info').hide()
		$('#org_active_address_paginate').hide()
		// for table show inactive
		$('#org_inactive_address_length').show()
		$('#org_inactive_address_info').show()
		$('#org_inactive_address_paginate').show()
	}else if(category == 'show_active'){
		$('.org_address_table_active').show()
		$('.org_address_table_inactive').hide()
		$('#active_row').hide()
		$('#inactive_row').show()

		// for table show active
		$('#org_active_address_length').show()
		$('#org_active_address_info').show()
		$('#org_active_address_paginate').show()
		// for table hide inactive
		$('#org_inactive_address_length').hide()
		$('#org_inactive_address_info').hide()
		$('#org_inactive_address_paginate').hide()
	}

}

/********************************************************************/
// ajax for check state address is one or multiple
/********************************************************************/

function org_address_check(addres_ids,address_state){
	event.preventDefault()
	$.post("/profile/org_address_check/",{'addres_ids':addres_ids,'address_state':address_state,'csrfmiddlewaretoken':csrf_token},function(data){
		if(data == 1){
			$('#msg_text'+addres_ids+'').hide()
			$('#msg_text_last'+addres_ids+'').show()
			$('#org_add_new'+addres_ids+'').show()
			$('#org_inactive'+addres_ids+'').modal('show')
		}else{
			$('#msg_text'+addres_ids+'').show()
			$('#msg_text_last'+addres_ids+'').hide()
			$('#org_add_new'+addres_ids+'').hide()
			$('#org_inactive'+addres_ids+'').modal('show')
		}
	});
}

function show_hide_address_modal(modal_ids){
	$('#org_inactive'+modal_ids).modal('hide')
	$('#accounts_add_modal').modal('show')
	// nsg and button
	$('#msg_text1').show()
	$('#msg_text2').hide()
	$('#org_add_new').hide()
}

/********************************************************************/
// check inactive address present in same state
/********************************************************************/

function exit_address(elem){
	var address_state = $(elem).val()
	var org_id = $('#accounts_add_modal,#newOrgAddressModal').find('input[name=ids]').val()
	if(address_state != ''){
		$.post("/profile/org_address_inactive_check/",{'org_id':org_id,'address_state':address_state,'csrfmiddlewaretoken':csrf_token},function(data){
			if(data != 0){
				if(data != 1){
					c_box = confirm('In this State your previous gst number is '+data+', do you want to use that gst number.if you click "cancel" then you not be able to use previous gst number for new voucher.');
					if(c_box){
						$('.check_gst').val('no');
					}else{
						$('.check_gst').val('yes');
					}
				}else if(data == 1){
					$('.check_gst').val('no');
				}
			}else if(data == 0){
				$('.check_gst').val('no');
			}
		});
	}
}
/********************************************************************/
// decimal point
/********************************************************************/
function float_profile(event, elem) { 
    // var $this = $(this);
    
    if ((event.which != 46 || $(elem).val().indexOf('.') != -1) &&
       ((event.which < 48 || event.which > 57) &&
       (event.which != 0 && event.which != 8))) {
           event.preventDefault();
    }

    var text = $(elem).val();
    if ((event.which == 46) && (text.indexOf('.') == -1)) {
        setTimeout(function() {
            if ($('#'+a+'').val().substring($(elem).val().indexOf('.')).length > 3) {
                $('#'+a+'').val($this.val().substring(0, $(elem).val().indexOf('.') + 3));
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
// basic setting gst less then 100 percent
/********************************************************************/

function check_percent(elem){
	var gst_val = $(elem).val()
	if(parseFloat(gst_val) >= 100.00){
		alert("Pelase enter valid tax")
		$(elem).val('')
	}
}

/******************************************************************/
// set default bank account
/******************************************************************/

function set_bank_default(bank_type){
	if(bank_type == 'add'){
		if($('#org_bank_account_modal').find('#add_switch_bank').is(':checked')){
			c_box = confirm('You want to set this bank details as default bank details');
			if(c_box){
				$('#org_bank_account_modal').find('#default_bank_switch').val('yes');
				$('#org_bank_account_modal').find('#add_switch_bank').prop('checked', true)
			}else{
				$('#org_bank_account_modal').find('#default_bank_switch').val('no');
				$('#org_bank_account_modal').find('#add_switch_bank').prop('checked', false)
			}
		}else{
			c_box = confirm('You want to unset this bank details');
			if(c_box){
				$('#org_bank_account_modal').find('#default_bank_switch').val('no');
				$('#org_bank_account_modal').find('#add_switch_bank').prop('checked', false)
			}else{
				$('#org_bank_account_modal').find('#default_bank_switch').val('yes');
				$('#org_bank_account_modal').find('#add_switch_bank').prop('checked', true)
			}
		}
	}else{
		if($('#edit_bank_switch'+bank_type).is(':checked')){
			c_box = confirm('You want to set this bank details as default bank details');
			if(c_box){
				$('#editBankModal-'+bank_type).find('#default_bank_switch'+bank_type).val('yes');
				$('#editBankModal-'+bank_type).find('#edit_bank_switch'+bank_type).prop('checked', true)
			}else{
				$('#editBankModal-'+bank_type).find('#default_bank_switch'+bank_type).val('no');
				$('#editBankModal-'+bank_type).find('#edit_bank_switch'+bank_type).prop('checked', false)
			}
		}else{
			c_box = confirm('You want to unset this bank details');
			if(c_box){
				$('#editBankModal-'+bank_type).find('#default_bank_switch'+bank_type).val('no');
				$('#editBankModal-'+bank_type).find('#edit_bank_switch'+bank_type).prop('checked', false)
			}else{
				$('#editBankModal-'+bank_type).find('#default_bank_switch'+bank_type).val('yes');
				$('#editBankModal-'+bank_type).find('#edit_bank_switch'+bank_type).prop('checked', true)
			}
		}
	}
}

function set_bankaccount_switch(model_number,is_deafult){
	if(is_deafult == 'True'){
		$('#editBankModal-'+model_number).find('#edit_bank_switch'+model_number).prop('checked', true)
		$('#editBankModal-'+model_number).find('#default_bank_switch'+model_number).val('yes');
	}else{
		$('#editBankModal-'+model_number).find('#default_bank_switch'+model_number).val('no');
		$('#editBankModal-'+model_number).find('#edit_bank_switch'+model_number).prop('checked', false)
	}
	$('#editBankModal-'+model_number).modal('show')
}
