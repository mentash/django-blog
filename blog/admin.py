from django.contrib import admin
from .models import Post, Comment



# Register your models with the Django admin site here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    raw_id_fields = ['post'] # Use raw_id_fields for foreign key relations to avoid performance issues
    date_hierarchy = 'created' # Use date_hierarchy for better navigation in the admin interface
    ordering = ['active', 'created'] # Order by active status and creation date
    show_facets = admin.ShowFacets.ALWAYS # Always show facets for better filtering options