from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Video


def filtered_video_list_view(request):
    selected_category_ids = request.GET.getlist('categories') #neznam kak ke se prate voa categories misleh pa turih deka ke e query moze i da e lista

    if selected_category_ids:
        query = Q()
        for category_id in selected_category_ids:
            query |= Q(title__icontains=category_id) | Q(description__icontains=category_id)

        videos = Video.objects.filter(query).distinct()
    else:
        videos = Video.objects.all()

    # ova sho ke se prate od video data
    video_data = [{
        'title': video.title,
        'description': video.description,
        'view_count': video.view_count,
        'like_count': video.like_count,
        'duration': video.duration,
        'created_at': video.created_at,
        'updated_at': video.updated_at,
    } for video in videos]

    return JsonResponse(video_data, safe=False)
