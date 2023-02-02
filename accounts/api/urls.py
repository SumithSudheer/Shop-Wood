from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SubjectRetrieveUpdateDestroyView, SubjectCreateView, CreateBranchAdmin,BranchAdminLogin,BranchListCreateView,BranchRetrieveUpdateDestroyView,CourseCreateView,CourseRetrieveUpdateDestroyView,BatchCreateView,BatchRetrieveUpdateDestroyView
urlpatterns = [
   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.Register.as_view(),name='register'),
    path('create-branch-admin/', CreateBranchAdmin.as_view(), name='create-branch-admin'),
    path('branch-admin-login/', BranchAdminLogin.as_view(), name='branch-admin-login'),
    path('create-branch/', BranchListCreateView.as_view(), name='create-branch'),
    path('crud-branch/<int:pk>/', BranchRetrieveUpdateDestroyView.as_view(), name='crud-branch'),
    path('courses/', CourseCreateView.as_view(), name='create-course'),
    path('crud-course/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='crud-course'),
    path('batch/', BatchCreateView.as_view(), name='create-batch'),
    path('crud-batch/<int:pk>/', BatchRetrieveUpdateDestroyView.as_view(), name='crud-batch'),
    path('subject/', SubjectCreateView.as_view(), name='create-subject'),
    path('crud-subject/<int:pk>/', SubjectRetrieveUpdateDestroyView.as_view(), name='crud-subject'),







]