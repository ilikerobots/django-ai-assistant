from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_ai_assistant.models import Thread, Message


class MessageProxy(Message):
    class Meta:
        proxy = True
        verbose_name = Message._meta.verbose_name
        verbose_name_plural = Message._meta.verbose_name_plural

    def __str__(self) -> str:
        return self.__repr__()


class MessageInline(admin.TabularInline):
    model = MessageProxy
    extra = 0
    fields = ("pk", "type", "content", "created_at")
    readonly_fields = fields
    ordering = ('created_at',)
    show_change_link = True

    def pk(self, obj):
        display_text = "<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(Message._meta.app_label, Message._meta.model_name), args=(obj.pk,)),
            obj.pk)
        if display_text:
            return mark_safe(display_text)
        return "-"

    def type(self, obj):
        return obj.message.get('type') if obj.message else None

    def content(self, obj):
        return obj.message.get('data', {}).get('content') if obj.message else None

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "created_by", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("created_by",)
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "created_at")
    search_fields = ("thread__name", "message")
    list_filter = ("created_at",)
    raw_id_fields = ("thread",)
