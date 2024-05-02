from django.contrib import admin
from .models import ItemTemplate, Shop, Player, PlayerItem, ShopItem, Vendor, StatSheet

# Register your models here.


class ShopItemInline(admin.TabularInline):
    model = ShopItem
    extra = 1  # Number of extra forms to display

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'currency')
    inlines = [ShopItemInline]

class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'itemType')
    list_filter = ('itemType',)
    search_fields = ('name',)

class PlayerItemInline(admin.TabularInline):
    model = PlayerItem
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'display_inventory')
    inlines = [PlayerItemInline]

    def display_inventory(self, obj):
        return ", ".join([item.item_template.name for item in obj.inventory.all()])
    display_inventory.short_description = 'Inventory'

class StatSheetAdmin(admin.ModelAdmin):
    # Assuming 'stat' is a complex field that needs processing
    list_display = ('display_stat',)

    def display_stat(self, obj):
        # Custom display function that handles the complex field
        return ", ".join([stat.name for stat in obj.some_related_field.all()])
    display_stat.short_description = 'Stat'

# Register each model with the admin site.
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Player, PlayerAdmin)  # Register Player using the custom admin class
admin.site.register(PlayerItem)
admin.site.register(ShopItem)
admin.site.register(Vendor)
admin.site.register(StatSheet, StatSheetAdmin)