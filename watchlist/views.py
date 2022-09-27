# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Movie
# # Create your views here.

# def movies_list(request):
#     movie_list = Movie.objects.all().values()
#     data = {
#         'movies': list(movie_list),
#     }
    
#     return JsonResponse(data)
    
# def movie_detail(request, pk):
#     movie_obj = Movie.objects.get(id=pk)
#     data = {
#         'title': movie_obj.title,
#         'summary': movie_obj.summary,
#         'is_published': movie_obj.is_published
#     }
    
#     return JsonResponse(data)
    
    
"""function based API views"""
# @api_view(['GET', 'POST'])
# def movies_list(request):
    
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     elif request.method == "POST":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     try:
#         movie = Movie.objects.get(id=pk)
#     except Movie.DoesNotExist:
#         msg = 'Error, movie not found'
#         return Response(msg, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""class based API Views"""

"""normal class based """
# class ReviewListView(APIView):
    
#     def get(self, request):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""generic views"""
# class ReviewListView(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs) 
    
# class ReviewDetailView(mixins.RetrieveModelMixin,
#                        mixins.UpdateModelMixin,
#                        mixins.DestroyModelMixin,
#                        generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer  
       
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)