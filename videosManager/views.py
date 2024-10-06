from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Video
from .serializers import VideoSerializer

class VideoSearchView(APIView): #Used gpt to convert function into class making it cleaner
    # permission_classes = [IsAuthenticated]  # Uncomment when implementing authentication

    def get(self, request):
        # Retrieve category IDs from query parameters
        selected_category_ids = request.GET.getlist('categories')

        if selected_category_ids:
            query = Q()
            for category_id in selected_category_ids:
                query |= Q(title__icontains=category_id) | Q(description__icontains=category_id)

            videos = Video.objects.filter(query).distinct()
        else:
            videos = Video.objects.all()

        # Prepare video data to send in response
        video_data = [VideoSerializer(video).data for video in videos]
        return Response(video_data)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return the created video data
        return Response(serializer.errors, status=400)

