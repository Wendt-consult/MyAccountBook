
function open_edit_modal(ids){

    $("#EditInventoryProductModal").find("#obj_ins").val(ids);

    $.post("/inventory/get_edit_inventory_product_form/", 
        {'csrfmiddlewaretoken': csrf_token, 'ids':ids},
        function(data){
            if(data!=''){
                edit_forms_creator(data);
                $("#EditInventoryProductModal").modal('show');
            }            
        }   
    );
}


