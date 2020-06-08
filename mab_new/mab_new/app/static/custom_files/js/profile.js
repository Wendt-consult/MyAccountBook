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

$("#id_state").on("change",function(){

	id_state = $(this).val();
	
	if(id_state !=""){
		$.post("/check_gst_existing/",{"state_id":id_state, "organisation_id":organisation_id, 'csrfmiddlewaretoken':csrf_token},
			function(data){
				if(parseInt(data)>0){
					$("tr.gst_tr").hide();
				}else{
					$("tr.gst_tr").show();
				}
		});
	}
});

/******************************************************************/
// STATE SELECT - SET GST
/******************************************************************/

$("select.state_select").on("change", function(){
	elem = $(this);
	ids = $(elem).closest(".modal").attr("id");
	if($(this).val() !=""){
		$.post("/get_state_gst/",{'state_id':$(this).val(), 'organisation_id':organisation_id, 'csrfmiddlewaretoken':csrf_token},function(data){
			if(data.gstin !="" && data.gstin != null){ 
				alert("Already a GST Number is registered in this state");
			}
			$("#"+ids).find("#id_gstin").val(data.gstin);
			$("#"+ids).find("#gst_reg").val(data.gst_reg_type);
		});
	}
});


