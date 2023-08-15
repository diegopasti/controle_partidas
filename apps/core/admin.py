from django.contrib import admin
from django.core.exceptions import FieldError
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

    def save_model(self, request, obj, form, change):
        """ Save user than create or update object on admim """

        try:
            obj.updated_by = request.user
            if obj.pk is None:
                obj.created_by = request.user
        except FieldError:
            pass

        super().save_model(request, obj, form, change)

    def column_separator(self, obj):
        message = format_html("<div style='width:0px;'></div>")
        return message

    def double_row(self, first_value, second_value):
        message = format_html(
            f"<div style='text-align:center;white-space: nowrap;'>"
            f"{first_value}<br><span style='font-size:9px;color:#777;'>"
            f"{second_value}</span>"
            f"</div>"
        )
        return message

    column_separator.allow_tags = False
    column_separator.short_description = " "

