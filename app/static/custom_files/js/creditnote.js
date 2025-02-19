
/************************************************************ */
// DATE PICKER
/************************************************************ */
$("#CreditNoteDate").datepicker({dateFormat: 'dd-mm-yy'}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");
$("#edit_CreditNoteDate").datepicker({dateFormat: 'dd-mm-yy'});
// $("#CreditNoteDate").val(date)

/********************************************************************/
//  Datepicker validation
/********************************************************************/

$("#CreditNoteDate,#edit_CreditNoteDate").on('change', function(event){
    if($(this).val() != ''){
        dateValidation($(this));
    }
});

function dateValidation(element){
    var date = $(element).val();
    var regEx = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
    if(!regEx.test(date)){
        alert('Invalid Date');
        $(element).val('');
    }
}
$('#Journalentrydate,#edit_Journalentrydate').keypress(function(event) {
    event.preventDefault();
});

/************************************************************ */
// PRODUCT ROW ADD/REMOVE
/************************************************************ */

var creditnote_number = 1
var count = 0
function creditnote_addRow(a) {
    if(count == 0){
        creditnote_number +=a
        count +=1
    }

    creditnote_number += 1

    $(document).on('click','#select2-ItemName'+creditnote_number+'-container',function(){
        for(var i = 1;i <= creditnote_number; i++){
            var a = $('#row_ItemName'+creditnote_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link credit_product" data-toggle="modal" id="row_ItemName'+creditnote_number+'" onclick="get_credit_product_id('+creditnote_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
            }  
        } 
    });
    $(document).on('click','#select2-product_account'+creditnote_number+'-container',function(){
            
        for(var i = 1;i <= creditnote_number; i++){
            var a = $('#row_account'+creditnote_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link credit_account" data-toggle="modal" id="row_account'+invoice_number+'" onclick="get_credit_account_id('+invoice_number+'),acc_product_account" data-target="#addGroupModal" style="margin-left: -24%;">+ Add New</button>');
            }  
        } 
    });
    var state = $("#supplyPlace1").val()
    var org_state = $('#single_gst_code option:selected').text()
    var html = '<tr id="creditnote_row'+creditnote_number+'">'
    html +='<td style="border:1px solid black;padding-bottom:0%"><select class="form-control select credit_note_item" id="ItemName'+creditnote_number+'" name="ItemName[]" onchange="product('+creditnote_number+')" style="padding-left:0px" required><option value="-------">None</option></select>'
    html +='<textarea id="desc'+creditnote_number+'" name="desc[]" rows="2" maxlength="200" size="200" placeholder="Product Description" style="width: 190.6px;margin-top:1px;"></textarea></td>'
    html +='<td style="border:1px solid black;"><select class="form-control product_credit_account" id="product_account'+creditnote_number+'" name="product_account[]" required><option value="-------">None</option></select></td>'
    html +='<td style="border:1px solid black;"><div class="row" style="margin-top:-5px"><div class="col-1" style="padding-right:0%"><label for="Price'+creditnote_number+'" style="margin-top:5px">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control" maxlength="10" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+')" id="Price'+creditnote_number+'" name="Price[]" style="margin-top:8%" required></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col" style="padding-right:0px"><input type="text" class="form-control" id="Quantity'+creditnote_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+')" name="Quantity[]" style="margin-top:-5px" required></div>'
    html +='<div class="col" style="padding-left:0px"><input class="form-control" id="Unit'+creditnote_number+'" name="Unit[]" style="padding-left:0px;margin-top:-4px" readonly></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row" style="margin-top:-5px"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control all_discount" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+')" id="Discount'+creditnote_number+'" name="Discount[]"></div>'
    html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+creditnote_number+'" name="Dis[]" onchange="dicount_type('+creditnote_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax_list'+creditnote_number+'" class="form-control tax" maxlength="5" size="5" onkeyup="row_gst_cal('+creditnote_number+')" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+creditnote_number+'\')" name="tax[]" id="tax'+creditnote_number+'" style="margin-top:-1px" readonly><datalist id="tax_list'+creditnote_number+'"></datalist></div>'
    html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: black;">%</font></div></div></td>'
    if(org_state != '' || state != '' || org_state.toLowerCase() == state.toLowerCase() || $('#org_gst_reg_type').val() == ''){
        html += '<td class="row_cs_gst" style="border:1px solid black;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+creditnote_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+creditnote_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;display:none;" style="margin-top: 4px;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+creditnote_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'
    }else if(org_state.toLowerCase() != state.toLowerCase()){
        html += '<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+creditnote_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+creditnote_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+creditnote_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+creditnote_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'    
    }
    html +='<td style="border:1px solid black;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right:0%"><label for="Amount'+creditnote_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount" id="Amount'+creditnote_number+'" name="Amount[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row" style="margin-top: 4px;"><div class="col-1" style="padding-right:0%"><label for="Amount_inc'+creditnote_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount_inc" id="Amount_inc'+creditnote_number+'" name="Amount_inc[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+creditnote_number+'" name="'+creditnote_number+'" onclick=" return creditnote_removeRow('+creditnote_number+')" style="cursor: default;">delete_forever</span></td></tr>'
        $('#creditnote_table').append(html)
        
        // SELECT PLUGIN
        $(function () {
            $(".select").select2();
          });

        $(function () {
            $(".product_credit_account").select2();
            $('.select2-container--default').css('padding-bottom','16px')

        });
        // 

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
        
        //   AJAX TO FETCH PRODUCT
        $.ajax({
            type:"GET",
            url: "/creditnotes/add/"+1+"/NA/",
            dataType: "json",
            success: function(data){
        
                var option = data.products
                // var unit = data.unit
                var id = data.ids
                for(var i = 0;i < option.length;i++){
                    $('<option/>').val(id[i]).html(option[i]).appendTo('#ItemName'+creditnote_number+'');
                }

                // account
                var acc_option = data.acc_group_name;
                var acc_id = data.acc_ids;
                for(var i = 0;i < acc_option.length;i++){
                    $('<option/>').val(acc_id[i]).html(acc_option[i]).appendTo('#product_account'+creditnote_number+'');
                }

                check_gst_status('vendor_side')
                // for(var i = 0;i < unit.length;i++){
                //     $('<option/>').val(unit[i]).html(unit[i]).appendTo('#Unit'+number+'');
                // }

                if(data.gst.length > 0){
                    var tax_option = data.gst
                    var tax_htm 
                    for(var k = 0; k < tax_option.length; k++){ 
                        tax_htm += '<option value="'+tax_option[k]+'">'; 
                    }
                    $('#tax_list'+creditnote_number).empty().append(tax_htm)
                }
            },
        });
    
};
// REMOVE JS TABLE
function creditnote_removeRow(a) {
    var first_row = $('#creditnote_table tbody tr:first').attr('id')
    if(first_row == 'creditnote_row'+a+''){
        var last_row = $('#creditnote_table tbody tr:last').attr('id')
        if(last_row != 'creditnote_row'+a+''){
            $('#creditnote_row'+a+'').remove();
        }else{
            $('#ItemName'+a+'').val('-------').change();
            $('#product_account'+a+'').val('-------').change();
        }
    }else{
        $('#creditnote_row'+a+'').remove();
    }
    validation()
}

/************************************************************ */
// GET CONTACT DETAILS
/************************************************************ */

function data() {
    var contact = $('#customerName option').filter(':selected').val()
    if(contact !=''){
        $.ajax({
            type:"GET",
            url: "/creditnote/contact/"+contact+"",
            dataType: "json",
            success: function(data){
                $("#email").val(data.contacts)
                var option = data.address
                // CLEAN SELECT OPTION //
                // var select = document.getElementById('BillingAddress');
                // var length = select.options.length;
                // if(length > 0){
                //     $("#BillingAddress").empty();
                // }
    
                // ADD SELECT OPTION //
                // for(var i = 0;i < option.length;i++){
                //     if(i == 0){
                //         $('<option/>').val(option[i]).html(option[i]).appendTo('#BillingAddress');
                //         $('#BillingAddress1').val(option[i])
                //     }else{
                //         $('<option/>').val(option[i]).html(option[i]).appendTo('#BillingAddress');
                //     }
                    
                // }
                // END //
                $('#BillingAddress1').text(option)
            },
        });
    }
    else{
        $('#BillingAddress1').val('')
        $("#BillingAddress").empty();
    }
};

/************************************************************ */
// DEFUALT CREDIT NOTE AND CHECK CREDIT NOT IS UNIQUE
/************************************************************ */
$("#creditnote_number_default").click(function(){
    if($(this).is(':checked')){
        var ins = 0
    var slug = 'a'
    $.ajax({
        type:"GET",
        url: "/creditnote/unique_number/"+ins+"/"+slug+"/",
        dataType: "json",
        success: function(data){
            $('#CreditNoteNumber').val(data.credit_number)
        },
        error: function (rs, e) {
            alert('Sorry, try again.');
        }
    });
    }else{
        $('#CreditNoteNumber').val('')
    }  
});

$("#CreditNoteNumber").focusout(function(){
    $("#creditnote_number_default").prop('checked',false);
    var ins = 1
    var credit_number = $("#CreditNoteNumber").val()
    $.ajax({
        type:"GET",
        url: "/creditnote/unique_number/"+ins+"/"+credit_number+"/",
        dataType: "json",
        success: function(data){
            if(data.unique != 0){
                alert('This credit note number is already exits. Please enter the different credit note number.')
                $('#CreditNoteNumber').focus();
                $('#CreditNoteNumber').val('')
            }
            
        },
    });
  });
  
/************************************************************ */
// FETCH PRODUCT type/unit/price/product description/currency
/************************************************************ */
function product(a) {
    var product = $('#ItemName'+a+' option').filter(':selected').val()
    //  $('#customerName :selected').text();
    if(product != "-------"){
        $.ajax({
            type:"GET",
            url: "/creditnote/product/"+product+"",
            dataType: "json",
            success: function(data){
                $("#desc"+a+"").val(data.desc)
                // if(data.product == 0){
                //     $("#type"+a+"").val("GOODS")
                // }
                // else if(data.product == 1){
                //     $("#type"+a+"").val("SERVICES")
                // }
                // else{
                //     $("#type"+a+"").val("BUNDLE")
                // }
                $("#Price"+a+"").val(parseFloat(data.price).toFixed(2))
    
                $("#Unit"+a+"").val(data.unit)

                $("#Quantity"+a+"").val("")
                $("#Discount"+a+"").val("")
                // $("#tax"+a+"").val("")
                 // include tax
                if(data.is_check_selling == 'no' || $("#tax"+a+"").is('[readonly]') ){
                    $("#tax"+a+"").val("")
                    }else{
                    $("#tax"+a+"").val(data.selling_tax)
                    }
                $("#Amount"+a+"").val("")
                sub_total()
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }
    else{
        $("#desc"+a+"").val("")
        // $("#type"+a+"").val("")
        $('#product_account'+a+'').val('-------').change();
        $("#Price"+a+"").val("")
        $("#Unit"+a+"").val("")
        $("#Quantity"+a+"").val("")
        $("#Discount"+a+"").val("")
        $("#tax"+a+"").val("")
        $("#Amount"+a+"").val("")
        sub_total()
    }
   
};

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
    // if ([69, 187, 188, 189, 190].includes(e.keyCode)) {
    //     e.preventDefault();
    //   }
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
//  SHOW AND HIDE EMAIL CC
/********************************************************************/

// SHOW EMAIL CC
function show_cc_mail() {
    $(".ccemail").show()
    $('#show_cc').hide()
  }

// HIDE EMAIL CC
function hide_cc_mail() {
    $(".ccemail").hide()
    $("#ccemail").val('')
    $('#show_cc').show()
  }

/********************************************************************/
// CELAN ATTACHEMENT
/********************************************************************/
function clean(){
    $("#Attachment").val('')
    $('#creditnote_filename').text('')
    $('#attach_check').prop('checked',false);
}

/********************************************************************/
// change ATTACHEMENT
/********************************************************************/

$(document).ready(function(){
    $('#Attachment').change(function(e){
        $('#creditnote_filename').hide()
        $(this).css('width','70%')
    });
});
/********************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".credit_note_item").select2();
      });
    });

    // select2-ItemName1-container

$(document).on('click','#select2-ItemName1-container',function(){
    for(var i = 1;i <= creditnote_number; i++){
        var a = $('#row_ItemName'+creditnote_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link credit_product" data-toggle="modal" id="row_ItemName'+creditnote_number+'" onclick="get_credit_product_id('+creditnote_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
        }  
    } 
});

function c(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".credit_note_item").select2();
          });
        });
}
function get_credit_product_id(ids){
    prefill_creditnote_product = ids

}
var prefill_creditnote_product 

/********************************************************************/
// CREDIT_NOTE LINE ITEMS(ACCOUNT) SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".product_credit_account").select2();
        $('.select2-container--default').css('padding-bottom','16px')
      });
    });

$(document).on('click','#select2-product_account1-container',function(){
    
    for(var i = 1;i <= creditnote_number; i++){
        var a = $('#row_account'+creditnote_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link credit_account" data-toggle="modal" id="row_account'+creditnote_number+'" onclick="get_credit_account_id('+creditnote_number+'),acc_product_account()" data-target="#addGroupModal" style="margin-left: -34%;">+ Add New</button>');
        }  
    } 
});

function acc_product_account(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".product_credit_account").select2();
          });
        });
}
function get_credit_account_id(ids){
    prefill_credit_account = ids

}
var prefill_credit_account 
/********************************************************************/
// CALCULATION
/********************************************************************/

function creditnote_calculate(a){
    var price = $("#Price"+a+"").val();
    var quantity = $("#Quantity"+a+"").val();
    var discount = $("#Discount"+a+"").val();
    var dis_type = $("#Dis"+a+"").val();
    var tax = $("#tax"+a+"").val();
    if(quantity != '' & quantity != '0'){
        var val = parseFloat(price) * parseFloat(quantity)
        if(dis_type == '%'){
            if(discount == '' || discount == '0' || discount == '0.0'){
                if(price == '' || price == '0.0' || price == '0.0'){
                    $("#Amount"+a+"").val('')
                    sub_total()
                }else{
                    $("#Amount"+a+"").val(parseFloat(val).toFixed(2))
                    sub_total()
                }   
            }
            else if(parseFloat(discount).toFixed(2) <= parseFloat(100.00)){
                var cal = (parseFloat(val) - (parseFloat(val) * (parseFloat(discount) / 100))).toFixed(2);
                if(price == '' || price == '0.0'){
                    $("#Amount"+a+"").val('')
                    sub_total()
                }else{
                    $("#Amount"+a+"").val(parseFloat(cal).toFixed(2))
                    sub_total()
                }
            }else{
                alert('Please enter valid value')
                $("#Discount"+a+"").val('');
                creditnote_calculate(a)
            }
        }
        else if(dis_type == '₹'){
            if(discount == '' || discount == '0' || discount == '0.0'){
                if(price == '' || price == '0.0' || price == '0'){
                    $("#Amount"+a+"").val('')
                    sub_total()
                }else{
                    $("#Amount"+a+"").val(parseFloat(val).toFixed(2))
                    sub_total()
                }   
            }
            else if (parseFloat(discount).toFixed(2) <= parseFloat(val)){
                var cal = (parseFloat(val) - parseFloat(discount)).toFixed(2);
                if(price == '' || price == '0.0'){
                    $("#Amount"+a+"").val('')
                    sub_total()
                }else{
                    $("#Amount"+a+"").val(parseFloat(cal).toFixed(2))
                    sub_total()
                }
            }else{
                alert('Please enter valid value')
                $("#Discount"+a+"").val('');
                creditnote_calculate(a)
            } 
        }  
    }	
    else{
        $("#Amount"+a+"").val('')
        sub_total()
    }
}

function dicount_type(a){
    creditnote_calculate(a)
}

function sub_total(){
    var sub_total = 0
    if ($('#blank_credit_toggle').is(":checked")){
            var sub = $('#blank_amount').val()
            if(sub == ''){
                sub_total += 0
            }
            else{
                sub_total +=  parseFloat(sub)
            }
    }
    else{
        $(".amount").each(function(){

            var a = $(this).val()
            if(a == ''){
                sub_total += 0
            }
            else{
                sub_total +=  parseFloat(a)
            }
        });
    }
    if(parseFloat(sub_total) != 0.00 ){
        $("#SubTotal").val(parseFloat(sub_total).toFixed(2))
    }else{
        $("#SubTotal").val('')
    }
    change_state()
}
/********************************************************************/
// CHECK GST STATUS FOR APPLY
/********************************************************************/

function check_gst_status(category){
    var state = $('#supplyPlace1').val()
    var org_state = $('#single_gst_code option:selected').text()
    if(category == 'user_side'){
        // org gst not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == ''){
            $('#creditnote_table').find('.tax').attr('readonly', true)
            $('#creditnote_table').find('.tax').val('')
            sub_total()
            // if(global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5'|| global_gst_type == ''){
            //     alert('tax not apply beacuse customer not select or customer is not gst register')
            // }else{
                alert('Organization not register GST')
            // }
        // org gst register
        }else if($('#org_gst_reg_type').val() == '1' || $('#org_gst_reg_type').val() == '2' ||$('#org_gst_reg_type').val() == '4' ||$('#org_gst_reg_type').val() == '6' || $('#org_gst_reg_type').val() == '7'){
            if(org_state !='' & state != ''){
                $('#creditnote_table').find('.tax').attr('readonly', false)
                sub_total()
            }
            else{
                $('#creditnote_table').find('.tax').attr('readonly', true)
                $('#creditnote_table').find('.tax').val('')
                sub_total()
            }
        // org in composite
        }else if($('#org_gst_reg_type').val()  == '8'){
            if( org_state !='' & state != '' & org_state.toLowerCase() == state.toLowerCase()){
                $('#creditnote_table').find('.tax').attr('readonly', false)
                sub_total()
            }else{
                $('#creditnote_table').find('.tax').attr('readonly', true)
                $('#creditnote_table').find('.tax').val('')
                sub_total()
                alert('Organization is register under composite scheme,is you choose different state of state tax will not be calculated.')
            }
        }
    }else if(category == 'vendor_side'){
        // org gst not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == ''){
            $('#creditnote_table').find('.tax').attr('readonly', true)
            $('#creditnote_table').find('.tax').val('')
            sub_total()
            // if(global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5'|| global_gst_type == ''){
            //     alert('tax not apply beacuse customer not select or customer is not gst register')
            // }else{
            //     alert('Organization not register GST')
            // }
        // org gst register
        }else if($('#org_gst_reg_type').val() == '1' || $('#org_gst_reg_type').val() == '2' ||$('#org_gst_reg_type').val() == '4' ||$('#org_gst_reg_type').val() == '6' || $('#org_gst_reg_type').val() == '7'){
            if(org_state !='' & state != ''){
                $('#creditnote_table').find('.tax').attr('readonly', false)
                sub_total()
            }
            else{
                $('#creditnote_table').find('.tax').attr('readonly', true)
                $('#creditnote_table').find('.tax').val('')
                sub_total()
            }
        // org in composite
        }else if($('#org_gst_reg_type').val()  == '8'){
            if( org_state !='' & state != '' & org_state.toLowerCase() == state.toLowerCase()){
                $('#creditnote_table').find('.tax').attr('readonly', false)
                sub_total()
            }else{
                $('#creditnote_table').find('.tax').attr('readonly', true)
                $('#creditnote_table').find('.tax').val('')
                sub_total()
                // alert('Organization is register under composite scheme,is you choose different state of state tax will not be calculated.')
            }
        }
    }
}

var global_gst_type = ''
function customer_gst_type(){
    var ins = $('#customerName').val()
    if(ins != ''){
        $.get("/invoice/customer_gst/"+ins+"/",function(data){
            global_gst_type = data.gst_type
            check_gst_status('user_side')
        });
    }else{
        global_gst_type = ''
        check_gst_status('user_side')
    }
}
/********************************************************************/
// CREDIT_NOTE SGST CGST AND IGST CALCULATION 
/********************************************************************/

    // $.ajax({
    //     type:"GET",
    //     url: "/creditnote/state_compare/",
    //     dataType: "json",
    //     success: function(data){
    //         credit_note_user_state = data.state
    //     },  
    // });


// creditnote_tax_cacultion()
// sub_total()
function creditnote_tax_cacultion(){
    var state = $('#supplyPlace1').val()
    var org_state = $('#single_gst_code option:selected').text()
    var csgst = 0
    var igst = 0

    if(org_state.toLowerCase() == state.toLowerCase()){
        $(".tax").each(function(){
            var tax_id = $(this).attr('id');
            var amount_id = 'Amount'+tax_id.slice(3)+''

            var tax_val = (parseFloat($('#'+amount_id+'').val()) * (parseFloat($('#'+tax_id+'').val()) / 100)).toFixed(2);
            var half = (parseFloat(tax_val)/2).toFixed(2);
            if(half != 'NaN'){
                csgst += parseFloat(half)
            }   
        });
        if(csgst != 0 & csgst != 0.0){
            $('#CGST').val(parseFloat(csgst).toFixed(2))
            $('#SGST').val(parseFloat(csgst).toFixed(2))
            $('#cs_gst').show()
        }else{
            $('#CGST').val('')
            $('#SGST').val('')
            $('#cs_gst').hide()
        }
            $('#i_gst').hide()
            $('#IGST').val('')

        var sub_total = $('#SubTotal').val()
        
        var sc_total = (parseFloat(sub_total) + parseFloat(csgst) + parseFloat(csgst)).toFixed(2)
        if(sc_total == 'NaN'){
            $('#Total').val('')
        }else{
            $('#Total').val(sc_total)
        }
        
    }
    else if(org_state.toLowerCase() != state.toLowerCase()){
        $(".tax").each(function(){
            var tax_id = $(this).attr('id');
            var amount_id = 'Amount'+tax_id.slice(3)+''
            var tax_val = (parseFloat($('#'+amount_id+'').val()) * (parseFloat($('#'+tax_id+'').val()) / 100)).toFixed(2);
            if(tax_val != 'NaN'){
                igst += parseFloat(tax_val)
            }
        });
        if(igst != 0 & igst != 0.0){
            $('#IGST').val(parseFloat(igst).toFixed(2))
            $('#i_gst').show()
        }else{
            $('#IGST').val()
            $('#i_gst').hide()
        }
        $('#cs_gst').hide()
        $('#CGST').val('')
        $('#SGST').val('')

        var sub_total = $('#SubTotal').val()
        var i_total = (parseFloat(sub_total) + parseFloat(igst)).toFixed(2)
        if(i_total == 'NaN'){
            $('#Total').val('')
        }
        else{
            $('#Total').val(i_total)
        }
    }
}
/********************************************************************/
// CHANGE CGST SGST TO IGST
/********************************************************************/

function change_state(){
    var state = $('#supplyPlace1').val()
    var org_state = $('#single_gst_code option:selected').text()
    if(org_state != '' & state != ''){
        if(org_state.toLowerCase() == state.toLowerCase() || $('#org_gst_reg_type').val() == ''){
            $('#creditnote_table').find('.row_i_gst').hide()
            $('#creditnote_table').find('.row_igst').val('')
            $('#creditnote_table').find('.row_cs_gst').show()
            $('#creditnote_table').find('.price_header').css('width','7%')
            // $('#creditnote_table').find('.unit_header').css('width','11%')
            $('#creditnote_table').find('.quantity_header').css('width','13%')
            $('#creditnote_table').find('.tax_header').css('width','7%')
        }else if(org_state.toLowerCase() != state.toLowerCase()){
            $('#creditnote_table').find('.row_cs_gst').hide()
            $('#creditnote_table').find('.row_cgst, .row_sgst').val('')
            $('#creditnote_table').find('.row_i_gst').show()
            $('#creditnote_table').find('.price_header').css('width','8%')
            // $('#creditnote_table').find('.unit_header').css('width','12%')
            $('#creditnote_table').find('.quantity_header').css('width','13%')
            $('#creditnote_table').find('.tax_header').css('width','8%')
        }
    }
    $(".credit_note_item").each(function(){

        var ids = $(this).attr('id');
        ids = ids.match(/\d+/);
        ids = ids[0]
        // ids = ids.substring(ids.length - 1, ids.length);
        single_row_gst_cal = 'state'
        var check = row_gst_cal(ids);
    });
    creditnote_tax_cacultion()
}
/********************************************************************/
// EACH ROW TAX CALCULATION
/********************************************************************/

var single_row_gst_cal = ''
function row_gst_cal(ids){
    var state = $('#supplyPlace1').val()
    var org_state = $('#single_gst_code option:selected').text()
    if($('#tax'+ids+'').val() < parseFloat(100.00)){
        var gst =  (parseFloat($('#Amount'+ids+'').val()) * (parseFloat($('#tax'+ids+'').val()) / 100));
        var amount = $('#Amount'+ids+'').val()
        var incl_tax = parseFloat(amount) + parseFloat(gst)
        if(org_state.toLowerCase() == state.toLowerCase()){
            var half = (parseFloat(gst)/2).toFixed(2);

            if(half != 'NaN' & half != 0 & half != 0 & half != 0.0 & half != 0.0){
                $('#row_cgst'+ids+'').val(half)
                $('#row_sgst'+ids+'').val(half)
                $('#Amount_inc'+ids+'').val()
            }else{
                $('#row_cgst'+ids+'').val('')
                $('#row_sgst'+ids+'').val('')
            }
        }else if(org_state.toLowerCase() != state.toLowerCase()){
            if(gst.toString() != 'NaN' & gst != 0 & gst != 0 & gst != 0.0 & gst != 0.0){
                $('#row_igst'+ids+'').val((parseFloat(gst)).toFixed(2))
            }else{
                $('#row_igst'+ids+'').val('')
            }
        }

        if(incl_tax.toString() != 'NaN' & incl_tax != 0 & incl_tax != 0 & incl_tax != 0.0 & incl_tax != 0.0){
            $('#Amount_inc'+ids+'').val(parseFloat(incl_tax).toFixed(2))
        }else{
            $('#Amount_inc'+ids+'').val('')
        }
    
        if(single_row_gst_cal == 'state'){
            single_row_gst_cal = ''
            var complete = 'done'
            return complete
        }else{
            creditnote_tax_cacultion()
        }
    }else{
        alert('Please enter valid Tax value')
        $('#tax'+ids+'').val('')
    }
}
/********************************************************************/
// product table validation
/********************************************************************/
var message = ''
$(document).ready(function(){
    validation()
});
function validation(){
    var count = $('#creditnote_table tbody tr').length
    var row_ids = $('#creditnote_table tbody tr:first').attr('id')
    // var last_row = $('#purchase_table tbody tr:first').attr('id')
    // var first_row =  $('#purchase_table tbody tr:first').attr('id')
    var number_of_row_blank = 1
    for(var i = 1; i<=count;i++){
        var row_last_str = row_ids.substring(row_ids.length-1,row_ids.length)
        
        if($('#ItemName'+row_last_str).val() == '' & $('#product_account'+row_last_str).val() == '' & $('#Price'+row_last_str).val() == '' & $('#Quantity'+row_last_str).val() == ''){
            if(number_of_row_blank == count){
                message = 'Please fill the product line item'
            }else{
                message = ''
            }
            number_of_row_blank +=1
        }else{
            if($('#ItemName'+row_last_str).val() == '-------'){
                message = 'Table row '+i+' product/service required'
                break;
            }else if($('#product_account'+row_last_str).val() == '-------'){
                message = 'Table row '+i+' product account required'
                break;
            }else if($('#Price'+row_last_str).val() == '' || parseFloat($('#Price'+row_last_str).val()).toFixed(2) == 0){
                message = 'Table row '+i+' product price required'
                break; 
            }else if($('#Quantity'+row_last_str).val() == '' || parseFloat($('#Quantity'+row_last_str).val()).toFixed(2) == 0){
                message = 'Table row '+i+' product qunatity required'
                break; 
            }else{
                message = ''
            }
        }
        row_ids = $('#'+row_ids+'').closest('tr').next('tr').attr('id');
    }
    
}
// function validation(){
//     for(var i = 1;i <= creditnote_number;i++){
//         message = ''
//         var product_name = $("#ItemName"+i+"").val()
//         var product_type =  $("#type"+i+"").val()
//         // var invoice = $("#Reference").val()
//         if( product_name != '-------' ){
//             var unit = $("#Unit"+i+"").val()
//             var quantity = $("#Quantity"+i+"").val()
//             var price = $("#Price"+i+"").val()
//             if(quantity == '' || quantity == '0'){
//                 message += 'Table row number '+i+':- fill quantity'
//                 break;
//             }
//             else if(unit == '-------'){
//                 message += 'Table row number '+i+':- choose unit'
//                 break;
//             }
//             else if(price == '' || price == '0.0'){
//                 message = 'Table row number '+i+':- fill price'
//                 break;
//             }

//         }
//     }
// }

function  sendbtn(){
    var a = $("#email").val()
    var b = $("#customerName").val()
    if(b == ''){
        alert('Contact name required')
        return false
    }
    else if($('#creditnote_table').is(":visible")){
        if(message != ''){
            alert(message)
            return false
        }
    }else if(a == ''){
        alert('Please fill email')
        return false
    }
    else{
        
        return true
    }
}

function savebtn(){
    var b = $("#customerName").val()
    if(b == ''){
        alert('Contact name required')
        return false
    }
    else if($('#creditnote_table').is(":visible")){
        if(message != ''){
            alert(message)
            return false
        }
    }
    else{
        
        return true
    }
}

function draftbtn(){
    var b = $("#customerName").val()
    if(b == ''){
        alert('Contact name required')
        return false
    }
    else if($('creditnote_table').is(":visible")){
        if(message != ''){
            alert(message)
            return false
        }
    }
    else{
        
        return true
    }
}

/********************************************************************/
// IF INVOICE REFENECE NUMBER FILL
/********************************************************************/

// function invoice_num(){
//     validation()
// }

/********************************************************************/
// CHOOSE FILE SIZE VALIDATION
/********************************************************************/

window.addEventListener('load', function() {
    document.querySelector('#Attachment').addEventListener('change', function() {
        
            //  Image file size less then 1MB
            if(this.files[0].size > 20000000){
                alert('File size less then 20MB');
                $('#Attachment').val("");
                
            }
        
    });
  });

/********************************************************************/
// SWITCH TOGGLE ON /OFF FOR ATTACHEMENT
/********************************************************************/

$("#attach_check").click(function(){
    var attach = $('#Attachment').val()
    if($(this).is(':checked')){
        var mail = $('#email').val()
        if(mail.length == 0){
            alert('Please first enter the maill address.')
            $('#email').focus();
            $('#attach_check').prop('checked',false);
            
        }else if(attach.length == 0){
            alert('Please first choose the file.')
            $('#Attachment').focus();
            $('#attach_check').prop('checked',false);
        }

    }
});

/********************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG CONTACT NAME
/********************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#customerName").select2();
      });
    });
$(document).on('click','#select2-customerName-container',function(){

    $(".credit_product").hide()
    var a = $('#addcontact').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact()" id="addcontact" data-target="#ContactModal" style="margin-left: -11%;">+ Add Contact</button>');
        }
        });
function add_contact(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#customerName").select2();
          });
        });

        $('#id_customer_type').remove()
        var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
        html+='<option value="1" selected="">CUSTOMER</option>'
        html +='<option value="2">VENDOR</option>'
        html+='<option value="3">EMPLOYEE</option>'
        html +='<option value="4">CUSTOMER AND VENDOR</select>'
       $('#con_type').append(html)
}

/********************************************************************/
// CREDIT_NOTE PRODUCT MODEL SAVE USING AJAX
/********************************************************************/


function creditnote_product_form(save_type){
	form_d = $("#add_creditnote_product_form")[0];

    var formData = new FormData(form_d);
    if($('#id_product_type').val() == ''){
        alert('Product type is requried')
        $('#id_product_type').focus()
        return false
    }else if($('#id_product_category').val() == ''){
        alert('product category is requried')
        $('#id_product_category').focus()
        return false
    }else if($('#id_sku').val() == ''){
        alert('sku/product id is requried')
        $('#id_sku').focus()
        return false
    }else if($('#id_product_name').val() == ''){
        alert('product name is requried')
        $('#id_product_name').focus()
        return false
    }

    if($('#id_is_sales').is(":checked")){
        if($('#id_selling_price').val() == ''){
            alert('Selling price is requried')
            $('#id_selling_price').focus()
            return false
        }else if($('#id_selling_tax').val() == ''){
            alert('Tax is requried')
            $('#id_selling_tax').focus()
            return false
        }else if($('#id_sales_account').val() == ''){
            alert('Selling account is requried')
            $('#id_sales_account').focus()
            return false
        }
    }
    
    if($('#id_is_purchase').is(":checked")){
        if($('#id_purchase_price').val() == ''){
            alert('Purchase price is requried')
            $('#id_purchase_price').focus()
            return false
        }else if($('#id_purchase_tax').val() == ''){
            alert('Tax is requried')
            $('#id_purchase_tax').focus()
            return false
        }else if($('#id_purchase_account').val() == ''){
            alert('Expense account is requried')
            $('#id_purchase_account').focus()
            return false
        }
    }

    $.ajax({
        type: 'POST',
        url: "/products/add/",
        data:formData,
        cache:false,
        contentType: false,
        processData: false,
        success: function(data) {
            if(data != '0'){
                $.get("/creditnote/product_fetch/",function(data){
                    $(".credit_note_item").each(function(){
                        $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                    });
                    $('#ItemName'+prefill_creditnote_product+'').val(data.ids).change(); 
                    // $('.productDropdown .dd-button').text(data.name);
                    $('#ItemName'+prefill_creditnote_product+'').val(data.ids).change(); 
                });
                $("#ProductModal").modal('hide');
            }
        },
    });
}
/********************************************************************/
// CREDIT_NOTE CONTACT MODEL SAVE USING AJAX
/********************************************************************/
function creditnote_contact_form(save_type){
  
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

    $.post("/contacts/add/",$("#add_creditnote_contact_form").serialize(), function(data){
        if(data != '0'){
            
            $.get("/creditnote/contact_fetch/",function(data){
                $("#customerName").each(function(){
                    $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                });
                // $('#BillingAddress1').val('')
                $('#email').val('')
                $('#customerName').val(data.ids).change(); 
                
            });
            $("#ContactModal").modal('hide');
        }
    });
}
/********************************************************************/
// CREDIT NOTE ACCOUNT_LEDGER(GROUP) MODEL SAVE USING AJAX
/********************************************************************/
function credit_account_ledger_form(save_type){
  
    event.preventDefault()

    if($('#id_group_name').val() == ''){
        alert('group name is requried')
        $('#id_group_name').focus()
        return false
    }

    $.post("/add_ledger_group/",$("#add_group_form").serialize(), function(data){
    if(data != '0'){
        
        $.get("/purchase_order/account_group_fetch/",function(data){

            $(".product_credit_account").each(function(){
                $('<option/>').val(data.ids).html(data.group_name).appendTo($(this));
            });
            $('#product_account'+prefill_credit_account+'').val(data.ids).change(); 
            
        });
        $("#addGroupModal").modal('hide');
    }
  
});
}
/********************************************************************/
// CREDIT_NOTE ITEM CLEAR FIRST ROW
/********************************************************************/

function clear_row(){
    $('#ItemName1').val('-------').change();
}


/*******************************************************************/
// ATTACHMNET WIDTH
/*******************************************************************/

$("#Attachment").change(function(){
    $("#Attachment").css('width','86%');
});
/********************************************************************/
// Blank Credit_note
/********************************************************************/

function balnk_credit(){
    var val = $('#Amount1').val()
    $('#Total').val(val)
}
/********************************************************************/
// CREDIT_NOTE DECIMAL POINT
/********************************************************************/
// $('.Quantity').keypress(function(event) { 
//     var $this = $(this);
//     if ((event.which != 46 || $this.val().indexOf('.') != -1) &&
//        ((event.which < 48 || event.which > 57) &&
//        (event.which != 0 && event.which != 8))) {
//            event.preventDefault();
//     }

//     var text = $(this).val();
//     if ((event.which == 46) && (text.indexOf('.') == -1)) {
//         setTimeout(function() {
//             if ($this.val().substring($this.val().indexOf('.')).length > 3) {
//                 $this.val($this.val().substring(0, $this.val().indexOf('.') + 3));
//             }
//         }, 1);
//     }

//     if ((text.indexOf('.') != -1) &&
//         (text.substring(text.indexOf('.')).length > 2) &&
//         (event.which != 0 && event.which != 8) &&
//         ($(this)[0].selectionStart >= text.length - 2)) {
//             event.preventDefault();
//     }      
// });

function float_value(event, a) { 
    // var $this = $(this);
    
    if ((event.which != 46 || $('#'+a+'').val().indexOf('.') != -1) &&
       ((event.which < 48 || event.which > 57) &&
       (event.which != 0 && event.which != 8))) {
           event.preventDefault();
    }

    var text = $('#'+a+'').val();
    if ((event.which == 46) && (text.indexOf('.') == -1)) {
        setTimeout(function() {
            if ($('#'+a+'').val().substring($('#'+a+'').val().indexOf('.')).length > 3) {
                $('#'+a+'').val($this.val().substring(0, $('#'+a+'').val().indexOf('.') + 3));
            }
        }, 1);
    }

    if ((text.indexOf('.') != -1) &&
        (text.substring(text.indexOf('.')).length > 2) &&
        (event.which != 0 && event.which != 8) &&
        ($('#'+a+'')[0].selectionStart >= text.length - 2)) {
            event.preventDefault();
    }      
};


/********************************************************************/
// INVOICE GST CHANGES
/********************************************************************/

$('#multiple_gst_link').click(function(){

    $.get("/gst_number/", function(data){
        $(".gst_row").each(function(){
                        
            $(this).remove()
        });
        for(var i = 0;i < data.gst_number.length;i++){
            var html = '<tr class="gst_row" id="choose_gst_row_'+i+'"><td style="border:1px solid black;" align="center"><label class="form-check-label" style="margin-left:27%;">'
                html+='<input class="form-check-input choose_gst" type="radio" name="radio" id="choose_gst_'+(parseInt(i)+1)+'" onclick="radio_click($(this))" value="on" style="margin-top:-2%"><span class="circle"><span class="check"></span></span></label></td>'
                html +='<td style="border:1px solid black;" id="c_gst_number'+(parseInt(i)+1)+'" align="center">'+data.gst_number[i]+'</td>'
                html +='<td style="border:1px solid black;display:none;" id="c_gst_type'+(parseInt(i)+1)+'" align="center">'+data.gst_type[i]+'</td>'
                $('#GST_table').append(html)
        }
        $('#invoice_multi_gst').modal('show')
    });
});

/********************************************************************/
// choose GST
/********************************************************************/

function radio_click(elem){
    var names = $(elem).attr('id')
    names = names.substring(names.length-1,names.length)
    $('#org_gst_number').val($('#c_gst_number'+names).text())
    $('#org_gst_reg_type').val($('#c_gst_type'+names).text())
};


function button_click(category){
    if(category = 'multiple'){
        var checkbox_count = 0
        $('.choose_gst').each(function(){
            if($(this).prop("checked") == true){
                checkbox_count +=1
            }
        })
        if(checkbox_count == 0){
            alert('Please first choose the GST')
            return false
        }
        var gst = $('#org_gst_number').val()
        $('#multiple_gst').text("Your default Organization gst number:-"+gst+". Do you want to create this invoice with another GST number.")
        gst = gst.substring(0,2)
		if($("#single_gst_code option[value="+gst+"]").length > 0){

            $('#single_gst_code').val(gst).change()
        }
        check_gst_status('user_side')
        $('#invoice_multi_gst').modal('hide')
    }
}
$(document).ready(function(){
    if($('#org_gst_reg_type') == '8'){
        alert('Organization is register under composite scheme, it can not choose delivery address of different state.')
    }
});
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
                    $('#single_gst_code').val(str).change()
				}
			});
		}else{
			$('#error_field').text('GST state code not matching with existing address state') 
			$('#org_single_gst_save').prop('disabled', true)
		}
	}
}

$('.mul_cancel_gst').click(function(){
	$('#error_field').text('') 
	$('.multiple_update').prop('disabled', false)
})

/********************************************************************/
// GST STATE ADDRESS CHECK
/********************************************************************/

function update_single_gst(){
    event.preventDefault()
    $.post("/profile/gst_configuration/",$("#org_gst_update").serialize(), function(data){
        if(data != '0'){
            var gst_num = $('#single_gst').val()
            $('#org_gst_reg_type').val($('#single_gst_type').val())
            $('#replace_change_update').find('h6').text('Your default Organization gst number:-'+gst_num+'.')
            $('#change_update_gst').hide()
            $('#replace_change_update').show()
            $('#org_gst_number').val(gst_num)
            $('#add_gst_number').modal('hide')
            check_gst_status('user_side')
        }
    });
}

  
/********************************************************************/
//  SHOW AND HIDE balnk table and product line item
/********************************************************************/
function hide_table() {
     if ($('#blank_credit_toggle').is(":checked")){
        c_box = confirm('You want to create blank credit note');
        if(c_box){
            $('#blank_desc').prop('required' ,true)
            $('#blank_amount').prop('required',true)
            $('#blank_creditnote_table').show()
            $('#creditnote_table').hide()
            $('#addrow').hide()
            $("#creditnote_table").find("tr:gt(1)").remove();
            $('.credit_note_item').each(function(){
               var ids = $(this).attr('id')
               ids = ids.match(/\d+/);
               ids = ids[0]
               $('#ItemName'+ids).val('-------').change()
            });
            sub_total()
        }else{
            $('#blank_credit_toggle').prop('checked',false)
        }
     }
     else{
        c_box = confirm('You want to create normal credit note');
        if(c_box){
            $('#blank_desc').prop('required' ,false)
            $('#blank_amount').prop('required',false)
            $('#blank_creditnote_table').hide()
            $('#creditnote_table').show()
            $('#addrow').show()
            $('#blank_desc').val('')
            $('#blank_amount').val('')
            sub_total()
        }else{
            $('#blank_credit_toggle').prop('checked',true)
        }
     }
   }

