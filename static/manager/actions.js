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


});