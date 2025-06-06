from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import BlogAuthor, BlogTag


class BlogTagAdmin(ModelAdmin):
    model = BlogTag
    menu_label = "Oznake objav"
    menu_order = 200
    add_to_settings_menu = False


class BlogAuthorAdmin(ModelAdmin):
    model = BlogAuthor
    menu_label = "Avtorji objav"
    menu_order = 201
    add_to_settings_menu = False


modeladmin_register(BlogTagAdmin)
modeladmin_register(BlogAuthorAdmin)
