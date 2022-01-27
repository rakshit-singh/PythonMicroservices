import pandas as pd
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, serializers, exceptions
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.db.models import F


from .models import LikeEvent, ReadEvent, User
from .Serializer import ReadEventSerializer, LikeEventSerializer, UserSerializer

class LikeServiceViewSet(viewsets.ViewSet):

    def list(self, request):
        likes = LikeEvent.objects.all()
        serializer = LikeEventSerializer(likes, many=True)
        return Response(serializer.data)

    # Stores the like event if the user performing the event exists
    def update(self, request):
        user_id = request.data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":"user with given id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = LikeEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ReadServiceViewSet(viewsets.ViewSet):

    def list(self, request):
        reads = ReadEvent.objects.all()
        serializer = ReadEventSerializer(reads, many=True)
        return Response(serializer.data)

    # Stores the read event is the user performing the event exists
    def update(self, request, title=None):
        user_id = int(request.data['user_id'])

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":"user with given id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            
            readEvent = ReadEvent.objects.filter(user_id=user_id).filter(title=request.data['title'])
            
            # If the user has not read any book before, add a new entry else update existing entry
            if len(readEvent) == 0:
                serializer = ReadEventSerializer(data={"user_id":user_id, "title":request.data['title'], "countReads":1})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                print("Here")
                readEvent = (ReadEvent.objects.filter(user_id=user_id).filter(title=request.data['title'])
                            ).update(countReads=F('countReads')+1)
                
            return Response(status=status.HTTP_202_ACCEPTED)

# Contains the methods POST & DELETE requests fro user
class UserView(viewsets.ViewSet):

    def createUser(self, request):
        print("creating user")
        userSerializer  = UserSerializer(data={"id":request.data['user_id']})
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def deleteUser(self, request, user_id=None):
        content = User.objects.get(id=user_id)
        content.delete()
        ReadEvent.objects.filter(user_id=user_id).delete()
        LikeEvent.objects.filter(user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Contains methods related to contents to which the REad & LIke Events correspond to
class ContentView(viewsets.ViewSet):

    def deleteContent(self, request, contentTitle=None):
        ReadEvent.objects.filter(title=contentTitle).delete()
        LikeEvent.objects.filter(title=contentTitle).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# contains get methods for the internal API to be used by the content service
class InternalInteractionViewSet(viewsets.ViewSet):

    #get method that provides the interactions for all the contents
    def getInteractions(self, request):
        #using aggregations to grp by title and get count of likes of a title
        likeInteractions = pd.DataFrame.from_records(LikeEvent.objects
                            .values('title')
                            .annotate(likes=Count('title'))
                            .order_by()
        )
        #using aggregations to grp by title and get count of reads of a title
        readInteractions = pd.DataFrame.from_records(ReadEvent.objects
                            .values('title')
                            .annotate(reads=Sum('countReads'))
                            .order_by()
        )
        
        if likeInteractions.size !=0 and readInteractions.size !=0:
            res = readInteractions.merge(likeInteractions, how='inner', on='title')
            res['interactions'] = res['reads'] + res['likes']
            return Response(res[['title', 'interactions']].to_dict())
        elif likeInteractions.size != 0:
            likeInteractions.columns = ['title', 'interactions']
            return Response(likeInteractions[['title', 'likes']].to_dict())
        elif readInteractions.size != 0:
            readInteractions.columns = ['title', 'interactions']
            return Response(readInteractions[['title', 'likes']].to_dict())
        else:
            return Response([])
        
        

