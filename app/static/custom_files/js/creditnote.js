
/************************************************************ */
// GENTRATE DATE
/************************************************************ */
var d = new Date();
var day = d.getDate()
var month =  (d.getMonth() + 1).toString()
var year = d.getFullYear().toString()
if(day < 10 ){
    day = "0" + day.toString()
}
if(month.length < 2){
    month = "0" + month
}
var date = year+ '-' + month + '-' + day.toString()
$("#CreditNoteDate").val(date)

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
        console.log(creditnote_number);
        for(var i = 1;i <= creditnote_number; i++){
            var a = $('#row_ItemName'+creditnote_number+'').length
            console.log("AA"+a);
            if(a == 0){
                $('.select2-search').append('<button class="btn btn-link credit_product" data-toggle="modal" id="row_ItemName'+creditnote_number+'" onclick="get_credit_product_id('+creditnote_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
            }  
        } 
    });
       



        var html = '<tr id="creditnote_row'+creditnote_number+'">'
        html +='<td style="border:1px solid black;padding-bottom:0%"><select class="form-control select credit_note_item" id="ItemName'+creditnote_number+'" name="ItemName[]" onchange="product('+creditnote_number+'),validation()" style="padding-left:0px"><option value="-------">-------</option></select>'
        html +='<textarea id="desc'+creditnote_number+'" name="desc[]" rows="2" maxlength="200"  size="200" placeholder="Product Description" style="width: 213.6px;margin-top:1px;"></textarea></td>'
        html +='<td style="border:1px solid black;"><input type="text" class="form-control" id="type'+creditnote_number+'" name="type[]" readonly></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Price'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+'),validation()" id="Price'+creditnote_number+'" name="Price[]" style="margin-top:1%"></div></div></td>'
        html +='<td style="border:1px solid black;"><input type="text" class="form-control" id="Quantity'+creditnote_number+'" onkeypress="return restrictAlphabets(event), float_value(event,\'Quantity'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+'), validation()" name="Quantity[]"></td>'
        html +='<td style="border:1px solid black;"><input class="form-control" onchange="validation()" id="Unit'+creditnote_number+'" name="Unit[]" style="padding-left:0px;" readonly></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-7" style="padding-right:3px;"><input type="text" class="form-control" onkeypress="return restrictAlphabets(event), float_value(event,\'Discount'+creditnote_number+'\')" onkeyup="creditnote_calculate('+creditnote_number+')" id="Discount'+creditnote_number+'" name="Discount[]"></div>'
        html += '<div class="col-5" style="padding-left:1px;"><select class="form-control"  id="Dis'+creditnote_number+'" name="Dis[]" onchange="dicount_type('+creditnote_number+')" style="background-color: white;color: black;padding-left:0%;"><option value="%">%</option><option value="₹">₹</option></select></div></div></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-8" style="padding-right:3px"><input list="tax" class="form-control tax" maxlength="5" size="5" onkeyup="creditnote_tax_cacultion()" onkeypress="return restrictAlphabets(event), float_value(event,\'tax'+creditnote_number+'\')" name="tax[]" id="tax'+creditnote_number+'" style="margin-top:-1px"><datalist id="tax"><option value="0"><option value="5"><option value="12"><option value="18"><option value="28"></datalist></div>'
        html += '<div class="col" style="padding-left:0%;padding-right:0%;"><font style="color: black;">%</font></div></div></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right:0%"><label for="Price1">₹</label></div>'
        html +='<div class="col"><input type="text" class="form-control amount" onkeypress="return restrictAlphabets(event), float_value(event,\'Amount'+creditnote_number+'\')" id="Amount'+creditnote_number+'" name="Amount[]" style="margin-top:1%;"></div></div></td>'
        html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+creditnote_number+'" name="'+creditnote_number+'" onclick="creditnote_removeRow('+creditnote_number+')" style="cursor: default;">delete_forever</span></td></tr>'
        $('#creditnote_table').append(html)
        
        // SELECT PLUGIN
        $(function () {
            $(".select").select2();
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
            url: "/creditnotes/add/"+1+"",
            dataType: "json",
            success: function(data){
        
                var option = data.products
                // var unit = data.unit
                var id = data.ids
                for(var i = 0;i < option.length;i++){
                    $('<option/>').val(id[i]).html(option[i]).appendTo('#ItemName'+creditnote_number+'');
                }
        
                // for(var i = 0;i < unit.length;i++){
                //     $('<option/>').val(unit[i]).html(unit[i]).appendTo('#Unit'+number+'');
                // }
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    
};
// REMOVE JS TABLE
function creditnote_removeRow(a) {

$('#creditnote_row'+a+'').remove();
$('#'+a+'').remove();
sub_total()
if(creditnote_number > 1){
    creditnote_number -=1
}

}

/************************************************************ */
// GET CONTACT DETAILS
/************************************************************ */

function data() {
    var contact = $('#customerName option').filter(':selected').val()
    //  $('#customerName :selected').text();
    $.ajax({
        type:"GET",
        url: "/creditnote/contact/"+contact+"",
        dataType: "json",
        success: function(data){
            $("#email").val(data.contacts)
            var option = data.address
            // CLEAN SELECT OPTION //
            var select = document.getElementById('BillingAddress');
            var length = select.options.length;
            console.log(length)
            if(length > 0){
                $("#BillingAddress").empty();
            }
            // for (var i = length; i >= 1; i--) {
            //     console.log(select.options[i] )
            //     select.options[i] = null;
            //     console.log('xxxxxxxxxx')
            // }
            // END //

            // ADD SELECT OPTION //
            for(var i = 0;i < option.length;i++){
                if(i == 0){
                    $('<option/>').val(option[i]).html(option[i]).appendTo('#BillingAddress');
                    $('#BillingAddress1').val(option[i])
                }else{
                    $('<option/>').val(option[i]).html(option[i]).appendTo('#BillingAddress');
                }
                
            }
            // END //
        },
        error: function (rs, e) {
            alert('Sorry, try again.');
        }
    });

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
                if(data.product == 0){
                    $("#type"+a+"").val("GOODS")
                }
                else if(data.product == 1){
                    $("#type"+a+"").val("SERVICES")
                }
                else{
                    $("#type"+a+"").val("BUNDLE")
                }
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
        $("#type"+a+"").val("")
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
        // var fileName = e.target.files[0].name;
        // alert('The file "' + fileName +  '" has been selected.');

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
    console.log("Called");
    for(var i = 1;i <= creditnote_number; i++){
        var a = $('#row_ItemName'+creditnote_number+'').length
        if(a == 0){
        $('.select2-search').append('<button class="btn btn-link credit_product" data-toggle="modal" id="row_ItemName'+creditnote_number+'" onclick="get_credit_product_id('+creditnote_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
        }  
    } 
});

function c(){
    console.log("closed");
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
                creditnote_calculate(a)
            }
        }
        else if(dis_type == '₹'){
            console.log(val)
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
        creditnote_tax_cacultion()
    }
    else{
        $("#SubTotal").val(sub_total)
        creditnote_tax_cacultion()
    }
    
}

/********************************************************************/
// CREDIT_NOTE SGST CGST AND IGST CALCULATION 
/********************************************************************/

    $.ajax({
        type:"GET",
        url: "/creditnote/state_compare/",
        dataType: "json",
        success: function(data){
            credit_note_user_state = data.state
        },  
    });

var credit_note_user_state =''
creditnote_tax_cacultion()
sub_total()
function creditnote_tax_cacultion(){
    var state = $("#supplyPlace1").val()
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
    if(credit_note_user_state.toLowerCase() == state.toLowerCase() || state == 'none'){
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
    else if(credit_note_user_state.toLowerCase() != state.toLowerCase() ){
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
}
/********************************************************************/
// product table validation
/********************************************************************/
var message = ''
function validation(){
    
    for(var i = 1;i <= creditnote_number;i++){
        message = ''
        var product_name = $("#ItemName"+i+"").val()
        var product_type =  $("#type"+i+"").val()
        // var invoice = $("#Reference").val()
        if( product_name != '-------' ){
            var unit = $("#Unit"+i+"").val()
            var quantity = $("#Quantity"+i+"").val()
            var price = $("#Price"+i+"").val()
            if(quantity == '' || quantity == '0'){
                message += 'Table row number '+i+':- fill quantity'
                break;
            }
            else if(unit == '-------'){
                message += 'Table row number '+i+':- choose unit'
                break;
            }
            else if(price == '' || price == '0.0'){
                message = 'Table row number '+i+':- fill price'
                break;
            }

        }
    }
}

function  sendbtn(){
    var a = $("#email").val()
    var b = $("#customerName").val()
    if(b == '-------'){
        alert('Contact name required')
        return false
    }
    else if(message != ''){
        alert(message)
        return false
    }
    else if(a == ''){
        alert('Please fill email')
        return false
    }
    else{
        
        return true
    }
}

function savebtn(){
    var b = $("#customerName").val()
    if(b == '-------'){
        alert('Contact name required')
        return false
    }
    else if(message != ''){
        alert(message)
        return false
    }
    else{
        
        return true
    }
}

function draftbtn(){
    var b = $("#customerName").val()
    if(b == '-------'){
        alert('Contact name required')
        return false
    }
    else if(message != ''){
        alert(message)
        return false
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

    $.post("/contacts/add/",$("#add_creditnote_contact_form").serialize(), function(data){
    if(data != '0'){
        
        $.get("/creditnote/contact_fetch/",function(data){

            $("#customerName").each(function(){
                $('<option/>').val(data.ids).html(data.name).appendTo($(this));
            });
            $('#BillingAddress1').val('')
            $('#email').val('')
            $('#customerName').val(data.ids).change(); 
            
        });
        $("#ContactModal").modal('hide');
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
//     console.log('aaaaaaaaaaa')
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

// $('.Quantity').bind(function(e) {
//     var text = e.originalEvent.clipboardData.getData('Text');
//     if ($.isNumeric(text)) {
//         if ((text.substring(text.indexOf('.')).length > 3) && (text.indexOf('.') > -1)) {
//             e.preventDefault();
//             $(this).val(text.substring(0, text.indexOf('.') + 3));
//        }
//     }
//     else {
//             e.preventDefault();
//          }
//     });
  