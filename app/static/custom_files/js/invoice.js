/********************************************************************/
// INPUT TYPE NUMBER SROLL HIDE
/********************************************************************/
// Disable Mouse scrolling
$('input[type=number]').on('mousewheel',function(e){ $(this).blur(); });
// Disable keyboard scrolling
$('input[type=number]').on('keydown',function(e) {
    var key = e.charCode || e.keyCode;
    // Disable Up and Down Arrows on Keyboard
    if(key == 38 || key == 40 || key == 69 || key == 189 || key == 190) {
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
// PRODUCT ROW header add/remove
/************************************************************ */
var invoice_header_number = 0
var header__row_count = 0
function add_header(a){
    var check = $('#invoice_table tr:last').attr('id')
    var last_row = check.substring(check.length - 1, check.length);
    if(check.substring(0,check.length-1) != 'invoice_row_header'){
        if(header__row_count == 0){
            invoice_header_number = a
            header__row_count += 1
        }
        invoice_header_number += 1

        // check vendor state
        var state = $('#invoice_state_supply').val()
        var org_state = $('#single_gst_code option:selected').text()

        var html = '<tr id="invoice_row_header'+invoice_header_number+'">'
        if(org_state.toLowerCase() == state.toLowerCase() || $('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val() == '8'|| $('#org_gst_reg_type').val() == '' || global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5' || global_gst_type == '8'||global_gst_type == ''){
            html +='<td class="invoice_row_header" colspan="8" style="border:1px solid black;"><input class="form-control" id="prduct_header'+invoice_header_number+'" name="ItemName[]" placeholder="Header" required><input type="text" id="header_quan'+invoice_header_number+'" name="Quantity[]" value="header" style="display:none;"></td>'
        }else if(org_state.toLowerCase() != state.toLowerCase()){
            html +='<td class="invoice_row_header" colspan="7" style="border:1px solid black;"><input class="form-control" id="prduct_header'+invoice_header_number+'" name="ItemName[]" placeholder="Header" required><input type="text" id="header_quan'+invoice_header_number+'" name="Quantity[]" value="header" style="display:none;"></td>'
        }
        html +='<td colspan="3" style="border-bottom:1px solid black; border-right:1px solid black;"><div class="row"><div class="col-lg-4 col-md-5" style="padding-right:0px;"><font style="color:black;">Sub Total:</font></div><div class="col-lg-8 col-md-7" style="padding-left:0px;margin-top:2%;"><input type="text" class="form-control" id="header_SubTotal'+invoice_header_number+'" name="Amount[]" readonly></div></div></td>'
        html +='<td style="border-top: none;"><span class="tbclose material-icons" id="header'+invoice_header_number+'" name="header'+invoice_header_number+'" onclick="header_remove('+invoice_header_number+'),header_subtotal('+last_row+')" style="cursor: default;">delete_forever</span></td></tr>'
        $('#invoice_table').append(html)
        // if(header_sub_total != 0){
        //     $('#header_SubTotal'+invoice_header_number+'').val(parseFloat(header_sub_total).toFixed(2))
        // }
    }else{
        alert("You can't add header before adding row ")
    }
}

function header_remove(a){
    var first_row = $('#invoice_table tbody tr:first').attr('id')
    var header_next = $('#invoice_row_header'+a+'').closest('tr').next('tr').attr('id');
    var header_prev = $('#invoice_row_header'+a+'').closest('tr').prev('tr').attr('id');
    if(first_row == 'invoice_row_header'+a+''){
        var last_row = $('#invoice_table tbody tr:last').attr('id')
        if(last_row != 'invoice_row_header'+a+''){
            $('#invoice_row_header'+a+'').remove();
            if(header_next.substring(0,header_next.length-1) == 'invoice_row' &  header_prev.substring(0,header_prev.length-1) == 'invoice_row'){
                var row_id = header_next.substring(header_next.length - 1, header_next.length);
                header_subtotal(row_id)
            }
        }else{
            alert("You can't delete row beacuse their is only one row in table")
        }
    }else{
        $('#invoice_row_header'+a+'').remove();
        if(header_next.substring(0,header_next.length-1) == 'invoice_row' &  header_prev.substring(0,header_prev.length-1) == 'invoice_row'){
            var row_id = header_next.substring(header_next.length - 1, header_next.length);
            header_subtotal(row_id)
        }
    }
    // $('#invoice_row_header'+a+'').remove();
}
/************************************************************ */
// header sub total calculation
/************************************************************ */

function header_subtotal(ids){
    var rowCount = $('#invoice_table tr').length;
    var row_name_next = 'invoice_row'+ids+''
    var row_name_prev = 'invoice_row'+ids+''
    var next_header_row =''
    var prev_header_row =''
    for(var i = 1; i < rowCount; i++){
        var next = $('#'+row_name_next+'').closest('tr').next('tr').attr('id');
        if(next == undefined){
            next_header_row = row_name_next
            break;
        }
        // row_name_next = next
        if(next.substring(0,next.length-1) == 'invoice_row_header'){
            next_header_row = row_name_next
            break;
        }else{
            next_header_row = next
        }
        row_name_next = next
    }
    for(var i = 1; i < rowCount; i++){
        if(row_name_prev == 'invoice_row1'){
            break;
        }
        var prev = $('#'+row_name_prev+'').closest('tr').prev('tr').attr('id');
        if(prev.substring(0,prev.length-1) == 'invoice_row_header'){
            prev_header_row = prev
            break;
        }
        else{
            row_name_prev = prev
        }
    }
    var header_subtotal = 0
    var id_number =  prev_header_row.substring(prev_header_row.length - 1, prev_header_row.length);
    for(var i = 1; i < rowCount; i++){
      var amount_ids = next_header_row.substring(next_header_row.length - 1, next_header_row.length);
      if($('#Amount'+amount_ids+'').val() != ''){
          header_subtotal += parseFloat($('#Amount'+amount_ids+'').val())
      }
      var verify_row = $('#'+next_header_row+'').closest('tr').prev('tr').attr('id');
      if(verify_row.substring(0,verify_row.length-1) == 'invoice_row_header'){
          break;
      }else{
        next_header_row = verify_row
      }
    }
    if(header_subtotal != 0){
        $('#header_SubTotal'+id_number+'').val(parseFloat(header_subtotal).toFixed(2))
    }else{
        $('#header_SubTotal'+id_number+'').val('')
    }
    return header_subtotal
}
/************************************************************ */
// PRODUCT ROW ADD/REMOVE
/************************************************************ */

var invoice_number = 1
var count = 0


// Disable Mouse scrolling
$('input[type=number]').on('mousewheel',function(e){ $(this).blur(); });
// Disable keyboard scrolling
$('input[type=number]').on('keydown',function(e) {
    var key = e.charCode || e.keyCode;
    // Disable Up and Down Arrows on Keyboard
    if(key == 38 || key == 40 || key == 69 || key == 189) {
        e.preventDefault();
    } else return true;
});

  
function product_row_creator(invoice_number){
    var state = $('#invoice_state_supply').val()
    var org_state = $('#single_gst_code option:selected').text()
    var html = '<tr id="invoice_row'+invoice_number+'">'
    html +='<td style="border:1px solid black;padding-bottom:0%"><select class="form-control select invoice_line_item" id="ItemName'+invoice_number+'" name="ItemName[]" onchange="product('+invoice_number+')" style="padding-left:0px" required><option value="">-------</option></select>'
    html +='<textarea id="desc'+invoice_number+'" name="desc[]" rows="2" maxlength="200" size="200" placeholder="Product Description" style="width: 158px;margin-top:1px;"></textarea></td>'
    html +='<td style="border:1px solid black;"><select class="form-control product_invoice_account" id="product_account'+invoice_number+'" name="product_account[]" required><option value="">-------</option></select></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+'),header_subtotal('+invoice_number+')" id="Price'+invoice_number+'" name="Price[]" style="margin-top:1%" required></div></div></td>'
    html +='<td style="border:1px solid black;"><input type="text" class="form-control" id="Quantity'+invoice_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+'),header_subtotal('+invoice_number+')" name="Quantity[]" required></td>'
    html +='<td style="border:1px solid black;"><input class="form-control" id="Unit'+invoice_number+'" name="Unit[]" style="padding-left:0px;" readonly></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control all_discount" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+invoice_number+'\')" onkeyup="purchase_calculate('+invoice_number+'),header_subtotal('+invoice_number+')" id="Discount'+invoice_number+'" name="Discount[]"></div>'
    html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+invoice_number+'" name="Dis[]" onchange="dicount_type('+invoice_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax" class="form-control tax" maxlength="5" size="5" onkeyup="row_gst_cal('+invoice_number+')" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+invoice_number+'\')" name="tax[]" id="tax'+invoice_number+'" style="margin-top:-1px" required><datalist id="tax" readonly><option value="0"><option value="5"><option value="12"><option value="18"><option value="28"></datalist></div>'
    html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: black;">%</font></div></div></td>'
    if(org_state.toLowerCase() == state.toLowerCase() || $('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val() == '8'|| $('#org_gst_reg_type').val() == '' || global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5' || global_gst_type == '8'||global_gst_type == ''){
        html += '<td class="row_cs_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+invoice_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+invoice_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+invoice_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'
    }else if(org_state.toLowerCase() != state.toLowerCase()){
        html += '<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_cgst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_cgst" id="row_cgst'+invoice_number+'" name="row_cgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_cs_gst" style="border:1px solid black;display:none;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_sgst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_sgst" id="row_sgst'+invoice_number+'" name="row_sgst[]" style="margin-top: 1%;" readonly></div></div></td>'
        html +='<td class="row_i_gst" style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="row_igst'+invoice_number+'">₹</label></div><div class="col"><input type="text" class="form-control row_igst" id="row_igst'+invoice_number+'" name="row_igst[]" style="margin-top: 1%;" readonly></div></div></td>'    
    }
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Amount'+invoice_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount" id="Amount'+invoice_number+'" name="Amount[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Amount_inc'+invoice_number+'">₹</label></div>'
    html +='<div class="col"><input type="text" class="form-control amount_inc" id="Amount_inc'+invoice_number+'" name="Amount_inc[]" style="margin-top:1%;" readonly></div></div></td>'
    html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+invoice_number+'" name="'+invoice_number+'" onclick=" return creditnote_removeRow('+invoice_number+')" style="cursor: default;">delete_forever</span></td></tr>'
    return html;
}

function get_func(next_id, value,product_quantity,product_price,product_unit, acc_group_name_htm, products_htm){

    $.get("/invoice/add/"+1+"/", function(data){
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
            // SELECT PLUGIN
            $(function () {
                $(".select").select2();
            });

            $(function () {
                $(".product_invoice_account").select2();
                $('.select2-container--default').css('padding-bottom','16px')

            });
            if(value != 'NA'){
                var amount_exc = parseFloat(product_price) * parseFloat(product_quantity)
                $("#ItemName"+next_id).val(value);
                $("#Price"+next_id).val(parseFloat(product_price).toFixed(2))
                $("#Quantity"+next_id).val(product_quantity)
                $("#Unit"+next_id).val(product_unit)
                if(amount_exc != 0 & amount_exc.toString() != 'NaN'){
                    $('#Amount'+next_id).val(parseFloat(amount_exc).toFixed(2))
                }
                var sub_value = sub_total()
                var head_subtotal = header_subtotal(next_id)
            }
        }
    }); 

    
}

//  add bulk product in the table

function run_others(counter,type){
    acc_group_name_htm = '<option value="">-------</option>';
    products_htm = '<option value="">-------</option>';
    if(type == 'single'){
        invoice_number += 1
        value = 'NA'
        product_quantity = 'NA'
        product_price = 'NA'
        product_unit = 'NA'
        next_id = invoice_number;       
        html = product_row_creator(next_id);
        $('#invoice_table').append(html);
        // console.log($("#invoice_table tbody tr:first td:visible").length)
        ret = get_func(next_id, value,product_quantity,product_price,product_unit, acc_group_name_htm, products_htm);
    }else if(type == 'multiple'){
        for(main_counter=1; main_counter<=counter; main_counter++){

            invoice_number += 1
            next_id = invoice_number;       
    
            html = product_row_creator(next_id);
            
            value = $("#product_ids"+main_counter).val()
            product_quantity = $("#bulk_quantity"+main_counter).val()
            product_price = $("#product_price"+main_counter).val()
            product_unit = $("#product_unit"+main_counter).val()
            $('#invoice_table').append(html);
            ret = get_func(next_id, value,product_quantity,product_price,product_unit, acc_group_name_htm, products_htm);
            if(main_counter == counter){
                $('#search_result').empty()
                $('#bulk_prodcut_table tbody').empty()
                bulk_product_item = 0
            }
        }
    }
}

function add_single_row(a){
    if(count == 0){
        invoice_number +=a
        count +=1
    }
    run_others(1,'single');
}


function add_bulk_product_item(){

        var bulk_count = $('#bulk_prodcut_table tr').length
        if(bulk_count == 1){
            alert('Please Chosse the Product before add item in bulk')
            return false
        }else{

            $('#add_item_bulk').modal('hide');
            
            counter = $(".bulk_product").length;
            if($('#bulk_item_type').val() == 'add'){
                run_others(counter,'multiple');
            }
        }
}



// REMOVE JS TABLE
function creditnote_removeRow(a) {
    var first_row = $('#invoice_table tbody tr:first').attr('id')
    if(first_row == 'invoice_row'+a+''){
        var last_row = $('#invoice_table tbody tr:last').attr('id')
        if(last_row != 'invoice_row'+a+''){
            $('#invoice_row'+a+'').remove();
        }else{
            $('#ItemName'+a+'').val('').change();
            $('#product_account'+a+'').val('').change();
        }
    }else{
        $('#invoice_row'+a+'').remove();
    }

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
       var button = '<button class="btn btn-sm  save_button " name="invoice_contact" id="add_contact_type" onclick="return invoice_contact_form(\'customer\')" style="margin-top:16px;background-color:#598ebb;">Save</button>'
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
       var button = '<button class="btn btn-sm  save_button" name="invoice_contact" id="add_contact_type" onclick="return invoice_contact_form(\'employee\')" style="margin-top:16px;background-color:#598ebb;">Save</button>'
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
        $('#Invoice_recurring_start').prop('required',false);
        $('#Invoice_recurring_repeat').prop('required',false);
        $('#invoice_recurring_Frequency').prop('required',false);
        $('#invoice_pay_terms').prop('required',true);
        $('#Invoice_one_due_date').prop('required',true);

    }else if(type == 'recurring'){
        $('#one_radio').prop('checked',false)
        $('#one_invoice').hide()
        $('#recurring_invoice').show()
        $('#invoice_pay_terms').val('')
        $('#Invoice_one_due_date').val('')
        $('#invoice_pay_terms').prop('required',false);
        $('#Invoice_one_due_date').prop('required',false);
        $('#Invoice_recurring_start').prop('required',true);
        $('#Invoice_recurring_repeat').prop('required',true);
        $('#invoice_recurring_Frequency').prop('required',true);
        
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
                // $('#product_account'+a+'').val(4).change();

                $("#Quantity"+a+"").val("")
                $("#Discount"+a+"").val("")
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
        $('#product_account'+a+'').val('').change();
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
                    $(".invoice_line_item").each(function(){
                        $('<option/>').val(data.ids).html(data.name).appendTo($(this));
                    });
                    $('#ItemName'+prefill_invoice_product+'').val(data.ids).change(); 
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
        // invoice_tax_cacultion()
        change_state()
        total_discount()

    }
    else{
        $("#SubTotal").val(parseFloat(sub_total).toFixed(2))
        $("#Total").val($("#SubTotal").val())
        change_state()
        // invoice_tax_cacultion()
        total_discount()
        // invoice_total = $("#SubTotal").val()
        invoice_shipping_charges()
    }
    
    return sub_total
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
    if(shipping_charges != '' & invoice_total != ''){
        cal  += parseFloat(shipping_charges)+parseFloat(invoice_total)
    }else if(invoice_total != ''){
        cal = parseFloat(invoice_total)
    }
    if(cal.toString() != 'NaN' & cal.toString() !='' & cal != 0.00){
        $('#Total').val(parseFloat(cal).toFixed(2))
    }else if(cal.toString() == 'NaN'){
        $('#Total').val('')
        $('#shipping_charges').val('')
    }else if($('#SubTotal').val() != ''){

        $('#Total').val(invoice_total)
    }

    if($('#SubTotal').val() == ''){
        $('#shipping_charges').val('')
    }
  
}
/********************************************************************/
// CHECK GST STATUS FOR APPLY
/********************************************************************/

function check_gst_status(){
    var state = $('#invoice_state_supply').val()
    var org_state = $('#single_gst_code option:selected').text()
        // org gst not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == '' || global_gst_type == '' ){
            $('#invoice_table').find('.tax').attr('readonly', true)
            $('#invoice_table').find('.tax,.row_cgst,.row_sgst,.row_igst').val('')
            sub_total()
            if(global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5'|| global_gst_type == ''){
                alert('tax not apply beacuse customer not select or customer is not gst register')
            }else{
                alert('Organization not register GST')
            }
        // org gst register
        }else if(($('#org_gst_reg_type').val() == '1' || $('#org_gst_reg_type').val() == '2' ||$('#org_gst_reg_type').val() == '4' ||$('#org_gst_reg_type').val() == '6' || $('#org_gst_reg_type').val() == '7') & global_gst_type != ''){
            if(org_state !='' & state != ''){
                $('#invoice_table').find('.tax').attr('readonly', false)
                sub_total()
            }
            else{
                $('#invoice_table').find('.tax').attr('readonly', true)
                $('#invoice_table').find('.tax,.row_cgst,.row_sgst,.row_igst').val('')
                sub_total()
            }
        // org in composite
        }else if($('#org_gst_reg_type').val()  == '8'){
            if( org_state !='' & state != '' & org_state.toLowerCase() == state.toLowerCase()){
                $('#invoice_table').find('.tax').attr('readonly', false)
                sub_total()
            }else{
                $('#invoice_table').find('.tax').attr('readonly', true)
                $('#invoice_table').find('.tax,.row_cgst,.row_sgst,.row_igst').val('')
                sub_total()
                alert('Organization is register under composite scheme,is you choose different state of state tax will not be calculated.')
            }
        }
}
/********************************************************************/
// invoice SGST CGST AND IGST CALCULATION 
/********************************************************************/
// var invoice_user_state =''
// $.ajax({
//     type:"GET",
//     url: "/invoice/org_address_state/",
//     dataType: "json",
//     success: function(data){
//         if(data.state == null){
//             invoice_user_state = ''
//         }else{
//             invoice_user_state = data.state
//         }
//     },  
// });
var global_gst_type = ''
function customer_gst_type(){
    var ins = $('#invoice_customer').val()
    if(ins != ''){
        $.get("/invoice/customer_gst/"+ins+"/",function(data){
            global_gst_type = data.gst_type
            check_gst_status()
        });
    }else{
        global_gst_type = ''
        check_gst_status()
    }
}

// invoice_tax_cacultion()
// change_state()
// sub_total()
function invoice_tax_cacultion(){
    var state = $('#invoice_state_supply').val()
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
        invoice_total = ''
        invoice_shipping_charges()
    }else{
        $('#Total').val(sc_total)
        invoice_total = sc_total
        invoice_shipping_charges()
    }
    
}
else if(org_state.toLowerCase() != state.toLowerCase()){
    $(".tax").each(function(){
        var tax_id = $(this).attr('id');
        var amount_id = 'Amount'+tax_id.slice(3)+''

        // if($('#'+tax_id+'').val() < parseFloat(100.00)){
        
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
        invoice_total = ''
        invoice_shipping_charges()
    }
    else{
        $('#Total').val(i_total)
        invoice_total = i_total
        invoice_shipping_charges()
    }
}
}
/********************************************************************/
// CHANGE CGST SGST TO IGST
/********************************************************************/

function change_state(){
    var state = $('#invoice_state_supply').val()
    var org_state = $('#single_gst_code option:selected').text()
    if(org_state != '' & state != ''){
        if(org_state.toLowerCase() == state.toLowerCase() || $('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val() == '8'|| $('#org_gst_reg_type').val() == '' || global_gst_type == '0' || global_gst_type =='3' || global_gst_type == '5' || global_gst_type == '8'||global_gst_type == ''){
            $('#invoice_table').find('.row_i_gst').hide()
            $('#invoice_table').find('.row_igst').val('')
            $('#invoice_table').find('.row_cs_gst').show()
            $('#invoice_table').find('.price_header').css('width','7%')
            $('#invoice_table').find('.unit_header').css('width','11%')
            $('#invoice_table').find('.quantity_header').css('width','5%')
            $('#invoice_table').find('.tax_header').css('width','7%')
            $('#invoice_table').find('.invoice_row_header').attr('colspan','8')
        }else if(org_state.toLowerCase() != state.toLowerCase()){
            $('#invoice_table').find('.row_cs_gst').hide()
            $('#invoice_table').find('.row_cgst, .row_sgst').val('')
            $('#invoice_table').find('.row_i_gst').show()
            $('#invoice_table').find('.price_header').css('width','8%')
            $('#invoice_table').find('.unit_header').css('width','12%')
            $('#invoice_table').find('.quantity_header').css('width','6%')
            $('#invoice_table').find('.tax_header').css('width','8%')
            $('#invoice_table').find('.invoice_row_header').attr('colspan','7')
        }
    }
    $(".invoice_line_item").each(function(){

        var ids = $(this).attr('id');
        ids = ids.substring(ids.length - 1, ids.length);
        single_row_gst_cal = 'state'
        var check = row_gst_cal(ids);
    });
    invoice_tax_cacultion()
}

/********************************************************************/
// EACH ROW TAX CALCULATION
/********************************************************************/

var single_row_gst_cal = ''
function row_gst_cal(ids){
    var state = $('#invoice_state_supply').val()
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
            invoice_tax_cacultion()
        }
    }else{
        alert('Please enter valid Tax value')
        $('#tax'+ids+'').val('')
    }
}

/********************************************************************/
// Date Picker
/********************************************************************/
//  NEW INVOICE FOR FIRST TIME 
$("#Invoice_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");
$("#Invoice_one_due_date").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()})
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
        var endDate = $('#Invoice_date').datepicker('getDate', '+31d'); 
        endDate.setDate(endDate.getDate()+31); 
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
    // $('#hasil').val(days);
    if(days == 0){
        $('#invoice_pay_terms').val('On Due Date').change();
    }else if(days == 9){
        $('#invoice_pay_terms').val('10 Days').change();
    }else if(days == 19){
        $('#invoice_pay_terms').val('20 Days').change();
    }else if(days == 31){
        $('#invoice_pay_terms').val('30 Days').change();
    }else if(days == 59){
        $('#invoice_pay_terms').val('60 Days').change();
    }else if(days == 89){
        $('#invoice_pay_terms').val('90 Days').change();
    }else {
        $('#invoice_pay_terms').val('Custom').change();
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
            var invoice_repeat = parseInt(repeat) * 31
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+'+invoice_repeat+'d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+invoice_repeat); 
            $("#hidden_recurring_end").datepicker({dateFormat: 'dd-mm-yy', minDate: new Date()}).datepicker("setDate", endDate );
            $('#Invoice_recurring_end').val($('#hidden_recurring_end').val())
        }else{
            var endDate = $('#Invoice_recurring_start').datepicker('getDate', '+31d'); 
            endDate.setTime(endDate.getTime() - (1000*60*60*24))
            endDate.setDate(endDate.getDate()+31); 
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

/*********************************************************************** */
// DEFUALT INVOICE AND CHECK INVOICE NUMBER IS UNIQUE
/*********************************************************************** */
$("#auto_invoice_number").click(function(){
    if($(this).is(':checked')){
        var ins = 0
        var slug = 'a'
        $.ajax({
            type:"GET",
            url: "/invoice/unique_number/"+ins+"/"+slug+"/",
            dataType: "json",
            success: function(data){
                $('#invoice_number').val(data.invoice_number)
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }else{
        $('#invoice_number').val('')
    }  
});

$("#invoice_number").focusout(function(){
    $("#auto_invoice_number").prop('checked',false);
    var ins = 1
    var invoice_number = $("#invoice_number").val()
    $.ajax({
        type:"GET",
        url: "/invoice/unique_number/"+ins+"/"+invoice_number+"/",
        dataType: "json",
        success: function(data){
            if(data.unique != 0){
                alert('This invoice number is already exits. Please enter the different invoice number.')
                $('#invoice_number').focus();
                $('#invoice_number').val('')
            }
            
        },
    });
  });

/********************************************************************/
//  SHOW AND HIDE EMAIL CC
/********************************************************************/

// SHOW EMAIL CC
function show_cc_mail() {
    $(".ccemail").show()
    // $(".cc").css("margin-top","-3%")
    $('#show_cc').hide()
    // $('#billing_state').css('margin-top', '4%')
  }

// HIDE EMAIL CC
function hide_cc_mail() {
    $(".ccemail").hide()
    $("#ccemail").val('')
    // $(".cc").css("margin-top","0px")
    $('#show_cc').show()
    // $('#billing_state').css('margin-top', '0%')
  }

/********************************************************************/
//  send mail validation
/********************************************************************/

function  sendbtn(){
    var a = $("#email").val()
    if(a == ''){
            alert('Please fill email')
            $("#email").focus()
            return false
        }
        else{
            return true
        }
}

/********************************************************************/
//  customer on change
/********************************************************************/
$('#invoice_customer').change(function(){
    var ids = $(this).val()
    if(ids !=''){
        if($('#one_radio').is(":checked")){
            $.get("/invoice/check_invoice_terms/"+ids+"/", function(data){
        
                if(data.invoice_terms != '0'){
                    $('#invoice_pay_terms').val(data.invoice_terms).change()
                }else{
                    $('#invoice_pay_terms').val('').change()
                    $('#Invoice_one_due_date').val('')
                }
            });
        };
    }else{
        $('#invoice_pay_terms').val('').change()
        $('#Invoice_one_due_date').val('')
    }
});

/********************************************************************/
//  bulk select product
/********************************************************************/
$(function(){
    $('#product_search').keyup(function(){
        $.ajax({
            type: "POST",
            url: "/invoice/search_engin/",
            data: {
                'search_text' : $('#product_search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken").val()
            },
            success: searchSuccess,
            dataType:  'html'
        });
    });
});

function searchSuccess(data, texStatus, jqXHR){
    $('#search_result').html(data);
}

// item add in bulk and remove

var bulk_product_item = 0
function ul_remove(a,b,c,d){
    $('#product_search').val(d)
    var product_bulk = d
    $('#search_result').empty()
    bulk_product_item +=1
    var html = '<tr id="bulk_table'+bulk_product_item+'"><td style="border: 1px solid black"><input type="text" class="form-control bulk_product" value="'+product_bulk+'" id="product'+bulk_product_item+'" readonly><input type="hidden" value="'+a+'" id="product_ids'+bulk_product_item+'">'
    html +='<input type="hidden" class="form-control" value="'+b+'" id="product_price'+bulk_product_item+'"><input type="hidden" class="form-control" value="'+c+'" id="product_unit'+bulk_product_item+'"></td>'
    html += '<td style="border: 1px solid black;"><input type="text" class="form-control" id="bulk_quantity'+bulk_product_item+'" onkeypress="return restrictAlphabets(event), float_value(event,\'bulk_quantity'+bulk_product_item+'\')"></td>'
    html += '<td style="border:1px solid black;"><span class="tbclose material-icons" id="'+bulk_product_item+'" onclick="bulk_removeRow('+bulk_product_item+')" style="margin-left:26%;cursor: default;">delete_forever</span></td></tr>'
    $('#bulk_prodcut_table').append(html)
}

// delete bulk table row

function bulk_removeRow(a){
    $('#bulk_table'+a+'').remove();
}
// bulk model cancel
function hide_bulk_item(){
    $('#search_result').empty()
    $('#bulk_prodcut_table tbody').empty()
    bulk_product_item = 0
}

/********************************************************************/
// CELAN ATTACHEMENT
/********************************************************************/
function clean(){
    $("#Attachment").val('')
    $('#invoice_filename').text('')
}
$(document).ready(function(){
    $('#Attachment').change(function(e){
        $('#invoice_filename').hide()
        $(this).css('width','50%')
        // var fileName = e.target.files[0].name;
        // alert('The file "' + fileName +  '" has been selected.');

    });
});
/********************************************************************/
// CHOOSE FILE SIZE VALIDATION
/********************************************************************/

window.addEventListener('load', function() {
    document.querySelector('#Attachment').addEventListener('change', function() {
        
            //  Image file size less then 1MB
            if(this.files[0].size > 25000000){
                alert('File size less then 25MB');
                $('#Attachment').val("");
                
            }
        
    });
  });

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
        var gst = $('#org_gst_number').val()
        $('#multiple_gst').text("Your default Organization gst number:-"+gst+". Do you want to change gst number.")
        gst = gst.substring(0,2)
		if($("#single_gst_code option[value="+gst+"]").length > 0){

            $('#single_gst_code').val(gst).change()
        }
        check_gst_status()
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
            check_gst_status()
        }
    });
}

$('#Invoice_date,#Invoice_one_due_date,#Invoice_recurring_start').keypress(function(event) {
    event.preventDefault();
});