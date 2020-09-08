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

function add_single_row(a){
    if(count == 0){
        purchase_number +=a
        count +=1
    }else{
        purchase_number += 1
    }
    run_others();
}
function run_others(){
    acc_group_name_htm = '<option value="">None</option>';
    products_htm = '<option value="">None</option>';

    next_id = purchase_number;       
    html = product_row_creator(next_id);
    $('#purchase_table').append(html);
    ret = get_func(next_id,acc_group_name_htm, products_htm);

}
function product_row_creator(purchase_number){
    var org_state = $('#single_gst_code option:selected').val()
    var vendor_g = ''
    if(vendor_gstin != ''){
        vendor_g = vendor_gstin.substring(0,2)
    }

    var html = '<tr id="entry_row'+purchase_number+'">'
    html +='<td style="border:1px solid black;padding-bottom:0%"><select class="form-control select purchase_line_item" id="ItemName'+purchase_number+'" name="ItemName[]" onchange="product('+purchase_number+'),validation()" style="padding-left:0px" required><option value="">None</option></select>'
    html +='<textarea id="desc'+purchase_number+'" name="desc[]" rows="2" maxlength="200" size="200" placeholder="Product Description" style="width: 174.6px;margin-top:1px;"></textarea></td>'
    html +='<td style="border:1px solid black;"><select class="form-control prodduct_purchase_account" id="product_account'+purchase_number+'" name="product_account[]" onchange="validation()" required><option value="">None</option></select></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+'),validation()" id="Price'+purchase_number+'" name="Price[]" style="margin-top:1%" required></div></div></td>'
    html +='<td style="border:1px solid black;"><input type="text" class="form-control" id="Quantity'+purchase_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+'),validation()" name="Quantity[]" required></td>'
    html +='<td style="border:1px solid black;"><input class="form-control" id="Unit'+purchase_number+'" name="Unit[]" style="padding-left:0px;" readonly></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control all_discount" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+purchase_number+'\')" onkeyup="purchase_calculate('+purchase_number+')" id="Discount'+purchase_number+'" name="Discount[]"></div>'
    html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+purchase_number+'" name="Dis[]" onchange="dicount_type('+purchase_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax" class="form-control tax" maxlength="5" size="5" onkeyup="row_gst_cal('+purchase_number+')" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+purchase_number+'\')" name="tax[]" id="tax'+purchase_number+'" style="margin-top:-1px" readonly><datalist id="tax"><option value="0"><option value="5"><option value="12"><option value="18"><option value="28"></datalist></div>'
    html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: black;">%</font></div></div></td>'
    if(org_state != '' || vendor_g != '' || org_state == vendor_g || $('#org_gst_reg_type').val() == ''){
        html += '<td class="row_cs_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+purchase_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+purchase_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+purchase_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'
    }else if(org_state != vendor_g){
        html += '<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+purchase_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+purchase_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+purchase_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+purchase_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'    
    }
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Amount'+purchase_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount" id="Amount'+purchase_number+'" name="Amount[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Amount_inc'+purchase_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount_inc" id="Amount_inc'+purchase_number+'" name="Amount_inc[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+purchase_number+'" name="'+purchase_number+'" onclick=" return creditnote_removeRow('+purchase_number+')" style="cursor: default;">delete_forever</span></td></tr>'
    return html;
}

function get_func(next_id, acc_group_name_htm, products_htm){

    $.get("/purchase_order/add_purchase_order/"+1+"/", function(data){
        if(data){
            if(data.acc_group_name.length > 0){  
                // for account_ledger details
                var acc_option = data.acc_group_name;
                var acc_id = data.acc_ids;
    
                for(var j = 0; j < acc_option.length; j++){
                    acc_group_name_htm += '<option value="'+acc_id[j]+'">'+acc_option[j]+'</option>'; 
                }
            }
            
            if(data.products.length > 0){
                var option = data.products
                var id = data.ids
                
                for(var j = 0; j < option.length; j++){                        
                    products_htm += '<option value="'+id[j]+'">'+option[j]+'</option>'; 
                }
            }

            $("#ItemName"+next_id).empty().append(products_htm);
            $("#product_account"+next_id).empty().append(acc_group_name_htm);


            check_gst_status('vendor_side')
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

            // SELECT PLUGIN
            $(function () {
                $(".select").select2();
            });

            $(function () {
                $(".prodduct_purchase_account").select2();
                $('.select2-container--default').css('padding-bottom','16px')
            });
            // 
            validation()
        }
    }); 
}

// REMOVE JS TABLE
function creditnote_removeRow(a) {
    var first_row = $('#purchase_table tbody tr:first').attr('id')
    if(first_row == 'purchase_row'+a+''){
        var last_row = $('#purchase_table tbody tr:last').attr('id')
        if(last_row != 'purchase_row'+a+''){
            $('#purchase_row'+a+'').remove();
        }else{
            $('#ItemName'+a+'').val('').change();
            $('#product_account'+a+'').val('').change();
        }
    }else{
        $('#purchase_row'+a+'').remove();
    }
    sub_total()
    validation()
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
       var button = '<button class="btn btn-sm btn-success save_button " name="purchase_contact" id="add_contact_type" style="margin-top:16px;background-color: #598ebb;" onclick="return purchase_contact_form(\'vendor\')">Save</button>'
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
       var button = '<button class="btn btn-sm btn-success save_button" name="purchase_contact" id="add_contact_type" style="margin-top:16px;background-color: #598ebb;" onclick="return purchase_contact_form(\'c_e\')">Save</button>'
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
               // include tax
               if(data.is_check_purchase == 'no' || $("#tax"+a+"").is('[readonly]') ){
                $("#tax"+a+"").val("")
                }else{
                $("#tax"+a+"").val(data.purchase_tax)
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
        $("#Price"+a+"").val("")
        $("#Unit"+a+"").val("")
        $("#Quantity"+a+"").val("")
        $("#Discount"+a+"").val("")
        $("#tax"+a+"").val("")
        $("#Amount"+a+"").val("")
        sub_total()
        total_discount()
        // freight_advance_totalamount()
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

    // if(sub_total == 0){
    //     $("#SubTotal").val('')
    //     purchase_tax_cacultion()
    //     total_discount()
    //     freight_advance_totalamount()
    // }
    // else{
        $("#SubTotal").val(parseFloat(sub_total).toFixed(2))
        change_state()
        purchase_tax_cacultion()
        total_discount()
        // freight_advance_totalamount()
    // }
    
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
                var row_price = parseFloat($("#Price"+a.slice(8)+"").val())
                var row_quantity = parseFloat($("#Quantity"+a.slice(8)+"").val())
                var row_amount = parseFloat(row_price) * parseFloat(row_quantity)
                var discount_cal = (parseFloat(row_amount) * (parseFloat(current_discount) / parseFloat(100)))
                discount += parseFloat(discount_cal)
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

var advance_count = 0
function freight_advance_totalamount(){

    var freight_charges = $('#Freight_Charges').val()
    if($('#advance_info').find('#advance_value').is(":visible")){
        var advance = $('#advance_info').find('#advance_value').val()
    }else{
        var advance = $('#advance').val()
    }
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
            purchase_calculate()
            total_balance += (parseFloat(total_amount) + parseFloat(freight_charges))
        }   
    }
    else if(freight_charges == '' & advance == '' & total_amount != ''){

        total_balance += parseFloat(total_amount)
    }
    if(total_balance.toString() != 'NaN'){
        if(total_balance == 0){
         $('#total_balance').val(parseFloat(0).toFixed(2))   
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
// FOR GST
/********************************************************************/
var vendor_gstin =''
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
                // gst = data.gst_type
                if(data.gst_type != null){
                    $('#gst_type').val(data.gst_type)
                }else{
                    $('#gst_type').val('')
                }
                vendor_gstin = data.gstin
                check_gst_status('user_side')
            },
        });
    }else{
        $('#mail').val('')
        $('#gst_type').val('')
        vendor_gstin = ''
        check_gst_status('user_side')
    }
}

function check_gst_status(cat){
    if(cat == 'user_side'){
        // for organization and vendor not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == '' ||  $('#gst_type').val() == '0' ||  $('#gst_type').val() == '3' ||  $('#gst_type').val() == '5' ||  $('#gst_type').val() == ''){
            $('#purchase_table').find('.tax').attr('readonly', true)
            $('#purchase_table').find('.tax,.row_cgst,.row_sgst,.row_igst').val('')
            sub_total()
            if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == ''){
                alert('Organization not register GST')
            }else if($('#gst_type').val() == '0' ||  $('#gst_type').val() == '3' ||  $('#gst_type').val() == '5'){
                alert('Vendor not register GST')
            }else if($('#gst_type').val() == ''){
                alert('Vendor not selected')
            }
        }else{
            $('#purchase_table').find('.tax').attr('readonly', false)
            sub_total()
        }
    }else if(cat == 'vendor_side'){
        // for organization and vendor not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == '' ||  $('#gst_type').val() == '0' ||  $('#gst_type').val() == '3' ||  $('#gst_type').val() == '5' ||  $('#gst_type').val() == ''){
            $('#purchase_table').find('.tax').attr('readonly', true)
            $('#purchase_table').find('.tax,.row_cgst,.row_sgst,.row_igst').val('')
            sub_total()
            // if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == ''){
            //     alert('Organization not register GST')
            // }else if($('#gst_type').val() == '0' ||  $('#gst_type').val() == '3' ||  $('#gst_type').val() == '5'){
            //     alert('Vendor not register GST')
            // }else if($('#gst_type').val() == ''){
            //     alert('Vendor not selected')
            // }
        }else{
            $('#purchase_table').find('.tax').attr('readonly', false)
            sub_total()
        }
    }
    
}

/********************************************************************/
// purchase SGST CGST AND IGST CALCULATION 
/********************************************************************/

function purchase_tax_cacultion(){
    var org_state = $('#single_gst_code option:selected').val()
    var vendor_g = ''
    if(vendor_gstin != ''){
        vendor_g = vendor_gstin.substring(0,2)
    }
    var csgst = 0
    var igst = 0

    if(org_state == vendor_g){
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
    else if(org_state != vendor_g){
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
    freight_advance_totalamount()
}

/********************************************************************/
// CHANGE CGST SGST TO IGST
/********************************************************************/

function change_state(){
    var org_state = $('#single_gst_code option:selected').val()
    var vendor_g = ''
    if(vendor_gstin != ''){
        vendor_g = vendor_gstin.substring(0,2)
    }
    if(org_state != '' & vendor_g != ''){
        if(org_state == vendor_g || $('#org_gst_reg_type').val() == ''){
            $('#purchase_table').find('.row_i_gst').hide()
            $('#purchase_table').find('.row_igst').val('')
            $('#purchase_table').find('.row_cs_gst').show()
            $('#purchase_table').find('.price_header').css('width','7%')
            $('#purchase_table').find('.unit_header').css('width','11%')
            $('#purchase_table').find('.quantity_header').css('width','5%')
            $('#purchase_table').find('.tax_header').css('width','7%')
        }else if(org_state != vendor_g){
            $('#purchase_table').find('.row_cs_gst').hide()
            $('#purchase_table').find('.row_cgst, .row_sgst').val('')
            $('#purchase_table').find('.row_i_gst').show()
            $('#purchase_table').find('.price_header').css('width','8%')
            $('#purchase_table').find('.unit_header').css('width','12%')
            $('#purchase_table').find('.quantity_header').css('width','6%')
            $('#purchase_table').find('.tax_header').css('width','8%')
        }
    }
    $(".purchase_line_item").each(function(){

        var ids = $(this).attr('id');
        ids = ids.substring(ids.length - 1, ids.length);
        single_row_gst_cal = 'state'
        var check = row_gst_cal(ids);
    });
    purchase_tax_cacultion()
}
/********************************************************************/
// EACH ROW TAX CALCULATION
/********************************************************************/

var single_row_gst_cal = ''
function row_gst_cal(ids){
    var org_state = $('#single_gst_code option:selected').val()
    var vendor_g = ''
    if(vendor_gstin != ''){
        vendor_g = vendor_gstin.substring(0,2)
    }

    if($('#tax'+ids+'').val() < parseFloat(100.00)){
        var gst =  (parseFloat($('#Amount'+ids+'').val()) * (parseFloat($('#tax'+ids+'').val()) / 100));
        var amount = $('#Amount'+ids+'').val()
        var incl_tax = parseFloat(amount) + parseFloat(gst)
        if(org_state == vendor_g){
            var half = (parseFloat(gst)/2).toFixed(2);

            if(half != 'NaN' & half != 0 & half != 0 & half != 0.0 & half != 0.0){
                $('#row_cgst'+ids+'').val(half)
                $('#row_sgst'+ids+'').val(half)
                $('#Amount_inc'+ids+'').val()
            }else{
                $('#row_cgst'+ids+'').val('')
                $('#row_sgst'+ids+'').val('')
            }
        }else if(org_state != vendor_g){
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
            purchase_tax_cacultion()
        }
    }else{
        alert('Please enter valid Tax value')
        $('#tax'+ids+'').val('')
    }
}
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
        $('#order_state').val('')
    }
});

$('#customer_radio').click(function(){
    
    if($('#customer_radio').is(':checked')){
        $('#org_radio').prop('checked', false)
        $('#cust_address').show()
        $('#purchase_address').text('')
        $('#purchase_attention').val('')
        // $('.select2-container--default').css('width','100%')
        $('#order_state').val('')
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
                var add = '<button class="btn btn-sm" type="button" name="add_address" id="button_add" style="background-color: #598ebb;" onclick="org_cont_address_form('+data.ids+',\'org\')">Add Address</button>'
                $( add ).insertBefore( "#table_close" );
                
                // empty table
                $(".address_row").each(function(){
                    
                    $(this).remove()
                });
                // add table row
                var con
                var a_branch
                var a_gst
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
                    var html = '<tr class="address_row" id="purchase_delivery_address_row_'+i+'"><td style="border:1px solid black;" align="center"><label class="form-check-label">'
                        html+='<input class="form-check-input choose_address" type="radio" name="radio_add" id="adress_'+(parseInt(i)+1)+'" onclick="radio_click_add($(this))" value="on" style="margin-top:-2%"><span class="circle"><span class="check"></span></span></label></td>'
                        html +='<td style="border:1px solid black;" align="center" class="choose_address_branch'+(parseInt(i)+1)+'">'+a_branch+'</td>'
                        html +='<td style="border:1px solid black;"><div class="row" id="con_person'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+con+'</div>'
                        html +='<div class="row" id="p_address'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+count[i]+'</div>'
                        html +='<div class="row" id="p_state'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;display:none">'+state[i]+'</div>'
                        html +='<div class="row" id="address_gst'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+a_gst+'</a></div></td></tr>'

                        $('#purchase_delivery_address').append(html)
                        
                }

            },
        });
        $('#Purchase_order_AddressModal').modal('show')
    }
}

//  CONTACT ADDRESS
function purchase_cont_address(){
    var contact_ids = $('#choose_customer_address option').filter(':selected').val()
    if(contact_ids != ''){
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
                    var add = '<button class="btn btn-sm" type="button" name="add_address" id="button_add" style="background-color: #598ebb;" onclick="org_cont_address_form('+data.ids+',\'cont\')">Add Address</button>'
                    $( add ).insertBefore( "#table_close" );
                    // empty table
                    $(".address_row").each(function(){
                        
                        $(this).remove()
                    });
                    // add table row
                    var con
                    var a_branch
                    var a_gst
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
                        if(branch[i] == null){
                    
                            a_branch = ''
                        }else if(branch[i] != null){
                            a_branch = branch[i]
                        }
                        var html = '<tr class="address_row" id="purchase_delivery_address_row_'+i+'"><td style="border:1px solid black;" align="center"><label class="form-check-label">'
                            html+='<input class="form-check-input choose_address" type="radio" name="radio_add" id="adress_'+(parseInt(i)+1)+'" onclick="radio_click_add($(this))" value="on" style="margin-top:-2%"><span class="circle"><span class="check"></span></span></label></td>'
                            html +='<td style="border:1px solid black;" align="center" class="choose_address_branch'+(parseInt(i)+1)+'">'+a_branch+'</td>'
                            html +='<td style="border:1px solid black;"><div class="row" id="con_person'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+con+'</div>'
                            html +='<div class="row"  id="p_address'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+count[i]+'</div>'
                            html +='<div class="row" id="p_state'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;display:none">'+state[i]+'</div>'
                            html +='<div class="row" id="address_gst'+(parseInt(i)+1)+'" style="margin-left:0px;margin-right:0px;">'+a_gst+'</a></div></td></tr>'
                        
                            $('#purchase_delivery_address').append(html)
                    }
                },
            });
            $('#Purchase_order_AddressModal').modal('show')
        }
    }else{
        $('#purchase_address').text('')
        $('#purchase_attention').val('')
        $('#order_state').val('')
        // check_gst_status('delivary_side')
    }
    
}
/********************************************************************/
// chosse address
/********************************************************************/
var global_parson = ''
var global_address =''
var global_gst = ''
// var global_delivery_state = ''
function radio_click_add(elem){
    var names = $(elem).attr('id')
    global_parson = $('#con_person'+names.substring(names.length - 1, names.length)).text()
    global_address = $('#p_address'+names.substring(names.length - 1, names.length)).text()
    global_gst = $('#address_gst'+names.substring(names.length - 1, names.length)).text()
    // global_delivery_state = $('#p_state'+names.substring(names.length - 1, names.length)).text()
};
/********************************************************************/
// ORGNIZATION AND CUSTOMER RADIO BUTTON
/********************************************************************/

function prefill(){
    var checkbox_count = 0
    $('.choose_address').each(function(){
        if($(this).prop("checked") == true){
            checkbox_count +=1
        }
    })
    if(checkbox_count == 0){
        alert('Please first choose the address')
        return false
    }
    var address = ''
    if(global_parson == ''){
        address = ''+global_address+''+'\n'+''+global_gst+''
    }else{
        address = ''+global_parson+''+'\n'+''+global_address+''+'\n'+''+global_gst+''
    }  
    $('#purchase_address').text(address)
    $('#purchase_attention').val(global_parson.substring(16,global_parson.length))
    // $('#order_state').val(global_delivery_state)
    // check_gst_status('delivary_side')
    
    $('#Purchase_order_AddressModal').modal('hide')
}

$('#table_close').click(function(){
    // $('#order_state').val('')
    $('#org_radio').prop('checked', false)
    $('#customer_radio').prop('checked', false)
    $('#cust_address').hide()
    $('#choose_customer_address').val('').change();
    // check_gst_status('delivary_side')
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
                    // var state = "_"+data.state+""
                    var address = ''
                    if(data.contact_person != null){
                        $('#purchase_attention').val(data.contact_person)
                        address += 'Contact person:-'+data.contact_person+''+'\n'+''+common_address.slice(0,(parseInt(count)-parseInt(1)))+''
                    }else{
                        address += common_address.slice(0,(parseInt(count)-parseInt(1)))
                    }
                    
                    $('#purchase_address').text(address)
                    $('#order_state').val(data.state)
                    // check_gst_status('delivary_side')
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
                    // var state = "_"+data.state+""
                    // delivery_state(state)
                    var address = ''
                    if(data.contact_person != null){
                        $('#purchase_attention').val(data.contact_person)
                        address += 'Contact person:-'+data.contact_person+''+'\n'+''+common_address.slice(0,(parseInt(count)-parseInt(1)))+''
                    }else{
                        address += common_address.slice(0,(parseInt(count)-parseInt(1)))
                    }

                    $('#purchase_address').text(address)
                    $('#order_state').val(data.state)
                    // check_gst_status('delivary_side')

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
// MOUSE HOVER
/*********************************************************************** */
vendor_info()
function vendor_info(){
    var ins = $('#purchase_vendor').val()
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
    }else if(global_save_message != ''){
        alert(global_save_message)
        return false
    }else{
        return true
    }
}
function check_mail(){
    if($('#purchase_address').text() == ''){
        alert('Deilvery address is required')
        $('#purchase_address').focus()
        return false
    }else if($('#mail').val() == ''){
        alert('can not send mail because vendor email id did not exisit')
        return false
    }else if(global_save_message != ''){
        alert(global_save_message)
        return false
    }
    else{
        return true
    }
}
$('#purchase_delivary_date,#purchase_date,#purchase_edit_date').keypress(function(event) {
        event.preventDefault();
});

/*********************************************************************** */
// VALIDATION FOR ROW IN SAVE BUTTON
/*********************************************************************** */
var global_save_message = ''
$(document).ready(function(){
    validation()
});
function validation(){
    var count = $('#purchase_table tbody tr').length
    var row_ids = $('#purchase_table tbody tr:first').attr('id')
    // var last_row = $('#purchase_table tbody tr:first').attr('id')
    // var first_row =  $('#purchase_table tbody tr:first').attr('id')
    var number_of_row_blank = 1
    for(var i = 1; i<=count;i++){
        var row_last_str = row_ids.substring(row_ids.length-1,row_ids.length)
        
        if($('#ItemName'+row_last_str).val() == '' & $('#product_account'+row_last_str).val() == '' & $('#Price'+row_last_str).val() == '' & $('#Quantity'+row_last_str).val() == ''){
            if(number_of_row_blank == count){
                global_save_message = 'Please fill the product line item'
            }else{
                global_save_message = ''
            }
            number_of_row_blank +=1
        }else{
            if($('#ItemName'+row_last_str).val() == ''){
                global_save_message = 'Table row '+i+' product/service required'
                break;
            }else if($('#product_account'+row_last_str).val() == ''){
                global_save_message = 'Table row '+i+' product account required'
                break;
            }else if($('#Price'+row_last_str).val() == '' || parseFloat($('#Price'+row_last_str).val()).toFixed(2) == 0){
                global_save_message = 'Table row '+i+' product price required'
                break; 
            }else if($('#Quantity'+row_last_str).val() == '' || parseFloat($('#Quantity'+row_last_str).val()).toFixed(2) == 0){
                global_save_message = 'Table row '+i+' product qunatity required'
                break; 
            }else{
                global_save_message = ''
            }
        }
        row_ids = $('#'+row_ids+'').closest('tr').next('tr').attr('id');
    }
    
}

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
// vandor gst update
/********************************************************************/
function v_gst_save(){
    $.post("/purchase_order/vendor_gst_save/",$("#vendor_gst_update").serialize(),function(data){
        if(data == 1){
            $('#contact_gst_change').modal('hide')
            vendor_info()
            state_compare()
        }
    });
}