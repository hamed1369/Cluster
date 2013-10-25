$(document).ready(function () {

    $('select[multiple]').select2({
        minimumResultsForSearch: 99
    });

    $('select[name*=send_type]').change(function () {
        var send_type = parseInt($(this).val());
        if (send_type == 9) {
            $(this).parents('tr').first().next('tr').fadeIn();
            $('[name*="member_receivers"]').parents('tr').first().fadeOut();
            $('[name*="arbiter_receivers"]').parents('tr').first().fadeOut();
        } else if (send_type == 4) {
            $('[name*="member_receivers"]').parents('tr').first().fadeIn();
            $('[name*="arbiter_receivers"]').parents('tr').first().fadeOut();
        } else if (send_type == 6) {
            $('[name*="arbiter_receivers"]').parents('tr').first().fadeIn();
            $('[name*="member_receivers"]').parents('tr').first().fadeOut();
        } else {
            $(this).parents('tr').first().next('tr').fadeOut();
            $('[name*="member_receivers"]').parents('tr').first().fadeOut();
            $('[name*="arbiter_receivers"]').parents('tr').first().fadeOut();
        }
    });
    $('select[name*=send_type]').change();


    $('input[name*="change_password"]').change(function () {
        var change_pass = $('input[name*="change_password"]:checked').val();
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

//    $('select[name*=receivers]').select2({
//        placeholder: "جستجو کاربران",
//        minimumInputLength: 1,
//        ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
//            url: "/ajax/select2/",
//            dataType: 'jsonp',
//            data: function (term, page) {
//                return {
//                    q: term, // search term
//                    send_type: $('select[name*=send_type]').val()
//                };
//            },
//            results: function (data, page) { // parse the results into the format expected by Select2.
//                // since we are using custom formatting functions we do not need to alter remote JSON data
//                return {results: data};
//            }
//        },
//        formatResult: function (m) { return m; }, // omitted for brevity, see the source of this page
//        formatSelection: function (m) { return m.id; },  // omitted for brevity, see the source of this page
//        dropdownCssClass: "bigdrop", // apply css that makes the dropdown taller
//        escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
//    });

});