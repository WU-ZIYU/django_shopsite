from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
User = get_user_model()
# Create your views here.


# 序列化
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')


class User_apiview(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-last_login')
    serializer_class = UserSerializer
    filter_fields = ('id', 'name',)

    @action(detail = True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


