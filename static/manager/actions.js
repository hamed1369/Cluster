$(document).ready(function () {

    $('select').select2({
        minimumResultsForSearch: 99
    });

    $('select[name*=send_type]').change(function () {
        var send_type = parseInt($(this).val());
        if (send_type in [4,6,9]){
            $(this).parents('tr').first().next('tr').fadeOut();
        }else{
            $(this).parents('tr').first().next('tr').fadeIn();
        }
    });


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