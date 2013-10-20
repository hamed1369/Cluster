$(document).ready(function () {

    if ($('input[name*=score]')) {
        $('select[name*="project_status"]').change(function () {
            if ($(this).val() == 1) {
                $('input[name*="score"]').parents('tr').first().fadeIn();
                $('#arbiter_formset_div').fadeIn();
                $('#project_arbiters_div').fadeIn();
            } else {
                $('input[name*="score"]').parents('tr').first().fadeOut();
                $('input[name*="score"]').val('');
                $('#arbiter_formset_div').fadeOut();
                $('#project_arbiters_div').fadeOut();
            }
        });
        $('select[name*="project_status"]').change();
    }
});