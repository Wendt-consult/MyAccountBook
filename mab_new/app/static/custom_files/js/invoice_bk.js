$(document).ready(function(){

    $("#tr-set-0").find("i").hide();

});

//********************************************************************************* */
// GLOBAL VARIABLES
//********************************************************************************** */
//

address_list = []

//
//
//
//
$("#id_recipient_state_code").on("change",function(){
    var usc = $("#user_state_code").val();

    if(usc!="None" && $(this).val() === usc && $(this).val()!=""){
        $(".tbody-cgst, .thead-cgst").show();
        $("#thead-igst, .tbody-igst").css('display', 'none');
    }else{
        $("#thead-igst, .tbody-igst").show();
        $(".tbody-cgst").hide();
        $(".thead-cgst").hide();
    }

});

//********************************************************************************* */
// ADD PRODUCT TO INVOICE
//********************************************************************************** */
//
$("#add_shopping_cart").on("click", function(){

    var tr_html = $("tr#tr-set-0").html();
    var rowCount = $('#product_table tr').length;

    tr_html = tr_html.replace(/invoiceproducts_set-0/g, "invoiceproducts_set-"+(rowCount-1));
    tr_html = tr_html.replace(/id_invoiceproducts_set-0/g, "id_invoiceproducts_set-"+(rowCount-1));

    new_html = '<tr id="tr-set-'+(rowCount-1)+'"></tr>';
    $('#product_table tbody').append(new_html);
    $("#tr-set-"+(rowCount-1)).empty().append(tr_html);

    $("#tr-set-"+(rowCount-1)).find("i").show();

    $("#id_invoiceproducts_set-TOTAL_FORMS").val(rowCount);

});

//**************************************************************************************** */
// DELETE PRODUCT FORM
//**************************************************************************************** */
//

function delete_product_from_invoice_form(elem){
    var tr = $(elem).parents('tr');    

    if(tr.attr("id") != 'tr-set-0'){
        $("#"+tr.attr("id")).remove();
        var rowCount = $('#product_table tr').length;
        $("#id_invoiceproducts_set-TOTAL_FORMS").val(rowCount);
    }
}

//**************************************************************************************** */
// FETCH CONTACTS DETAILS
//**************************************************************************************** */
//

$("select#id_service_recipient").on("change", function(){
    var ids = $(this).val();  
    address_list = []
    fetch_addresses(ids);
});


function fetch_addresses(ids){
    if(ids){
        $.get('/fetch_contact_addresses/'+ids+'/', function(data){
            address_list = data = $.parseJSON(data);
    
            var htm = '';
    
            $.each(data.addresses, function(i,v){

                if(v.id != null){
                    htm += '<option value="'+v.id+'">'+v.contact_person+', ';
                    htm += v.flat_no+', '; 
                    htm += v.street+', '; 
                    htm += v.city+', ';
                    htm += v.state+', ';
                    htm += v.country+', ';
                    htm += v.pincode+'</option>';
                }                
            });
    
            $("#contact_addresses").find("i").show();
    
            $("#id_service_recipient_address").empty().append(htm);
            $("td#organization_name").empty().text(data.organization_name);
    
        });
    }else{
        $("#contact_addresses").find("i").hide();
        $("#id_service_recipient_address").empty();
    }  
}



//**************************************************************************************** */
// FETCH PRODUCT DETAILS
//**************************************************************************************** */
//

function get_product_details(elem){

    ids = $(elem).val();
    atr = $(elem).attr("id");

    atr = atr.replace("id_invoiceproducts_set-","")
    atr = atr.replace("-product","")

    $.get('/fetch_product_details/'+ids+'/', function(data){
        data = $.parseJSON(data);

        $("#id_invoiceproducts_set-"+atr+"-producttype").val(data.product_type);

        /*
        quantity_in_stock_html = '';
        for(i=0; i <= data.quantity_in_stock; i++){
            quantity_in_stock_html += '<option>'+i+'</option>';
        }

        $("#id_invoiceproducts_set-"+atr+"-quantity").empty().append(quantity_in_stock_html);
        */

        $("#id_invoiceproducts_set-"+atr+"-quantity").val(0);
        $("#id_invoiceproducts_set-"+atr+"-price").val(data.details[0].selling_price);
        $("#id_invoiceproducts_set-"+atr+"-discount").val(data.details[0].discount);
        $("#id_invoiceproducts_set-"+atr+"-tax").val(parseInt(data.details[0].gst));        
    });
}

//**************************************************************************************** */
// 
//**************************************************************************************** */
//

function product_quantity(elem){
    atr = $(elem).attr("id");

    atr = atr.replace("id_invoiceproducts_set-","");
    atr = atr.replace("-quantity","");

    subtotal = $(elem).val() * $("#id_invoiceproducts_set-"+atr+"-price").val();
    subtotal_inc_tax = 0;
    
    if($("#id_invoiceproducts_set-"+atr+"-tax").val()>0){
        subtotal_inc_tax = subtotal + (subtotal * (parseInt($("#id_invoiceproducts_set-"+atr+"-tax").val())/100));
    }
    
    $("#id_invoiceproducts_set-"+atr+"-subtotal").val(subtotal);
    $("#id_invoiceproducts_set-"+atr+"-subtotal_inc_tax").val(subtotal_inc_tax);
  
    //
    var np_forms = $("#id_invoiceproducts_set-TOTAL_FORMS").val();

    sum = 0;
    total_tax = 0;
    for(i=0; i<np_forms; i++){
        sum += parseInt($("#id_invoiceproducts_set-"+i+"-subtotal").val());
        total_tax += subtotal * (parseInt($("#id_invoiceproducts_set-"+atr+"-tax").val())/100);
    }

    $("#id_subtotal").val(sum);
    $("#id_subtotal_inc_tax").val(total_tax);
    $("#id_total").val(sum+total_tax);
}

//**************************************************************************************** */
//
//**************************************************************************************** */
//
$("#id_invoice_type").on("change", function(){
    $("tr#tr-recurring").hide();
    if($(this).val()==1) $("tr#tr-recurring").show();
});


//**************************************************************************************** */
//
//**************************************************************************************** */
//
function ajax_add_product(){
    $.post("/ajax_add_product/", $("#addProductModal_form").serialize(), function(data){
        $.get("/fetch_products_dropdown/", function(data){
            document.getElementById("addProductModal_form").reset();
            $(".product_dropdown_select").empty().append(data);
        });
    });
}

//**************************************************************************************** */
//
//**************************************************************************************** */
//
function ajax_add_contact(){
    
    if($("#id_contact_name").val()!=""){
        $.post("/add_contact_or_employee/", $("#addContactModal_form").serialize(), function(data){
            $.get("/get_contacts_dropdown/",function(data){
                $("#id_service_recipient").empty().append(data);
                $("#addContactModal_form").reset();
                $("#addContactModal").modal('hide');                
            });
        });
    }else{
        $("#id_contact_name").focus();
    }
}

//**************************************************************************************** */
//
//**************************************************************************************** */
//

function open_address_modal(ids){

    document.getElementById("addressModal_form").reset();
    
    $("#edit_or_add").val(ids);

    if(ids == 0){
        
        $.each(address_list.addresses, function(i,v){

            if(v.id == $("#id_service_recipient_address").val()){
                $("#id_form3-contact_person").val(v.contact_person);
                $("#id_form3-flat_no").val(v.flat_no);
                $("#id_form3-street").val(v.street);
                $("#id_form3-city").val(v.city);
                $("#id_form3-pincode").val(v.pincode);
                $("#id_form3-state").val(v.state);
                $("#id_form3-country").val(v.country);

                if(v.is_shipping_address) is_shipping_address = "True";
                else is_shipping_address = "False";

                if(v.is_billing_address) is_billing_address = "True";
                else is_billing_address = "False";

                $("#id_form3-is_shipping_address").val(is_shipping_address);
                $("#id_form3-is_billing_address").val(is_billing_address);
            }
        });
    }

    $("#addressModal").modal('show');
}


//**************************************************************************************** */
//
//**************************************************************************************** */
//
function ajax_add_address(){

    ids = $("#id_service_recipient").val();
    obj = $("#edit_or_add").val();

    url = "/add_edit_address/"+ids+"/";

    if(obj == 0){
        var x_obj = $("#id_service_recipient_address").val();
        if(x_obj!=null) url = "/add_edit_address/"+ids+"/"+x_obj+"/";
    } 

    address_list = []

    $.post(url, $("#addressModal_form").serialize(), function(data){
        if(data == 1) fetch_addresses(ids);        
    });

    $("#addressModal").modal('hide');

}