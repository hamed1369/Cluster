$(document).ready(function () {
    $('button, input[type=submit], input[type=reset], input[type=button], .button_link').button();
    $(".js-validation-from").validationEngine({
        promptPosition: "topLeft:-60,3",
        scroll: true,
        validationEventTrigger: 'submit'
    });

});