$(document).ready(function () {
    const $notificationTemplateDropdown = $(".notificationTemplateDropdown");
    const $triggerPointSelect = $("#id_trigger_point");
    const $triggerPointSelect2 = $triggerPointSelect.select2();
    const $moduleSelect = $("#id_module_name");
    const $templateTitle = $("#id_template_title");
    const $templateContent = $("#id_template_content");
    const $templateContentMenu = $("#templateContentMenu");
    const $templateTitleMenu = $("#templateTitleMenu");
    const originalOptions = $triggerPointSelect.html();

    // Function to set trigger points based on the module name selected
    function updateOptions() {
        $triggerPointSelect2.empty();
        const selectedModule = $moduleSelect.val().toUpperCase();
        if (selectedModule !== "") {
            const requiredOptions = [];
            requiredOptions.push($(originalOptions).eq(0));
            $(originalOptions).slice(1).each(function () {
                const triggerPoint = $(this).val();
                if (triggerPoint.startsWith(selectedModule)) {
                    requiredOptions.push($(this));
                }
            });
            $triggerPointSelect.html(requiredOptions);
            $triggerPointSelect2.html(requiredOptions);
        }
        $triggerPointSelect2.trigger('change.select2');
    }

    // Function to set dynamic variables based on the trigger point selected
    function handleTriggerPointChange(clearValues = true) {
        const selectedTriggerPoint = $triggerPointSelect.val();
        if (clearValues) {
            $templateTitle.val("");
            $templateContent.val("");
        }
        const dynamicVariables = triggerPoints[selectedTriggerPoint];
        if (dynamicVariables && dynamicVariables.length > 1) {
            $notificationTemplateDropdown.show();
        } else {
            $notificationTemplateDropdown.hide();
        }
        $templateContentMenu.empty();
        $templateTitleMenu.empty();
        $.each(dynamicVariables, function (index, variable) {
            const $contentListItem = $("<li></li>").attr("data-value", variable).text(variable);
            const $titleListItem = $contentListItem.clone();
            $templateContentMenu.append($contentListItem);
            $templateTitleMenu.append($titleListItem);
        });
    }

    // Function to add or insert value into fields based on dynamic variable clicked
    function handleMenuItemClick(selectedMenu, targetElement) {
        let selectedValue = $(selectedMenu).data('value');
        const currentContent = $(targetElement).val();
        if (currentContent.charAt(currentContent.length - 1) !== ' ') {
            selectedValue = ' ' + selectedValue;
        }
        $(targetElement).val(currentContent + selectedValue);
    }

    // Events to call handleMenuItemClick on dynamic variable insertion click
    $(document).on('click', '#templateTitleMenu li, #templateContentMenu li', function () {
        const menuType = $(this).parent().attr('id');
        if (menuType === 'templateTitleMenu') {
            handleMenuItemClick(this, $templateTitle);
        } else if (menuType === 'templateContentMenu') {
            handleMenuItemClick(this, $templateContent);
        }
    });

    updateOptions();
    handleTriggerPointChange(false);
    $moduleSelect.on("change", function () {
        updateOptions();
    });
    $triggerPointSelect.on("change", function () {
        handleTriggerPointChange();
    });
});
