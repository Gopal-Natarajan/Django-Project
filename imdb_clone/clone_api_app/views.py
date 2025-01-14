from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from .models import WatchList, StreamingPlatform, Review
from .serializers import WatchListSerializers, StreamingPlatformSerializer, ReviewSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from .permissions import AdminOrReadOnly,ReviewUserOrReadOnly
# from django_filters.rest_framework import DjangoFilterBackend
from .pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle




class StreamPlatformView(APIView):
    
    def get(self, request):
        plateforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(plateforms, many = True)
        permission_classes = [IsAuthenticated]
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamingPlatformSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamplatformDetails(APIView):
    
    def get(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serializer = StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""# function based view
@api_view(['GET', 'POST'])
def movielist(request):
    
    if request.method == 'GET':
        movies = WatchList.objects.all() 
        serializers = WatchListSerializers(movies, many = True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        serializers = WatchListSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.error)
    

@api_view(['GET','PUT', 'DELETE'])
def movie_details(request, pk):
    
    try: 
        movie = WatchList.objects.get(pk=pk)
    except WatchList.DoesNotExist:
        return Response({'ERROR' : 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == "GET":
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializers(movie)
        return Response(serializers.data)
    
    if request.method == 'PUT':
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializers(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else: 
            return Response(serializers.error)
    
    if request.method == 'DELETE':
        movie = WatchList.objects.get(pk=pk)
        movie.delete()   
        return Response(status=status.HTTP_204_NO_CONTENT)  

"""

#generic based

class WatchListView(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['tittle','active']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['tittle', 'platform__streamplatform']
    
    


#class based view
# class WatchListView(APIView):
    
#     def get(self, request):
#         movie = WatchList.objects.all()
#         serializers = WatchListSerializers(movie, many=True)
#         return Response(serializers.data)
    
#     def post(self, request):
#         serializers = WatchListSerializers(data= request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
        
class Movie_details(APIView):
    
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializers(movie)
        return Response(serializers.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializers(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewView(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [AdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist = pk)
    
class ReviewCreateView(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [AdminOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError('You are already reviewed this movie!')
        
        if WatchList.no_of_rating == 0:
            WatchList.avg_rating = serializer.validated_data['rating']
        else:
            WatchList.avg_rating = (WatchList.avg_rating + serializer.validated_data['rating'])/2
        
        WatchList.no_of_rating = WatchList.no_of_rating + 1
        
        WatchList.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)
    


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [ReviewUserOrReadOnly]


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)
