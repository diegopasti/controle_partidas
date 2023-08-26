from django.contrib import admin
from django_admin_geomap import ModelAdmin

from apps.core.admin import BaseModelAdmin
from apps.entities.models import Company, Area, Group, Location


@admin.register(Company)
class CompanyAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['name']
    list_filter = ["city", "state"]
    list_display = ["name_with_local", "route", "owner_with_phone", "created", "updated"]

    readonly_fields = ["created_by", "updated_by", "creation_date", "last_update"]

    fieldsets = (
        ("Informações Gerais", {
            "fields": (
                "name", "owner", "phone", "address", "city", "state", "location", "geolocation",
            )
        }),

        ("Detalhes", {
            "fields": (
                "created_by", "creation_date", "updated_by", "last_update", "is_active"
            )
        }),
    )

    add_fieldsets = (
        ("Informações Gerais", {
            "fields": ("name", "owner", "phone", "address", "city", "state", "location", "geolocation",)
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
             return self.add_fieldsets
        return super(CompanyAdmin, self).get_fieldsets(request, obj)

    def name_with_local(self, obj):
        return self.double_row(
            f"{obj.name.upper()}", f"{obj.address.upper()}", "left"
        )

    def owner_with_phone(self, obj):
        return self.double_row(
            f"{obj.phone.upper()}", f"{obj.owner.upper()}", "center"
        )

    def city_with_uf(self, obj):
        return self.double_row(
            f"{obj.city.upper()}", f"{obj.state.upper()}", "center"
        )

    def route(self, obj):
        return self.double_row(
            f"LOCALIZAÇÃO", f"CLIQUE AQUI", "center", link=obj.location
        )


    name_with_local.allow_tags = True
    name_with_local.short_description = "Empresa"
    name_with_local.admin_order_field = 'name'

    owner_with_phone.allow_tags = True
    owner_with_phone.short_description = "Responsável"
    owner_with_phone.admin_order_field = 'owner'

    route.allow_tags = True
    route.short_description = "Localização"


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['owner']
    list_filter = ["owner", "status", "type", "days"]
    list_display = ["group_owner", "days", "bookings", "created", "updated"]

    fieldsets = (
        ("Informações Gerais", {
            "fields": (
                "owner", "name", "status", "type", "days", "bookings"
            )
        }),

        ("Detalhes", {
            "fields": (
                "created_by", "creation_date", "updated_by", "last_update", "is_active"
            )
        }),
    )

    add_fieldsets = (
        ("Informações Gerais", {
            "fields": ("owner", "name", "type", "days")
        }),
    )

    readonly_fields = ["created_by", "updated_by", "creation_date", "last_update", "bookings"]

    def group_owner(self, obj):
        return self.double_row(
            f"{obj.name.upper()} ({obj.type})", f"{obj.owner.get_full_name().upper()}", "left"
        )

    group_owner.allow_tags = True
    group_owner.short_description = "GRUPO"
    group_owner.admin_order_field = 'name'


@admin.register(Area)
class AreaAdmin(BaseModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['owner']
    list_filter = ["company","company__city", "status", "type"]
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


@admin.register(Location)
class Admin(ModelAdmin):
    geomap_item_zoom = "8"
    geomap_height = "350px"
    geomap_new_feature_icon = "/myicon.png"
    geomap_show_map_on_list = False



