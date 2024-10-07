from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


def generic_like(request, model, pk):
    """
    Generic like function to like/unlike a model instance.
    :param request: The request object.
    :param model: The model class.
    :param pk: The primary key of the model instance.
    :return: Response object.
    """
    queryset = model.objects.all()
    instance = get_object_or_404(queryset, pk=pk)

    user = request.user

    if user in instance.liked_by.all():
        instance.liked_by.remove(user)
        instance.like_count -= 1
        message = 'Unlike'
    else:
        instance.liked_by.add(user)
        instance.like_count += 1
        message = 'Like'

    instance.save()

    return Response({
        'message': message,
        'like_count': instance.like_count
    }, status=status.HTTP_200_OK)
