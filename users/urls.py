from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView   
from .api_users_docs import original_register_user, CustomTokenObtainPairView


urlpatterns = [
    path('register/', original_register_user, name='register_user'), 
    path('login/',  CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]

