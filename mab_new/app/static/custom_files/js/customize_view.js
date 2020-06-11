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
    //  var search = $('#search').val();
    data = {}
    if(ids == 1){
        if($('#customize_contact_org').is(':checked')){
            data['org'] = 1
        }else{
            data['org'] = 0
        }

        if($('#customize_contact_mail').is(':checked')){
            data['mail'] = 1
        }else{
            data['mail'] = 0
        }

        if($('#customize_contact_phone').is(':checked')){
            data['phone'] = 1
        }else{
            data['phone'] = 0
        }

    }else if(ids == 2){

        if($('#customize_product_hsn').is(':checked')){
            data['hsn'] = 1
        }else{
            data['hsn'] = 0
        }

        if($('#customize_product_desc').is(':checked')){
            data['desc'] = 1
        }else{
            data['desc'] = 0
        }

        if($('#customize_product_selling').is(':checked')){
            data['selling'] = 1
        }else{
            data['selling'] = 0
        }

        if($('#customize_product_purchase').is(':checked')){
            data['purchase'] = 1
        }else{
            data['purchase'] = 0
        }

    }else if(ids == 3){

        if($('#customize_credit_reference').is(':checked')){
            data['reference'] = 1
        }else{
            data['reference'] = 0
        }

        if($('#customize_credit_date').is(':checked')){
            data['date'] = 1
        }else{
            data['date'] = 0
        }

        if($('#customize_credit_amount').is(':checked')){
            data['amount'] = 1
        }else{
            data['amount'] = 0
        }

    }else if(ids == 4){

        if($('#customize_order_reference').is(':checked')){
            data['reference'] = 1
        }else{
            data['reference'] = 0
        }

        if($('#customize_order_vendor').is(':checked')){
            data['vendor'] = 1
        }else{
            data['vendor'] = 0
        }

        if($('#customize_order_total').is(':checked')){
            data['total'] = 1
        }else{
            data['total'] = 0
        }

    }else if(ids == 5){

    }else if(ids == 6){

    }
    console.log(data)
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
            if($('#customize_contact_org').is(':checked')){
                $('.customize_org').hide()
            }else{
                $('.customize_org').show()
            }
    
            if($('#customize_contact_mail').is(':checked')){
                $('.customize_mail').hide()
            }else{
                $('.customize_mail').show()
            }
    
            if($('#customize_contact_phone').is(':checked')){
                $('.customize_phone').hide()
            }else{
                $('.customize_phone').show()
            }
        }else if(ids == 2){

            if($('#customize_product_hsn').is(':checked')){
                $('.customize_hsn').hide()
            }else{
                $('.customize_hsn').show()
            }
    
            if($('#customize_product_desc').is(':checked')){
                $('.customize_desc').hide()
            }else{
                $('.customize_desc').show()
            }
    
            if($('#customize_product_selling').is(':checked')){
                $('.customize_selling').hide()
            }else{
                $('.customize_selling').show()
            }
    
            if($('#customize_product_purchase').is(':checked')){
                $('.customize_purchase').hide()
            }else{
                $('.customize_purchase').show()
            }
    
        }else if(ids == 3){
    
            if($('#customize_credit_reference').is(':checked')){
                $('.customize_reference').hide()
            }else{
                $('.customize_reference').show()
            }
    
            if($('#customize_credit_date').is(':checked')){
                $('.customize_date').hide()
            }else{
                $('.customize_date').show()
            }
    
            if($('#customize_credit_amount').is(':checked')){
                $('.customize_amount').hide()
            }else{
                $('.customize_amount').show()
            }
    
        }else if(ids == 4){
    
            if($('#customize_order_reference').is(':checked')){
                $('.customize_reference').hide()
            }else{
                $('.customize_reference').show()
            }
    
            if($('#customize_order_vendor').is(':checked')){
                $('.customize_vendor').hide()
            }else{
                $('.customize_vendor').show()
            }
    
            if($('#customize_order_total').is(':checked')){
                $('.customize_total').hide()
            }else{
                $('.customize_total').show()
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