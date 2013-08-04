$(document).ready(function () {
    var $formsets = $('.formset_container');
    $formsets.formset(
            {
                addText: 'افزودن',
                deleteText: 'حذف',
                addCssClass: 'formset_add',
                deleteCssClass: 'formset_delete'
            }
    );

    $("#register_form").validationEngine({promptPosition: "centerLeft", scroll: false});
});