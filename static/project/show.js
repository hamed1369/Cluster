$(document).ready(function () {
    $('.seen-by-member-input').change(function () {
        var is_seen = $(this).is(':checked');
        var comment_id = $(this).next('input').val();
        var $img_element = $(this).parent().find('img').first();
        $.ajax({
            type: "POST",
            url: "/ajax/change_seen_by_member/",
            data: { i: is_seen, c: comment_id },
            beforeSend: function () {
                $img_element.fadeIn();
            },
            error: function () {
                alert('ارسال اطلاعات با مشکل مواجه شد');
                if (is_seen)
                    $(this).removeAttr('checked');
                else
                    $(this).attr('checked', 'checked');
                $img_element.fadeOut(1000);
            },
            success: function () {
                $img_element.fadeOut(1000);
            }
        })
            .done(function (msg) {
            });
    });
});