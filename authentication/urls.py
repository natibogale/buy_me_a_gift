from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView, SigninView

urlpatterns = [

    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
