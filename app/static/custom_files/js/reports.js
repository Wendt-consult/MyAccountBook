// datepicker 
$("#start_date").datepicker({ 
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    // minDate: new Date(),
    maxDate: '+2y',
    onSelect: function(date){

        // var selectedDate = new Date(date);
        // var msecsInADay = 86400000;
        var endDate = $('#start_date').datepicker('getDate', '+1d'); 
        endDate.setDate(endDate.getDate()+1); 

       //Set Minimum Date of EndDatePicker After Selected Date of StartDatePicker
        $("#end_date").datepicker( "option", "minDate", endDate );
        $("#end_date").datepicker( "option", "maxDate", '+2y' );

    }
});

$("#end_date").datepicker({ 
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    minDate: new Date(),
});





$(document).ready(function(){

    $(".custom_dates_show_month, .custom_dates_show_month_q, .custom_dates_show_month_h").hide();
    $("#start_date, #end_date, #year, #month, #q_month, #h_month").prop("required", false);

    if(start_date || end_date){ 
        $(".custom_dates_show").show();
        $("#start_date, #end_date").prop("required", true);
    }

    if(year_t){ 
        $(".custom_dates_show").hide();
        $(".custom_dates_show_year").show();
        $("#year").prop("required", true);
    }

    if(month_t){
        $(".custom_dates_show").hide();
        $(".custom_dates_show_month").show();
        $("#year, #month").prop("required", true); 
    }

    if(month_tq){
        $(".custom_dates_show").hide();
        $(".custom_dates_show_month_q").show();
        $("#year, #q_month").prop("required", true);
    }

    if(month_th){
        $(".custom_dates_show").hide();
        $(".custom_dates_show_month_h").show();
        $("#year, #h_month").prop("required", true);
    }

    $("#html_content").val($("#table_content").html());

});



function show_hide_custom_dates(elem){
    var xx = $(elem).val();

    $(".custom_dates_show, .custom_dates_show_year, .custom_dates_show_month, .custom_dates_show_month_q, .custom_dates_show_month_h").hide();
    $("#start_date, #end_date, #year, #month, #q_month, #h_month").prop("disabled", true);
    $("#start_date, #end_date, #year, #month, #q_month, #h_month").prop("required", false);


    if(xx == 1){
        $(".report_dates").val('');
        $(".custom_dates_show_year, .custom_dates_show_month").show();  
        $("#year, #month").prop("disabled", false);  
        $("#year, #month").prop("required", true); 
    }
    else if(xx == 2){
        $(".report_dates").val('');
        $(".custom_dates_show_year, .custom_dates_show_month_q").show();
        $("#year, #q_month").prop("disabled", false);
        $("#year, #q_month").prop("required", true);

    }
    else if(xx == 3){        
        $(".report_dates").val('');
        $(".custom_dates_show_year, .custom_dates_show_month_h").show();
        $("#year, #h_month").prop("disabled", false);
        $("#year, #h_month").prop("required", true);
    }
    else if(xx ==4){        
        $(".report_dates").val('');
        $(".custom_dates_show_year").show();
        $("#year").prop("disabled", false);
        $("#year").prop("required", true);
    }
    else{
        $(".custom_dates_show").show();
        $(".report_dates").val('');
        $("#start_date, #end_date").prop("disabled", false);
        $("#start_date, #end_date").prop("required", true);
    }
}



