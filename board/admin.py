from django.contrib import admin

from board.models import Board


# class BoardAdmin(admin.ModelAdmin):
#     list_display = ('name', 'source', 'is_recipe', 'user', 'group')
#     list_filter = ('source__name', 'is_recipe', 'group')
#     search_fields = ('name', 'user__first_name', 'source__name')
#     ordering = ('-created_at',)
#     list_per_page = 14


# admin.site.register(Board, BoardAdmin)
admin.site.register(Board)
