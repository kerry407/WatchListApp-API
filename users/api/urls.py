from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    


urlpatterns = [
    path("account/login/", obtain_auth_token, name="login"), 
    path("create-account/", views.create_account, name="create-account"),
    path("account/logout/", views.logout_view),
    
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    
]
