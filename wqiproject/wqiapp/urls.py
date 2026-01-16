from django.contrib import admin
from django.urls import path
from wqiapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.chemistry,name='chemistry'),
    path('chemistry',views.chemistry,name='chemistry'),
    path('signin',views.signin,name='signin'),
    path('main',views.main,name='main'),
    path('logoutUser',views.logoutUser,name='logoutUser'),
    path('signup',views.signup,name='signup'),
    path("display", views.display_data, name="display_data"),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('about',views.about,name='about'),
]
