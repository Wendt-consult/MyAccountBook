/*******************************************************************/
// CODE BY LAWRENCE GANDHAR
/*******************************************************************/
function send_creditnote(id){
	$.get("/send_creditnote/"+id+"/", function(data){
		if(data=='1') alert("Credit Note Sent");
		else alert('Email address not mentioned');
	});
}
/*******************************************************************/
// CUSTOMIZE VIEW LIST
/*******************************************************************/
// $(document).ready(function(){
 
    function customize_view(ids){
    $('#CustomizeViewModel').modal('hide')
    data = {}
    if(ids == 1){
        if($("#first #customize_contact_name").length){
            data['name'] = 1
        }else{
            data['name'] = 0
        }
        if($("#first #customize_contact_org").length){
            data['org'] = 1
        }else{
            data['org'] = 0
        }

        if($('#first #customize_contact_mail').length){
            data['mail'] = 1
        }else{
            data['mail'] = 0
        }

        if($('#first #customize_contact_phone').length){
            data['phone'] = 1
        }else{
            data['phone'] = 0
        }

    }else if(ids == 2){
        if($('#first #customize_product_sku').length){
            data['sku'] = 1
        }else{
            data['sku'] = 0
        }
        if($('#first #customize_product_type').length){
            data['type'] = 1
        }else{
            data['type'] = 0
        }
        if($('#first #customize_product_name').length){
            data['name'] = 1
        }else{
            data['name'] = 0
        }
        if($('#first #customize_product_hsn').length){
            data['hsn'] = 1
        }else{
            data['hsn'] = 0
        }

        if($('#first #customize_product_desc').length){
            data['desc'] = 1
        }else{
            data['desc'] = 0
        }

        if($('#first #customize_product_selling').length){
            data['selling'] = 1
        }else{
            data['selling'] = 0
        }

        if($('#first #customize_product_purchase').length){
            data['purchase'] = 1
        }else{
            data['purchase'] = 0
        }

    }else if(ids == 3){

        if($('#first #customize_credit_note').length){
            data['note'] = 1
        }else{
            data['note'] = 0
        }
        if($('#first #customize_credit_name').length){
            data['name'] = 1
        }else{
            data['name'] = 0
        }
        if($('#first #customize_credit_reference').length){
            data['reference'] = 1
        }else{
            data['reference'] = 0
        }

        if($('#first #customize_credit_date').length){
            data['date'] = 1
        }else{
            data['date'] = 0
        }

        if($('#first #customize_credit_amount').length){
            data['amount'] = 1
        }else{
            data['amount'] = 0
        }

    }else if(ids == 4){

        if($('#first #customize_order_number').length){
            data['number'] = 1
        }else{
            data['number'] = 0
        }
        if($('#first #customize_order_reference').length){
            data['reference'] = 1
        }else{
            data['reference'] = 0
        }

        if($('#first #customize_order_vendor').length){
            data['vendor'] = 1
        }else{
            data['vendor'] = 0
        }

        if($('#first #customize_order_status').length){
            data['status'] = 1
        }else{
            data['status'] = 0
        }

        if($('#first #customize_order_total').length){
            data['total'] = 1
        }else{
            data['total'] = 0
        }

        if($('#first #customize_order_date').length){
            data['date'] = 1
        }else{
            data['date'] = 0
        }

    }else if(ids == 5){

    }
    
     $.ajax({
      url: '/customize_view/'+ids+'/',
      type: 'POST',
      data: {'data':JSON.stringify(data), 'csrfmiddlewaretoken':csrf_token},
      beforeSend: function(){
       // Show image container
       $('#customize_table').hide();
       $(".loader").show();
       
      },
      success: function(data){
        if(ids == 1){
            if(data['name']  == 1){
                $('.customize_name').show()
            }else{
                $('.customize_name').hide()
            }
            if(data['org'] == 1){
                $('.customize_org').show()
            }else{
                $('.customize_org').hide()
            }
    
            if(data['mail'] == 1){
                $('.customize_mail').show()
            }else{
                $('.customize_mail').hide()
            }
    
            if(data['phone'] == 1){
                $('.customize_phone').show()
            }else{
                $('.customize_phone').hide()
            }
        }else if(ids == 2){
            if(data['sku'] == 1){
                $('.customize_sku').show()
            }else{
                $('.customize_sku').hide()
            }
            if(data['type'] == 1){
                $('.customize_type').show()
            }else{
                $('.customize_type').hide()
            }
            if(data['name'] == 1){
                $('.customize_name').show()
            }else{
                $('.customize_name').hide()
            }
            if(data['hsn'] == 1){
                $('.customize_hsn').show()
            }else{
                $('.customize_hsn').hide()
            }
    
            if(data['desc'] == 1){
                $('.customize_desc').show()
            }else{
                $('.customize_desc').hide()
            }
    
            if(data['selling'] == 1){
                $('.customize_selling').show()
            }else{
                $('.customize_selling').hide()
            }
    
            if(data['purchase'] == 1){
                $('.customize_purchase').show()
            }else{
                $('.customize_purchase').hide()
            }
    
        }else if(ids == 3){
    
            if(data['note'] == 1){
                $('.customize_note').show()
            }else{
                $('.customize_note').hide()
            }

            if(data['name'] == 1){
                $('.customize_name').show()
            }else{
                $('.customize_name').hide()
            }

            if(data['reference'] == 1){
                $('.customize_reference').show()
            }else{
                $('.customize_reference').hide()
            }
    
            if(data['date'] == 1){
                $('.customize_date').show()
            }else{
                $('.customize_date').hide()
            }
    
            if(data['amount'] == 1){
                $('.customize_amount').show()
            }else{
                $('.customize_amount').hide()
            }
    
        }else if(ids == 4){
    
            if(data['number'] == 1){
                $('.customize_number').show()
            }else{
                $('.customize_number').hide()
            }

            if(data['reference'] == 1){
                $('.customize_reference').show()
            }else{
                $('.customize_reference').hide()
            }
    
            if(data['vendor'] == 1){
                $('.customize_vendor').show()
            }else{
                $('.customize_vendor').hide()
            }

            if(data['status'] == 1){
                $('.customize_status').show()
            }else{
                $('.customize_status').hide()
            }
    
            if(data['total'] == 1){
                $('.customize_total').show()
            }else{
                $('.customize_total').hide()
            }

            if(data['date'] == 1){
                $('.customize_date').show()
            }else{
                $('.customize_date').hide()
            }
    
        }
      },
      complete:function(data){
       // Hide image container
    //    $("#loader").hide();
        $(".loader").hide();
        $('#customize_table').show();
        
      }
     });
    
    };
//    });



// *************************************************//

(function()
{

    //exclude older browsers by the features we need them to support
    //and legacy opera explicitly so we don't waste time on a dead browser
    if
    (
        !document.querySelectorAll 
        || 
        !('draggable' in document.createElement('span')) 
        || 
        window.opera
    ) 
    { return; }
    
    //get the collection of draggable items and add their draggable attribute
    for(var 
        items = document.querySelectorAll('[data-draggable="item"]'), 
        len = items.length, 
        i = 0; i < len; i ++)
    {
        items[i].setAttribute('draggable', 'true');
    }

    //variable for storing the dragging item reference 
    //this will avoid the need to define any transfer data 
    //which means that the elements don't need to have IDs 
    var item = null;

    //dragstart event to initiate mouse dragging
    document.addEventListener('dragstart', function(e)
    {
        //set the item reference to this element
        item = e.target;
        
        //we don't need the transfer data, but we have to define something
        //otherwise the drop action won't work at all in firefox
        //most browsers support the proper mime-type syntax, eg. "text/plain"
        //but we have to use this incorrect syntax for the benefit of IE10+
        e.dataTransfer.setData('text', '');
    
    }, false);

    //dragover event to allow the drag by preventing its default
    //ie. the default action of an element is not to allow dragging 
    document.addEventListener('dragover', function(e)
    {
        var ids = $(item).parent().attr("id");
        var count = $('#'+ids+' li').length;
        if(ids == 'first'){
                if(count > 1){
                    if(item)
                    {
                        e.preventDefault();
                    }
            }
        }else if(ids == 'seconde'){
            
            if(item)
                {                    
                    e.preventDefault();
                }
        }
        
        
    
    }, false);  

    //drop event to allow the element to be dropped into valid targets
    document.addEventListener('drop', function(e)
    {
        //if this element is a drop target, move the item here 
        //then prevent default to allow the action (same as dragover)
        if(e.target.getAttribute('data-draggable') == 'target')
        {
            e.target.appendChild(item);
            
            e.preventDefault();
        }
    
    }, false);
    
    //dragend event to clean-up after drop or abort
    //which fires whether or not the drop target was valid
    document.addEventListener('dragend', function(e)
    {
        item = null;
    
    }, false);

})();   