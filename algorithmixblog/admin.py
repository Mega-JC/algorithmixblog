from django.contrib import admin
from django import forms

from .models import (
    User,
    BlogPost,
    BlogPostTag,
    BlogPostComment,
    
    )

class UserAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(UserAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "bio":
            attrs_dict = formfield.widget.attrs
            attrs_dict.update({"minlength": 1, "maxlength": 1024})
            formfield.widget = forms.Textarea(attrs=attrs_dict)
        return formfield

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "author", "title", "text")
    raw_id_fields = ("likers",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BlogPostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ("description", "text"):
            attrs_dict = formfield.widget.attrs
            attrs_dict.update({"minlength": 1, "maxlength": 40960})
            formfield.widget = forms.Textarea(attrs=attrs_dict)
        return formfield


class BlogPostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "author", "text")
    raw_id_fields = ("likers",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BlogPostCommentAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "text":
            attrs_dict = formfield.widget.attrs
            attrs_dict.update({"minlength": 1, "maxlength": 4096})
            formfield.widget = forms.Textarea(attrs=attrs_dict)
        return formfield

admin.site.register(User, UserAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPostTag)
admin.site.register(BlogPostComment, BlogPostCommentAdmin)



