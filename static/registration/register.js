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
    var validated = false;
    function updateValidations(){
        if (validated){
            $("#register_form").validationEngine("updatePromptsPosition");
            alert(1);
        }
    }
//    function hideValidations(){
//        if (validated){
//            $('#register_form').validationEngine('hideAll');
//        }
//    }

    $("#register_form").validationEngine({
        promptPosition: "centerLeft",
        scroll: true,
        autoPositionUpdate:true,
        validationEventTrigger:'submit',
        onValidationComplete: function(){
            validated = true;
        }

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
        updateValidations();


    });

    $('select[name*="employment_status"]').change(function () {
        if ($(this).val() == 1) {
            $('input[name*="organization"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="organization"]').parents('tr').first().fadeOut();
            $('input[name*="organization"]').val('');
        }
        updateValidations();

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
        updateValidations();

    });


    $('input[name*="foundation_of_elites"]').change(function () {
        var foundation_of_elites = $('input[name*="foundation_of_elites"]:checked', '#register_form').val();

        if (foundation_of_elites == 'True') {
            $('input[name*="elite_certification"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="elite_certification"]').parents('tr').first().fadeOut();
            $('input[name*="elite_certification"]').val('');
        }
        updateValidations();


    });


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
});
