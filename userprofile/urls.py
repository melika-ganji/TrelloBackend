from django.urls import path

from userprofile.views import ProfileAPIView, getuserid, UserCreateAPIView

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='user-info'),
    path('get/<str:username>/', getuserid, name='user-id'),
    path('create/', UserCreateAPIView.as_view(), name='user-create')
]
