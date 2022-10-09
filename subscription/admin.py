from django.contrib import admin
from subscription.models import Subscription, SubscriptionType


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'type', 'created_at')


class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'term', 'price',)


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)


