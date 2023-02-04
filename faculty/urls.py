from django.urls import path
from . import views
urlpatterns = [
        #done
        path('Facultyragister/',views.FacultyRegisterView.as_view(),name='Facultyragister'),
        path('facultylogin/',views.facultylogin.as_view(),name="facultylogin"),
        #done
        path('adminfacultymessagewhatsap/<int:id>/',views.adminfacultyverificationwithWhatsapp.as_view()),
        #forgotpassword
        path('facultyforgotpassword/',views.facultyforgotpassword.as_view(),name="facultylogin"),


        
        
        
]
