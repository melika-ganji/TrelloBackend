from django.contrib import admin
from django.contrib.admin import register
from worklist.models import List, Board, Card, Comment


class ListInline(admin.TabularInline):
    model = List
    extra = 1


class CardInline(admin.TabularInline):
    model = Card
    extra = 1


@register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    inlines = [ListInline]


@register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'board']
    inlines = [CardInline]


@register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'deadline', 'is_finished',
                    'list', 'tag', 'description']


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["card", "text"]
