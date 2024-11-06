from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('users',views.CRUD,basename='users')
urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='reg'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('changepassword/',views.ChangePasswordView.as_view(),name='changepassword'),
    path('sendmail/',views.SendEmailView.as_view(),name='sendmail'),
    path('reset-password/<uid>/<token>/',views.PasswordResetView.as_view()),
    path('',include(router.urls)),
    # path('list/',views.LIstCreate.as_view()),
    
    # path('delete/<int:pk>/',views.DeleteView.as_view()),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
       

       
    
