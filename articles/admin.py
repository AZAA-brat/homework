from django.contrib import admin
from .models import Article, Category, Feedback


admin.site.site_header = "Article magazine"
admin.site.site_title = "Admin panel article magazines website"
admin.site.index_title = "Article management"

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Feedback)
