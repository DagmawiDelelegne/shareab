from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name=''),  
    path('register', views.register, name='register'),
    path('login', views.my_login, name='login'),
    path('logout', views.my_logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_book', views.add_book, name='add_book'),
    path('search_books', views.search_books, name='search_books'), 
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'), 
    path('profile/', views.Profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
