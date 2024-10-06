from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Video
from .serializers import VideoSerializer

class VideoSearchView(APIView):
    # permission_classes = [IsAuthenticated]  # Uncomment when implementing authentication

    def get(self, request):
        selected_category_ids = request.GET.getlist('categories')
        selected_difficulty = request.GET.get('difficulty')
        sort_by = request.GET.get('sort_by')

        # Start with all videos
        videos = Video.objects.all()

        # Apply difficulty filter
        if selected_difficulty == 'easy':
            videos = videos.filter(duration__lte=60)  # Gets Videos less than or equal to 60 sec
        elif selected_difficulty == 'medium':
            videos = videos.filter(duration__gt=60, duration__lt=120)  # Gets Videos between 60 and 120 seconds
        elif selected_difficulty == 'hard':
            videos = videos.filter(duration__gte=120)  # Gets Videos greater than or equal to 2 mins

        # Now apply category filtering
        if selected_category_ids:
            query = Q()
            for category_id in selected_category_ids:
                # This assumes the categories are linked via a ManyToMany relationship or similar
                query |= Q(title__icontains=category_id) | Q(description__icontains=category_id)

            # Filter videos by category after filtering by difficulty
            videos = videos.filter(query).distinct()

        # Sort by most recent if specified
        if sort_by == 'mostRecent':
            videos = videos.order_by('-created_at')

        # Prepare video data to send in response
        video_data = [VideoSerializer(video).data for video in videos]
        return Response(video_data)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return the created video data
        return Response(serializer.errors, status=400)
