from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CreateBranchAdmin,BranchAdminLogin
urlpatterns = [
   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.Register.as_view(),name='register'),
    path('create-branch-admin/', CreateBranchAdmin.as_view(), name='create-branch-admin'),
    path('branch-admin-login/', BranchAdminLogin.as_view(), name='branch-admin-login'),


]