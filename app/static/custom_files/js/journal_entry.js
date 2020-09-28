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

var journal_number = 1
var count = 0
function journal_addRow(a) {
    if(count == 0){
        journal_number +=a
        count +=1
    }

    journal_number += 1

    // $(document).on('click','#select2-ItemName'+creditnote_number+'-container',function(){
    //     for(var i = 1;i <= creditnote_number; i++){
    //         var a = $('#row_ItemName'+creditnote_number+'').length
    //         if(a == 0){
    //             $('.select2-search').append('<button class="btn btn-link credit_product" data-toggle="modal" id="row_ItemName'+creditnote_number+'" onclick="get_credit_product_id('+creditnote_number+'),c()" data-target="#ProductModal" style="margin-left: -11%;">+ Add New</button>');
    //         }  
    //     } 
    // });
       
        var html = '<tr id="journal_row'+journal_number+'">'
        html +='<td style="border:1px solid black;padding-bottom:0%"><select class="form-control journal_item" id="account_header'+journal_number+'" name="account_header[]"  style="margin-top:-10px;padding-left: 0px;width: 174.6px;" required><option value="">-------</option></select></td>'
        html +='<td style="border:1px solid black;"><textarea id="details'+journal_number+'" name="details[]" rows="2" placeholder="Max character 250" style="padding-left: 0px;width: 100%;" required></textarea></td>'
        html +='<td style="border:1px solid black;"><select class="form-control " id="contactname'+journal_number+'" name="contactname[]"  style="padding-left: 0px;width: 174.6px;" required> <option value="">-------</option></select></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="debit'+journal_number+'">₹</label> </div><div class="col"><input type="text" class="form-control debit" maxlength="10" onkeyup="debit_total()" onkeypress="return restrictAlphabets(event), float_value(event,\'debit'+journal_number+'\')"  id="debit'+journal_number+'" name="debit[]" style="margin-top: 1%;"></div></div></td>'
        html +='<td style="border:1px solid black;"><div class="row"><div class="col-1" style="padding-right: 0%;"><label for="credit'+journal_number+'">₹</label> </div><div class="col"> <input type="text" class="form-control credit" maxlength="10" onkeyup="credit_total()" onkeypress="return restrictAlphabets(event), float_value(event,\'credit'+journal_number+'\')" id="credit'+journal_number+'" name="credit[]" style="margin-top: 1%;"></div></div></td>'
        html +='<td style="border-top: none;"><span class="tbclose material-icons" id="'+journal_number+'" name="'+journal_number+'" onclick="journal_removeRow('+journal_number+')" style="cursor: default;">delete_forever</span></td></tr>'
        // $('#journal_table').append(html)
        $(html).insertBefore( "#total_debit_credit" );
        
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
            url: "/journalentry/add_journalentry/"+1+"",
            dataType: "json",
            success: function(data){
                // for account header
                var account_option = data.account_name
                var account_id = data.account_ids
                for(var i = 0;i < account_option.length;i++){
                    $('<option/>').val(account_id[i]).html(account_option[i]).appendTo('#account_header'+journal_number+'');
                }
                // for contact
                var contact_option = data.contact_name
                var contact_id = data.contact_ids
                for(var i = 0;i < contact_option.length;i++){
                    $('<option/>').val(contact_id[i]).html(contact_option[i]).appendTo('#contactname'+journal_number+'');
                }
            },
        });
    
};
// REMOVE JS TABLE
function journal_removeRow(a) {
    var first_row = $('#journal_table tbody tr:first').attr('id')
    if(first_row == 'journal_row'+a+''){
        var last_row = $('#journal_table tbody tr:last').attr('id')
        if(last_row != 'journal_row'+a+''){
            $('#journal_row'+a+'').remove();
        }else{
            $('#account_header'+a+'').val('').change();
            $('#details'+a+'').val('')
            $('#contactname'+a+'').val('').change();
            $('#debit'+a+'').val('')
            $('#credit'+a+'').val('')
        }
    }else{
        $('#journal_row'+a+'').remove();
    }
    // validation()
}

/************************************************************ */
// debit and credit sub total
/************************************************************ */

function debit_total(){
    var debit = 0
    $('.debit').each(function(){
        var val =  $(this).val()
        if(val == ''){
            val = 0.00
        }
        debit += parseFloat(val)
    });
    if(debit.toString() != 'NaN'){
        $('#debit_SubTotal').val(parseFloat(debit).toFixed(2))
    }else{
        $('#debit_SubTotal').val('')
    }
}

function credit_total(){
    var credit = 0
    $('.credit').each(function(){
        var val =  $(this).val()
        if(val == ''){
            val = 0.00
        }
        credit += parseFloat(val)
    });
    if(credit.toString() != 'NaN'){
        $('#credit_SubTotal').val(parseFloat(credit).toFixed(2))
    }else{
        $('#credit_SubTotal').val('')
    }
}

/*********************************************************************** */
// DEFUALT JOURNAL ENTRY AND CHECK JORNAL ENTRY NUMBER IS UNIQUE
/*********************************************************************** */
$("#journal_checkbox").click(function(){
    if($(this).is(':checked')){
        var ins = 0
        var slug = 'a'
        $.ajax({
            type:"GET",
            url: "/journalentry/unique_number/"+ins+"/"+slug+"/",
            dataType: "json",
            success: function(data){
                $('#journalnumber').val(data.journal)
            },
            error: function (rs, e) {
                alert('Sorry, try again.');
            }
        });
    }else{
        $('#journalnumber').val('')
    }  
});

$("#journalnumber").focusout(function(){
    $("#journal_checkbox").prop('checked',false);
    var ins = 1
    var journal_number = $("#journalnumber").val()
    $.ajax({
        type:"GET",
        url: "/journalentry/unique_number/"+ins+"/"+journal_number+"/",
        dataType: "json",
        success: function(data){
            if(data.unique != 0){
                alert('This journal entry number is already exits. Please enter the different journal entry number.')
                $('#journalnumber').focus();
                $('#journalnumber').val('')
            }
            
        },
    });
  });

/*********************************************************************** */
// BEFORE SVAE CHECK JOURNAL ENTRY DEBIT AND CREDIT ARE SAME 
/*********************************************************************** */

function journal_check(){
    if($('#debit_SubTotal').val() == '' & $('#credit_SubTotal').val() == ''){
        alert('Can not save blank journal entry')
        return false
    }else if($('#debit_SubTotal').val() == $('#credit_SubTotal').val()){
        return true
    }else{
        alert('Journal entry total debit amount and credit amount should be same')
        return false
    }
}

/********************************************************************/
// Date Picker
/********************************************************************/


$("#Journalentrydate").datepicker({dateFormat: 'dd-mm-yy'}).datepicker("setDate", new Date(),dateFormat = "dd-mm-yy");
$("#edit_Journalentrydate").datepicker({dateFormat: 'dd-mm-yy'});
/********************************************************************/
//  Datepicker validation
/********************************************************************/

$("#Journalentrydate,#edit_Journalentrydate").on('change', function(event){
    if($(this).val() != ''){
        dateValidation($(this));
    }
});

function dateValidation(element){
    var date = $(element).val();
    var regEx = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
    if(!regEx.test(date)){
        alert('Invalid Date');
        $(element).val('');
    }
}
$('#Journalentrydate,#edit_Journalentrydate').keypress(function(event) {
    event.preventDefault();
});
