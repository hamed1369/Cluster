$(document).ready(function () {
    $('button, input[type=submit], input[type=reset], input[type=button], .button_link').button();

    if (typeof $.validationEngineLanguage != 'undefined') {

        $.extend($.validationEngineLanguage.allRules, {
            only_english: {
                "regex": /^[0-9a-zA-Z!#\$%&'\*\+\-\/=\?\^_`{\|}~@.,]+$/,
                "alertText": "* فقط اعداد و حروف انگلیسی وارد کنید"
            },
            usernameAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
                "alertTextOk": "این نام کاربری در دسترس است",
                "alertText": "* این نام‌کاربری تکراری است",
                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            },
            emailAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
                "alertTextOk": "این ایمیل در دسترس است",
                "alertText": "* این ایمیل تکراری است",
                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            }
        });
        $(".js-validation-from").validationEngine({
            promptPosition: "topLeft:-60,3",
            scroll: true,
            validationEventTrigger: 'submit'
        });
    }
//    $(".js-validation-from").submit(function () {
//        $('.dynamic-formset0').each(function () {
//            var has_val = false;
//            $(this).find('input[type=text], select').each(function () {
//                var value = $(this).val();
//                if (value && value != '') {
//                    has_val = true
//                }
//            });
//            if (!has_val) {
//                alert($(this).attr('class'));
//                $(this).validationEngine('detach');
//                $(this).validationEngine('hideAll');
//            }
//        });
//    });

});