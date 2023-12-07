$(document).ready(function () {
    const $templateNameSelect = $("#id_template_name");
    const $notificationTitleTextarea = $("#id_notification_title");
    const $notificationContentTextarea = $("#id_notification_content");

    function updateFields() {
        const selectedTemplateName = $templateNameSelect.val();
        const selectedTemplate = notificationTemplates.find(function (template) {
            return template.template_name === selectedTemplateName;
        });

        if (selectedTemplate) {
            $notificationTitleTextarea.val(selectedTemplate.template_title);
            $notificationContentTextarea.val(selectedTemplate.template_content);
        } else {
            $notificationTitleTextarea.val("");
            $notificationContentTextarea.val("");
        }
    }

    $templateNameSelect.on("change", updateFields);
    updateFields();

    function addOptionsToSelect() {
        $templateNameSelect.empty();
        $templateNameSelect.append($('<option>', {value: '',  text: '---------', disabled: true, selected: true}));
        $.each(notificationTemplates, function (index, template) {
            $templateNameSelect.append($('<option>', {
                value: template.template_name,
                text: template.template_name
            }));
        });
    }
    addOptionsToSelect();

    $('.cancel-link').click(function(e) {
            e.preventDefault();
            const parentWindow = window.parent;
            if (parentWindow && typeof(parentWindow.dismissRelatedObjectModal) === 'function' && parentWindow !== window) {
                parentWindow.dismissRelatedObjectModal();
            } else {
                // fallback to default behavior
                window.history.back();
            }
            return false;
        });
});
