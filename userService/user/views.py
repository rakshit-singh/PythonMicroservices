from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import Http404

from .producer import publish
from .Serializer import UserSerializer
from .models import User

class UserServiceViewSet(viewsets.ViewSet):

    def list(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('create_user', str(serializer.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        try :
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error":"user with given id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(UserSerializer(user).data)
        

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def deleteUser(self, request, pk=None):
        try:
            content = User.objects.get(id=pk)
            content.delete()
        except User.DoesNotExist:
            return Response({"error":"user with given id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        publish("delete_user", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)




    