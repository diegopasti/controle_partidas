from django.contrib import admin
from django.core.exceptions import FieldError


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """ Save user than create or update object on admim """

        try:
            obj.updated_by = request.user
            if obj.pk is None:
                obj.created_by = request.user
        except FieldError:
            pass

        super().save_model(request, obj, form, change)
