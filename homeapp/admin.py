from django.contrib import admin
from homeapp.models import Tables, Item, ItemList
# Register your models here.
admin.site.register(Tables)
admin.site.register(ItemList)
admin.site.register(Item)