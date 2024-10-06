from moviepy.video.io.VideoFileClip import VideoFileClip
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Video
from .name import file_hash
from .serializers import VideoSerializer


class VideoView(viewsets.ViewSet):
    """
    Video view to list and create videos.
    """
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
        video_file = request.FILES.get('file', None)
        if video_file:
            video_hash = file_hash(video_file)
            existing_video = Video.objects.filter(file_hash=video_hash).first()
            if existing_video:
                data = {
                    'title': request.data.get('title'),
                    'description': request.data.get('description'),
                    'video_file': existing_video.video_file,
                    'duration': existing_video.duration,
                    'file_hash': video_hash,
                    'user': request.user.id
                }
                serializer = VideoSerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    video = serializer.save()
                    response_data = VideoSerializer(video).data
                    return Response({'message': 'New entry created using existing video.', 'video': response_data},
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    with VideoFileClip(video_file.temporary_file_path()) as clip:
                        duration = clip.duration
                except Exception as e:
                    print(f"Error processing video file: {e}")
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            data = {
                'title': request.data.get('title'),
                'description': request.data.get('description'),
                'video_file': request.FILES.get('file'),
                'duration': duration,
                'file_hash': video_hash,
                'user': request.user.id
            }

            serializer = VideoSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                video = serializer.save()
                response_data = VideoSerializer(video).data
                return Response({'video': response_data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
