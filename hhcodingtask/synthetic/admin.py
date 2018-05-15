from django import forms
from django.contrib import admin
from .models import GenericModel, AnyData


class GenericChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, kind in AnyData().fields.items():
            self.fields[field] = forms.CharField()
        # TODO: add date type, populate with instance's data
        if self.instance.pk:
            pass

    def clean(self):
        try:
            data_obj = AnyData(raw_data=self.cleaned_data)
            data_obj.validate()
        except (ModelValidationError, ModelConversionError) as exc:
            result = {}
            for field, messages in exc.messages.items():
               raise forms.ValidationError(str(exc.messages[field].to_primitive()))
        return self.cleaned_data

    class Meta:
        model = GenericModel
        #fields = "__all__"
        exclude = ['any_data']


@admin.register(GenericModel)
class GenericModelAdmin(admin.ModelAdmin):
    form = GenericChangeForm

    # TODO: define get_list_display, make fieldsets dynamic, etc
