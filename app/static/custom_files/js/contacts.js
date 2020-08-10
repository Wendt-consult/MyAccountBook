/************************************************************ */
// code by Lawrence - Start
/************************************************************ */

$(document).ready(function(){
    setLocalStorageValue('form_errors_email', false);
    setLocalStorageValue('form_errors_phone', false);
    setLocalStorageValue('form_errors_pan', false);
    setLocalStorageValue('form_errors_gst', false);
    setLocalStorageValue('form_errors_url', false);
    setLocalStorageValue('form_errors_ifsc', false);
	
	$(".default_address").each(function(){		
		if($(this).val() == "True"){
			$(this).closest("td").find(".default_address_checkbox").prop("checked", true);
		}
	});
});

$("#app_id_input_2").removeClass("show-row").addClass("hide-row");

$("#more_address_table").find("input").attr('disabled', "true");
$("#more_address_table").find("select").attr('disabled', "true");

$("#tr-id_user_address_details_set-tr-0 td:nth-child(2)").find("table > tbody tr:nth-child(1)").hide();

$("#tr-id_user_address_details_set-tr-0 td:nth-child(2)").find("table > tbody tr:nth-child(1)").after(
    '<tr><td colspan="2" style="display:block; height:34px;"></td></tr>'
);

$("tr#tr-id_user_address_details_set-tr-0 > td:nth-child(2)").hide()
$(".is_billing_address, .is_shipping_address").prop("required",false);





/**************************************************************/
// Email Validation
/**************************************************************/

function valid_Email(elem){
    ret = validate_Email($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_email', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text(ret[1]);       
        $(elem).focus();
        $(".save_button, #editContactModal > .save_button").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_email', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");
        $(".save_button, #editContactModal > .save_button").prop("disabled",false);
    } 
}


/**************************************************************/
// Phone/Mobile Validation
/**************************************************************/

function valid_Phone(elem){
    ret = validate_Phone($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_phone', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text(ret[1]);
        $('#error_field').append("p").text(ret[1]);
        $('#c_error_field').append("p").text(ret[1]);
        $(elem).focus();
        $(".save_button, #editContactModal > .save_button,").prop("disabled",true);
        $(".order_button").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_phone', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");
        $('#error_field').append("p").text('');
        $('#c_error_field').append("p").text('');
        $(".save_button, #editContactModal > .save_button").prop("disabled",false);
        $(".order_button").prop("disabled",false);
    } 
}
function setMessage(elem){
    var value = $(elem).val();
    if(value.length == 0) {
        $(".error_field,.org_error_field").text('');
    }
 
 }


/**************************************************************/
// PAN Validation
/**************************************************************/

function valid_PAN(elem){
    ret = validate_PAN($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_pan', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("*Please enter valid pan card number");
        $('.org_error_field').text("*Please enter valid pan card number");
        $(elem).focus();
        $(".save_button, #editContactModal > .save_button,.org_update").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_pan', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");
        $('.org_error_field').text("");
        $(".save_button, #editContactModal > .save_button,.org_update").prop("disabled",false);
    } 
}


/**************************************************************/
// GST Validation
/**************************************************************/

function valid_GST(elem){
    ret = validate_GST($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_get', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text(ret[1]);
        $(elem).focus();
        $('#error_field').text(ret[1]);
        $('#vendor_error_field').text(ret[1]);
        $(".save_button, #editContactModal > .save_button,#org_single_gst_save,#vendor_gst_save").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_get', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");
        $('#error_field').text('');
        $('#vendor_error_field').text('');
        $(".save_button, #editContactModal > .save_button,#org_single_gst_save,#vendor_gst_save").prop("disabled",false);
    }  
}

/**************************************************************/
// WEBSITE Validation
/**************************************************************/

function valid_URL(elem){
    ret = validate_URL($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_url', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text(ret[1]);
        $(elem).focus();
        $(".save_button, #editContactModal > .save_button").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_url', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");
        $(".save_button, #editContactModal > .save_button").prop("disabled",false);
    }  
}



/************************************************************ */
// IFSC Validations
/************************************************************ */

function valid_IFSC(elem){
    ret = validate_IFSC($(elem));
    if(!ret[0]){
        setLocalStorageValue('form_errors_ifsc', true);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text(ret[1]);
        $(elem).focus();
        $(".save_button, #editContactModal > .save_button").prop("disabled",true);
    }else{
        setLocalStorageValue('form_errors_ifsc', false);
        $(elem).closest("tr").find("td.error_field").empty().append("p").text("");     
        $(".save_button, #editContactModal > .save_button").prop("disabled",false);
    }  
}

/************************************************************ */
// Check if APP ID exists
/************************************************************ */
function has_app_id(elem){

    $("#app_id_input").find("input").val("").removeClass("wrong_input");
    $("#id_app_id_check").empty();

    if($(elem).prop("checked") == true){
        $("#app_id_input").removeClass("hide-row").addClass("show-row");
    }
    else if($(elem).prop("checked") == false){
        $("#app_id_input").removeClass("show-row").addClass("hide-row");
        $("#app_id_input_2").removeClass("show-row").addClass("hide-row");
    }
}

//******************************************* 
//  CHECK IF APPLICATION ID EXISTS 
//********************************************

function check_app_id(elem){

    csrf = $("form").find("input[name='csrfmiddlewaretoken']").val();

    if($(elem).val()!=""){
        $("#wait_Modal").show();
        $("#wait_Modal").find("#loader_container").show();
        $("#wait_Modal").find("#modal-text").empty();

        $.post('/contacts/check_appid/',{'id':$(elem).val(), 'csrfmiddlewaretoken':csrf}, function(data){

            data = JSON.parse(data);

            if(data.ret == 0){ 
                
                $("#wait_Modal").find("#modal-text").html('<span style="color:#FF0000; font-weight:bold">Invalid Application ID</span>');              
                $("#id_app_id_check").empty().append('<i class="material-icons">clear</i>');
                $("#app_id_input_2").removeClass("show-row").addClass("hide-row");
                $("#success_svg").hide();
                $("#failure_svg").show().css("display", "block");
                $(elem).addClass("wrong_input");
            }
            if(data.ret =='1'){
                $("#id_app_id_check").empty().append('<i class="material-icons">check</i>');
                $("#wait_Modal").find("#modal-text").html('<span style="color:#00cc00; font-weight:bold">Found Application ID</span>');              
                $("#app_id_input_2").removeClass("hide-row").addClass("show-row");
                $("#failure_svg").hide();
                $("#success_svg").show().css("display", "block");
                $("#id_imported_user").val(data.id);
                $(elem).removeClass("wrong_input");
            }

            $("#svg_container").show();
            $("#wait_Modal").find(".modal-title").empty().text("Result");
            $("#wait_Modal").find("#loader_container").hide();
        });
    }
}

//******************************************* 
//  Check imported User
//********************************************

$("#id_is_imported_user").on("click", function(){

    if($(this).prop("checked") === true){

        csrf = $("form").find("input[name='csrfmiddlewaretoken']").val();

        $.post('/contacts/user_exists_in_list/',{'id':$("#id_imported_user").val(), 'csrfmiddlewaretoken':csrf}, function(data){
                        
            if(data == 0){
                r = confirm("Do you want to use the existing details of this user as the contact details");
                if (r === true) {
                    $("#id_contact_name").val('Existing App User');
                }else{
                    $(this).prop("checked", false);
                }
            }
            if(data >=1){
                r = confirm("A user with the same AppId exists in your contact list. Do you still want to create a new contact?");
                if (r === true) {
                    $("#id_contact_name").val('Existing App User');
                }else{
                    $(this).prop("checked", false);
                }
            }
        });
    }
});

/****************************************************************/
// Add Accounts Block
/****************************************************************/

$("#add_more_accounts").on("click", function(){
    inc = $("#id_form-TOTAL_FORMS").val();

    htm_all = '<tr class="tr-set-'+inc+'">';
    htm_all += '<td style="padding-top:10px; color:#FF0000; border:0px; border-bottom:3px solid #ccc;" colspan="4">';
    htm_all += '<i class="material-icons pull-right" style="cursor:pointer;" onclick="delete_account_block($(this),'+(parseInt(inc)-1)+')">delete_forever</i></td></tr>';

    $("#accounts-form tr.accounts_formset ").each(function(index, tr){

        xx = $(tr).html().replace("form-0", "form-"+inc)

        htm = '<tr class="tr-set-'+inc+'">'+xx+'</tr>';
        htm_all += htm;
    });

    $("#id_form-TOTAL_FORMS").val(parseInt(inc)+1);

    $("#accounts-form > table > tbody").append(htm_all);

    $('tr.tr-set-'+inc).find("td.error_field").empty();

});



/****************************************************************/
// Add Address Block
/****************************************************************/

$("#add_more_addresses").on("click",function(){

    inc = $("#id_user_address_details_set-TOTAL_FORMS").val();

    htm_all = '';

    htm = $("tr#tr-id_user_address_details_set-tr-0").html();

    htm_all = '<tr>';
    htm_all += '<td style="padding-top:10px; color:#FF0000; border:0px; border-bottom:3px solid #ccc;" colspan="2">';
    htm_all += '<i class="material-icons pull-right" style="cursor:pointer;" onclick="delete_address_block($(this),'+(parseInt(inc)-1)+')">delete_forever</i></td></tr>';
    htm_all += '<tr id="tr-id_user_address_details_set-tr-'+(parseInt(inc)-1)+'">'+htm+'</tr>';

    ids = parseInt(inc);

    row_num = 0;
    
    htm_all = htm_all.replace(/user_address_details_set-0/g, "user_address_details_set-"+ids);
    htm_all = htm_all.replace(/user_address_details_set-1/g, "user_address_details_set-"+parseInt(ids + 1));
    
    $("#address_table > tbody").append(htm_all);

    $("#tr-id_user_address_details_set-tr-"+(parseInt(inc)-1)+"  td:nth-child(2)").find("table > tbody tr:nth-child(1)").hide();

    $("#tr-id_user_address_details_set-tr-"+(parseInt(inc)-1)+"  td:nth-child(2)").find("table").hide();

    $("#id_user_address_details_set-TOTAL_FORMS").val(parseInt(inc) + 2);

    $("#tr-id_user_address_details_set-tr-"+(parseInt(inc)-1)+"  td:nth-child(2)").find($(".address_is_billing_diff")).attr("onclick","set_shipping_diff($(this),"+parseInt(ids)+")")

});


/****************************************************************/
// is shipping different
/****************************************************************/

function set_shipping_diff(elem,ids){

    if($(elem).prop("checked") == true){
       
        $("select#id_user_address_details_set-"+ids+"-is_shipping_address_diff").val(1);
        $("select#id_user_address_details_set-"+ids+"-is_shipping_address").val(0);
        $("select#id_user_address_details_set-"+ids+"-is_billing_address").val(1);
        $("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-is_shipping_address").val(1);
        $("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-is_billing_address").val(0);
        $(".address_diff").show()
		
		if($("select#id_user_address_details_set-"+parseInt(ids)+"-default_address").prop("checked") == true){
			$("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-default_address").val("False");
		}else{
			$(".default_address_checkbox").prop("checked",false);
        }
		
    }else{
        $("select#id_user_address_details_set-"+ids+"-is_shipping_address_diff").val(0);
        $("select#id_user_address_details_set-"+ids+"-is_shipping_address").val(1);
        $("select#id_user_address_details_set-"+ids+"-is_billing_address").val(1);
        $("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-is_shipping_address").val(1);
        $("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-is_billing_address").val(1);
		
		if($("select#id_user_address_details_set-"+parseInt(ids)+"-default_address").prop("checked") == true){
			$("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-default_address").val("False");
		}else{
			$(".default_address_checkbox").prop("checked",false);
		}
		
		/*
		$("select#id_user_address_details_set-"+(parseInt(ids)+1)+"-default_address").val("False");
		$(".default_address_checkbox").prop("checked",false);
		*/
        $("#id_user_address_details_set-"+(parseInt(ids)+1)+"-contact_person").val("")
        $("#id_user_address_details_set-"+(parseInt(ids)+1)+"-flat_no").val("")
        $("#id_user_address_details_set-"+(parseInt(ids)+1)+"-street").val("")
        $("#id_user_address_details_set-"+(parseInt(ids)+1)+"-city").val("")
        $("#id_user_address_details_set-"+(parseInt(ids)+1)+"-pincode").val("")    
        $(".address_diff").hide()
    } 
    
    if(ids == 0){
        elem_htm = $("tr#tr-id_user_address_details_set-tr-0 > td:nth-child(2)");
    }else{
        elem_htm = $(elem).closest("table").parent("td").parent("tr").children().eq(1);
    }

    if($(elem).prop("checked") == true){
        $(elem_htm).show();
        $(elem_htm).find("table").show();
    }else{
        $(elem_htm).find("table").hide();
    }
}


/****************************************************************/
// Remove Address Block
/****************************************************************/

function delete_address_block(elem, ids){
    inc = $("#id_user_address_details_set-TOTAL_FORMS").val();
    $(elem).closest('tr').remove();
    $("#tr-id_user_address_details_set-tr-"+ids).remove();
    $("#id_user_address_details_set-TOTAL_FORMS").val(parseInt(inc) -2);
}

/****************************************************************/
// Remove Accounts Block
/****************************************************************/

function delete_account_block(elem, ids){
    inc = $("#id_user_address_details_set-TOTAL_FORMS").val();
    
    elem = $(elem).closest("tr").attr("class");

    $("tr."+elem).remove();
    $("#id_form-TOTAL_FORMS").val(parseInt(inc)-1);
}


$(".disabled-tr").find("input").attr("disabled","true");
$(".disabled-tr").find("select").attr("disabled","true");
$(".disabled-tr").find("textarea").attr("disabled","true");

$(".set_required").find("input").attr("required", "true");
$(".set_required").find("select").attr("required", "true");

$("#editAccountsModal").find("input").attr("required", "true");


/********************************************************************/
//
/********************************************************************/
function openAddressModal(ids, is_billing_address, is_shipping_address, default_address, address_id = null, organisation = false){
    if(is_billing_address == 1){
        $("#editAddressModal-"+ids).find(".checkbox_billing").prop("checked", true);
    }else{
        $("#editAddressModal-"+ids).find(".checkbox_billing").prop("checked", false);
    }
    
    if(is_shipping_address == 1){
        $("#editAddressModal-"+ids).find(".checkbox_shipping").prop("checked", true);
    }else{
        $("#editAddressModal-"+ids).find(".checkbox_shipping").prop("checked", false);
    }
	
	if(default_address == "True"){
		$("#editAddressModal-"+ids).find(".default_address_checkbox").prop("checked", true);
	}else{
		$("#editAddressModal-"+ids).find(".default_address_checkbox").prop("checked", false);
	}
	
	if(organisation && address_id){
		
		$.post("/get_gst/",{'address_id':address_id, 'csrfmiddlewaretoken':csrf_token},function(data){
						
			$("#editAddressModal-"+ids).find(".tax_id_input").val(data.tax_id);
			$("#editAddressModal-"+ids).find("#id_gstin").val(data.gstin);
            $("#editAddressModal-"+ids).find("#gst_reg").val(data.gst_reg_type);
            $("#editAddressModal-"+ids).find("#org_address_ids").val(address_id);
		});
	}
	
    $("#editAddressModal-"+ids).modal('show');
}

function openAccountsModal(ids){
    $("#editAccountsModal-"+ids).modal('show');
}


/********************************************************************/
//
/********************************************************************/
function delete_address(ids){    
    $.get("/contacts/delete_address/"+ids+"/", function(data){
        if(data == '1') location.reload();
        else alert("Unauthorized Access");
    });
} 

/********************************************************************/
// 
/********************************************************************/
function delete_accounts(ids){
    $.get("/contacts/delete_accounts/"+ids+"/", function(data){
        if(data == '1') location.reload();
        else alert("Unauthorized Access");
    });
}

/********************************************************************/
// 
/********************************************************************/
function check() {
    if (getLocalStorageValue('form_errors_email') &&
    getLocalStorageValue('form_errors_phone') &&
    getLocalStorageValue('form_errors_pan') &&
    getLocalStorageValue('form_errors_gst') &&
    getLocalStorageValue('form_errors_url') &&
    getLocalStorageValue('form_errors_ifsc')){
        $(".save_button").prop("disabled",false);
        return true;
    }else{
        $(".save_button").prop("disabled",true);
        return false;
    } 
    
}

function set_shipping(elem, target_elem){
    if($(elem).prop("checked")){
        $(target_elem).val(1);
    }else{
        $(target_elem).val(0);
    }  
}

function set_billing(elem, target_elem){
    if($(elem).prop("checked")){
        $(target_elem).val(1);
    }else{
        $(target_elem).val(0);
    }    
}

/************************************************************ */
// code by Lawrence - Ended
/************************************************************ */


/* Below Code By Roshan*/

/********************************************************************/
// GST NUMBER SHOW AND HIDE
/********************************************************************/
function hide_gst(elem){
    var a = $('#gst_reg :selected').text();
    if(a != "Not Applicable" & a != "GST Unregistered" & a != "Overseas"){
        $("#gst_row").show()
        
        
    }
    else{
        $("#gst_row").hide()
        $("#id_gstin").val("")
    }
}
// Global 
var a = $('#gst_reg :selected').text();
    
    if(a != "Not Applicable" & a != "GST Unregistered"){
        $("#gst_row").show()
        
    }
    else{
        $("#gst_row").hide()
    }


/********************************************************************/
// active, inactive and delete
/********************************************************************/
function status(a,c) {
    var status = 's'+a.toString()
    var remove = 't'+a.toString()
    var b = document.getElementById(status).innerHTML;
    if(b.length == 13){
        $.ajax({
        type: 'GET',
        url: "/contacts/status_change/deactivate/"+a+"",
        success: function() {
            // document.getElementById(a).innerHTML = 'clear'
            // document.getElementById(status).innerHTML = 'Make Active'
            $("#"+remove).hide();
            $('#'+'status'+a.toString()).modal('hide')
            // document.getElementById('text').innerHTML = 'Are you sure you want to make '+c+' active '
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("some error");
        }

    });
    }
    if(b.length == 11){
        $.ajax({
        type: 'GET',
        url: "/contacts/status_change/activate/"+a+"",
        success: function() {
            // document.getElementById(a).innerHTML = 'check'
            // document.getElementById(status).innerHTML = 'Make Inactive'
            $("#"+remove).hide();
            $('#'+'status'+a.toString()).modal('hide')
            // document.getElementById('text').innerHTML = 'Are you sure you want to make '+c+' inactive '
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("some error");
        }

    });
    }    
}
function nodeactive(d) {
$('#'+'status'+d.toString()).modal('hide')
}
function noactive(d) {
$('#'+'status'+d.toString()).modal('hide')
}
// //////////////////////////////////////////////////
// delete and cancel
function remove(c) {
var remove = 't'+c.toString()
$.ajax({
        type: 'GET',
        url: "/contacts/delete/"+c+"",
        success: function() {
            $("#"+remove).hide();
            $('#'+'del'+c.toString()).modal('hide')
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("some error");
        }

    });
}

function can(d) {
$('#'+'del'+d.toString()).modal('hide')
}



/********************************************************************/
// INPUT TYPE NUMBER SROLL HIDE
/********************************************************************/
// Disable Mouse scrolling
$('input[type=number]').on('mousewheel',function(e){ $(this).blur(); });
// Disable keyboard scrolling
$('input[type=number]').on('keydown',function(e) {
    var key = e.charCode || e.keyCode;
    // Disable Up and Down Arrows on Keyboard
    if(key == 38 || key == 40 || key == 69 || key == 189 || key == 43 || key == 187) {
	e.preventDefault();
    } else {
	return;
    }
});
/*code: 48-57 Numbers
			  8  - Backspace,
			  35 - home key, 36 - End key
			  37-40: Arrow keys, 46 - Delete key*/
              function restrictAlphabets(e){
				var x=e.which||e.keycode;
				if((x>=48 && x<=57) || x==8 ||
					(x>=35 && x<=40)|| x==46)
					return true;
				else
					return false;
            }
/********************************************************************/
// INPUT TYPE NUMBER SROLL HIDE
/********************************************************************/

window.addEventListener('load', function() {
    document.querySelector('.contact_attachment').addEventListener('change', function() {

        // image extension validation
        // if (!this.files[0].name.match(/.(jpg|jpeg|png|gif)$/i)){
        //     alert('Please select Image file ');
        //     $('#files').val("");
        // }
        
            //  Image file size less then 1MB
            if(this.files[0].size > 2048000){
                alert('File size less then 2 MB');
                $('#files').val("");
                $('#upload').val('');
            }
            // else if (this.files && this.files[0]) {
            //     var img = document.querySelector('img');  // $('img')[0]
            //     img.src = URL.createObjectURL(this.files[0]); // set src to blob url
            //     $(".close").show()
                
            // }
        
    });
  });

/********************************************************************/
// Edit contact shirk table
/********************************************************************/
tax = 0
function tax2(){
    if(tax == 0){
        $("#tax1").removeClass('fa-plus-circle')
        $("#tax1").addClass('fa-minus-circle')
        tax +=1
    }
    else{
        $("#tax1").removeClass('fa-minus-circle')
        $("#tax1").addClass('fa-plus-circle')
        tax -=1
    }
}

address = 0
function addres(){
    if(address == 0){
        $("#address1").removeClass('fa-plus-circle')
        $("#address1").addClass('fa-minus-circle')
        address +=1
    }
    else{
        $("#address1").removeClass('fa-minus-circle')
        $("#address1").addClass('fa-plus-circle')
        address -=1
    }
}

account = 0
function acount(){
    if(account == 0){
        $("#account1").removeClass('fa-plus-circle')
        $("#account1").addClass('fa-minus-circle')
        account +=1
    }
    else{
        $("#account1").removeClass('fa-minus-circle')
        $("#account1").addClass('fa-plus-circle')
        account -=1
    }
}

other = 0
function othe(){
    if(other == 0){
        $("#other1").removeClass('fa-plus-circle')
        $("#other1").addClass('fa-minus-circle')
        other +=1
    }
    else{
        $("#other1").removeClass('fa-minus-circle')
        $("#other1").addClass('fa-plus-circle')
        other -=1
    }
}

social = 0
function soc(){
    if(social == 0){
        $("#social1").removeClass('fa-plus-circle')
        $("#social1").addClass('fa-minus-circle')
        social +=1
    }
    else{
        $("#social1").removeClass('fa-minus-circle')
        $("#social1").addClass('fa-plus-circle')
        social -=1
    }
}
/********************************************************************/
// contact_name and contact_display_name equal
/********************************************************************/

$('#id_contact_name').keyup(function(){
    var con_name = $(this).val()
    $('#id_display_name').val(con_name)
});

/*********************************************************************************/
// contact organization type if not individul then organization name require 
/*********************************************************************************/

$('#id_organization_type').change(function(){
    if($(this).val() == '1'){

        $('#id_organization_name').prop('required', false)
    }
    else if($(this).val() != '1'){

        $('#id_organization_name').prop('required', true)
    }
});

/*********************************************************************************/
// File preview
/*********************************************************************************/
$(document).ready(function(){
    $('#files').change(function(){
        $('#files').css('width','100%')
        $('#contact_file_preview').hide()
    });
});

/*********************************************************************************/
// opening Balance float value
/*********************************************************************************/

$('#id_opening_balance').keypress(function(event) { 
    var $this = $(this);
    if ((event.which != 46 || $this.val().indexOf('.') != -1) &&
       ((event.which < 48 || event.which > 57) &&
       (event.which != 0 && event.which != 8))) {
           event.preventDefault();
    }

    var text = $(this).val();
    if ((event.which == 46) && (text.indexOf('.') == -1)) {
        setTimeout(function() {
            if ($this.val().substring($this.val().indexOf('.')).length > 3) {
                $this.val($this.val().substring(0, $this.val().indexOf('.') + 3));
            }
        }, 1);
    }

    if ((text.indexOf('.') != -1) &&
        (text.substring(text.indexOf('.')).length > 2) &&
        (event.which != 0 && event.which != 8) &&
        ($(this)[0].selectionStart >= text.length - 2)) {
            event.preventDefault();
    }      
});


/**/



function set_default_address(elem){
	
	if($(elem).prop("checked")){
		c_box = confirm('Do you really want to set this address as a default');
	
		if(c_box){	
			$("select.default_address").val("False");
			$(elem).closest("td").find("select").val("True");
			$("input.default_address_checkbox").prop("checked",false);
			$(elem).closest("td").find("input").prop("checked",true);
		}else{
			$("input.default_address_checkbox").prop("checked",false);	
		}
	}else{
		c_box = confirm('Do you really want to remove this address from default');
		if(c_box){
			$(elem).closest("td").find("select").val("False");	
			$(elem).closest("td").find("select").val("False");
			$("input.default_address_checkbox").prop("checked",false);			
		}
	}
	
	
}