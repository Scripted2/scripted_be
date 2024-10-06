from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.viewsets import ViewSet

from .models import Video
from .serializers import VideoSerializer

class VideoSearchView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        selected_category_ids = request.GET.getlist('categories')
        selected_difficulty = request.GET.get('difficulty')
        sort_by = request.GET.get('sort_by')

        videos = Video.objects.all()

        if selected_difficulty == 'easy':
            videos = videos.filter(duration__lte=60)
        elif selected_difficulty == 'medium':
            videos = videos.filter(duration__gt=60, duration__lt=120)
        elif selected_difficulty == 'hard':
            videos = videos.filter(duration__gte=120)


        if selected_category_ids:
            query = Q()
            for category_id in selected_category_ids:

                query |= Q(title__icontains=category_id) | Q(description__icontains=category_id)


            videos = videos.filter(query).distinct()


        if sort_by == 'mostRecent':
            videos = videos.order_by('-created_at')


        video_data = [VideoSerializer(video).data for video in videos]
        return Response(video_data)

    def create(self, request):
        serializer = VideoSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            video = serializer.save(user=request.user)  # Save the video instance

            # Prepare user information as a dictionary
            user_info = {
                'id': request.user.id,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
                'email': request.user.email,
            }

            # Combine video and user info in the response
            response_data = VideoSerializer(video).data  # Serialize the video instance
            response_data['user'] = user_info  # Include user info in the video dict

            return Response({
                'video': response_data  # Return video and user information together
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)