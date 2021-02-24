from django.contrib import admin

from board.models import Board, Mentioned


admin.site.register(Board)
admin.site.register(Mentioned)
