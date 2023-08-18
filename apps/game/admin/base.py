from apps.core.admin import BaseModelAdmin


class ResultAdmin(BaseModelAdmin):

    def victories_result(self, obj):
        return self.double_row(f"{obj.victories}", f"{obj.victories_rate}%")

    def losses_result(self, obj):
        return self.double_row(f"{obj.losses}", f"{obj.losses_rate}%")

    def empaths_result(self, obj):
        return self.double_row(f"{obj.empaths}", f"{obj.empaths_rate}%")

    victories_result.allow_tags = True
    victories_result.short_description = "Vitórias"
    victories_result.admin_order_field = 'victories'

    empaths_result.allow_tags = True
    empaths_result.short_description = "Empates"
    empaths_result.admin_order_field = 'empaths'

    losses_result.allow_tags = True
    losses_result.short_description = "Derrotas"
    losses_result.admin_order_field = 'losses'