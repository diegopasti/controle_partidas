from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.entities.models import Company, Area, Group


@admin.register(Company)
class CompanyAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['name']
    list_filter = ["city", "state"]
    list_display = ["name", "address", "city", "state"]


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['owner']
    list_filter = ["owner", "status", "type", "days"]
    list_display = ["owner", "status", "type", "days"]


@admin.register(Area)
class AreaAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['owner']
    list_filter = ["company", "status", "type"]
    list_display = ["area", "local", "value"]

    def area(self, obj):
        return self.double_row(
            f"{obj.name.upper()}", f"{obj.players*2} PESSOAS", "left"
        )

    def local(self, obj):
        return self.double_row(
            f"{obj.company.name.upper()}", f"{obj.company.city.upper()} - {obj.company.state.upper()}", "left"
        )

    def value(self, obj):
        return self.double_row(
            f"{obj.price}", f"POR HORA", "center"
        )

    area.allow_tags = True
    area.short_description = "QUADRA / CAMPO"
    area.admin_order_field = ''

    local.allow_tags = True
    local.short_description = "LOCAL"
    local.admin_order_field = 'company__city'

    value.allow_tags = True
    value.short_description = "VALOR"
    value.admin_order_field = 'price'
