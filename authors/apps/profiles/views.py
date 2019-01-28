from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .renderers import ProfilesJSONRenderer
from .serializers import ProfileSerializer


class ProfileListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (ProfilesJSONRenderer,)

    def get(self, request, *args, **kwargs):
        # fetches all profiles except the requester
        queryset = UserProfile.objects.all().exclude(user=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'profiles': serializer.data}, status=status.HTTP_200_OK)


class ProfileItemView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (ProfilesJSONRenderer,)

    def get(self, request, username):
        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except BaseException:
            response = {"error": "User profile does not exist."}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user_profile)
        return Response({
            'profile': serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, username):
        """
        This method allows users to update their own profiles
        A user is forbidden from updating other user's profiles
        """
        if request.user.username != username:
            response = {
                "message": "You don't have permission to edit this profile"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(instance=request.user.profile,
                                           data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
