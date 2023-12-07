from django.template import loader
from django.utils.safestring import mark_safe
from django import forms


class CustomTemplateTitleWidget(forms.Widget):
    template_name = 'notifications/custom_template_title_widget.html'

    def get_context(self, name, value, attrs=None, renderer=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs, renderer=renderer)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class CustomTemplateContentWidget(forms.Widget):
    template_name = 'notifications/custom_template_content_widget.html'

    def get_context(self, name, value, attrs=None, renderer=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs, renderer=renderer)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)