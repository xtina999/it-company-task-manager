from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import(
    Position,
    TaskType,
    Task,
    Worker
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "task_type", "deadline", "priority", "is_completed"]
    list_filter = ["is_completed", "priority", "task_type"]
    search_fields = ["name"]


@admin.register(Worker)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    list_filter = UserAdmin.list_filter + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "position",)}),)
    search_fields = ["position"]
