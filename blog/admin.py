from django.contrib import admin

from .models import Post, Author, Tag, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date",)
    list_display = ("title", "date", "author",)
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "created_at")
    list_filter = ("post", "user")
    search_fields = ("user__username", "text")
    
    def post_date(self, obj):
        return obj.post.date
    post_date.short_description = "Post Date"

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)