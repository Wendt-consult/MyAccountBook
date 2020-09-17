window.addEventListener("dragover",function(e){
    if (e.target.id != 'uploadFile'){
        e = e || event;
        e.preventDefault();
    }
});
window.addEventListener("drop",function(e){
    if (e.target.id != 'uploadFile'){
        e = e || event;
        e.preventDefault();
    }
    if (e.target.id == 'exp_bill_img'){
        alert('First remove existing file')
    }
});

$('#tax_5').hide();
$('.tax_csgst_2').hide();
$('#tax_12').hide();
$('.tax_csgst_6').hide();
$('#tax_18').hide();
$('.tax_csgst_9').hide();
$('#tax_28').hide();
$('.tax_csgst_14').hide();

$('.cancel_file_btn').hide();

/********************************************************************/
//  org state
/********************************************************************/
// var expenss_user_state =''
// $.ajax({
//     type:"GET",
//     url: "/creditnote/state_compare/",
//     dataType: "json",
//     success: function(data){
//         if(data.state == null){
//             expenss_user_state  = 'null'
//         }else{
//             expenss_user_state = data.state
//         }
//     },  
// });

var vendor_gstin =''
var vendor_gst_type = ''
function state_compare(){
    var ids = $('#select_vendor').val()
    if(ids != ''){
        $.ajax({
            type:"GET",
            url: "/purchase_order/vendor_state/"+ids+"/",
            dataType: "json",
            success: function(data){
                // if(data.mail != null){
                    // $('#mail').val(data.mail)
                // }
                // gst = data.gst_type
                if(data.gst_type != null){
                    vendor_gst_type = data.gst_type
                    // $('#gst_type').val(data.gst_type)
                }else{
                    vendor_gst_type = ''
                    // $('#gst_type').val('')
                }
                vendor_gstin = data.gstin
                check_gst_status('user_side')
            },
        });
    }else{
        // $('#mail').val('')
        // $('#gst_type').val('')
        vendor_gst_type = ''
        vendor_gstin = ''
        check_gst_status('user_side')
    }
}

function check_gst_status(cat){
    if(cat == 'user_side'){
        // for organization and vendor not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == '' || vendor_gst_type == 0 || vendor_gst_type == 3 || vendor_gst_type == 5 || vendor_gst_type == ''){
            $('.category_table').find('.cate_tax').attr('readonly', true)
            $('.category_table').find('.cate_tax').val('0').change()

            $('.item_table').find('.item_tax').attr('disabled', true)
            $('.item_table').find('.item_tax').val('0').change()

            // sub_total()
            show_taxes()
            if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == ''){
                alert('Organization not register GST')
            }else if(vendor_gst_type == 0 ||  vendor_gst_type == 3 ||  vendor_gst_type == 5){
                alert('Vendor not register GST')
            }else if(vendor_gst_type == ''){
                alert('Vendor not selected')
            }
        }else{
            $('.category_table').find('.cate_tax').attr('readonly', false)
            $('.item_table').find('.item_tax').attr('disabled', false)
            // sub_total()
            show_taxes()
        }
    }else if(cat == 'vendor_side'){
        // for organization and vendor not register
        if($('#org_gst_reg_type').val() == '0' || $('#org_gst_reg_type').val()  =='3' || $('#org_gst_reg_type').val()  == '5' || $('#org_gst_reg_type').val()  == '' || vendor_gst_type == 0 || vendor_gst_type == 3 || vendor_gst_type == 5 || vendor_gst_type == ''){
            $('.category_table').find('.cate_tax').attr('readonly', true)
            $('.category_table').find('.cate_tax').val('0').change()

            $('.item_table').find('.item_tax').attr('disabled', true)
            $('.item_table').find('.item_tax').val('0').change()
            show_taxes()
            // sub_total()
        }else{
            $('.category_table').find('.cate_tax').attr('readonly', false)
            $('.item_table').find('.item_tax').attr('disabled', false)
            // sub_total()
            show_taxes()
        }
    }  
}

/********************************************************************/
//  org vendor state
/********************************************************************/

// var expenss_state = ''

// function expenss_vendor(){
//     var ids = $('#select_vendor').val()
//     if(ids != ''){
//         $.get("/expense/vendor_state/"+ids+"/", function(data){
//             if(data){
//                 expenss_state = data.vendor_state  
//                 show_taxes()
//             }
//         });
//     }else{
//         expenss_state = ''
//         show_taxes()
//     }
// }

$('[type=cate]').filter(function(){
    var select_tag = $(this).find('select').first();
    select_tag.find('option').first().attr('disabled',true);
    select_tag.find('option').first().text('Select Category');
});

$('[type=item]').filter(function(){
    var select_tag = $(this).find('select').first();
    select_tag.find('option').first().attr('disabled',true);
    select_tag.find('option').first().text('Select Product');
});

// For Edit Form and Clone Expense
var edit_expense = $('#edit_expense').val();
var clone_expense = $('#clone_expense').val();
if (edit_expense == 'True'){
    if (clone_expense == 'True'){
        $('#exp_number').val('');
        if ($('#select_vendor option:selected').text().includes('(Inactive)')){
            $('#select_vendor').val('');
        }
        alert("This record is a copy of expense. Please make the necessary changes to the record before saving it")
    }

    numberValidatuion('.item_rate', false);
    numberValidatuion('.item_quantity', true);

    var total_form = $('.table_form').attr('count');
    for (i=1; i<=total_form; i++){
        var form_id = $("#cate_form_"+i).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        if ($('#cate_tax_'+i).val() == 'None'){
            $("#id_category-"+form_id+'-tax').val('');
            $("#id_category-"+form_id+'-tax').prop('required', false);
            $("#id_category-"+form_id+'-tax').prop('disabled', true);
            $("#id_category-"+form_id+'-amount').prop('readonly', true);
            state_compare()
            show_taxes();

        }
        $('#delete_cate_btn_'+i).on('click', function(){
            deleteCategoryForm($(this), true);
            state_compare()
            show_taxes();
        });
        $('.item_form_'+i).filter(function(){
            var item_id = i
            var delete_btn =  $(this).find('button');
            delete_btn.on('click', function(){
                var table_tag = $(this).closest('table');
                $(this).parent().find('input[type=checkbox]').prop('checked', true);
                table_tag.hide();
                table_tag.removeClass('item_form_'+item_id);
                if ($('#id_category-'+form_id+'-tax').val() == null){
                    changeCateAmount(item_id, form_id)
                }
                if ($('.item_form_'+item_id).length == 0){
                    $('#id_category-'+form_id+'-tax').prop('disabled', false);
                    $('#id_category-'+form_id+'-amount').prop('readonly', false);
                }
                state_compare()
                show_taxes();
            });
            item = $(this).find('input[type=hidden]').attr('id').replace('item'+i,'');
            id = item.replace(/[^0-9]/g, '')
            var tax_id = 'id_item'+item_id+'-'+id+'-tax';
            var rate_id = 'id_item'+item_id+'-'+id+'-rate';
            var quantity_id = 'id_item'+item_id+'-'+id+'-quantity';
            var amount_id = 'id_item'+item_id+'-'+id+'-amount';
            var total_amount_id = 'id_item'+item_id+'-'+id+'-total_amount';
            var product_id = 'id_item'+item_id+'-'+id+'-product'
            var desc_id = 'id_item'+item_id+'-'+id+'-item_description'

            if (clone_expense == 'True' && $('#'+product_id).find(":selected").text().includes('(Inactive)')){
                alert('Inactive Product Selected')
                $(this).find('input[type=checkbox]').prop('checked', true);
                $(this).hide();
                $(this).removeClass('item_form_'+item_id);
                if ($('#id_category-'+form_id+'-tax').val() == null){
                    changeCateAmount(i, form_id);
                }
                if ($('.item_form_'+i).length == 0){
                    $('#id_category-'+form_id+'-tax').prop('disabled', false);
                    $('#id_category-'+form_id+'-amount').prop('readonly', false);
                }
                state_compare()
                show_taxes();
            }

            $('#'+quantity_id).parent().css('padding-top','20px');
            CalItemTotalAmount(tax_id, rate_id, quantity_id, amount_id, total_amount_id);
            addnewProduct(product_id, desc_id, quantity_id, rate_id, amount_id, tax_id, total_amount_id);
        });
    }
    
    $('[type=cate]').filter(function(){
        var id = $(this).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        var tax = Number($('#id_category-'+id+'-tax').val());
        if (tax){
            var amount = Number($('#id_category-'+id+'-amount').val());
            var prev_tax_amount = Number($('#tax_'+tax).find('input').val());
            $('#tax_'+tax).find('input').val(prev_tax_amount+(amount*(tax/100)));
            $('#tax_'+tax).show();
        }
        CalCategoryTotalAmount(id);
    });

    if (file){
        $('.cancel_file_btn').show();
        var file_exe = file.split('.').pop();

        if (file_exe == 'jpg' || file_exe == 'png' || file_exe == 'jpeg'){
            $('#preview').append('<img src='+file+' />');
        }
        else{
            $('#preview').append('<embed src='+file+'/>');

        }
    }

    var initial_exp_number = $('#exp_number').val();
}
else{
    var initial_exp_number = ''
    CalCategoryTotalAmount(0);
}

// Datepicker Function
$(function(){
    $('#exp_date_icon').click(function() {
        $('.datepicker1').datepicker({ maxDate: new Date(), dateFormat: 'dd/mm/yy' });
        $(".datepicker1").focus();
    });
    $('#payment_date_icon').click(function() {
        $('.datepicker2').datepicker({ dateFormat: 'dd/mm/yy' });
        $(".datepicker2").focus();
    });
});

// Auto Fill Expense Number
$('#exp_num_check_box').on('click', function(){
    if($(this).prop("checked") == true){
        var exp_num = $('#random').val();
        $('#exp_number').val(exp_num);
    }
    else if($(this).prop("checked") == false){
        $('#exp_number').val('');
    }
});

// Add +add Button in Dropdown
$('#select_vendor').append('<option value="add" style="color: #8e24aa;">+ Add</option>');
$('.select_ledger').append('<option value="add" style="color: #8e24aa;">+ Add</option>');
$('.select_product').append('<option value="add" style="color: #8e24aa;">+ Add</option>');

// Ajax Request to Check Valid Expense Number 
function check_expense_number(element){
    exp_no = element.val();
    if (exp_no == ''){
        element.focus();
    }
    else{
        $.ajax({
            url : "/check-expense-number/",
            data : {'exp_number' : exp_no, 'initial_exp_number':initial_exp_number},
            success : function(data){
                if (data['exists']){
                    element.val('');
                    $('#exp_num_check_box').prop('checked', false);
                    alert('Expense number already Exists');
                }
            }
        });
    }
}

numberValidatuion('.cate_amount', false);

// Pre Fill Expense in Add Ledger Form
$(".ledger_type option[value=1]").attr("selected", false);
$(".ledger_type option[value=2]").attr("selected", true);

// Pre Fill Vendor in Add Contact Form 
$(".customer_type option[value=1]").attr("selected", false);
$(".customer_type option[value=2]").attr("selected", true);

// Show Add Payment Method Popup
$('#pm_error').hide();
$('#add_payment_method').append('<option value="add" style="color: #8e24aa;">+ Add</option>');
$('#add_payment_method').change(function(){
    if ($(this).val() == "add"){
        $('#add_payment_method').val('');
        $('#paymentMethodModal').modal('show');
    }
});

// Ajax Request to Add New Payment Method
$('.add_payment_method_btn').on('click', function(){
    var name = $('input[name=payment_method]').val();
    if (name){
        $.ajax({
            url : "/add-payment-method",
            data : {'name':name},
            success : function(data){
                if(data['created']){
                    $('#add_payment_method').find('option').last().remove();
                    $('#add_payment_method').append('<option value="'+data['id']+'">'+name+'</option>');
                    $('#add_payment_method').append('<option value="add" style="color: #8e24aa;">+ Add</option>');
                    $('#add_payment_method').val(data['id']);
                    $('#paymentMethodModal').modal('hide');
                    $('#pm_error').hide();
                    $('input[name=payment_method]').val('');
                }
                else{
                    $('#pm_error').show();
                }
            },
            error : function(){
                $('#paymentMethodModal').modal('hide');
                $('input[name=payment_method]').val('');
            }
        });
    }
});

$(".close_btn").on('click', function(){
    $('#pm_error').hide();
    $('input[name=payment_method]').val('');
});

addNewLedger();

// Ajax Request to Add New Contact
$('#select_vendor').change(function() {
    if ($(this).val() == "add"){
        $(this).val('');
        $('#contactFormModal').modal('show');
        $('#contactForm').unbind('submit')
        $('#contactForm').submit(function(e){
            e.preventDefault();
            var formData = $('#contactForm').serializeArray();
            $.ajax({
                type : "POST",
                url : "/contacts/add/",
                data : formData,
                success : function(data){
                    if (data['success']){
                        $('#select_vendor').find('option').last().remove();
                        $('#select_vendor').append('<option value="'+data['contact_id']+'" selected>'+data['contact_name']+'</option>');
                        $('#select_vendor').append('<option value="add" style="color: #8e24aa;">+ Add</option>');
                    }
                    else{
                        $('#select_vendor').val('');
                    }
                    $('#contactFormModal').modal('hide');
                },
                error : function(){
                    $('#contactFormModal').modal('hide');
                    $('#select_vendor').val('');
                }
            });
        });
    }
    $('#cancelContactBtn').on('click', function(){
        $('#contactFormModal').modal('hide');
    });
});

// Function to Call Ajax Request to Add New Ledger
function addNewLedger(){
    $('.select_ledger').change(function() {
        var id = $(this).attr('id');
        if ($(this).val() == "add"){
            $(this).val('');
            $('#ledgerFormModal').modal('show');
            $('#ledgerForm').unbind('submit')
            $('#ledgerForm').submit(function(e){
                e.preventDefault();
                var formData = $('#ledgerForm').serializeArray();
                $.ajax({
                    type : "POST",
                    url : "/ledger/add/",
                    data : formData,
                    success : function(data){
                        if (data['success']){
                            $('.select_ledger').filter(function(){
                                $(this).find('option').last().remove();
                                $(this).append('<option value="'+data['ledger_id']+'">'+data['ledger_name']+'</option>');
                                $(this).append('<option value="add" style="color: #8e24aa;">+ Add</option>');
                            });
                            $('#'+id).val(data['ledger_id']);
                        }
                        else{
                           $('#'+id).val('');
                        }
                        $('#ledgerFormModal').modal('hide');
                    },
                    error : function(){
                        $('#ledgerFormModal').modal('hide');
                        $('#'+id).val('');
                    }
                });
            });
        }
        $('#ledgerCancelBtn').on('click', function(){
            $('#ledgerFormModal').modal('hide');
        });
    });
}

function addnewProduct(product_id, desc_id, quantity_id, rate_id, amount_id, tax_id, total_amount_id){
    $('#'+product_id).on('change', function(){
        if ($(this).val() == "add"){
            $(this).val('');
            $('#productFormModal').modal('show');
            $('#product_form').unbind('submit')
            $('#product_form').submit(function(e){
                e.preventDefault();
                // var formData = $('#product_form').serializeArray();
                form_d = $("#product_form")[0];
                var formData = new FormData(form_d);
                $.ajax({
                    type : "POST",
                    url : "/products/add/",
                    data : formData,
                    cache:false,
                    contentType: false,
                    processData: false,
                    success : function(data){
                        if (data['success']){
                            $('.select_product').filter(function(){
                                $(this).find('option').last().remove();
                                $(this).append('<option value="'+data['product_id']+'">'+data['product_name']+'</option>');
                                $(this).append('<option value="add" style="color: #8e24aa;">+ Add</option>');
                            });
                            $('#'+product_id).val(data['product_id']);
                            $('#'+rate_id).val(data['product_rate']);
                            $('#'+desc_id).val(data['product_description']);
                            calculateItemRate(Number(data['product_rate']), $("#"+rate_id), quantity_id, tax_id, amount_id, total_amount_id);
                            if (data['product_tax']){
                                $('#'+tax_id).val(data['product_tax']);
                                calculateItemTax(data['product_tax'], $('#'+tax_id), amount_id, total_amount_id);
                            }
                            $('#'+quantity_id).val('');
                            $('#'+quantity_id).parent().find('span').text("("+data['product_unit']+")")
                            $('#'+quantity_id).parent().css({'padding-top':'20px','display':'inline-grid'});
                        }
                        $('#productFormModal').modal('hide');
                    },
                    error : function(){
                        $('#productFormModal').modal('hide');
                        $(this).val('');
                    }
                });
            });
        }else{
            var id = Number($(this).val());
            $.ajax({
                url : "/product-details/",
                data : {'id':id},
                success : function(data){
                    $('#'+rate_id).val(data['product_rate']);
                    $('#'+desc_id).val(data['product_description']);
                    calculateItemRate(Number(data['product_rate']), $("#"+rate_id), quantity_id, tax_id, amount_id, total_amount_id);
                    if (data['product_tax']){
                        $('#'+tax_id).val(data['product_tax']);
                        calculateItemTax(data['product_tax'], $('#'+tax_id), amount_id, total_amount_id);
                        var item_form_id = $(this).parents
                    }
                    $('#'+quantity_id).val('');
                    $('#'+quantity_id).parent().find('span').text("("+data['product_unit']+")")
                    $('#'+quantity_id).parent().css({'padding-top':'20px','display':'inline-grid'});
                }
            });
        }

        $('#cancel_product').on('click', function(){
            $('#productFormModal').modal('hide');
            $('#'+quantity_id).parent().find('span').text("");
            $('#'+quantity_id).parent().css({'padding-top':'','display':''});
        });
    });
}

// Add New Category Form
$('#add_category_btn').on('click', function(){
    valid = totalAmountValidation();
    if (!valid){
        alert("Total amount of Category and it's items are not same");
        return false
    }
    
    let total_form = $('#id_category-TOTAL_FORMS').val();
    $('#id_category-TOTAL_FORMS').val(parseInt(total_form)+1);

    count = Number($('.table_form').attr('count'));
    $('.table_form').attr('count', (count+1));
    var table_id = 'cate_form_' + (count+1);

    var element = $('.extra_cate_form').html().replace(/__prefix__/g, total_form);
    $('.table_form').append(element);

    $('.table_form').find('table').last().attr('id', table_id);

    if ($("[type=cate]").length == 2){
        $('.cate_table_header').hide();
    }

    $('#'+table_id).find('button').attr('id','delete_cate_btn_'+(count+1));

    $('#delete_cate_btn_'+(count+1)).on('click', function(){
        deleteCategoryForm($(this), false);
    });

    var form_id = $('#'+table_id).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
    CalCategoryTotalAmount(form_id);

    addNewLedger();

    numberValidatuion('.cate_amount', false);
    check_gst_status('vendor_side')
});

// Delete a Category Form
$('#delete_cate_btn_0').on('click', function(){
   deleteCategoryForm($(this), false);
});

// Add New Item Form, Add New Tax Field Under Subtotal, Ajax Request to Add New Product, Delete a Item Form
$('#add_item_btn').on('click', function(){
    if ($("[type=cate]").length == 1){
        alert('First Add a Category')
    }
    else{
        let total_form = $('#id_item-TOTAL_FORMS').val();
        $('#id_item-TOTAL_FORMS').val(parseInt(total_form)+1);

        count = Number($('.table_form').attr('count'));
        var table_id = 'item_form_' + (count);
        
        var element = $('.extra_item_form').html().replace(/__prefix__/g, total_form);
        $('.table_form').append(element);

        var item_table = $('.table_form').find('table').last();

        if ($('.'+table_id).length == 0){
            item_table.addClass(table_id);
            $('.'+table_id).prepend('');
        }

        item_table.addClass(table_id);

        var cate_form_id = $('#cate_form_'+count).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        var tax = $('#id_category-'+cate_form_id+'-tax').val();
        var item_form_id = $('.'+table_id).last().find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        $('#id_item-'+item_form_id+'-tax').val(tax);

        $('.delete_item_btn').on('click', function(){
            var table_tag = $(this).closest('table');
            table_tag.remove();
            if ($('#id_category-'+cate_form_id+'-tax').val() == null){
                changeCateAmount(count, cate_form_id);
            }
            if ($('.item_form_'+count).length == 0){
                $('#id_category-'+cate_form_id+'-tax').prop('disabled', false);
                $('#id_category-'+cate_form_id+'-amount').prop('readonly', false);
            }
            show_taxes();
        });

        var tax_id = 'id_item-'+item_form_id+'-tax';
        var rate_id = 'id_item-'+item_form_id+'-rate';
        var quantity_id = 'id_item-'+item_form_id+'-quantity';
        var amount_id = 'id_item-'+item_form_id+'-amount';
        var total_amount_id = 'id_item-'+item_form_id+'-total_amount';
        var product_id = 'id_item-'+item_form_id+'-product';
        var desc_id = 'id_item-'+item_form_id+'-item_description';
        CalItemTotalAmount(tax_id, rate_id, quantity_id, amount_id, total_amount_id);

        addnewProduct(product_id, desc_id, quantity_id, rate_id, amount_id, tax_id, total_amount_id);

        numberValidatuion('.item_rate', false);
        numberValidatuion('.item_quantity', true);
    }
    check_gst_status('vendor_side')
});

// Show Cancel Button After Adding Bill
$('#uploadFile').on('change', function(){
    if ($('#uploadFile').val()){
        $('.cancel_file_btn').show();
    }
    $('input[name=remove_file]').val('False');
});

// Remove Preview of File
$('.cancel_file_btn').on('click', function(){
    $('#preview').empty();
    $('#uploadFile').val(null);
    $('.cancel_file_btn').hide();
    $('input[name=remove_file]').val('True');
});

$('.save').on('click', function(){
    valid = totalAmountValidation();
    if (!valid){
        alert("Total amount of Category and it's items are not same")
        return false
    }
    $('#save_button').val(0);
    var ref_id = 0;
    $('.expense_forms').filter(function(){
        var type = $(this).attr('type');
        if (type == 'cate'){
            ref_id += 1
        }
        $(this).find('input[type=hidden]').val(ref_id);
    });
});

$('.save_new').on('click', function(){
    valid = totalAmountValidation();
    if (!valid){
        alert("Total amount of Category and it's items are not same")
        return false
    }
    $('#save_button').val(1);
    var ref_id = 0;
    $('.expense_forms').filter(function(){
        var type = $(this).attr('type');
        if (type == 'cate'){
            ref_id += 1
        }
        $(this).find('input[type=hidden]').val(ref_id);
    });
});

$('.save_print').on('click', function(){
    valid = totalAmountValidation();
    if (!valid){
        alert("Total amount of Category and it's items are not same")
        return false
    }
    $('#save_button').val(2);
    var ref_id = 0;
    $('.expense_forms').filter(function(){
        var type = $(this).attr('type');
        if (type == 'cate'){
            ref_id += 1
        }
        $(this).find('input[type=hidden]').val(ref_id);
    });
});

// Function to Check Total Amount of Category is Equal or Not to It's Items
function totalAmountValidation(){
    all_cate_forms = $("[type=cate]");
    for (let i=0; i<all_cate_forms.length-1; i++){
        element = all_cate_forms[i]
        var t_id = $(element).attr('id').slice(10);
        var f_id = $(element).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        var cate_total_amount = $('#id_category-'+f_id+'-total_amount').val() ? $('#id_category-'+f_id+'-total_amount').val() : 0;
        if ($('.item_form_'+t_id).length > 0){
            var items_total_amount = 0;
            if ($('.item_form_'+t_id).length == 1){
                var item = $('.item_form_'+t_id).find('input[type=hidden]').attr('id').replace('item'+t_id,'');
                var item_id = item.replace(/[^0-9]/g, '');
                if (item.indexOf('item') == -1){
                    amount = $('#id_item'+t_id+'-'+item_id+'-total_amount').val() ? $('#id_item'+t_id+'-'+item_id+'-total_amount').val() : 0
                }else{
                    amount = $('#id_item-'+item_id+'-total_amount').val() ? $('#id_item-'+item_id+'-total_amount').val() : 0
                }
                items_total_amount += Number(amount);
            }else{
                $('.item_form_'+t_id).filter(function(){

                    var item = $(this).find('input[type=hidden]').attr('id').replace('item'+t_id,'');
                    var item_id = item.replace(/[^0-9]/g, '');
                    if (item.indexOf('item') == -1){
                        amount = $('#id_item'+t_id+'-'+item_id+'-total_amount').val() ? $('#id_item'+t_id+'-'+item_id+'-total_amount').val() : 0
                    }else{
                        amount = $('#id_item-'+item_id+'-total_amount').val() ? $('#id_item-'+item_id+'-total_amount').val() : 0
                    }
                    items_total_amount += Number(amount);
                });
            }
            if (Number(cate_total_amount) != items_total_amount){
                return false
                break;
            }
        }
    }
    return true
}

// Function to Delete a Category Form
function deleteCategoryForm(element, edit){
    if (confirm('Deleting the Category will also delete the items added to it. Are you sure you want to delete ?')){
        var id = element.parent().find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');

        var table_tag = element.closest('table');

        if(edit){
            if ($("[type=cate]").length == 2){
                table_tag.find('input').filter(function(){
                    $(this).val('');
                });
                table_tag.find('select').filter(function(){
                    if ($(this).attr('id').indexOf('tax') != -1){
                        $(this).val(0);    
                    }else{
                        $(this).val('');
                    }
                });

                $('#id_category-'+id+'-tax').prop('disabled', false);
                $('#id_category-'+id+'-amount').prop('readonly', false);

                var items_id = table_tag.attr('id').slice(10);
                $('.item_form_'+items_id).filter(function(){
                    $(this).hide();
                    $(this).removeClass('item_form_'+items_id);
                    var item_form_id = $(this).find('input[type=hidden]').attr('id').slice(0,-12);
                    $('#'+item_form_id+'DELETE').prop('checked', true);
                });
            }
            else{
                table_tag.hide();
                table_tag.attr('type','');
                $('#id_category-'+id+'-DELETE').prop('checked', true);
                $('#id_category-'+id+'-amount').val(0);
                $('#id_category-'+id+'-tax').val(0);
                $('#id_category-'+id+'-total_amount').val(0);
            }
        }else{
            if ($("[type=cate]").length == 2){
                table_tag.find('input').filter(function(){
                    $(this).val('');
                });
                table_tag.find('select').filter(function(){
                    if ($(this).attr('id').indexOf('tax') != -1){
                        $(this).val(0);    
                    }else{
                        $(this).val('');
                    }
                });
                $('#id_category-'+id+'-tax').prop('disabled', false);
                $('#id_category-'+id+'-amount').prop('readonly', false);
            }
            else{
                count = Number($('.table_form').attr('count'));
                $('.table_form').attr('count', (count-1));
                table_tag.remove();
            }
        }

        var items_id = table_tag.attr('id').slice(10);
        $('.item_form_'+items_id).filter(function(){
            $(this).remove();
        });

        var sub_total = calExpenseSubTotal();
        $('.expense_sub_total').val(sub_total);
        $('.expense_sub_total').text(sub_total);

        var total = calExpenseTotal();
        $('.expense_total').val(total);
        $('.expense_total').text(total);

        show_taxes();
    }
}

// Function to Add File From Drag&Drop
function dragNdrop(event) {
    var fileName = URL.createObjectURL(event.target.files[0]);
    var fileExe = $('#uploadFile').val().split('.').pop();
    var preview = document.getElementById("preview");
    if (fileExe == 'jpg' || fileExe == 'png' || fileExe == 'jpeg'){
        var previewImg = document.createElement("img");
        previewImg.setAttribute("id", 'exp_bill_img');
    }
    else if (fileExe == 'pdf'){
        var previewImg = document.createElement("embed");
    }
    else{
        alert('Accept only pdf and image file')
        $('#uploadFile').val(null);
        $('.cancel_file_btn').hide();
        return false
    }
    previewImg.setAttribute("src", fileName);
    preview.innerHTML = "";
    preview.appendChild(previewImg);
}
function drag() {
    document.getElementById('uploadFile').parentNode.className = 'draging dragBox';
}
function drop() {
    document.getElementById('uploadFile').parentNode.className = 'dragBox';
}

// Function To Calculate SubTotal
function calExpenseSubTotal(){
    var sub_total = 0;
    $('.cate_amount').filter(function(){
        sub_total += Number($(this).val());
    });
    if (sub_total > 99999999999999999){
        $('.cate_amount').val('');
        alert('Invalid Amount')
        return false
    }
    return sub_total.toFixed(3);
}

// Function To Calculate Total
function calExpenseTotal(){
    var total = 0;
    $('.cate_total_amount').filter(function(){
        total += Number($(this).val());
    });
    if (total > 99999999999999999){
        $('.cate_total_amount').val('');
        alert('Invalid Amount')
        return false
    }
    return total.toFixed(3);
}

// Function to Calculate Total Amount After Changing Amount or Tax 
function CalCategoryTotalAmount(id){
    $('#id_category-'+id+'-amount').change(function(){
        var amount = parseInt($(this).val());
        var tax = Number($('#id_category-'+id+'-tax').val());
        if (tax == 0){
            var total_amount = amount;
        }
        else{
            var total_amount = amount + (amount * (tax/100));
        }

        if (total_amount > 99999999999999999){
            $(this).val('')
            alert('Invalid Amount')
            return false
        }
        
        $('#id_category-'+id+'-total_amount').val(total_amount.toFixed(3));

        var sub_total = calExpenseSubTotal();
        $('.expense_sub_total').val(sub_total);

        var total = calExpenseTotal();
        $('.expense_total').val(total);

        show_taxes();
    });

    $('#id_category-'+id+'-tax').on('change', function(){
        var tax = Number($(this).val());
        var amount = Number($('#id_category-'+id+'-amount').val());
        
        if (amount == 0){
            var total_amount = amount;
        }
        else{
            var total_amount = amount + (amount * (tax/100));
        }

        if (total_amount > 99999999999999999){
            $(this).val('')
            alert('Invalid Amount')
            return false
        }
        
        $('#id_category-'+id+'-total_amount').val(total_amount.toFixed(3));

        var total = calExpenseTotal();
        $('.expense_total').val(total);

        var cate_id = $(this).parents('table').attr('id').replace(/[^0-9]/g, '');
        $('.item_form_'+cate_id).filter(function(){
            var item_id = $(this).find('input[type=hidden]').attr('id').slice(0,-12);
            var item_amount = $('#'+item_id+'amount').val() ? Number($('#'+item_id+'amount').val()) : 0
            var new_item_amount = item_amount + (item_amount*(tax/100));
            $('#'+item_id+'tax').val(tax);
            $('#'+item_id+'total_amount').val(new_item_amount.toFixed(3));
        });

        show_taxes();
    });
}

// Function to Calculate Total Amount After Changing Item's Rate 
function calculateItemRate(rate, element, quantity_id, tax_id, amount_id, total_amount_id){
    var quantity = $('#'+quantity_id).val() ? Number($('#'+quantity_id).val()) : 0
    var amount = quantity * rate;
    if (amount > 99999999999999999){
        alert('Invalid Amount')
        element.val('');
        return false
    }
    var tax = Number($('#'+tax_id).val());
    
    $('#'+amount_id).val(amount.toFixed(3));
    
    if (tax == 0){
        var total_amount = amount;
    }
    else{
        var total_amount = amount + (amount * (tax/100));
    }
    
    $('#'+total_amount_id).val(total_amount.toFixed(3));

    var cate_table_id = element.parents('table').attr('class').replace(/[^0-9]/g, '');
    var cate_form_id = $('#cate_form_'+cate_table_id).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
    if ($('#id_category-'+cate_form_id+'-tax').val() == null){
        changeCateAmount(cate_table_id, cate_form_id);
    }

    show_taxes();
}

// Function to Calculate Total Amount After Changing Item's Tax 
function calculateItemTax(tax, element, amount_id, total_amount_id){
    var cate_table_id = element.parents('table').attr('class').replace(/[^0-9]/g, '');
    var cate_form_id = $('#cate_form_'+cate_table_id).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
    $('#id_category-'+cate_form_id+'-tax').prop('disabled', true);
    $('#id_category-'+cate_form_id+'-amount').prop('readonly', true);

    var amount = $('#'+amount_id).val() ? Number($('#'+amount_id).val()) : 0
        
    if (tax == 0){
        var total_amount = amount;
    }
    else{
        var total_amount = amount + (amount * (tax/100));
    }

    if (total_amount > 99999999999999999){
        alert('Invalid Amount')
        element.val('')
        return false
    }

    $('#'+total_amount_id).val(total_amount.toFixed(3));

    changeCateAmount(cate_table_id, cate_form_id);

    show_taxes();
}

// Function to Calculate Total Amount of Items
function CalItemTotalAmount(tax_id, rate_id, quantity_id, amount_id, total_amount_id){
    $('#'+quantity_id).change(function(){
        var quantity = Number($(this).val());
        var rate = $('#'+rate_id).val() ? Number($('#'+rate_id).val()) : 0
        var amount = quantity * rate;
        if (amount > 99999999999999999){
            alert('Invalid Amount')
            $(this).val('');
            return false
        }
        var tax = Number($('#'+tax_id).val());
        
        $('#'+amount_id).val(amount.toFixed(3));
        
        if (tax == 0){
            var total_amount = amount;
        }
        else{
            var total_amount = amount + (amount * (tax/100));
        }
        
        $('#'+total_amount_id).val(total_amount.toFixed(3));

        var cate_table_id = $(this).parents('table').attr('class').replace(/[^0-9]/g, '');
        var cate_form_id = $('#cate_form_'+cate_table_id).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
        if ($('#id_category-'+cate_form_id+'-tax').val() == null){
            changeCateAmount(cate_table_id, cate_form_id);
        }

        show_taxes();
    });
    
    $('#'+rate_id).change(function(){
        var rate = Number($(this).val());
        calculateItemRate(rate, $(this), quantity_id, tax_id, amount_id, total_amount_id);
    });

    $('#'+tax_id).change(function(){
        var tax = Number($(this).val());
        calculateItemTax(tax, $(this), amount_id, total_amount_id);
    });
}

function show_taxes(){
    all_taxes = {'5':0,'2':0,'12':0,'6':0,'18':0,'9':0,'28':0,'14':0}
    var org_state = $('#single_gst_code option:selected').val()
    var vendor_g = ''
    if(vendor_gstin != ''){
        vendor_g = vendor_gstin.substring(0,2)
    }

    var all_cate_form = $('[type=cate]');
    $('[type=cate]').filter(function(){
        if ($(this).attr('id')){
            var form_id = $(this).attr('id').slice(10);
            var cate_id = $(this).find('input[type=hidden]').attr('id').replace(/[^0-9]/g, '');
            if ($('#id_category-'+cate_id+'-tax').val()){
                var cate_tax = Number($('#id_category-'+cate_id+'-tax').val());
                var cate_amount = $('#id_category-'+cate_id+'-amount').val() ? Number($('#id_category-'+cate_id+'-amount').val()) : 0;
                var cate_tax_amount = cate_amount * (cate_tax/100);
                if(org_state == vendor_g){
                    var half = cate_tax_amount/2
                    if(cate_tax == 5){
                        all_taxes[2] += half
                    }else if(cate_tax == 12){
                        all_taxes[6] += half
                    }else if(cate_tax == 18){
                        all_taxes[9] += half
                    }else if(cate_tax == 28){
                        all_taxes[14] += half
                    }
                }
                else if(org_state != vendor_g){
                    all_taxes[cate_tax] += cate_tax_amount
                }
            }
            else{
                $('.item_form_'+form_id).filter(function(){
                    var item_id = $(this).find('input[type=hidden]').attr('id').slice(0,-12);
                    var item_tax = Number($('#'+item_id+'tax').val());
                    var item_amount = $('#'+item_id+'amount').val() ? Number($('#'+item_id+'amount').val()) : 0;
                    var item_tax_amount = item_amount * (item_tax/100)
                    if(org_state == vendor_g){
                        var half = item_tax_amount/2
                        if(item_tax == 5){
                            all_taxes[2] += half
                        }else if(item_tax == 12){
                            all_taxes[6] += half
                        }else if(item_tax == 18){
                            all_taxes[9] += half
                        }else if(item_tax == 28){
                            all_taxes[14] += half
                        }
                    }else if(org_state != vendor_g){
                        all_taxes[item_tax] += item_tax_amount
                    }
                });
            }
        }
    });
    for (tax in all_taxes){
        if(all_taxes[tax]){
            if(tax == 2 || tax == 6 || tax == 9 || tax == 14){
                $('.tax_csgst_'+tax).find('input').val(all_taxes[tax].toFixed(3));
                $('.tax_csgst_'+tax).show();
            }else{
                $('#tax_'+tax).find('input').val(all_taxes[tax].toFixed(3));
                $('#tax_'+tax).show();
            }
        }else{
            if(tax == 2 || tax == 6 || tax == 9 || tax == 14){
                $('.tax_csgst_'+tax).find('input').val(0);
                $('.tax_csgst_'+tax).hide();
            }else{
                $('#tax_'+tax).find('input').val(0);
                $('#tax_'+tax).hide();
            }
        }
    }
}

function changeCateAmount(cate_table_id, cate_form_id){
    var cate_amount = 0
    var cate_total_amount = 0
    $('.item_form_'+cate_table_id).filter(function(){
        var item_form_id = $(this).find('input[type=hidden]').attr('id').slice(0,-12);
        cate_amount += Number($('#'+item_form_id+'amount').val());
        cate_total_amount += Number($('#'+item_form_id+'total_amount').val());
    });

    $('#id_category-'+cate_form_id+'-tax').val('');
    $('#id_category-'+cate_form_id+'-tax').prop("required", false);
    $('#id_category-'+cate_form_id+'-amount').val(cate_amount.toFixed(3));
    $('#id_category-'+cate_form_id+'-total_amount').val(cate_total_amount.toFixed(3));

    var sub_total = calExpenseSubTotal();
    $('.expense_sub_total').val(sub_total);

    var total = calExpenseTotal();
    $('.expense_total').val(total);
}

function numberValidatuion(element, is_quantity){
    $(element).keypress(function(event){
        var charCode = (event.which) ? event.which : event.keyCode
        if (charCode == 45 || charCode == 69 || charCode == 101 || charCode == 43){
            return false
        }

        var value = $(this).val();
        var len = 15;
        var code = 2;
        if (is_quantity){
            var len = 10;
            var code = 1;
        }
        
        if (value.length > len){
            return false
        }
        if(value.indexOf(".") > -1 && (value.split('.')[1].length > code)){
            return false
        }
    });
}

var vendor_options = $('#select_vendor option:not(:selected)');
for(var i=0;i < vendor_options.length;i++){
    if(vendor_options[i].text.includes('(Inactive)')){
        vendor_options[i].remove();
    }
}

var product_options = $('.select_product option:not(:selected)');
for(var i=0;i < product_options.length;i++){
    if(product_options[i].text.includes('(Inactive)')){
        product_options[i].remove();
    }
}

$.get("/get_predefined_groups/",{"ids":"2"}, function(data){
    $("#id_acc_group").empty().append(data);
});


/********************************************************************/
//  Datepicker validation
/********************************************************************/

$("#id_exp_date").on('keypress', function(event){
    var charCode = (event.which) ? event.which : event.keyCode
    return (charCode >= 47 && charCode <= 57) ? true : false
});

$("#id_payment_date").on('keypress', function(event){
    var charCode = (event.which) ? event.which : event.keyCode
    return (charCode >= 47 && charCode <= 57) ? true : false
});

$("#id_exp_date").on('change', function(event){
    dateValidation($(this));
});

$("#id_payment_date").on('change', function(event){
    dateValidation($(this));
});

function dateValidation(element){
    var date = $(element).val();
    var regEx = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
    if(!regEx.test(date)){
        alert('Invalid Date');
        $(element).val('');
    }
}


/********************************************************************/
// INVOICE GST CHANGES
/********************************************************************/
$('#multiple_gst_link').click(function(){

    $.get("/gst_number/", function(data){
        $(".gst_row").each(function(){
                        
            $(this).remove()
        });
        for(var i = 0;i < data.gst_number.length;i++){
            var html = '<tr class="gst_row" id="choose_gst_row_'+i+'"><td style="border:1px solid black;" align="center"><label class="form-check-label" style="margin-left:27%;">'
                html+='<input class="form-check-input choose_gst" type="radio" name="radio" id="choose_gst_'+(parseInt(i)+1)+'" onclick="radio_click($(this))" value="on" style="margin-top:-2%"><span class="circle"><span class="check"></span></span></label></td>'
                html +='<td style="border:1px solid black;" id="c_gst_number'+(parseInt(i)+1)+'" align="center">'+data.gst_number[i]+'</td>'
                html +='<td style="border:1px solid black;display:none;" id="c_gst_type'+(parseInt(i)+1)+'" align="center">'+data.gst_type[i]+'</td>'
                $('#GST_table').append(html)
        }
        $('#invoice_multi_gst').modal('show')
    });
});

/********************************************************************/
// choose GST
/********************************************************************/

function radio_click(elem){
    var names = $(elem).attr('id')
    names = names.substring(names.length-1,names.length)
    $('#org_gst_number').val($('#c_gst_number'+names).text())
    $('#org_gst_reg_type').val($('#c_gst_type'+names).text())
};


function button_click(category){
    if(category = 'multiple'){
        var checkbox_count = 0
        $('.choose_gst').each(function(){
            if($(this).prop("checked") == true){
                checkbox_count +=1
            }
        })
        if(checkbox_count == 0){
            alert('Please first choose the GST')
            return false
        }
        var gst = $('#org_gst_number').val()
        $('#multiple_gst').text("Your default Organization gst number:-"+gst+". Do you want to create this invoice with another GST number.")
        gst = gst.substring(0,2)
		if($("#single_gst_code option[value="+gst+"]").length > 0){

            $('#single_gst_code').val(gst).change()
        }
        check_gst_status('user_side')
        $('#invoice_multi_gst').modal('hide')
    }
}
$(document).ready(function(){
    if($('#org_gst_reg_type') == '8'){
        alert('Organization is register under composite scheme, it can not choose delivery address of different state.')
    }
});
/********************************************************************/
// GST STATE ADDRESS CHECK
/********************************************************************/

function gst_state_code(elem){
	if($('#error_field').text() == '' & $(elem).val() != ''){
		var str = $(elem).val()
		str = str.substring(0,2)
		if($("#single_gst_code option[value="+str+"]").length > 0){
			var state = $("#single_gst_code option[value="+str+"]").text()
			var org_id = $('#org_id').val()
			$.post("/org/gst_state_code/",{'state':state, 'org_id':org_id,'csrfmiddlewaretoken':csrf_token},function(data){
				if(data == 0){
					$('#error_field').text('GST state code not matching with existing address state') 
					$('#org_single_gst_save').prop('disabled', true)
				}else{
                    $('#gst_state').val($("#single_gst_code option[value="+str+"]").text())
                    $('#single_gst_code').val(str).change()
				}
			});
		}else{
			$('#error_field').text('GST state code not matching with existing address state') 
			$('#org_single_gst_save').prop('disabled', true)
		}
	}
}

$('.mul_cancel_gst').click(function(){
	$('#error_field').text('') 
	$('.multiple_update').prop('disabled', false)
})

/********************************************************************/
// GST STATE ADDRESS CHECK
/********************************************************************/

function update_single_gst(){
    event.preventDefault()
    $.post("/profile/gst_configuration/",$("#org_gst_update").serialize(), function(data){
        if(data != '0'){
            var gst_num = $('#single_gst').val()
            $('#org_gst_reg_type').val($('#single_gst_type').val())
            $('#replace_change_update').find('h6').text('Your default Organization gst number:-'+gst_num+'.')
            $('#change_update_gst').hide()
            $('#replace_change_update').show()
            $('#org_gst_number').val(gst_num)
            $('#add_gst_number').modal('hide')
            check_gst_status('user_side')
        }
    });
}