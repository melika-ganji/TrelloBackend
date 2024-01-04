from django.urls import path

from userprofile.views import ProfileAPIView, getuserid

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='user-info'),
    path('get/<str:username>/', getuserid, name='user-id'),
]
