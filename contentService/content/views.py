import io, requests, pathlib
import pandas as pd
from django.forms import models
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets, status
from datetime import date

from .producer import publish

from .Serializer import ContentPartialSerializer, ContentSerializer
from .models import Content

class contentServiceViewSet(viewsets.ViewSet):

    renderer_classes = [JSONRenderer]

    def list(self, request):
        content = Content.objects.all()
        serializer = ContentPartialSerializer(content, many=True)
        return Response(serializer.data)

   
    def create(self, request):
        
        serializer = ContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ContentPartialSerializer(serializer.data).data, status=status.HTTP_201_CREATED)

    #Reads the content from the .csv file and uploads the content to db
    def fileupload(self, request):
        
        files = request.FILES
        if len(files) > 0:
            for file in files:
                if (pathlib.Path(files[file]).suffix != '.csv'):
                    return Response({"Error":"Only csv files are supported"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    df = pd.read_csv(io.StringIO(files[file].read().decode('utf-8')), delimiter=',')
                    Content.objects.bulk_create(
                        Content(**vals) for vals in df.to_dict('records')
                    )
                except:
                    return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"There is no file in the request"}, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        
        try:
            content = Content.objects.get(title=pk)
            serializer = ContentPartialSerializer(content)
            return Response(serializer.data)
        except Content.DoesNotExist:
            return Response({"error":"The requested resource does not exist"}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None):
        print(pk)
        try:
            content = Content.objects.get(title=pk)
            if 'title' in request.data.keys():
                return Response({"error":"Cannot change the title"}, status=status.HTTP_400_BAD_REQUEST)
            title = content.title
            story = request.data['story'] 
            serializer = ContentSerializer(instance=content, data={"title":title, "story":story, "date_published":content.date_published,
                                             "user_id":content.user_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(ContentPartialSerializer(serializer.data).data, status=status.HTTP_202_ACCEPTED)
        except Content.DoesNotExist:
            return Response({"error":"The requested resource does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def deleteContent(self, request, pk=None):
        content = Content.objects.get(title=pk)
        content.delete()
        publish('delete_content', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    #calls the userInteraction API to get the popular content
    def getPopularContent(self, request):
        response = requests.get("http://docker.for.mac.localhost:9000/api/interactions")

        if len(response.json()) == 0: #If no read/likes available simply return content from the db
            return self.list(request)
        elif response.status_code == 200:
            # Performing a join b/w interaction table and content table
            popularityDF = pd.DataFrame.from_dict(response.json())
            contentDF = pd.DataFrame.from_records(Content.objsects.all().values())
            popularContent = (contentDF.merge(popularityDF, on='title',how='inner')
                            ).sort_values(by=['title'],ascending=True).iloc[:, :2]
            return Response(popularContent.to_dict(orient='records'))
        else:
            return Response({"error":response.status_code})

        
    
    #returns sorted content by the date_published value
    def getLatestContent(self, request):
        contents = Content.objects.order_by('-date_published')
        serializer = ContentPartialSerializer(contents, many=True)
        return Response(serializer.data)
        




    