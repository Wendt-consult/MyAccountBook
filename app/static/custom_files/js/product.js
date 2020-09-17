$(document).ready(function(){

    // $("#id_selling_tax").empty().append(selling_tax);
    // $('#id_purchase_tax').empty().append(selling_tax);
    // $("#id_selling_tax").val(selling_tax_old);

})



$("#id_is_sales").on("click", function(){
    if($(this).prop("checked") === true){
        $("#id_selling_price, #id_sales_account, #id_edit_sales_account, #sales_tax, #id_selling_tax,#id_preferred_currency").prop("disabled", false);
        
        $('#id_selling_price').prop('required', true)
        $('#id_selling_tax').prop('required', true)
        $('#id_sales_account,#id_edit_sales_account').prop('required', true)
    }else if($('#id_is_purchase').prop("checked") === true){
        $("#id_selling_price, #id_sales_account, #id_edit_sales_account, #sales_tax, #id_selling_tax,#id_preferred_currency").prop("disabled", true);
        $('#sales_tax').prop('checked',false)
        $('#id_selling_price').prop('required', false)
        $('#id_selling_tax').prop('required', false)
        $('#id_sales_account').prop('required', false)
        $('#id_selling_price').val('')
        $('#id_selling_tax').val('')
        $('#id_sales_account,#id_edit_sales_account').val('').change()
        calculate()
    }else{
        alert('Please fill at least one information between sales and purchase')
        $('#id_is_sales').prop('checked',true)
    }
});
// sales information
if($('#id_is_sales').prop("checked") === true){
    $('#id_selling_price').prop('required', true)
    $('#id_selling_tax').prop('required', true)
    $('#id_sales_account').prop('required', true)
}else{
    $("#id_selling_price, #id_sales_account, #sales_tax, #id_selling_tax,#id_preferred_currency").prop("disabled", true);
}
    
$('#id_product_type').prop('required', true)

// Purchase Information
if($('#id_is_purchase').prop("checked") === true){
    $('#id_purchase_price').prop('required', true)
    $('#id_purchase_tax').prop('required', true)
    $('#id_purchase_account').prop('required', true)
}else{
    $("#id_purchase_currency, #id_purchase_price,#purchase_tax,#id_purchase_tax,#id_reverse_charges,#id_purchase_account").prop("disabled", true);
}

$("#id_is_purchase").on("click", function(){
    if($(this).prop("checked") === true){
        $("#id_purchase_currency, #id_purchase_price,#purchase_tax,#id_purchase_tax,#id_reverse_charges,#id_purchase_account,#id_edit_purchase_account").prop("disabled", false);
        
        $('#id_purchase_price').prop('required', true)
        $('#id_purchase_tax').prop('required', true)
        $('#id_purchase_account').prop('required', true)
    }else if($('#id_is_sales').prop("checked") === true){
        $("#id_purchase_currency, #id_purchase_price,#purchase_tax,#id_purchase_tax,#id_reverse_charges,#id_purchase_account,#id_edit_purchase_account").prop("disabled", true);
        $('#purchase_tax').prop('checked',false)
        $('#id_purchase_price').prop('required', false)
        $('#id_purchase_tax').prop('required', false)
        $('#id_purchase_account').prop('required', false)
        $('#id_purchase_price').val('')
        $('#id_purchase_tax').val('')
        $('#id_reverse_charges').val('')
        $('#id_purchase_account').val('').change()
        calculate_pc()
    }else{
        alert('Please fill at least one information between sales and purchase')
        $('#id_is_purchase').prop('checked',true)
    }
});

$(".disabled-tr select, .disabled-tr input, .disabled-tr textarea").prop("disabled", true);

$("#id_product").empty().html('<option value="" selected="">---------</option>"');

/********************************************************************/
// PRODUCT CHECK
/********************************************************************/


function check_product_name(elem, add_form){
	if($(elem).val()!=""){
		
		if(add_form){
			add_form = 0; 
			prod_id = 0;
		}
		else{
			add_form = 1;
			prod_id = prod_id;
		}
		
		$.get("/check_existing_product/",{"ins":$(elem).val(), "add_form":add_form, "prod_id":prod_id}, function(data){
						
			if(data["counter"]>0){				
				$(elem).val(data["pre_val"]);
				$(elem).focus();
				alert("Another product or service is already using this name. Please use a different name.");
				$("#add_product").prop("disabled", true);
			}else{
				$("#add_product").prop("disabled", false);
			}
		});
	
	}else{
		$(elem).focus();
		$("#add_product").prop("disabled", true);
	}	
}
	


/********************************************************************/
// IMAGE SLIDER
/********************************************************************/

var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
    var i;
    x = $("img.mySlides");
    
    if (n > x.length) {slideIndex = 1}
    if (n < 1) {slideIndex = x.length}
    
    for (i = 0; i < x.length; i++) {
        x.eq(i).css("display","none");  
    }

    x.eq(slideIndex-1).css("display","block");
}


function deleteDivs(pid, ids){
    // $.get("/delete_product_image/"+pid+"/"+ids+"/", function(data){
    //     location.reload();
    // });

    $("#id_hidden_img").val(pid);
    $("#myImg").attr('src','');

}


/********************************************************************/
// SHOW PRODUCT IMAGE 
/********************************************************************/

// $(document).ready(function() {
//     if (window.File && window.FileList && window.FileReader) {
//       $("#files").on("change", function(e) {
//         var files = e.target.files,
//           filesLength = files.length;
//           console.log(files)
//           console.log(filesLength)
//           var check = 1
          
//         for (var i = 0; i < filesLength; i++) {
//           var f = files[i]
//           console.log(i)
//           var fileReader = new FileReader();
//            fileReader.onload = (function(e) {
//             var file = e.target;
//             $("<span class=\"pip\">" +
//               "<img class=\"imageThumb\" src=\"" + e.target.result + "\" title=\"" + file.name + "\"/>" +
//               "<br/><span class=\"remove\">Remove image</span>" +
//               "</span>").insertAfter("#files");
//             $(".remove").click(function(){
//               $(this).parent(".pip").remove();
//             });
            
//             // Old code here
//             /*$("<img></img>", {
//               class: "imageThumb",
//               src: e.target.result,
//               title: file.name + " | Click to remove"
//             }).insertAfter("#files").click(function(){$(this).remove();});*/
            
//           });
//           fileReader.readAsDataURL(f);
//         }
      
//       });
    
//     } else {
//       alert("Your browser doesn't support to File API")
//     }
//   });

/*
window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function() {

        // image extension validation
        if (!this.files[0].name.match(/.(jpg|jpeg|png|gif)$/i)){
            alert('Please select Image file ');
            $('#files').val("");
        }
        else {
            //  Image file size less then 1MB
            if(this.files[0].size > 1000000){
                alert('Image file size less then 1MB');
                $('#files').val("");

            }
            else if (this.files && this.files[0]) {
                var img = document.querySelector('img');  // $('img')[0]
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url
                $(".close").show()
                
            }
        }
    });
  });
  $('.close').click(function (e) {
    $('img').attr('src', '');
    $('#files').val("");
    $('.close').hide()

    
});

*/
/********************************************************************/
// view product active inactive and delete 
/********************************************************************/

function status(a,b) {

    var status = 's'+a.toString()
    var remove = 't'+a
    var c = document.getElementById(status).innerHTML;
    if(c.length == 13){
        $.ajax({
        type: 'GET',
        url: "/products/status_change/deactivate/"+a+"",
        success: function() {
            // document.getElementById(a).innerHTML = 'clear'
            // document.getElementById(status).innerHTML = 'Make Active'
            $("#"+remove).hide();
            $('#'+'status'+a.toString()).modal('hide')
            // document.getElementById('text').innerHTML = 'Are you sure you want to make '+b+' active '
            
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("some error");
        }

    });
    }
    if(c.length == 11){
        $.ajax({
        type: 'GET',
        url: "/products/status_change/activate/"+a+"",
        success: function() {
            // document.getElementById(a).innerHTML = 'check'
            // document.getElementById(status).innerHTML = 'Make Inactive'
            $("#"+remove).hide();
            $('#'+'status'+a.toString()).modal('hide')
            // document.getElementById('text').innerHTML = 'Are you sure you want to make '+b+' inactive '
            
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
var remove = 't'+c
$.ajax({
        type: 'GET',
        url: "/products/delete/"+c+"",
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
// bundle table -- Changes Made By Lawrence
/********************************************************************/
// Add Row
/*
var number = 1
function addRow() {
    number += 1
    $('#table').append('<tr id="row'+number+'"><th scope="row'+number+'">'+number+'</th><td> <select class="form-control" id="product_type'+number+'" name="product_type'+number+'" onclick="bundle('+number+')" style="width: 107% !important;"><option value="------">------</option><option value="Goods">GOODS</option><option value="Services">SERVICES</option></td><td><select class="form-control" id="Product_name'+number+'" name="Product_name'+number+'" style="margin-left: 31px !important;width: 142% !important;"><option value="product_name">------</option></td><td><input type="number" class="form-control" id="Quantity'+number+'" name="Quantity'+number+'" style="margin-left: 90px !important;width:37% !important;"></td><td><button class="btn btn-danger btn-remove" type="button" id="'+number+'" name="'+number+'" onclick="removeRow(number)" style="padding-left:7px;padding-right:7px;margin-top:-8px;padding-top:6px;padding-bottom:6px;width: 96%;"><b>X</b></button></td></tr>')
    
};
*/
var number = 1
var count = 0
function addRow(b) {
    if(count == 0){
        number +=b
        count +=1
    }
    number += 1
    htm = '<tr id="row_'+number+'"></th>';
    htm += '<td style="border: 1px solid black;padding-bottom:2%;"> <select class="form-control bundle_product_type" name="prod_type[]" onchange="bundle($(this),\'#product_name_'+number+'\', [\'#quantity_'+number+'\'])" style="margin-top: 7%;" required><option value="">------</option><option value="0">GOODS</option><option value="1">SERVICES</option></td>';
    htm += '<td style="border: 1px solid black;padding-bottom:2%;"><select class="form-control bundle_product_name" id="product_name_'+number+'" name="prod_name[]" style="margin-top: 3%;" requried><option value="">------</option></td>';
    htm += '<td style="border: 1px solid black;padding-bottom:2%;"><input id="quantity_'+number+'" type="text" onkeypress="return restrictAlphabets(event), float_value(event,\'quantity_'+number+'\')"  class="form-control bundle_product_qunatity" name="qty[]" style="margin-top: 7%;" requried></td>';
    htm += '<td style=""><span class="tbclose material-icons" onclick="removeRow('+number+')" id="'+number+'" name="'+number+'" >delete_forever</span></td></tr>';
    $('#table').append(htm);
    
};


function removeRow(a) {
    $('#row_'+a+'').remove();
    if(creditnote_number > 1){
        number -=1;
    }
    
}

function bundle(elem, target_elem, empty_elems){

    if(empty_elems.length > 0){
        for(i=0; i<empty_elems.length; i++){
            $(empty_elems[i]).val("");
        }
    }   

    if($(elem).val() !="-1"){
        get_products($(elem).val(), target_elem);   
    }else{   
        $(target_elem).empty("").append('<option value="-1">---------</option>');
    }
}

function get_products(prod_type, target_elem){
    $.get("/prducts/bundle/",{'prod_type' : prod_type},function(data){
        $(target_elem).empty().append(data);
    });
}


/********************************************************************/
// bundle table   select INPUT FIELD
/********************************************************************/

/*
function bundle(number) {
    var value = $('#product_type'+number+' :selected').text();
    if(value == 'GOODS' || value == 'SERVICES'){
        $.ajax({
            type:"GET",
            url: "/prducts/bundle/"+value+"",
            dataType: "json",
            success: function(data){
                var option = data.products
                // CLEAN SELECT OPTION //
                var select = document.getElementById('Product_name'+number+'');
                var length = select.options.length;
                for (i = length-1; i >= 1; i--) {
                    select.options[i] = null;
                }
                // END //

                // ADD SELECT OPTION //
                for(var i = 0;i < option.length;i++){
                    $('<option/>').val(option[i]).html(option[i]).appendTo('#Product_name'+number+'');
                }
                // END //
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }
}
*/

/********************************************************************/
// product type to show and hide 
/********************************************************************/

function show_bundle(elem){
    var a = $(elem).val();
    if(a == "2"){
        $(".bundle_dont_show").hide();
        $(".bundle_show").show();
        $('#hsn_code').hide();
        $('#id_hsn_code').val('')
        $("#set_row_span").attr("rowspan",5);
        $("#td1").css('margin-top','8%')
        $('#id_tds').prop("disabled", false);
        $('.bundle_product_type').prop('required',true)
        $('.bundle_product_name').prop('required',true)
        $('.bundle_product_qunatity').prop('required',true)
    }
    else if(a == '0' || a == '1'){
        $('#id_tds').val('0.0')
        $('#id_tds').prop("disabled", true);
        $(".bundle_dont_show").show();
        $(".bundle_show").hide();
        $('#hsn_code').show();
        $('.bundle_product_type').prop('required',false)
        $('.bundle_product_name').prop('required',false)
        $('.bundle_product_qunatity').prop('required',false)
    }
    else{
        $(".bundle_dont_show").show();
        $(".bundle_show").hide();
        $('#hsn_code').show();
        $('#id_tds').prop("disabled", false);
        $('.bundle_product_type').prop('required',false)
        $('.bundle_product_name').prop('required',false)
        $('.bundle_product_qunatity').prop('required',false)
    }
}
var a = $('#id_product_type :selected').text();
if(a == "BUNDLE"){
    $(".bundle_dont_show").hide();
    $(".bundle_show").show();
    $('#hsn_code').hide();
    $('#id_hsn_code').val('')
    $("#set_row_span").attr("rowspan",5);
    $("#td1").css('margin-top','8%')
    $('#id_tds').prop("disabled", false);
    $('.bundle_product_type').prop('required',true)
    $('.bundle_product_name').prop('required',true)
    $('.bundle_product_qunatity').prop('required',true)
}
else if(a == 'GOODS' || a == 'SERVICES'){
    $('#id_tds').prop("disabled", true);
    $(".bundle_dont_show").show();
    $(".bundle_show").hide();
    $('#hsn_code').show();
    $('.bundle_product_type').prop('required',false)
    $('.bundle_product_name').prop('required',false)
    $('.bundle_product_qunatity').prop('required',false)
}
else{
    $(".bundle_dont_show").show();
    $(".bundle_show").hide();
    $('#hsn_code').show();
    $('#id_tds').prop("disabled", false);
    $('.bundle_product_type').prop('required',false)
    $('.bundle_product_name').prop('required',false)
    $('.bundle_product_qunatity').prop('required',false)
}


// COMMENTED BY LAWRENCE

/********************************************************************/
// ADD PRODUCT SALE ACCOUNT SELECT OPTION
/********************************************************************/
/*
    var opt = {
        Income:[
            {name:"Discount"},
            {name:"General Income"},
            {name:"Interest Income"},
            {name:"Late Fee Income"},
            {name:"Other Charges"},
            {name:"Sales"},
            {name:"Shipping Charges"},
        ],       
    };
    
    $(function(){
        var $select = $('#id_sales_account');
        $.each(opt, function(key, value){
            var group = $('<optgroup label="' + key + '" />').css('color','yello');
            $.each(value, function(){
                $('<option />').val(this.name).html(this.name).appendTo(group);
            });
            group.appendTo($select);
        });
    });
*/
/********************************************************************/
// INPUT TYPE NUMBER SROLL HIDE
/********************************************************************/

// Disable Mouse scrolling
$('input[type=number]').on('mousewheel',function(e){ $(this).blur(); });
// Disable keyboard scrolling
$('input[type=number]').on('keydown',function(e) {
    var key = e.charCode || e.keyCode;
    // Disable Up and Down Arrows on Keyboard
    if(key == 38 || key == 40 ) {
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
/*******************************************************************/
//  CODE BY LAWRENCE
/*******************************************************************/

function delete_bundle_product(ids, pro_id, sku, name){

    if(sku!="" && name!="") $("#product_details_span").text(sku +" - "+name);
    else if(sku!="" && name=="") $("#product_details_span").text(sku);
    else if(sku=="" && name!="") $("#product_details_span").text(name);
    else $("#product_details_span").text("");

    $("#product_delete_link").attr("href","/delete_bundle_product/"+ids+"/"+pro_id+"/"); 

    $("#delProductModal").modal('show');
}


function edit_bundle_product(ids, pro_id, sku, name, qty = 0){
    if(sku!="" && name!="") $("#product_edit_details_span").text(sku +" - "+name);
    else if(sku!="" && name=="") $("#product_edit_details_span").text(sku);
    else if(sku=="" && name!="") $("#product_edit_details_span").text(name);
    else $("#product_edit_details_span").text("");

    $("#product_edit_link").attr("href","/edit_bundle_product/"+ids+"/"+pro_id+"/"); 

    $("#bundle_product_quantity").val(qty);
    $("#bundle_product_obj").val(pro_id);
    
    $("#editProductModal").modal('show');
}


/************************************************************/
//   IMAGE PREVIEWS
/************************************************************/
// function readURL(input, target_elem) {

//     const file = document.querySelector('input[type=file]').files[0];

//     var reader = new FileReader();
    
//     reader.addEventListener("load", function () {
//         $(target_elem).css('background-image', 'url("'+reader.result+'")');
//         $(target_elem).css('background-repeat', 'no-repeat');
//         $(target_elem).css('background-size', '260px 160px');
//         $("#delete_image_or_preview").attr("onclick","DeletePreview()")
//     }, false);
    
//     if (file) {
//         reader.readAsDataURL(file);
//     }
// }

/************************************************************/
//   IMAGE PREVIEW DELETE
/************************************************************/
// function DeletePreview(elem) {
//     $("input[type=file]").val("");
//     $("#img_block").css('background-image', 'url("")');
// }


/************************************************************/
//   IMAGE VALIDATION DELETE
/************************************************************/


window.addEventListener('load', function() {
    document.querySelector('#files').addEventListener('change', function() { 
        // image extension validation
        if (!this.files[0].name.match(/.(jpg|jpeg|png|gif)$/i)){
            alert('Please select Image file type: jpg,jpeg,png,gif');
            $('#files').val("");
        }
        else {
            //  Image file size less then 1MB
            if(this.files[0].size > 1000000){
                alert('Image file size less then 1MB');
                $('#files').val("");

            }
            else if (this.files && this.files[0]) {
                var img = document.querySelector('#myImg_preview');  // $('img')[0]
				$("img").hide();
				$(".close").show()
				$("span.image_deleter").hide();
				$("#myImg_preview").show();				
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url 
                $("#files").css('width','210px');              
            }
        }
    });
  });
  
$('.close').click(function (e) {
    $('#myImg_preview').attr('src', '');
    $('#files').val("");
    $('.close').hide()
	$("#myImg_preview").hide();	
	$(".image_deleter").show();
    $("#myImg").show();
    $("#myImgclone").hide()
    
});

  /************************************************************/
//   SELLING PRICE + GST CALCULATION
/************************************************************/
var temp = '0.0'
var temp2 = '0.0'
function calculate(){
    
    change_SP()
    
}

function change_SP(){
    var gst = $("#id_selling_tax").val()
    if(gst != ''){
        var selling_price = $("#id_selling_price").val();
        if ($('#sales_tax').is(":checked")){
            temp = $("#id_selling_price").val();
            var cal = (parseFloat(selling_price) + (parseFloat(selling_price)*(parseFloat(gst) / 100))).toFixed(2);
            if(cal == 'NaN'){
                $("#id_inclusive_tax").val('');
            }else{
                $("#id_inclusive_tax").val(parseFloat(cal));
            }	
        }
        else{
            
            $("#id_inclusive_tax").val('');
        }
    }
}

function capture_SP(){
	setLocalStorageValue('captured_SP', $("#id_selling_price").val());
}	
    

function calculate_pc(){
    
    change_PC()
    
}
function change_PC(){
    var purchase_tax = $("#id_purchase_tax").val()
    if(purchase_tax != ''){
        var purchase_price = $("#id_purchase_price").val();
        if ($('#purchase_tax').is(":checked")){
            temp2 = $("#id_purchase_price").val();
            var cal = (parseFloat(purchase_price) + (parseFloat(purchase_price)*(parseFloat(purchase_tax) / 100))).toFixed(2);
            if(cal == 'NaN'){
                $("#id_inclusive_purchase_tax").val('');
            }else{
                $("#id_inclusive_purchase_tax").val(parseFloat(cal));
            }	
        }
        else{
            
            $("#id_inclusive_purchase_tax").val('');
        }
    }
}
/********************************************************************/
// PRODUCT CHECK
/********************************************************************/

function product_clear_row(){
    $('#product_type_1').val('-1').change();
    $('#product_name_1').val('0').change();
    $('#quantity_1').val('')
        
    }

/********************************************************************/
// PRODUCT CHECK
/********************************************************************/
$('#currnecy_type').text($("#id_preferred_currency option:selected").text())
function select_change(){
    var a = $("#id_preferred_currency option:selected").text()
    $('#currnecy_type').text(a)
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
/*code: 48-57 Numbers 8  - Backspace, 35 - home key, 36 - End key 37-40: Arrow keys, 46 - Delete key*/
function restrictAlphabets(e){
    var x=e.which||e.keycode;
    if((x>=48 && x<=57) || x==8 ||
        (x>=35 && x<=40)|| x==46) 
        return true;
    else
        return false;
}

/**********************************************************/
// VALIDATION
/**********************************************************/
function check(){
    $("#error_major").text('')
    // $("#select2-id_acc_group-container").text('')
    $("#error_group").text('')
    $("#error_account").text('')
    $("#error_name").text('')
}

function info(ins,slug){
    $.ajax({
        type:"GET",
        url: "/add_ledger_group/"+ins+"/"+slug+"",
        dataType: "json",
        success: function(data){
            var info = data.account
            $("#id_info_message").val(info)
        },  
    });
}

/**********************************************************/
// FLoat value Calculation
/**********************************************************/
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

/**********************************************************/
// Sellinh=g / Purchase Tax Validation
/**********************************************************/

$('#id_selling_tax').keyup(function(){
    if(parseFloat($(this).val()) > parseFloat(99.99)){
        alert("Enter Vaild Tax")
        $(this).val('')
    }
});

$('#id_purchase_tax').keyup(function(){
    if(parseFloat($(this).val()) > parseFloat(99.99)){
        alert("Enter Vaild Tax")
        $(this).val('')
    }
});

$('#id_tds').keyup(function(){
    if(parseFloat($(this).val()) > parseFloat(99.99)){
        alert("TDS must be less than 100%")
        $(this).val('')
    }
});
/********************************************************************/
// SALES_ACCOUNT SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $("#id_sales_account").select2();
        // $('.select2-container--default').css('padding-bottom','16px')
      });
    });

$(document).on('click','#select2-id_sales_account-container',function(){
    var a = $('#addProductIncome').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="product_income_sales()" id="addProductIncome" data-target="#addGroupModalIncome" style="margin-left: -8%;">+ Add Income</button>');
        }
        });

function product_income_sales(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#id_sales_account").select2();
          });
        });
} 

/********************************************************************/
// PURCHASE_ACCOUNT SEARCH AND BUTTON INSIDE SELECT TAG 
/********************************************************************/

$(document).ready(function() {
    $(function () {
        $("#id_purchase_account").select2();
        $('.select2-container--default').css('margin-top','-4px')
      });
    });

$(document).on('click','#select2-id_purchase_account-container',function(){
    var a = $('#addProductExpence').length
        if(a == 0){
            $('.select2-search').append('<button class="btn btn-link " data-toggle="modal" onclick="product_expence_sales()" id="addProductExpence" data-target="#addGroupModalExpense" style="margin-left: -8%;">+ Add Expense</button>');
        }
        });

function product_expence_sales(){
    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $("#id_purchase_account").select2();
          });
        });
} 
/********************************************************************/
// AJAX USE TO SAVE PRODUCT INCOME FORM
/********************************************************************/
function add_group_income_form(save_type){
  
    event.preventDefault()

    if($('#addGroupModalIncome').find('#id_group_name').val() == ''){
        alert('group name is requried')
        $('#addGroupModalIncome').find('#id_group_name').focus()
        return false
    }

    $.post("/add_ledger_group/",$("#add_group_income").serialize(), function(data){
    if(data != '0'){
        
        $.get("/purchase_order/account_group_fetch/",function(data){

            $('<option/>').val(data.ids).html(data.group_name).appendTo($("#id_sales_account optgroup"));
            $('#id_sales_account').val(data.ids).change(); 
            
        });
        $("#addGroupModalIncome").modal('hide');
    }
  
});
}
/********************************************************************/
// AJAX USE TO SAVE PRODUCT INCOME FORM
/********************************************************************/
function add_group_expence_form(save_type){
  
    event.preventDefault()

    if($('#addGroupModalExpense').find('#id_group_name').val() == ''){
        alert('group name is requried')
        $('#addGroupModalExpense').find('#id_group_name').focus()
        return false
    }

    $.post("/add_ledger_group/",$("#add_group_expense").serialize(), function(data){
    if(data != '0'){
        
        $.get("/purchase_order/account_group_fetch/",function(data){

            $('<option/>').val(data.ids).html(data.group_name).appendTo($("#id_purchase_account optgroup"));
            $('#id_purchase_account').val(data.ids).change(); 
            
        });
        $("#addGroupModalExpense").modal('hide');
    }
  
});
}