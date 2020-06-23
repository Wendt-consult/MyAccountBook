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
//  DECIMAL POINT
/********************************************************************/

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

/************************************************************ */
// PRODUCT ROW ADD/REMOVE
/************************************************************ */

var invoice_number = 1
var count = 0
function invoice_addRow(a) {
    if(count == 0){
        invoice_number +=a
        count +=1
    }

    invoice_number += 1

    $(document).on('click','#select2-ItemName'+invoice_number+'-container',function(){

        for(var i = 1;i <= invoice_number; i++){
            var a = $('#row_ItemName'+invoice_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link purchase_product" data-toggle="modal" id="row_ItemName'+invoice_number+'" onclick="get_invoice_product_id('+invoice_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
            }  
        } 
    });

    $(document).on('click','#select2-product_account'+invoice_number+'-container',function(){

        for(var i = 1;i <= invoice_number; i++){
            var a = $('#row_account'+invoice_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link purchase_account" data-toggle="modal" id="row_account'+invoice_number+'" onclick="get_invoice_account_id('+invoice_number+'),c()" data-target="#addGroupModal" style="margin-left: -24%;">+ Add New</button>');
            }  
        } 
    });
       
        var html = '<tr id="invoice_row'+invoice_number+'">'
        html +='<td style="border:1px solid white;padding-bottom:0%"><select class="form-control select purchase_line_item" id="ItemName'+invoice_number+'" name="ItemName[]" onchange="product('+invoice_number+')" style="padding-left:0px" required><option value="">-------</option></select>'
        html +='<textarea id="desc'+invoice_number+'" name="desc[]" rows="2" maxlength="200" size="200" placeholder="Product Describtion" style="width: 213.6px;margin-top:1px;"></textarea></td>'
        html +='<td style="border:1px solid white;"><select class="form-control product_invoice_account" id="product_account'+invoice_number+'" name="product_account[]" required><option value="">-------</option></select></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+')" id="Price'+invoice_number+'" name="Price[]" style="margin-top:1%" required></div></div></td>'
        html +='<td style="border:1px solid white;"><input class="form-control" id="Unit'+invoice_number+'" name="Unit[]" style="padding-left:0px;" readonly></td>'
        html +='<td style="border:1px solid white;"><input type="text" class="form-control" id="Quantity'+invoice_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+')" name="Quantity[]" required></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control all_discount" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+')" id="Discount'+invoice_number+'" name="Discount[]"></div>'
        html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+invoice_number+'" name="Dis[]" onchange="dicount_type('+invoice_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax" class="form-control tax" maxlength="5" size="5" onkeyup="invoice_tax_cacultion()" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+invoice_number+'\')" name="tax[]" id="tax'+invoice_number+'" style="margin-top:-1px" required><datalist id="tax"><option value="0"><option value="5"><option value="12"><option value="18"><option value="28"></datalist></div>'
        html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: white;">%</font></div></div></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control amount" onkeypress="return restrictAlphabets(event), float_value(event,\'Amount'+invoice_number+'\')" id="Amount'+invoice_number+'" name="Amount[]" style="margin-top:1%;" readonly></div></div></td>'
        html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+invoice_number+'" name="'+invoice_number+'" onclick="creditnote_removeRow('+invoice_number+')" style="cursor: default;">delete_forever</span></td></tr>'
        $('#invoice_table').append(html)
        
        // SELECT PLUGIN
        $(function () {
            $(".select").select2();
          });

        $(function () {
            $(".product_invoice_account").select2();
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
            url: "/invoice/add/"+1+"/",
            dataType: "json",
            success: function(data){
                
                // for product details
                var option = data.products
                var id = data.ids
                for(var i = 0;i < option.length;i++){
                    $('<option/>').val(id[i]).html(option[i]).appendTo('#ItemName'+invoice_number+'');
                }
                
                // for account_ledger details
                var acc_option = data.acc_group_name
                var acc_id = data.acc_ids
                for(var i = 0;i < acc_option.length;i++){
                    $('<option/>').val(acc_id[i]).html(acc_option[i]).appendTo('#product_account'+invoice_number+'');
                }
            },

        });
    // vendor_gst_type()
    // if(gst == '8'){
    //     if(vendor_state != $('#order_state').val()){
    //         $('.tax').each(function(){
    //             $(this).attr('readonly', true)
    //         });
    //     }else{
    //         $('.tax').each(function(){
    //             $(this).attr('readonly', false)
    //         });
    //     }
    // }
};
// REMOVE JS TABLE
function creditnote_removeRow(a) {

$('#invoice_row'+a+'').remove();
$('#'+a+'').remove();
sub_total()
if(invoice_number > 1){
    invoice_number -=1
}

}
/********************************************************************/
// PURCHASE ORDER ITEM CLEAR FIRST ROW
/********************************************************************/

function clear_row(){
    $('#ItemName1').val('').change();
    $('#product_account1').val('').change();

}
/********************************************************************/
// INVOICE LINE ITEMS SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".invoice_line_item").select2();
      });
    });

$(document).on('click','#select2-ItemName1-container',function(){

    for(var i = 1;i <= invoice_number; i++){
        var a = $('#row_ItemName'+invoice_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link invoice_product" data-toggle="modal" id="row_ItemName'+invoice_number+'" onclick="get_invoice_product_id('+invoice_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
        }  
    } 
});

function c(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".invoice_line_item").select2();
          });
        });
}
function get_invoice_product_id(ids){
    prefill_invoice_product = ids

}
var prefill_invoice_product 

/********************************************************************/
// INVOICE LINE ITEMS(ACCOUNT) SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".product_invoice_account").select2();
        $('.select2-container--default').css('padding-bottom','16px')
      });
    });

$(document).on('click','#select2-product_account1-container',function(){
    
    for(var i = 1;i <= invoice_number; i++){
        var a = $('#row_account'+invoice_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link purchase_account" data-toggle="modal" id="row_account'+invoice_number+'" onclick="get_invoice_account_id('+invoice_number+'),acc_product_account()" data-target="#addGroupModal" style="margin-left: -24%;">+ Add New</button>');
        }  
    } 
});

function acc_product_account(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".product_invoice_account").select2();
          });
        });
}
function get_invoice_account_id(ids){
    prefill_invoice_account = ids

}
var prefill_invoice_account 
/********************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG CUSTOMER NAME
/********************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#invoice_customer").select2();
      });
    });
$(document).on('click','#select2-invoice_customer-container',function(){

    $(".invoice_product").hide()
    var a = $('#addcontact').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact()" id="addcontact" data-target="#ContactModal" style="margin-left: -8%;">+ Add Contact</button>');
        }
        });
function add_contact(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#invoice_customer").select2();
          });
        });

        $('#id_customer_type').remove()
        var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
        html +='<option value="1">CUSTOMER</option></select>'
       $('#con_type').append(html)

       $('#add_contact_type').remove()
       var button = '<button class="btn btn-sm btn-success save_button " name="invoice_contact" id="add_contact_type" onclick="return invoice_contact_form(\'customer\')">Save</button>'
       $( button ).insertBefore("#contact_type_add");
    }


/********************************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG  contact type employee
/********************************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#invoice_seales_person").select2();
      });
    });
$(document).on('click','#select2-invoice_seales_person-container',function(){

    $(".invoice_product").hide()
    var a = $('#addcontact_employee').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" id="addcontact_employee" onclick="add_contact_invoice()" data-target="#ContactModal" style="margin-left: -8%;">+ Add Employee</button>');
        }
        });
function add_contact_invoice(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#invoice_seales_person").select2();
          });
        });
    $('#id_customer_type').remove()
    var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
    html +='<option value="3">EMPLOYEE</option></select> '
    $('#con_type').append(html)

    $('#add_contact_type').remove()
       var button = '<button class="btn btn-sm btn-success save_button" name="invoice_contact" id="add_contact_type" onclick="return invoice_contact_form(\'employee\')">Save</button>'
       $( button ).insertBefore("#contact_type_add");
}

/********************************************************************************/
// invoice type new or recurring
/********************************************************************************/

function invoice_type(type){
    if(type == 'one_time'){
        $('#recurring_radio').prop('checked',false)
        $('#one_invoice').show()
        $('#recurring_invoice').hide()
        $('#Invoice_recurring_start').val('')
        $('#Invoice_recurring_repeat').val('')
        $('#invoice_recurring_Frequency').val('')
        $('#Invoice_recurring_end').val('')

    }else if(type == 'recurring'){
        $('#one_radio').prop('checked',false)
        $('#one_invoice').hide()
        $('#recurring_invoice').show()
        $('#invoice_pay_terms').val('')
        $('#Invoice_one_due_date').val('')
        
    }
}

/************************************************************ */
// FETCH PRODUCT account/unit/price/product description/currency
/************************************************************ */
function product(a) {
    var product = $('#ItemName'+a+' option').filter(':selected').val()
    //  $('#customerName :selected').text();
    if(product != ''){
        $.ajax({
            type:"GET",
            url: "/purchase/product/"+product+"",
            dataType: "json",
            success: function(data){
                $("#desc"+a+"").val(data.desc)

                $("#Price"+a+"").val(parseFloat(data.selling).toFixed(2))
    
                $("#Unit"+a+"").val(data.unit)

                $("#Quantity"+a+"").val("")
                $("#Discount"+a+"").val("")
                $("#tax"+a+"").val("")
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
        $("#Price"+a+"").val("")
        $("#Unit"+a+"").val("")
        $("#Quantity"+a+"").val("")
        $("#Discount"+a+"").val("")
        $("#tax"+a+"").val("")
        $("#Amount"+a+"").val("")
        sub_total()
        total_discount()
        invoice_shipping_charges()
    }
};
/********************************************************************/
// invoice PRODUCT MODEL SAVE USING AJAX
/********************************************************************/


function invoice_product_form(save_type){
	form_d = $("#add_purchase_product_form")[0];

    var formData = new FormData(form_d);
    if($('#id_product_type').val() == ''){
        alert('Product type is requried')
        $('#id_product_type').focus()
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
                    $(".purchase_line_item").each(function(){
                        $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                    });
                    $('#ItemName'+prefill_purchase_product+'').val(data.ids).change(); 
                    // $('.productDropdown .dd-button').text(data.name);
                    // $('#ItemName'+prefill_purchase_product+'').val(data.ids).change(); 
                });
                $("#ProductModal").modal('hide');
            }
        },
    });
}

/********************************************************************/
// invoice CONTACT MODEL SAVE USING AJAX
/********************************************************************/
function invoice_contact_form(category){
  
    event.preventDefault()

    if($('#id_contact_name').val() == ''){
        alert('Contact name is requried')
        $('#id_contact_name').focus()
        return false
    }else if($('#id_organization_type option').filter(':selected').val() != '1' & $('#id_organization_name').val() == ''){
        alert('Organization name is requried')
        $('#id_organization_name').focus()
        return false
    }else if($('#id_user_address_details_set-0-city').val() == ''){
        alert('City is requried')
        $('#id_user_address_details_set-0-city').focus()
        return false
    }else if($('#id_user_address_details_set-0-state').val() == ''){
        alert('State is requried')
        $('#id_user_address_details_set-1-state').focus()
        return false
    }else if($('#id_user_address_details_set-0-country').val() == ''){
        alert('Country is requried')
        $('#id_user_address_details_set-0-country').focus()
        return false
    }

    if($('.address_is_billing_diff').is(':checked')){
        if($('#id_user_address_details_set-1-city').val() == ''){
            alert('City is requried')
            $('#id_user_address_details_set-1-city').focus()
            return false
        }else if($('#id_user_address_details_set-1-state').val() == ''){
            alert('State is requried')
            $('#id_user_address_details_set-1-state').focus()
            return false
        }else if($('#id_user_address_details_set-1-country').val() == ''){
            alert('Country is requried')
            $('#id_user_address_details_set-1-country').focus()
            return false
        }
    }
    
    $.post("/contacts/add/",$("#add_purchase_contact_form").serialize(), function(data){
    if(data != '0'){
        
        $.get("/creditnote/contact_fetch/",function(data){
            if(category == 'customer'){
                $("#invoice_customer").each(function(){
                    $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                });
                $('#invoice_customer').val(data.ids).change(); 
            }
            else if(category == 'employee'){
                $("#invoice_seales_person").each(function(){
                    $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                });
                $('#invoice_seales_person').val(data.ids).change(); 
            }
            
            
        });
        $("#ContactModal").modal('hide');
    }
  
});
}

/********************************************************************/
// INVOICE ACCOUNT_LEDGER(GROUP) MODEL SAVE USING AJAX
/********************************************************************/
function invoice_account_ledger_form(save_type){
  
    event.preventDefault()

    if($('#id_group_name').val() == ''){
        alert('group name is requried')
        $('#id_group_name').focus()
        return false
    }

    $.post("/add_ledger_group/",$("#add_group_form").serialize(), function(data){
    if(data != '0'){
        
        $.get("/purchase_order/account_group_fetch/",function(data){

            $(".product_invoice_account").each(function(){
                $('<option/>').val(data.ids).html(data.group_name).appendTo($(this));
            });
            $('#product_account'+prefill_invoice_account+'').val(data.ids).change(); 
            
        });
        $("#addGroupModal").modal('hide');
    }
  
});
}
/********************************************************************/
// CALCULATION
/********************************************************************/

function purchase_calculate(a){
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
            else if(parseFloat(discount).toFixed(2) < parseFloat(100.00)){
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
                purchase_calculate(a)
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
            else if (parseFloat(discount).toFixed(2) < parseFloat(val)){
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
                purchase_calculate(a)
            } 
        }  
    }	
    else{
        $("#Amount"+a+"").val('')
        sub_total()
    }
}

function dicount_type(a){
    purchase_calculate(a)
}

function sub_total(){
    var sub_total  = 0
    
    $(".amount").each(function(){

        var a = $(this).val()
        if(a == ''){
                    sub_total += 0
                }
                else{
                    sub_total +=  parseFloat(a)
                }
    });

    if(sub_total == 0){
        $("#SubTotal").val('')
        invoice_tax_cacultion()
        total_discount()
        // freight_advance_totalamount()
    }
    else{
        $("#SubTotal").val(parseFloat(sub_total).toFixed(2))
        invoice_tax_cacultion()
        total_discount()
        // freight_advance_totalamount()
    }
    
}


/********************************************************************/
// TOTAL DISCOUNT CALCULATION
/********************************************************************/

function total_discount(){
    var discount = 0
    
    // for loop
    $(".all_discount").each(function(){
        var a = $(this).attr('id')
        var ids = '#Dis'+a.slice(8)+''
        if($(ids).val() == '%'){
            if($(this).val() != ''){
                var current_discount = $(this).val()
                var remaining_discount = ( parseFloat(100) - parseFloat(current_discount) )
                var current_amount = $("#Amount"+a.slice(8)+"").val()
                var discount_cal =( ( parseFloat(current_amount) * (parseFloat(100)) ) / (parseFloat(remaining_discount)) )
                discount += (parseFloat(discount_cal) - parseFloat(current_amount))
            }
            
        }
        else if($(ids).val() == '₹'){
            if($(this).val()){
                discount += parseFloat($(this).val())
            }  
        }
    });
    if(discount.toString() != 'NaN'){
        $('#purchase_Discountotal').val(parseFloat(discount).toFixed(2))
    }
    if(discount == 0){
        $('#purchase_Discountotal').val('')
    }      
}
/********************************************************************/
// shipping charges calculation
/********************************************************************/
var invoice_total = ''
function invoice_shipping_charges(){
    var shipping_charges = $('#shipping_charges').val()
    var total_amount = $('#Total').val()
    var cal = 0
    cal  += parseFloat(shipping_charges)+parseFloat(invoice_total)
    if(cal.toString() != 'NaN' & cal.toString() !='' & cal != 0.00){
        $('#Total').val(parseFloat(cal).toFixed(2))
    }else{
        $('#Total').val(parseFloat(invoice_total).toFixed(2))
    }
    
}
/********************************************************************/
// invoice SGST CGST AND IGST CALCULATION 
/********************************************************************/

$.ajax({
    type:"GET",
    url: "/invoice/org_address_state/",
    dataType: "json",
    success: function(data){
        invoice_user_state = data.state
    },  
});

var invoice_user_state =''
invoice_tax_cacultion()
sub_total()
function invoice_tax_cacultion(){
var state = $("#invoice_state_supply").val()
var cgst_5 = 0
var sgst_5 = 0
var igst_5 = 0
var cgst_12 = 0
var sgst_12 = 0
var igst_12 = 0
var cgst_18 = 0
var sgst_18 = 0
var igst_18 = 0
var cgst_28 = 0
var sgst_28 = 0
var igst_28 = 0
var cgst_other = 0
var sgst_other = 0
var igst_other = 0
if(invoice_user_state.toLowerCase() == state.toLowerCase() || state == ''){
    $(".tax").each(function(){
        var tax_id = $(this).attr('id');
        var amount_id = 'Amount'+tax_id.slice(3)+''

        if($('#'+tax_id+'').val() < parseFloat(100.00)){

            var tax_val = (parseFloat($('#'+amount_id+'').val()) * (parseFloat($('#'+tax_id+'').val()) / 100)).toFixed(2);
            var half = (parseFloat(tax_val)/2).toFixed(2);
            if($('#'+tax_id+'').val() == '5' & half != 'NaN'){
                cgst_5 += parseFloat(half)
                sgst_5 += parseFloat(half)
            }
            else if($('#'+tax_id+'').val() == '12' & half != 'NaN'){
                cgst_12 += parseFloat(half)
                sgst_12 += parseFloat(half)
            }
            else if($('#'+tax_id+'').val() == '18' & half != 'NaN'){
                cgst_18 += parseFloat(half)
                sgst_18 += parseFloat(half)
            }
            else if($('#'+tax_id+'').val() == '28' & half != 'NaN'){
                cgst_28 += parseFloat(half)
                sgst_28 += parseFloat(half)
            }
            else if($('#'+tax_id+'').val() != '' & $('#'+tax_id+'').val() != '5' & $('#'+tax_id+'').val() != '12' &$('#'+tax_id+'').val() != '18' & $('#'+tax_id+'').val() != '28' & half != 'NaN' ){
                cgst_other += parseFloat(half)
                sgst_other += parseFloat(half)
            }
        }else{
            alert('Please enter valid Tax value')
            $('#'+tax_id+'').val('')
        }
        
    });
    if(cgst_5 != 0 & sgst_5 != 0 & cgst_5 != 0.0 & sgst_5 != 0.0 ){
        $('#CGST_5').val(cgst_5)
        $('#SGST_5').val(sgst_5)
        $('#gst_5').show()
    }else{
        $('#gst_5').hide()
    }
    if(cgst_12 != 0 & sgst_12 != 0 & cgst_12 != 0.0 & sgst_12 != 0.0){
        $('#CGST_12').val(cgst_12)
        $('#SGST_12').val(sgst_12)
        $('#gst_12').show()

    }else{
        $('#gst_12').hide()
    }
    if(cgst_18 != 0 & sgst_18 != 0 & cgst_18 != 0.0 & sgst_18 != 0.0){
        $('#CGST_18').val(cgst_18)
        $('#SGST_18').val(sgst_18)
        $('#gst_18').show()

    }else{
        $('#gst_18').hide()
    }
    if(cgst_28 != 0 & sgst_28 != 0 & cgst_28 != 0.0 & sgst_28 != 0.0){
        $('#CGST_28').val(cgst_28)
        $('#SGST_28').val(sgst_28)
        $('#gst_28').show()

    }else{
        $('#gst_28').hide()
    }
    if(cgst_other != 0 & sgst_other != 0 & cgst_other != 0.0 & sgst_other != 0.0){
        $('#CGST_other').val(cgst_other)
        $('#SGST_other').val(sgst_other)
        $('#gst_other').show()

    }else{
        $('#gst_other').hide()
    }

    if($("#gst_5").is(":visible")){
        var a = '0'
    }else{
        $('#CGST_5').val('')
        $('#SGST_5').val('')
    }

    if($("#gst_12").is(":visible")){
        var a = '0'
    }else{
        $('#CGST_12').val('')
        $('#SGST_12').val('')
    }

    if($("#gst_18").is(":visible")){
        var a = '0'
    }else{
        $('#CGST_18').val('')
        $('#SGST_18').val('')
    }

    if($("#gst_28").is(":visible")){
        var a = '0'
    }else{
        $('#CGST_28').val('')
        $('#SGST_28').val('')
    }

    if($("#gst_other").is(":visible")){
        var a = '0'
    }else{
        $('#CGST_other').val('')
        $('#SGST_other').val('')
    }
    $('#igst_5').hide()
    $('#igst_5').val('')

    $('#igst_12').hide()
    $('#igst_12').val('')

    $('#igst_18').hide()
    $('#igst_18').val('')

    $('#igst_28').hide()
    $('#igst_28').val('')

    $('#igst_other').hide()
    $('#igst_other').val('')

    var sub_total = $('#SubTotal').val()
    
    var sc_total = (parseFloat(sub_total) + parseFloat(cgst_5) + parseFloat(sgst_5) + parseFloat(cgst_12) + parseFloat(sgst_12) + parseFloat(cgst_18) + parseFloat(sgst_18) + parseFloat(cgst_28) + parseFloat(sgst_28) +parseFloat(cgst_other) + parseFloat(sgst_other)).toFixed(2)
    if(sc_total == 'NaN'){
        $('#Total').val('')
        invoice_total = ''
    }else{
        $('#Total').val(sc_total)
        invoice_total = sc_total
    }
    
}
else if(invoice_user_state.toLowerCase() != state.toLowerCase() ){
    $(".tax").each(function(){
        var tax_id = $(this).attr('id');
        var amount_id = 'Amount'+tax_id.slice(3)+''

        if($('#'+tax_id+'').val() < parseFloat(100.00)){

            var tax_val = (parseFloat($('#'+amount_id+'').val()) * (parseFloat($('#'+tax_id+'').val()) / 100)).toFixed(2);
            if($('#'+tax_id+'').val() == '5' & tax_val != 'NaN' ){
                igst_5 += parseFloat(tax_val)
            }
            else if($('#'+tax_id+'').val() == '12' & tax_val != 'NaN'){
                igst_12 += parseFloat(tax_val)
            }
            else if($('#'+tax_id+'').val() == '18' & tax_val != 'NaN'){
                igst_18 += parseFloat(tax_val)
            }
            else if($('#'+tax_id+'').val() == '28' & tax_val != 'NaN'){
                igst_28 += parseFloat(tax_val)
            }else if($('#'+tax_id+'').val() != '' & $('#'+tax_id+'').val() != '5' & $('#'+tax_id+'').val() != '12' &$('#'+tax_id+'').val() != '18' & $('#'+tax_id+'').val() != '28' & tax_val != 'NaN'){
                igst_other += parseFloat(tax_val)
            }
        }else{
            alert('Please enter valid Tax value')
            $('#'+tax_id+'').val('')
        }
    
    });
    if(igst_5 != 0 & igst_5 != 0.0){
        $('#IGST_5').val(igst_5)
        $('#igst_5').show()

    }else{
        $('#igst_5').hide()
    }
    if(igst_12 != 0 & igst_12 != 0.0){
        $('#IGST_12').val(igst_12)
        $('#igst_12').show()

    }else{
        $('#igst_12').hide()
    }
    if(igst_18 != 0 & igst_18 != 0.0){
        $('#IGST_18').val(igst_18)
        $('#igst_18').show()

    }else{
        $('#igst_18').hide()
    }
    if(igst_28 != 0 & igst_28 != 0.0){
        $('#IGST_28').val(igst_28)
        $('#igst_28').show()

    }else{
        $('#igst_28').hide()
    }
    if(igst_other != 0 & igst_other != 0.0 ){
        $('#IGST_other').val(igst_other)
        $('#igst_other').show()

    }else{
        $('#igst_other').hide()
    }

    if($("#igst_5").is(":visible")){
        var a = '0'
    }else{
        $('#IGST_5').val('')

    }

    if($("#igst_12").is(":visible")){
        var a = '0'
    }else{
        $('#IGST_12').val('')

    }

    if($("#igst_18").is(":visible")){
        var a = '0'
    }else{
        $('#IGST_18').val('')

    }

    if($("#igst_28").is(":visible")){
        var a = '0'
    }else{
        $('#IGST_28').val('')

    }

    if($("#igst_other").is(":visible")){
        var a = '0'
    }else{
        $('#IGST_other').val('')

    }
    $('#gst_5').hide()
    $('#CGST_5').val('')
    $('#SGST_5').val('')

    $('#gst_12').hide()
    $('#CGST_12').val('')
    $('#SGST_12').val('')

    $('#gst_18').hide()
    $('#CGST_18').val('')
    $('#SGST_18').val('')

    $('#gst_28').hide()
    $('#CGST_28').val('')
    $('#SGST_28').val('')

    $('#gst_other').hide()
    $('#CGST_other').val('')
    $('#SGST_other').val('')

    var sub_total = $('#SubTotal').val()
    var i_total = (parseFloat(sub_total) + parseFloat(igst_5) + parseFloat(igst_12) + parseFloat(igst_18) + parseFloat(igst_28) + parseFloat(igst_other)).toFixed(2)
    if(i_total == 'NaN'){
        $('#Total').val('')
        invoice_total = ''
    }
    else{
        $('#Total').val(i_total)
        invoice_total = i_total
    }
}
}
/********************************************************************/
// Date Picker
/********************************************************************/
//  NEW INVOICE FOR FIRST TIME 
$("#Invoice_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");

//  REVERSE TRACKING
$('#Invoice_date').change(function() {
    if($('#one_radio').is(':checked') & $("#invoice_pay_terms").is(":visible")){
        invoice_pay_date()
    }
});
//  ON CHANGE TO SET NEW INVOICE DUE DATE
function invoice_pay_date(){
    var pay_terms = $('#invoice_pay_terms').val()
    if(pay_terms == 'On Due Date'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+0d'); 
        endDate.setDate(endDate.getDate()+0); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == '10 Days'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+9d'); 
        endDate.setDate(endDate.getDate()+9); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == '20 Days'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+19d'); 
        endDate.setDate(endDate.getDate()+19); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == '30 Days'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+29d'); 
        endDate.setDate(endDate.getDate()+29); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == '60 Days'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+59d'); 
        endDate.setDate(endDate.getDate()+59); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == '90 Days'){
        var endDate = $('#Invoice_date').datepicker('getDate', '+89d'); 
        endDate.setDate(endDate.getDate()+89); 
        $("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
    }else if(pay_terms == 'Custom'){

    }
}

// on change in new invoice due date

$('#Invoice_one_due_date').change(function() {

    var start = $('#Invoice_date').datepicker('getDate');
    var end = $('#Invoice_one_due_date').datepicker('getDate');
    var days = (end - start)/1000/60/60/24;
    console.log(days)
    // $('#hasil').val(days);
    if(days == 0){
        $('#invoice_pay_terms').val('On Due Date').change();
    }else if(days == 9){
        $('#invoice_pay_terms').val('10 Days').change();
    }else if(days == 19){
        $('#invoice_pay_terms').val('20 Days').change();
    }else if(days == 29){
        $('#invoice_pay_terms').val('30 Days').change();
    }else if(days == 59){
        $('#invoice_pay_terms').val('60 Days').change();
    }else if(days == 89){
        $('#invoice_pay_terms').val('90 Days').change();
    }else {
        $('#invoice_pay_terms').val('').change();
    }
});

//  recurring invoice

$("#Invoice_recurring_start").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()})

//  REVERSE TRACKING FOR RECURRING START DATE
$('#Invoice_recurring_start').change(function() {
    if($('#recurring_radio').is(':checked') & $("#recurring_invoice").is(":visible")){
        invoice_recurring_end()
    }
});
// INVOICE RECURRING REPEAT
function invoice_recurring_repeat(){
    if($('#invoice_recurring_Frequency').val() != ''){
        invoice_recurring_end()
    }
}

function invoice_recurring_end(){
    var frequency = $('#invoice_recurring_Frequency').val()
    var repeat = $('#Invoice_recurring_repeat').val()
    if(frequency == 'Weekly'){
        if(repeat != ''){
            var invoice_repeat = parseInt(repeat) * 7
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+6d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+7); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }
    }else if(frequency == 'Monthly'){
        if(repeat != ''){
            var invoice_repeat = parseInt(repeat) * 29
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+29d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+29); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }
        
    }else if(frequency == 'Quarterly'){
        if(repeat != ''){
            var invoice_repeat = parseInt(repeat) * 84
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d');
            endDate.setTime(endDate.getTime() - (1000*60*60*24)) 
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+84d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+84); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }
        
    }else if(frequency == ' Half yearly'){
        if(repeat != ''){
            var invoice_repeat = parseInt(repeat) * 180
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+180d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+180); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }
    }else if(frequency == 'Yearly'){
        if(repeat != ''){
            var invoice_repeat = parseInt(repeat) * 365
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+365d'); 
            endDate.setDate(endDate.getDate()+365); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }
    }
}