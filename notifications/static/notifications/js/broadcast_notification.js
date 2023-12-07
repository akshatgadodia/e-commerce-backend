$(document).ready(function () {
    $('input#action-toggle').on('change', function () {
        var isChecked = $(this).is(':checked');
        if (isChecked) {
            const showAll = $('a[title="Click here to select the objects across all pages"]');
            showAll[0]?.click();
        } else {
            const clearAll = $('.clear a');
            clearAll[0]?.click();
        }
    });
});
