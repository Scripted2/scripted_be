from moviepy.video.io.VideoFileClip import VideoFileClip
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action

from scripted_be.utils import generic_like
from .models import Video
from .name import file_hash
from .serializers import VideoSerializer


class VideoView(viewsets.ViewSet):
    """
    Video view to list and create videos.
    """

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

        video_data = [VideoSerializer(video, context={'request': request}).data for video in videos]
        return Response(video_data)

    def retrieve(self, request, pk=None):
        queryset = Video.objects.all()
        video = get_object_or_404(queryset, pk=pk)
        video.view_count += 1
        video.save()
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        video_file = request.FILES.get('file', None)
        if not video_file:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        video_hash = file_hash(video_file)
        existing_video = Video.objects.filter(file_hash=video_hash).first()

        if existing_video:
            video_file = existing_video.video_file
            duration = existing_video.duration
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
            'video_file': video_file,
            'duration': duration,
            'file_hash': video_hash,
            'user': request.user.id
        }

        serializer = VideoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            video = serializer.save()
            response_data = VideoSerializer(video).data
            message = 'New entry created using existing video.' if existing_video else 'New video uploaded.'
            return Response({'message': message, 'video': response_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, pk=None):
        queryset = Video.objects.all()
        video = get_object_or_404(queryset, pk=pk)

        if video.user != request.user:
            return Response({'error': 'You do not have permission to delete this video'},
                            status=status.HTTP_403_FORBIDDEN)
        video.delete()
        return Response({'message': 'Video deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], url_path='like')
    def like(self, request, pk=None):
        return generic_like(request, Video, pk)
