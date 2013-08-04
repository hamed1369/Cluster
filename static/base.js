$(document).ready(function () {
    $('input[type=text]').addClass('form-control');
    $('input[type=password]').addClass('form-control');
    if (typeof formset != 'undefined')
        $('.formset_container').formset();
});