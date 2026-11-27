from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import BlogAuthor, BlogTag


class BlogTagPermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        if obj.is_fundraiser:
            return False
        return super().user_can_delete_obj(user, obj)


class BlogTagAdmin(ModelAdmin):
    model = BlogTag
    menu_label = "Oznake objav"
    menu_order = 200
    add_to_settings_menu = False
    form_fields_exclude = ("is_fundraiser",)
    permission_helper_class = BlogTagPermissionHelper


class BlogAuthorAdmin(ModelAdmin):
    model = BlogAuthor
    menu_label = "Avtorji objav"
    menu_order = 201
    add_to_settings_menu = False


class BlogAdminGroup(ModelAdminGroup):
    menu_label = "Objave"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (BlogTagAdmin, BlogAuthorAdmin)


modeladmin_register(BlogAdminGroup)
