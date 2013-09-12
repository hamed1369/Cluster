$(document).ready(function () {
//    var $formsets = $('.formset_container');
//    $formsets.each(function () {
//        var prefix = $(this).parent('div').find('input[name="formset_prefix"]').first().val();
//        var table_id = $(this).find('table').attr('id');
//        alert(table_id);
//        $('#' + table_id + ' tbody tr').formset(
//            {
//                prefix: 'id_' + prefix,
//                addText: 'افزودن',
//                deleteText: 'حذف',
//                addCssClass: 'formset_add',
//                deleteCssClass: 'formset_delete'
//            }
//        );
//
//    });
//    function validate(){
//        $("#id_language_skill-0-language").validationEngine('validate');
//    }
//    $("[name=register-submit]").click(function(){
//        validate();
//        return true;
//    });
//    var validated = false;
//        if (validated){
//            $("#register_form").validationEngine("updatePromptsPosition");
//        }
//    function hideValidations(){
//        if (validated){
//            $('#register_form').validationEngine('hideAll');
//        }
//    }

    $('select[name*="domain_choice"]').each(function () {
        if ($(this).val().trim() == '') {
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').show();
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').addClass('validate[required,] text-input');
        } else {
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').hide();
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').val('');
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').removeClass('validate[required,] text-input');
        }
    });

    $('select[name*="domain_choice"]').change(function () {
        if ($(this).val().trim() == '') {
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').show();
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').addClass('validate[required,] text-input');
        } else {
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').hide();
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').val('');
            $(this).parents('tr').first().find('input[name*="new_domain_name"]').removeClass('validate[required,] text-input');
            $(this).parents('tr').first().find('.formError').remove();
        }
    });

    $('#cluster_member_formset select').focusin(function () {

        var options = {};

        $('select[name*="domain_choice"]').each(function () {
            if ($(this).parents('tr').first().css('display') != 'none')
                if ($(this).val().trim() == '') {
                    var text_val = $(this).parents('tr').first().find('input[name*="new_domain_name"]').val().trim();
                    if (text_val != "") {
                        options[text_val] = text_val;
                    }
                } else {
                    options[$(this).val()] = $(this).find(':selected').text();
                }
        });

        var $this_select = $(this);
        $this_select
            .find('option')
            .remove();
        $this_select
            .append($("<option></option>")
                .attr("value", '')
                .text('---------'));
        $.each(options, function (key, value) {
            $this_select
                .append($("<option></option>")
                    .attr("value", key)
                    .text(value));
        });
    });


    $('input[name*="is_cluster"]').change(function () {
        var is_cluster = $('input[name*="is_cluster"]:checked', '#register_form').val();


        if (is_cluster == 'True') {
            $('#only_for_cluster').slideDown();
            $('#only_for_cluster input[type="text"]').addClass('validate[required,] text-input');

        } else {
            $('#only_for_cluster').slideUp();
            $('#only_for_cluster input[type="text"]').removeClass('validate[required,] text-input');
        }


    });

    $('select[name*="employment_status"]').change(function () {
        if ($(this).val() == 1) {
            $('input[name*="organization"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="organization"]').parents('tr').first().fadeOut();
            $('input[name*="organization"]').val('');
        }

    });


    $('select[name*="military_status"]').change(function () {
        if ($(this).val() == 2) {
            $('select[name*="exemption_type"]').parents('tr').first().fadeOut();
            $('input[name*="military_place"]').parents('tr').first().fadeIn();
            $('select[name*="exemption_type"]').val('');
        } else if ($(this).val() == 3) {
            $('select[name*="exemption_type"]').parents('tr').first().fadeIn();
            $('input[name*="military_place"]').parents('tr').first().fadeOut();
            $('input[name*="military_place"]').val('');
        } else {
            $('select[name*="exemption_type"]').parents('tr').first().fadeOut();
            $('input[name*="military_place"]').parents('tr').first().fadeOut();
            $('select[name*="exemption_type"]').val('');
            $('input[name*="military_place"]').val('');
        }

    });


    $('input[name*="foundation_of_elites"]').change(function () {
        var foundation_of_elites = $('input[name*="foundation_of_elites"]:checked', '#register_form').val();

        if (foundation_of_elites == 'True') {
            $('input[name*="elite_certification"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="elite_certification"]').parents('tr').first().fadeOut();
            $('input[name*="elite_certification"]').val('');
        }


    });

    $('input[name*="change_password"]').change(function () {
        var change_pass = $('input[name*="change_password"]:checked', '#register_form').val();
        var $first_tr = $(this).parents('tr').first().next('tr');
        var $second_tr = $first_tr.next('tr');

        if (change_pass == 'True') {
            $first_tr.show(500);
            $second_tr.show(500);
        } else {
            $first_tr.hide(500);
            $second_tr.hide(500);
        }
    });
    $('input[name*="change_password"]').change();


//    $('.register_table tr, .inner_formset tr').click(function () {
//        $('.register_table tr, .inner_formset tr').css({
//            border: '0',
//            backgroundColor: '#fff'
//        });
//        $(this).css({
//            border: '1px solid rgb(221, 221, 0)',
//            backgroundColor: 'rgb(255, 253, 226)'
//        });
//    });


    // important for disable first formsets row delete icon
//    $(function () {
//        $('.formset_container').each(function () {
//            $(this).find('tbody tr').first().find('.formset_delete').remove();
//        });
//    });
});


function check_date_picker() {
    var $date_fields = $('.' + $(this)[0].formCssClass).last().find('.hasDatepicker');
    $date_fields.removeClass('hasDatepicker');
    $date_fields.datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: '1300,1400',
        dateFormat: 'yy/mm/dd'
    });
}
