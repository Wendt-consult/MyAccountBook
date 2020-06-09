/********************************************************************/
// Date Picker
/********************************************************************/


$("#purchase_date").datepicker({dateFormat: 'dd-mm-yy'}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");
// $("#advance_date,#hidden_advance_date").datepicker({dateFormat: 'dd-mm-yy'}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");
$("#purchase_date,#purchase_edit_date").datepicker({ 
    dateFormat: 'dd-mm-yy',
    changeMonth: true,
    // minDate: new Date(),
    maxDate: '+2y',
    onSelect: function(date){

        // var selectedDate = new Date(date);
        // var msecsInADay = 86400000;
        var endDate = $('#purchase_date,#purchase_edit_date').datepicker('getDate', '+1d'); 
        endDate.setDate(endDate.getDate()+1); 

       //Set Minimum Date of EndDatePicker After Selected Date of StartDatePicker
        $("#purchase_delivary_date").datepicker( "option", "minDate", endDate );
        $("#purchase_delivary_date").datepicker( "option", "maxDate", '+2y' );

    }
});

$("#purchase_delivary_date").datepicker({ 
    dateFormat: 'dd-mm-yy',
    changeMonth: true,
    minDate: new Date(),
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

var purchase_number = 1
var count = 0
function purchase_addRow(a) {
    if(count == 0){
        purchase_number +=a
        count +=1
    }

    purchase_number += 1

    $(document).on('click','#select2-ItemName'+purchase_number+'-container',function(){

        for(var i = 1;i <= purchase_number; i++){
            var a = $('#row_ItemName'+purchase_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link purchase_product" data-toggle="modal" id="row_ItemName'+purchase_number+'" onclick="get_purchase_product_id('+purchase_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
            }  
        } 
    });

    $(document).on('click','#select2-product_account'+purchase_number+'-container',function(){

        for(var i = 1;i <= purchase_number; i++){
            var a = $('#row_account'+purchase_number+'').length
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link purchase_account" data-toggle="modal" id="row_account'+purchase_number+'" onclick="get_purchase_account_id('+purchase_number+'),c()" data-target="#addGroupModal" style="margin-left: -24%;">+ Add New</button>');
            }  
        } 
    });
       
        var html = '<tr id="purchase_row'+purchase_number+'">'
        html +='<td style="border:1px solid white;padding-bottom:0%"><select class="form-control select purchase_line_item" id="ItemName'+purchase_number+'" name="ItemName[]" onchange="product('+purchase_number+')" style="padding-left:0px" required><option value="">-------</option></select>'
        html +='<textarea id="desc'+purchase_number+'" name="desc[]" rows="2" maxlength="200" size="200" placeholder="Product Describtion" style="width: 213.6px;margin-top:1px;"></textarea></td>'
        html +='<td style="border:1px solid white;"><select class="form-control prodduct_purchase_account" id="product_account'+purchase_number+'" name="product_account[]" required><option value="">-------</option></select></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+')" id="Price'+purchase_number+'" name="Price[]" style="margin-top:1%" required></div></div></td>'
        html +='<td style="border:1px solid white;"><input class="form-control" id="Unit'+purchase_number+'" name="Unit[]" style="padding-left:0px;" readonly></td>'
        html +='<td style="border:1px solid white;"><input type="text" class="form-control" id="Quantity'+purchase_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+')" name="Quantity[]" required></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control all_discount" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+')" id="Discount'+purchase_number+'" name="Discount[]"></div>'
        html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+purchase_number+'" name="Dis[]" onchange="dicount_type('+purchase_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax" class="form-control tax" maxlength="5" size="5" onkeyup="purchase_tax_cacultion()" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+purchase_number+'\')" name="tax[]" id="tax'+purchase_number+'" style="margin-top:-1px" required><datalist id="tax"><option value="0"><option value="5"><option value="12"><option value="18"><option value="28"></datalist></div>'
        html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: white;">%</font></div></div></td>'
        html +='<td style="border:1px solid white;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control amount" onkeypress="return restrictAlphabets(event), float_value(event,\'Amount'+purchase_number+'\')" id="Amount'+purchase_number+'" name="Amount[]" style="margin-top:1%;" readonly></div></div></td>'
        html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+purchase_number+'" name="'+purchase_number+'" onclick="creditnote_removeRow('+purchase_number+')" style="cursor: default;">delete_forever</span></td></tr>'
        $('#purchase_table').append(html)
        
        // SELECT PLUGIN
        $(function () {
            $(".select").select2();
          });

        $(function () {
            $(".prodduct_purchase_account").select2();
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
            url: "/purchase_order/add_purchase_order/"+1+"/",
            dataType: "json",
            success: function(data){
                
                // for product details
                var option = data.products
                var id = data.ids
                for(var i = 0;i < option.length;i++){
                    $('<option/>').val(id[i]).html(option[i]).appendTo('#ItemName'+purchase_number+'');
                }
                
                // for account_ledger details
                var acc_option = data.acc_group_name
                var acc_id = data.acc_ids
                for(var i = 0;i < acc_option.length;i++){
                    $('<option/>').val(acc_id[i]).html(acc_option[i]).appendTo('#product_account'+purchase_number+'');
                }
            },

        });
    vendor_gst_type()
    if(gst == '8'){
        if(vendor_state != $('#order_state').val()){
            $('.tax').each(function(){
                $(this).attr('readonly', true)
            });
        }else{
            $('.tax').each(function(){
                $(this).attr('readonly', false)
            });
        }
    }
};
// REMOVE JS TABLE
function creditnote_removeRow(a) {

$('#purchase_row'+a+'').remove();
$('#'+a+'').remove();
sub_total()
if(purchase_number > 1){
    purchase_number -=1
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
// PUCHASE LINE ITEMS SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".purchase_line_item").select2();
      });
    });

$(document).on('click','#select2-ItemName1-container',function(){

    for(var i = 1;i <= purchase_number; i++){
        var a = $('#row_ItemName'+purchase_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link purchase_product" data-toggle="modal" id="row_ItemName'+purchase_number+'" onclick="get_purchase_product_id('+purchase_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
        }  
    } 
});

function c(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".purchase_line_item").select2();
          });
        });
}
function get_purchase_product_id(ids){
    prefill_purchase_product = ids

}
var prefill_purchase_product 

/********************************************************************/
// PUCHASE LINE ITEMS(ACCOUNT) SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $(".prodduct_purchase_account").select2();
        $('.select2-container--default').css('padding-bottom','16px')
      });
    });

$(document).on('click','#select2-product_account1-container',function(){
    
    for(var i = 1;i <= purchase_number; i++){
        var a = $('#row_account'+purchase_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link purchase_account" data-toggle="modal" id="row_account'+purchase_number+'" onclick="get_purchase_account_id('+purchase_number+'),acc_product_account()" data-target="#addGroupModal" style="margin-left: -24%;">+ Add New</button>');
        }  
    } 
});

function acc_product_account(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".prodduct_purchase_account").select2();
          });
        });
}
function get_purchase_account_id(ids){
    prefill_purchase_account = ids

}
var prefill_purchase_account 

/********************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG  VANDOR NAME
/********************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#purchase_vendor").select2();
      });
    });
$(document).on('click','#select2-purchase_vendor-container',function(){

    $(".purchase_product").hide()
    var a = $('#addcontact').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact()" id="addcontact" data-target="#ContactModal" style="margin-left: -8%;">+ Add Contact</button>');
        }
        });
function add_contact(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#purchase_vendor").select2();
          });
        });

        $('#id_customer_type').remove()
        var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
        html +='<option value="2" selected>VENDOR</option></select>'
       $('#con_type').append(html)

       $('#add_contact_type').remove()
       var button = '<button class="btn btn-sm btn-success save_button " name="purchase_contact" id="add_contact_type" onclick="return purchase_contact_form(\'vendor\')">Save</button>'
       $( button ).insertBefore("#contact_type_add");
    }

/********************************************************************************/
// SEARCH AND BUTTON INSIDE SELECT TAG  contact type customer and employee
/********************************************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $("#choose_customer_address").select2();
      });
    });
$(document).on('click','#select2-choose_customer_address-container',function(){

    $(".purchase_product").hide()
    var a = $('#addcontact_delivary').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="add_contact_delivary()" id="addcontact_delivary" data-target="#ContactModal" style="margin-left: -8%;">+ Add Customer</button>');
        }
        });
function add_contact_delivary(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#choose_customer_address").select2();
          });
        });
    
    $('#id_customer_type').remove()
    var html='<select name="customer_type" class="form-control input-sm" required="" id="id_customer_type">'
     html +='<option value="">---------</option><option value="1" selected="">CUSTOMER</option>'
     html +='<option value="3">EMPLOYEE</option></select> '
    $('#con_type').append(html)

    $('#add_contact_type').remove()
       var button = '<button class="btn btn-sm btn-success save_button" name="purchase_contact" id="add_contact_type" onclick="return purchase_contact_form(\'c_e\')">Save</button>'
       $( button ).insertBefore("#contact_type_add");
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
        freight_advance_totalamount()
    }
   
};
/********************************************************************/
// PRUCHASE_ORDER PRODUCT MODEL SAVE USING AJAX
/********************************************************************/


function purchase_product_form(save_type){
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
// PURCHASE_OREDR CONTACT MODEL SAVE USING AJAX
/********************************************************************/
function purchase_contact_form(category){
  
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
            if(category == 'vendor'){
                $("#purchase_vendor").each(function(){
                    $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                });
                $('#purchase_vendor').val(data.ids).change(); 
            }
            else if(category == 'c_e'){
                $("#choose_customer_address").each(function(){
                    $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                });
                $('#choose_customer_address').val(data.ids).change(); 
            }
            
            
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

            $(".prodduct_purchase_account").each(function(){
                $('<option/>').val(data.ids).html(data.group_name).appendTo($(this));
            });
            $('#product_account'+prefill_purchase_account+'').val(data.ids).change(); 
            
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
        purchase_tax_cacultion()
        total_discount()
        freight_advance_totalamount()
    }
    else{
        $("#SubTotal").val(parseFloat(sub_total).toFixed(2))
        purchase_tax_cacultion()
        total_discount()
        freight_advance_totalamount()
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
// Freight Charges, advance and total amount calculation
/********************************************************************/

function freight_advance_totalamount(){
    var freight_charges = $('#Freight_Charges').val()
    var advance = $('#advance_value').val()
    var total_amount = $('#Total').val()
    var total_balance = 0
    if(advance == '' & freight_charges != '' & total_amount != ''){
        
        total_balance += (parseFloat(total_amount) + parseFloat(freight_charges))
    }
    else if(freight_charges == '' & advance != '' & total_amount != ''){
        if(parseFloat(advance) < parseFloat(total_amount)){
            total_balance += (parseFloat(total_amount) - parseFloat(advance))
        }
        else{
            alert('advance must be lesser than total balance')
            $('#advance_value').val('')
            $('#advance').val('')
            total_balance += parseFloat(total_amount)
        }
        
    }
    else if(freight_charges != '' & advance != '' & total_amount != ''){
        if(parseFloat(advance) < parseFloat($('#total_balance').val())){
            total_balance += (parseFloat(freight_charges) + parseFloat(total_amount)) - (parseFloat(advance))
        }
        else{
            alert('advance must be lesser then total balance')
            $('#advance_value').val('')
            $('#advance').val('')
            // purchase_calculate()
            total_balance += (parseFloat(total_amount) + parseFloat(freight_charges))
        }   
    }
    else if(freight_charges == '' & advance == '' & total_amount != ''){
        total_balance += parseFloat(total_amount)
    }
    if(total_balance.toString() != 'NaN'){
        if(total_balance == 0){
         $('#total_balance').val('')   
        }
        else{
            $('#total_balance').val(parseFloat(total_balance).toFixed(2))
        }  
        if(total_amount == ''){
            $('#Freight_Charges').val('')
            $('#advance_value').val('')
            $('#advance').val('')
        } 
    }
}

/********************************************************************/
// purchase SGST CGST AND IGST CALCULATION 
/********************************************************************/
state_compare()
function state_compare(){
    var ids = $('#purchase_vendor').val()
    if(ids != ''){
        $.ajax({
            type:"GET",
            url: "/purchase_order/vendor_state/"+ids+"/",
            dataType: "json",
            success: function(data){
                if(data.mail != null){
                    $('#mail').val(data.mail)
                }
                gst = data.gst_type
                if(data.gst_type != null){
                    $('#gst_type').val(gst)
                }
                vendor_state = data.vendor_state
               
                purchase_tax_cacultion()
                vendor_count = '1'
                vendor_gst_type()
                composite_vendor = '1'
                delivery_state('_'+$('#order_state').val()+'')
            },
        });
    }
}
var vendor_count=''
var composite_vendor = ''
function vendor_gst_type(){
    var gst_type = $('#gst_type').val()
    if(gst_type == '0' || gst_type =='3' || gst_type == '5'){
        $('.tax').each(function(){
            $(this).attr('readonly', true)
            $(this).val('')
            if(vendor_count == '1'){
                alert('Vendor not register GST')
                vendor_count = ''
            }
            
        });
    }else{
        $('.tax').each(function(){
            $(this).attr('readonly', false)
            // alert('Vendor not register GST')
        });
    }
}

function delivery_state(state){

    if(gst == '8'){
        if(vendor_state != state.slice(1)){
            $('.tax').each(function(){
                $(this).val('')
                $(this).attr('readonly', true)
            });
            if(composite_vendor == '1'){
                alert('Vendor is register under composite scheme, it can not choose delivery address of different state.')
                composite_vendor = ''
            }
            
        }else{
            $('.tax').each(function(){
                $(this).attr('readonly', false)
            });
        }
    }

    $('#order_state').val(state.slice(1))
    purchase_tax_cacultion()
    
}

var vendor_state =''
var gst = ''
// var delivery_address = ''
purchase_tax_cacultion()
sub_total()
function purchase_tax_cacultion(){
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
if(vendor_state == $('#order_state').val()){
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
    }else{
        $('#Total').val(sc_total)
    }
    
}
else if(vendor_state != $('#order_state').val()){
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
    }
    else{
        $('#Total').val(i_total)
    }
}
freight_advance_totalamount()
}
/********************************************************************/
// product table validation
/********************************************************************/
// var message = ''
// function validation(){

// for(var i = 1;i <= purchase_number;i++){
//     message = ''
//     var product_name = $("#ItemName"+i+"").val()
//     // var invoice = $("#Reference").val()
//     if( product_name != '-------' ){
//         var unit = $("#Unit"+i+"").val()
//         var quantity = $("#Quantity"+i+"").val()
//         var price = $("#Price"+i+"").val()
//         if(quantity == '' || quantity == '0'){
//             message += 'Table row number '+i+':- fill quantity'
//             break;
//         }
//         else if(unit == '-------'){
//             message += 'Table row number '+i+':- choose unit'
//             break;
//         }
//         else if(price == '' || price == '0.0'){
//             message = 'Table row number '+i+':- fill price'
//             break;
//         }

//     }
// }
// }

/********************************************************************/
// ORGNIZATION AND CUSTOMER RADIO BUTTON
/********************************************************************/

$('#org_radio').click(function(){

    if($('#org_radio').is(':checked')){
        $('#customer_radio').prop('checked',false)
        $('#cust_address').hide()
        $('#choose_customer_address').val('-------').change();
        $('#purchase_address').text('')
        $('#purchase_attention').val('')
    }
});

$('#customer_radio').click(function(){
    
    if($('#customer_radio').is(':checked')){
        $('#org_radio').prop('checked', false)
        $('#cust_address').show()
        $('#purchase_address').text('')
        $('#purchase_attention').val('')
        $('.select2-container--default').css('width','100%')
    }
});

/*******************************************************************************************/
// PURCHASE_ORDER DELIVERY ADDRESS FETCH (ORGANIZATION OR CUSTOMER) USING AJAX
/*******************************************************************************************/

// ORGANIZATION ADDRESS
var organisation_id = ''

function ajax_org_address(){

    if($('#org_radio').is(':checked')){
        //   AJAX TO FETCH ORGNANISATION ADDRESS
        $.ajax({
            type:"GET",
            url: "/purchase_order/address/"+'org'+"/",
            dataType: "json",
            success: function(data){
            
                var count = data.address
                var contact_name = data.contact_person
                var state = data.state
                var branch = data.branch
                var gst = data.gst
                organisation_id = data.ids
                // pass organization id
                $('#button_add').remove()
                var add = '<button class="btn btn-sm btn-primary" type="button" name="add_address" id="button_add" onclick="org_cont_address_form('+data.ids+',\'org\')">Add</button>'
                $( add ).insertBefore( "#table_close" );
                
                // empty table
                $(".address_row").each(function(){
                    
                    $(this).remove()
                });
                // add table row
                var con
                var a_branch
                var a_gst
                Organization_address_list.length = 0;
                for(var i = 0;i < count.length;i++){

                    if( contact_name[i] == null){
                    
                        con = ''
                    }else if(contact_name[i] != null){
                
                        con = "Contact person:- "+contact_name[i]+""
                    }

                    if( gst[i] == null){
                    
                        a_gst = ''
                        
                    }else if(gst[i] != null){
                
                        a_gst = "Gst Number:- "+gst[i]+""
                        
                    }

                    if( contact_name[i] == null){
                    
                        a_branch = ''
                    }else if(contact_name[i] != null){
                
                        a_branch = branch[i]
                    }
                    var html = '<tr class="address_row" id="purchase_delivery_address_row_'+i+'"><td style="border:1px solid white;" align="center">'+(parseInt(i)+1)+'</td>'
                        html +='<td style="border:1px solid white;"><a href="#" id="branch_'+i+'" onclick="prefill('+i+',\'org\'),delivery_state(\'_'+state[i]+'\')">'+a_branch+'</a></td>'
                        html +='<td style="border:1px solid white;"><div class="row" style="margin-left:0px;margin-right:0px;"><a href="#" onclick="prefill('+i+',\'org\'),delivery_state(\'_'+state[i]+'\')">'+con+'</a></div>'
                        html +='<div class="row" style="margin-left:0px;margin-right:0px;"><a href="#" id="address_'+i+'" onclick="prefill('+i+',\'org\'),delivery_state(\'_'+state[i]+'\')">'+count[i]+' <br> '+a_gst+' </a></div></td></tr>'
                        // html +='<div class="row" style="margin-left:0px;margin-right:0px;"><a href="#" id="address_'+i+'" onclick="prefill('+i+',\'org\'),delivery_state(\'_'+state[i]+'\')">'+a_gst+'</a></div></td></tr>'
                    
                        $('#purchase_delivery_address').append(html)
                        Organization_address_list.push(contact_name[i])
                }

            },
        });
        $('#Purchase_order_AddressModal').modal('show')
    }
}

//  CONTACT ADDRESS
function purchase_cont_address(){
    var contact_ids = $('#choose_customer_address option').filter(':selected').val()
    if(contact_ids != '-------'){
        if($('#customer_radio').is(':checked')){
            //   AJAX TO FETCH  CONTACT ADDRESS
            $.ajax({
                type:"GET",
                url: "/purchase_order/address/"+contact_ids+"/",
                dataType: "json",
                success: function(data){
                    
                    var count = data.address
                    var contact_name = data.contact_person
                    var state = data.state
                    var branch = data.branch
                    var gst = data.gst
    
                    // pass organization id
                    $('#button_add').remove()
                    var add = '<button class="btn btn-sm btn-primary" type="button" name="add_address" id="button_add" onclick="org_cont_address_form('+data.ids+',\'cont\')">Add</button>'
                    $( add ).insertBefore( "#table_close" );
                    // empty table
                    $(".address_row").each(function(){
                        
                        $(this).remove()
                    });
                    // add table row
                    var con
                    var a_branch
                    var a_gst
                    contact_person_list.length = 0;

                    if(gst[0] == null){
                        a_gst =''
    
                    }else if(gst[0] != null){
                        a_gst = "Gst Number:- "+gst[0]+""
                    }
                    for(var i = 0;i < count.length;i++){
                        if( contact_name[i] == null){
                        
                            con = ''
                        }else if(contact_name[i] != null){
                    
                            con = "Contact person:- "+contact_name[i]+""
                        }
                        if( contact_name[i] == null){
                    
                            a_branch = ''
                        }else if(contact_name[i] != null){
                    
                            a_branch = branch[i]
                        }
                        var html = '<tr class="address_row" id="purchase_delivery_address_row_'+i+'"><td style="border:1px solid white;" align="center">'+(parseInt(i)+1)+'</td>'
                            html +='<td style="border:1px solid white;"><a href="#" id="branch_'+i+'" onclick="prefill('+i+',\'cont\'),delivery_state(\'_'+state[i]+'\')">'+a_branch+'</a></td>'
                            html +='<td style="border:1px solid white;"><div class="row" style="margin-left:0px;margin-right:0px;"><a href="#" onclick="prefill('+i+',\'cont\'),delivery_state(\'_'+state[i]+'\')">'+con+'</a></div>'
                            html +='<div class="row" style="margin-left:0px;margin-right:0px;"><a href="#" id="address_'+i+'" onclick="prefill('+i+',\'cont\'),delivery_state(\'_'+state[i]+'\')">'+count[i]+' <br> '+a_gst+'</a></div></td></tr>'
                        
                            $('#purchase_delivery_address').append(html)
                            contact_person_list.push(contact_name[i])
                    }
                },
            });
            $('#Purchase_order_AddressModal').modal('show')
        }
    }
    
}
var Organization_address_list= []
var contact_person_list =[]
/********************************************************************/
// ORGNIZATION AND CUSTOMER RADIO BUTTON
/********************************************************************/

function prefill(ids,category){
    
    $('#purchase_address').text($('#address_'+ids+'').text())
    if(category == 'org'){
        $('#purchase_attention').val(Organization_address_list[ids])
    }else if(category == 'cont'){
        $('#purchase_attention').val(contact_person_list[ids])
    }
    
    $('#Purchase_order_AddressModal').modal('hide')
}

$('#table_close').click(function(){
    $('#org_radio').prop('checked', false)
    $('#customer_radio').prop('checked', false)
    $('#cust_address').hide()
    $('#choose_customer_address').val('').change();
});

/********************************************************************/
// ORGNIZATION AND CONTACT ADD NEW ADDRESS
/********************************************************************/
function org_cont_address_form(ids,category){
    if(category == 'cont'){
        $("#ids_con").val(ids)
        
        $('#Purchase_order_AddressModal').modal('hide')
        $('#newContactAddressModal').modal('show')
    }

    if(category == 'org'){
        $("#ids").val(ids)
        $('#Purchase_order_AddressModal').modal('hide')
        $('#newOrgAddressModal').modal('show')
    }

    // $('#Purchase_order_AddressModal').modal('hide')
    // $('#newAddressModal').modal('show')
}

/*******************************************************************************/
// PURCHASE_ORDER (ORGANIZATION OR CONTACT) ADD ADDRESS MODEL SAVE USING AJAX
/*******************************************************************************/
function save__address(event,category){
  
    event.preventDefault()

    if(category == 'org'){
        if($('#add_address_organization').find('input[id="id_city"]').val() == ''){
            alert('City is requried')
            $('#add_address_organization').find('input[id="id_city"]').focus()
            return false
        }else if($('#add_address_organization').find('select[id="id_state"]').val() == ''){
            alert('State is requried')
            $('#add_address_organization').find('select[id="id_state"]').focus()
            return false
        }else if($('#add_address_organization').find('select[id="id_country"]').val() == ''){
            alert('Country is requried')
            $('#add_address_organization').find('select[id="id_country"]').focus()
            return false
        }
        $.post("/profile/add_organisation_addres/",$("#add_address_organization").serialize(), function(data){
            if(data != '0'){
                
                $.get("/purchase_order/last_address/",function(data){
                    
                    var common_address = ''
                    if(data.flat_no != null){
                        common_address += data.flat_no +','
                    }
                    if(data.street != null){
                        common_address += data.street +','
                    }
                    if(data.city != null){
                        common_address += data.city +','
                    }
                    if(data.state != null){
                        common_address += data.state +','
                    }
                    if(data.country != null){
                        common_address += data.country +','
                    }
                    if(data.pincode != null){
                        common_address += data.pincode +','
                    }
                    var count = common_address.length
                    var state = "_"+data.state+""
                    delivery_state(state)
                    $('#purchase_address').text(common_address.slice(0,(parseInt(count)-parseInt(1))))

                    if(data.contact_person != null){
                        $('#purchase_attention').val(data.contact_person)
                    }
                });
               $('#newOrgAddressModal').modal('hide');
            }
        });
    }
    else if(category == 'cont'){
        if($('#add_address_contact').find('input[id="id_city"]').val() == ''){
            alert('City is requried')
            $('#add_address_contact').find('input[id="id_city"]').focus()
            return false
        }else if($('#add_address_contact').find('select[id="id_state"]').val() == ''){
            alert('State is requried')
            $('#add_address_contact').find('select[id="id_state"]').focus()
            return false
        }else if($('#add_address_contact').find('select[id="id_country"]').val() == ''){
            alert('Country is requried')
            $('#add_address_contact').find('select[id="id_country"]').focus()
            return false
        }
        $.post("/contacts/add_address/",$("#add_address_contact").serialize(), function(data){
            if(data != '0'){

                $.get("/purchase_order/last_address/",function(data){
                    
                    var common_address = ''
                    if(data.flat_no != null){
                        common_address += data.flat_no +','
                    }
                    if(data.street != null){
                        common_address += data.street +','
                    }
                    if(data.city != null){
                        common_address += data.city +','
                    }
                    if(data.state != null){
                        common_address += data.state +','
                    }
                    if(data.country != null){
                        common_address += data.country +','
                    }
                    if(data.pincode != null){
                        common_address += data.pincode +','
                    }
                    var count = common_address.length
                    var state = "_"+data.state+""
                    delivery_state(state)

                    $('#purchase_address').text(common_address.slice(0,(parseInt(count)-parseInt(1))))

                    if(data.contact_person != null){
                        $('#purchase_attention').val(data.contact_person)
                    }
                });
               $('#newContactAddressModal').modal('hide');
            }
        });
    }
}

/*********************************************************************** */
// DEFUALT PURCHASE_OREDER AND CHECK PURCHASE_OREDER NUMBER IS UNIQUE
/*********************************************************************** */
$("#auto_purchase_number").click(function(){
    if($(this).is(':checked')){
        var ins = 0
        var slug = 'a'
        $.ajax({
            type:"GET",
            url: "/purchase_order/unique_number/"+ins+"/"+slug+"/",
            dataType: "json",
            success: function(data){
                $('#purchse_order').val(data.purchase_number)
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }else{
        $('#purchse_order').val('')
    }  
});

$("#purchse_order").focusout(function(){
    $("#auto_purchase_number").prop('checked',false);
    var ins = 1
    var purchase_number = $("#purchse_order").val()
    $.ajax({
        type:"GET",
        url: "/purchase_order/unique_number/"+ins+"/"+purchase_number+"/",
        dataType: "json",
        success: function(data){
            if(data.unique != 0){
                alert('This purchase order number is already exits. Please enter the different purchase order number.')
                $('#purchse_order').focus();
                $('#purchse_order').val('')
            }
            
        },
    });
  });

/*********************************************************************** */
// get contact type vendor (state)
/*********************************************************************** */

function check_mail(){
    if($('#purchase_address').text() == ''){
        alert('Deilvery address is required')
        $('#purchase_address').focus()
        return false
    }else if($('#mail').val() == ''){
        alert('can not send mail because vendor email id did not exisit')
        return false
    }else{
        return true
    }
}

/*********************************************************************** */
// MOUSE HOVER
/*********************************************************************** */

function vendor_info(){
    var ins = $('#purchase_vendor').val()
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
            

        var html2 = ''
        
        html2 +='Name:- '+name+''+'\n'+ 'Organisation Name:-'+'\n'+organization+''+'\n'+'Email:-'+mail+''+'\n'+'Number:-'+number+''+'\n'+'Address:-'+address+'';
        $("#vendor_details").attr('data-tip', html2);
    });
}
/*********************************************************************** */
// ADVANCE INFO
/*********************************************************************** */

function show_advance_info(){
    var ins = $('#purchase_vendor').val()
    $('#advance_value').val($('#advance').val())
    $('#advance_payment').val($('#total_balance').val())
    $('#advance_date').val($('#hidden_advance_date').val())
    $('#advance_method').val($('#hidden_advance_method').val()).change();
    $('#advance_notes').val($('#hidden_advance_notes').val())
    if(ins != ''){
        $.get("/purchase_order/vendor_details/"+ins+"/",function(data){
            $('#advance_vendor_name').val(data.name)
            $('#advance_vendor_mail').val(data.mail)
            $('#advance_vendor_contact').val(data.number)
        });
    }
    $('#advance_info').modal('show')
}
function add_advance_info(){
    $('#advance').val($('#advance_value').val())
    $('#hidden_advance_date').val($('#advance_date').val())
    console.log($('#hidden_advance_date').val())
    $('#hidden_advance_method').val($('#advance_method').val()).change();
    $('#hidden_advance_notes').val($('#advance_notes').val())
    $('#advance_info').modal('hide')
}

function clear_advance_info(){
    // $('#hidden_advance_date').val('')
    $('#advance_value').val('')
    $('#advance').val('')
    freight_advance_totalamount()
    $('#hidden_advance_method').val('').change();
    $('#hidden_advance_notes').val('')
    $('#advance_info').modal('hide')
}

/*********************************************************************** */
// ON SAVE VALIDATION
/*********************************************************************** */
function order_check(){
    if($('#purchase_address').text() == ''){
        alert('Deilvery address is required')
        $('#purchase_address').focus()
        return false
    }
}