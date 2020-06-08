
function get_predefined_groups(elem){

    if($(elem).val()!=""){
        $("#select2-id_acc_group-container").text('')
        $("#id_info_message").val('')
        var ids = $(elem).val();
        ajax_get_predefined_groups(ids);
        

    }else{
        $("#id_acc_group").empty().append('<option value="">-----</option>');
    }
}

function ajax_get_predefined_groups(ids){
    $.get("/get_predefined_groups/",{"ids":ids}, function(data){
        // $('<option/>').val(ids).html(ids).appendTo('#id_acc_group');
        $("#id_acc_group").empty().append(data);
    });
}

/**********************************************************/
//
/**********************************************************/

function openNewGroupModal(elem){
    if($(elem).val() == -1){
        $("#major_head_ins").val($("#id_major_heads").val());
		$("#set_major_head").text($("#id_major_heads option:selected").text());
        $("#addGroupModal").modal('show');
    }else{
        var ins = $('#id_major_heads option').filter(':selected').val()
        var slug = $("#id_acc_group  option:selected").text()
        info(ins,slug)
    }
}

function add_group_form(save_type){
    var name = $("#id_group_name").val()
    if(name == ''){
        document.getElementById('error_name').innerHTML = '*Please enter the group name'
        return false
    }
    else{
        event.preventDefault()
        $.post("/add_ledger_group/",$("#add_group_form").serialize(), function(data){
        if(data != '0'){
        //    ajax_get_predefined_groups($("#id_major_heads").val());
            $('<option/>').val(data).html(name).appendTo('#id_acc_group');
            var ins = $('#id_major_heads option').filter(':selected').val()
            $("#select2-id_acc_group-container").text(name)
            $("#addGroupModal").modal('hide');
            info(ins,name)
        }
    });
    } 
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
// ADD GROUP WITHOUT REFRECH
/**********************************************************/

function add_group(){
    var name = $("#id_group_name").val()
    if(name == ''){
        document.getElementById('error_name').innerHTML = '*Please enter the group name'
        return false
    }else{
        event.preventDefault()
        $.post("/add_ledger_group/",$("#add_group_form").serialize(), function(data){
        $("#id_group_name").val('')
        $("#id_group_info").val('')
        if(data != '0'){
            ajax_get_predefined_groups($("#id_major_heads").val());
            $("#addGroupModal").modal('show');
        }
    });
    }
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

function validation(){
    var major_heads =$("#id_major_heads option:selected").text()
    var group = $("#select2-id_acc_group-container").text()
    var account = $("#id_accounts_name").val()
    if(major_heads == '---------'){
        document.getElementById('error_major').innerHTML = '*Please select the major head'
        return false
    }else if(group == ''){
        document.getElementById('error_group').innerHTML = '*Please select the group'
        return false
    }else if(account == ''){
        document.getElementById('error_account').innerHTML = '*Please enter the account name'
        return false
    }else{
        return true
    }
}

/**********************************************************/
// SELECT SEARCH BAR AND BUTTON
/**********************************************************/

$(document).ready(function() {
    // $('.mdb-select').materialSelect();
    $(function () {
        $(".select").select2();
      });
    });

// var button = 1
$(document).on('click','.select2-container--open',function(){
    var a = $('#GroupModal').length
    if(a == 0){
        $('.select2-search ').append('<button class="btn btn-link" data-toggle="modal" id="GroupModal"  onclick="openNewGroupModal($(this)),leger_c()" value="-1" data-target="#addGroupModal" style="margin-left: -5%;">+ Add New</button>');
    }
});

function leger_c(){

    $(".select2-container--default").removeClass("select2-container--open","select2-container--focus");
    $(document).ready(function() {
        $(function () {
            $(".select").select2();
          });
        });
}
/**********************************************************/
// GORUPING UNIQUE
/**********************************************************/
$("#id_group_name").keyup(function(){
    var group_name = $("#id_group_name").val()
    console.log(group_name)
    var ins = $('#id_major_heads option').filter(':selected').val()
    $.ajax({
        type:"GET",
        url: "/add_ledger_group/unique/"+ins+"/"+group_name+"",
        dataType: "json",
        success: function(data){
            var info = data.unique
            if(info == '1'){
                alert('This group already exits. Please enter different group.')
                $("#id_group_name").val('')
            }  
        },  
    });
  });

  $("#id_accounts_name").keyup(function(){
    var head = $("#id_major_heads").val()
   
    var account = $("#id_accounts_name").val()
    console.log(account)
    // var ins = $('#id_major_heads option').filter(':selected').val()
    console.log(head)
    $.ajax({
        type:"GET",
        url: "/add_ledger_group/unique2/"+head+"/"+account+"/",
        dataType: "json",
        success: function(data){
            var info = data.unique
            if(info == '1'){
                alert('This account name is already exits. Please enter different account name.')
                $("#id_accounts_name").val('')
            }  
        },  
    });
  });
