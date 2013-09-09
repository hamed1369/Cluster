$(document).ready(function () {

    $('input[type=text], textarea').addClass('form-control');
    $('input[type=submit], input[type=button], button').addClass('btn btn-primary');

    $('select').removeClass('form-control');
    $('select').select2({
    });


});