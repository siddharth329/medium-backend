from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from .serializers import ImageSerializer
# Create your views here.


class ImageUploadThrottle(UserRateThrottle):
    scope = 'sustained'


class ImageUploadStrategy(APIView):
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ImageUploadThrottle] if not settings.DEBUG else []

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            # response = {'success': 1, 'file': {'url': serializer.validated_data.get('image')}}
            # return JsonResponse(response, safe=False)
        else:
            return Response(serializer.errors)
            # response = {'success': 0}
            # return JsonResponse(response, safe=False)


# class ImageUploadByURL(APIView):
#     permission_classes = [IsAuthenticated]
#     throttle_classes = [ImageUploadThrottle] if not settings.DEBUG else []
#
#     def post(self, request):
#         url = request.POST.get('url')
#         if url:

