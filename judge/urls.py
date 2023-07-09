from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'judge'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage,  name='login'),
    path('logout', views.logoutUser, name='logoutUser'),

    path('', views.problems, name='problems'),
    path('problem/<int:problem_id>/', views.problemDetail, name='problemDetail'),
    path('problem/<int:problem_id>/submit', views.submitProblem, name='submit'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]


urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
