$(document).ready(function(){

    var backgrounds = {
        "1" : ["template_header", "template_body_green", "th_green"],
        "2" : ["template_header_orange", "template_body_orange", "th_orange"],
        "3" : ["template_header_blue", "template_body_blue", "th_blue"],
        "4" : ["template_header_white", "template_body_white", "th_white"],
        "5" : ["template_header_grey", "template_body_grey", "th_grey"],
    };

    $("button.color-button").on('click', function(){
        var x = $(this).text();

        $("div.hidden_div").removeClass('d-table-row');

        $("#invoice_template_body").find(".card-header").removeClass().addClass("card-header").removeAttr('style').addClass(backgrounds[x][0]);
        $("#template_body").removeClass().addClass("card-body").removeAttr('style').addClass(backgrounds[x][1]);
        $("#address_bar").removeClass().addClass(backgrounds[x][2])

        $("#id_design_number").val(x);
            
    });

    $("select#id_design_number").on('change', function(){
        var x = $(this).val();

        if(x == 6){
            $("div.hidden_div").addClass('d-table-row');
        }
        else{
            $("#invoice_template_body").find(".card-header").removeClass().addClass("card-header").removeAttr('style').addClass(backgrounds[x][0]);
            $("#template_body").removeClass().addClass("card-body").addClass(backgrounds[x][1]);
            $("#address_bar").removeClass().addClass(backgrounds[x][2])

            $("div.hidden_div").removeClass('d-table-row');
        }
    });

    $("#id_header_bgcolor").on('change', function(){
        var bg_color = $(this).val();
        $("#invoice_template_body").find(".card-header").removeClass().addClass("card-header").css('background-color',bg_color);
    });

    $("#id_header_fgcolor").on('change', function(){
        var fg_color = $(this).val();
        $("#invoice_template_body").find(".card-header").removeClass().addClass("card-header").find('p').css('color',fg_color);
    });


    $("#id_billing_address").on('change', function(){
        var tex = $('#id_billing_address').children("option:selected").text();
        
        tex = tex.replace(/,/g,",<br/>");
        $("#invoice_user_billing_address").empty().html(tex);
    });

    $("#id_user_email").on('change', function(){
        $("#invoice_email").text($("#id_user_email").children("option:selected").text());
    });

    $("#id_user_phone").on('change', function(){
        $("#invoice_phone").text($("#id_user_phone").children("option:selected").text());
    });
    

});

