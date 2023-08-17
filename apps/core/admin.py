from django.contrib import admin
from django.core.exceptions import FieldError
from django.db import models
from django.forms import TextInput, Select, SelectMultiple, DateInput, DateTimeInput
from django.utils.html import format_html

from django_admin_filters import MultiChoice


class StatusFilter(MultiChoice):
    FILTER_LABEL = "By status"


class BaseModelAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': ('core/css/admin.css',)
        }
        js = ['core/js/admin.js']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.IntegerField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.DecimalField: {'widget': TextInput(attrs={"style": "width:100vh"})},
        #models.DateTimeField: {'widget': DateTimeInput(attrs={"style": "width:100vh"})},
        #models.DateField: {'widget': DateInput(attrs={"style": "width:100vh"})},
        #models.DurationField: {'widget': TextInput(attrs={"style": "width:100vh"})},
        models.ForeignKey: {'widget': Select(attrs={"style": "min-width:100vh"})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={"style": "min-width:100vh"})},
    }

    def save_model(self, request, obj, form, change):
        """ Save user than create or update object on admim """

        try:
            obj.updated_by = request.user
            if obj.pk is None:
                obj.created_by = request.user
        except FieldError:
            pass

        super().save_model(request, obj, form, change)

    def created(self, obj):
        return self.double_row(
            f"{obj.creation_date.strftime('%d/%m/%Y às %H:%M:%S')}", f"POR {obj.created_by.username.upper()}"
        )

    def updated(self, obj):
        return self.double_row(
            f"{obj.last_update.strftime('%d/%m/%Y às %H:%M:%S')}", f"POR {obj.updated_by.username.upper()}"
        )

    def column_separator(self, obj):
        message = format_html("<div style='width:0px;'></div>")
        return message

    def double_row(self, first_value, second_value, align="center"):
        message = format_html(
            f"<div style='text-align:{align};white-space: nowrap;'>"
            f"{first_value}<br><span style='font-size:9px;color:#777;'>"
            f"{second_value}</span>"
            f"</div>"
        )
        return message

    column_separator.allow_tags = False
    column_separator.short_description = " "

    created.allow_tags = True
    created.short_description = "Cadastrado em"
    created.admin_order_field = 'creation_date'

    updated.allow_tags = True
    updated.short_description = "Atualizado em"
    updated.admin_order_field = 'last_updated'

