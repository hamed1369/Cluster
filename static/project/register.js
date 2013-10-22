$(document).ready(function () {

    $('input[name*="has_confirmation"]').change(function () {
        var field_val = $('input[name*="has_confirmation"]:checked').val();

        if (field_val == 'True') {
            $('select[name*="confirmation_type"]').parents('tr').first().fadeIn();
            $('input[name*="certificate_image"]').parents('tr').first().fadeIn();
        } else {
            $('select[name*="confirmation_type"]').parents('tr').first().fadeOut();
            $('select[name*="confirmation_type"]').val('');
            $('input[name*="certificate_image"]').parents('tr').first().fadeOut();
            $('input[name*="certificate_image"]').val('');
        }
    });
    $('input[name*="has_confirmation"]').change();


    $('input[name*="has_patent"]').change(function () {
        var field_val = $('input[name*="has_patent"]:checked').val();

        if (field_val == 'True') {
            $('input[name*="patent_number"]').parents('tr').first().fadeIn();
            $('input[name*="patent_date"]').parents('tr').first().fadeIn();
            $('input[name*="patent_certificate"]').parents('tr').first().fadeIn();
        } else {
            $('input[name*="patent_number"]').parents('tr').first().fadeOut();
            $('input[name*="patent_number"]').val('');
            $('input[name*="patent_date"]').parents('tr').first().fadeOut();
            $('input[name*="patent_date"]').val('');
            $('input[name*="patent_certificate"]').parents('tr').first().fadeOut();
            $('input[name*="patent_certificate"]').val('');
        }
    });
    $('input[name*="has_patent"]').change();

    $('select[name*="attended_members"]').select2();
});