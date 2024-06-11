from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from .models import Movie, Rating

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

    @action(detail=True, methods=["POST"])
    def rate_movie(self, request, pk=None):
        if "stars" not in request.data:
            return Response(
                {"message": "You need to provide stars"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie = Movie.objects.get(id=pk)
        stars = request.data["stars"]
        user = request.user

        if isinstance(user, User):
            try:
                rating = Rating.objects.get(user=user, movie=movie)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                return Response(
                    {"message": "Rating updated", "result": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except Rating.DoesNotExist:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                return Response(
                    {"message": "Rating created", "result": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {"message": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
