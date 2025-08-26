from django.urls import path
from . import views



urlpatterns = [
    path('',views.index),
    path('about/',views.about,name='about'),
    path('sregister/',views.Sregister),
     path('login/',views.loginall,name="login"),
     path('homepage/',views.homepage,name='homepage'),
     path('logout/',views.logoutall),
     path('tregister/',views.Tregister),
     path("instructors/", views.view_instructors, name="view_instructors"),
    path("students/", views.view_students, name="view_students"),
     path('activate/<int:id>/',views.activate,name='active'),
    path('deactivate/<int:id>/',views.deactivate,name='deactive'),
     path('forgotPassword',views.forgotPassword),
    path('resetPassword',views.resetPassword,name='resetPassword'),
    path('editProfile',views.editProfile),
    path('changeUsername',views.changeUsername),
    path('changeImage',views.changeProfile)
]