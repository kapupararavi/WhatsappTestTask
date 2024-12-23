"""
Admin site registration for the all models of this app.
"""
# pylint: disable=missing-class-docstring, unused-argument


from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import APIToken, WhatsappMessage, TestWhatsappMessage, ReceivedWhatsappMessage, WhatsappUser


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_id', 'created_date')

    def has_add_permission(self, *args, **kwds):
        return False

    def has_change_permission(self, *args, **kwds):
        return False


@admin.register(WhatsappMessage)
class WhatsappMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_date')
    list_select_related = ('sender', )


@admin.register(TestWhatsappMessage)
class TestWhatsappMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_date')
    list_select_related = ('sender', )


@admin.register(ReceivedWhatsappMessage)
class ReceivedWhatsappMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message_type', 'sent_time')


@admin.register(WhatsappUser)
class WhatsappUserAdmin(admin.ModelAdmin):
    list_display = ('wa_id', 'name')
