from django.contrib import admin
from .models import ArduinoData

class ArduinoDataAdmin(admin.ModelAdmin):
    list_display = ('tag_uid', 'servo_state', 'food_level', 'timestamp')
    list_filter = ('servo_state', 'timestamp')
    search_fields = ('tag_uid',)
    readonly_fields = ('timestamp',)

admin.site.register(ArduinoData, ArduinoDataAdmin)
