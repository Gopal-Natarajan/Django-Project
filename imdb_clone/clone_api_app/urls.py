from django.urls import path,include
from . import views

urlpatterns = [
    path('stream/', views.StreamPlatformView.as_view(), name='platforms-list'),
    path('stream/<int:pk>', views.StreamplatformDetails.as_view(), name='platforms-details'),
    # path('movies/', views.movielist, name='list_of_movies'),
    # path('movies/<int:pk>', views.movie_details, name='movie_details'),
    path("movie/", views.WatchListView.as_view(), name='movie-list'),
    path('movie/<int:pk>', views.Movie_details.as_view(), name='movie'),
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name='Movie-Review-details'),
    path('<int:pk>/review/', views.ReviewView.as_view(), name='Movie-Review'),
    path('review/', views.UserReview.as_view(), name='user-Reviews'),
    path('<int:pk>/review-create/', views.ReviewCreateView.as_view(), name='Movie-Create-Review'),
    
]
