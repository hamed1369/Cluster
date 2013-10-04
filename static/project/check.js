$(document).ready(function () {

    if ($('input[name*=score]')) {
        $('select[name*="arbiter"]').select2();
        $('select[name*="project_status"]').change(function () {
            if ($(this).val() == 1) {
                $('input[name*="score"]').parents('tr').first().fadeIn();
                $('select[name*="arbiter"]').parents('tr').first().fadeIn();
            } else {
                $('input[name*="score"]').parents('tr').first().fadeOut();
                $('input[name*="score"]').val('');
                $('select[name*="arbiter"]').parents('tr').first().fadeOut();
                $('select[name*="arbiter"]').val('');
            }

        });
    }
});