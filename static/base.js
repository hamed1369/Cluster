$(document).ready(function () {
    $('button, input[type=submit], input[type=reset], input[type=button], .button_link').button();

    if (typeof $.validationEngineLanguage != 'undefined') {

        $.extend($.validationEngineLanguage.allRules, {
            "mobile": {
                "regex": /^0\d{10}$/,
                "alertText": "* شماره تلفن همراه معتبر وارد کنید"
            },
            only_english: {
                "regex": /^[0-9a-zA-Z!#\$%&'\*\+\-\/=\?\^_`{\|}~@.,]+$/,
                "alertText": "* فقط اعداد و حروف انگلیسی وارد کنید"
            },
            usernameAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این نام کاربری در دسترس است",
                "alertText": "* این نام‌کاربری تکراری است",
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            },
            emailAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این ایمیل در دسترس است",
                "alertText": "* این ایمیل تکراری است",
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            },
            clusterNameAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این ایمیل در دسترس است",
                "alertText": "* این نام تکراری است",
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            }
        });
        $(".js-validation-from").validationEngine({
            promptPosition: "centerLeft:0,-5",
            scroll: true,
            validationEventTrigger: 'blur'
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

function popitup(url, windowName) {
    var width = '600';
    var height = '500';
    var left = (screen.width / 2) - (width / 2);
    var top = (screen.height / 2) - (height / 2);

    newwindow = window.open(url, windowName, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
    if (window.focus) {
        newwindow.focus()
    }
    return false;
}