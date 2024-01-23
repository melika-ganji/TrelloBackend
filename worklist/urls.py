from django.urls import path
from worklist.views import (BoardAPIView, BoardDetailAPIView, BoardCreateAPIView, ListCreateAPIView, getBoardId,
                            CardCreateAPIView, getListId, CommentAPIView, CommentCreateAPIView)


urlpatterns = [
    path('board/detail/', BoardDetailAPIView.as_view(), name='board-detail'),
    path('create/board/', BoardCreateAPIView.as_view(), name='create-board'),
    path('board/', BoardAPIView.as_view(), name='show-board'),
    path('create/list/', ListCreateAPIView.as_view(), name='create-list'),
    path('get/board/<str:name>/', getBoardId, name='board-id'),
    path('create/card/', CardCreateAPIView.as_view(), name='create-card'),
    path('get/list/<str:name>/', getListId, name='list-id'),
    path('comment/<int:id>/', CommentAPIView.as_view(), name='comment-show'),
    path('comment/', CommentCreateAPIView.as_view(), name='comment-create'),
]
