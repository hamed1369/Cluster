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

    $("#register_form").validationEngine({promptPosition: "centerLeft", scroll: false});


    $('input[name*="is_cluster"]').change(function () {
        var is_cluster = $('input[name*="is_cluster"]:checked', '#register_form').val();

        if (is_cluster == 1) {
            $('#only_for_cluster').slideDown();
        } else {
            $('#only_for_cluster').slideUp();
        }

    });

    $('select[name*="employment_status"]').change(function () {
        if ($(this).val() == 1) {
            $('input[name*="organization"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="organization"]').parents('tr').first().fadeOut();
        }
    });


    $('select[name*="military_status"]').change(function () {
        if ($(this).val() == 2) {
            $('select[name*="exemption_type"]').parents('tr').first().fadeOut();
            $('input[name*="military_place"]').parents('tr').first().fadeIn();
        } else if ($(this).val() == 3) {
            $('select[name*="exemption_type"]').parents('tr').first().fadeIn();
            $('input[name*="military_place"]').parents('tr').first().fadeOut();
        } else {
            $('select[name*="exemption_type"]').parents('tr').first().fadeOut();
            $('input[name*="military_place"]').parents('tr').first().fadeOut();
        }
    });


    $('input[name*="foundation_of_elites"]').change(function () {
        var is_cluster = $('input[name*="foundation_of_elites"]:checked', '#register_form').val();

        if (is_cluster == 'True') {
            $('input[name*="elite_certification"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="elite_certification"]').parents('tr').first().fadeOut();
        }

    });


    $('.register_table tr, .inner_formset tr').click(function () {
        $('.register_table tr, .inner_formset tr').css({
            border: '0',
            backgroundColor: '#fff'
        });
        $(this).css({
            border: '1px solid rgb(221, 221, 0)',
            backgroundColor: 'rgb(255, 253, 226)'
        });
    });
});
