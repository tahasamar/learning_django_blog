from django.contrib import admin
from .models import Post, PostHashtag


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',) }
    list_display = ('title','slug','updated_at')

class PostHashtagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',) }


admin.site.register(Post, PostAdmin)
admin.site.register(PostHashtag, PostHashtagAdmin)