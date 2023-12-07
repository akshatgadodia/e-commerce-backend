$(document).ready(function () {
    var dropdowns = $('.notificationTemplateDropdown');
    dropdowns.css('display', 'flex');

    function populateMenu(menu, targetField) {
        menu.empty();
        dynamicVariables.forEach(function (value) {
            var listItem = $('<li>', {
                text: value,
                'data-value': value,
            });
            listItem.on('click', function (event) {
                var selectedValue = $(event.target).data('value');
                var currentContent = $(targetField).val();
                if (currentContent.charAt(currentContent.length - 1) !== ' ') {
                    selectedValue = ' ' + selectedValue;
                }
                $(targetField).val(currentContent + selectedValue);
            });
            menu.append(listItem);
        });
    }

    populateMenu($('#templateTitleMenu'), '#id_notification_title');
    populateMenu($('#templateContentMenu'), '#id_notification_content');

    $('.cancel-link').click(function (e) {
        e.preventDefault();
        const parentWindow = window.parent;
        if (parentWindow && typeof (parentWindow.dismissRelatedObjectModal) === 'function' && parentWindow !== window) {
            parentWindow.dismissRelatedObjectModal();
        } else {
            window.history.back();
        }
        return false;
    });
});
