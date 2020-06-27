$(document).ready(function(){
    $('input[type="file"]').hide();
});

//******************************************************************
// LABEL CLICK
//******************************************************************

$('label#custom-file-upload').on("click", function(){
	$('#id_logo').click();
});


//******************************************************************
// DELETE ENTRIES
//******************************************************************

function del_all_entries(ids){
    if(ids == 0){
        $("span#title_head").empty().text(" Organisation Contact Details");
    }else{
        $("span#title_head").empty().text(" Account Details");
    }

    $("#del_all_modal").modal("show");
}

/************************************************************/
//   IMAGE VALIDATION DELETE
/************************************************************/

// Code by Lawrence Gandhar
$('#id_logo').on("change", function(){
	if (this.files && this.files[0]) {
		var img = document.querySelector('img');  // $('img')[0]
		img.src = URL.createObjectURL(this.files[0]); // set src to blob url       
	}
});


/********************************************************************/
// delete contact
/********************************************************************/
function delete_org_account(ids){    
    $.get("/profile/delete_account/"+ids+"/", function(data){
        if(data == '1') location.reload();
        else alert("Unauthorized Access");
    });
} 

/********************************************************************/
// check gst state code
/********************************************************************/

// $("#id_state").on("change",function(){

// 	id_state = $(this).val();
	
// 	if(id_state !=""){
// 		$.post("/check_gst_existing/",{"state_id":id_state, "organisation_id":organisation_id, 'csrfmiddlewaretoken':csrf_token},
// 			function(data){
// 				if(parseInt(data)>0){
// 					$("tr.gst_tr").hide();
// 				}else{
// 					$("tr.gst_tr").show();
// 				}
// 		});
// 	}
// });

/******************************************************************/
// STATE SELECT - SET GST
/******************************************************************/

function check_gst(forloop,address_id,state){
	// elem = $(this);
	// ids = $(elem).closest(".modal").attr("id");
	if(state !=""){
		$.post("/get_state_gst/",{'state_id':state, 'organisation_id':organisation_id,'address_id':address_id, 'csrfmiddlewaretoken':csrf_token},function(data){
			
			// $("#"+ids).find("#id_gstin").val(data.gstin);
			// $("#"+ids).find("#gst_reg").val(data.gst_reg_type);
			$("#editAddressModal-"+forloop).find(".tax_id_input").val(data.tax_id);
			$("#editAddressModal-"+forloop).find("#id_gstin").val(data.gstin);
            $("#editAddressModal-"+forloop).find("#gst_reg").val(data.gst_reg_type);
			$("#editAddressModal-"+forloop).find("#org_address_ids").val(address_id);
			$("#editAddressModal-"+forloop).find("#org_address_state").val(data.state);
			$("#editAddressModal-"+forloop).modal('show')
			if(data.gstin !="" && data.gstin != null && data.count == 'yes'){ 
				alert("Already a GST Number is registered in this state");
			}
		});
	}
};

/******************************************************************/
// gst configuration
/******************************************************************/
//  is register
$('#is_orginsation_register').click(function(){

    if($('#is_orginsation_register').is(':checked')){
        $('#no_orginsation_register').prop('checked',false)
        $('#gst_multiple').show()
    }
});

$('#no_orginsation_register').click(function(){
    
    if($('#no_orginsation_register').is(':checked')){
        $('#is_orginsation_register').prop('checked', false)
		$('#gst_multiple').hide()
		$('#gst_configuration_setting').hide()
		$('#is_single_gst').prop('checked', false)
		$('#is_multiple_gst').prop('checked', false)
    }
});

// multiple gst

$('#is_multiple_gst').click(function(){
    
    if($('#is_multiple_gst').is(':checked')){
        $('#is_single_gst').prop('checked', false)
		$('#gst_configuration_setting').show()
		$('.single_gst_field').hide()
    }
});

$('#is_single_gst').click(function(){
    
    if($('#is_single_gst').is(':checked')){
        $('#is_multiple_gst').prop('checked', false)
		$('#gst_configuration_setting').hide()
		$('.single_gst_field').show()
    }
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