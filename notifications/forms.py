from django import forms
from django.db import IntegrityError
from notifications.models import NotificationTemplates
from notifications.widgets import CustomTemplateContentWidget, CustomTemplateTitleWidget
from notifications.messages import TEMPLATE_NAME_NOT_UNIQUE


class NotificationTemplateForm(forms.ModelForm):
    class Meta:
        model = NotificationTemplates
        fields = '__all__'
        widgets = {
            'template_title': CustomTemplateTitleWidget(),
            'template_content': CustomTemplateContentWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        template_name = cleaned_data.get('template_name')
        trigger_point = cleaned_data.get('trigger_point')
        existing_record = NotificationTemplates.objects.filter(
            template_name=template_name,
            trigger_point=trigger_point,
            is_deleted=False
        ).exclude(pk=self.instance.pk if self.instance else None)
        if existing_record.exists():
            self.add_error('template_name', IntegrityError(TEMPLATE_NAME_NOT_UNIQUE))
        return cleaned_data


class NotificationTemplateSelectForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    template_name = forms.ChoiceField()
    notification_title = forms.CharField()
    notification_content = forms.CharField()


class NotificationForm(forms.Form):
    """
    Form for the broadcast notification model
    """
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    notification_title = forms.CharField(widget=CustomTemplateTitleWidget(), required=False)
    notification_content = forms.CharField(widget=CustomTemplateContentWidget(), required=True)
    notification_image = forms.ImageField(required=False)
    widgets = {
        'notification_title': CustomTemplateTitleWidget(),
        'notification_content': CustomTemplateContentWidget(),
    }
