import re
from tempfile import TemporaryFile
from rest_framework.parsers import JSONParser
from file.models import File
from file.serializers import FileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView  
from file import s3_f
from rest_framework import status
import os
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))
class Files(APIView):
    cursor = connection.cursor()

    # Get File List
    def get(self, request):
        if request.method == 'GET':
            strsql = "SELECT * FROM File;"
            self.cursor.execute(strsql)
            result = self.cursor.fetchall()
            return Response(result)
    
    # Upload File
    def post(self, request):
        if request.method == 'POST':
            UploadUser = 5
            path = request.POST['path']
            Folder = request.POST['Folder']
            file_name = request.POST['file_name']
            IsPublic = request.POST.get('IsPublic', 0)
            Color = request.POST.get('Color', 0)

            # Add to MYSQL DB
            strsql = "INSERT INTO File(UploadUser, Folder, file_name, IsPublic, Color) VALUES({0}, {1}, '{2}', {3}, {4})".format(UploadUser, Folder, file_name, IsPublic, Color)
            self.cursor.execute(strsql)
            result = self.cursor.fetchall()

            # Get File ID From MYSQL DB
            strsql = "SELECT ID FROM File WHERE Folder = {0} and file_name = '{1}';".format(Folder, file_name)
            self.cursor.execute(strsql)
            result = self.cursor.fetchall()

            # upload to S3
            s3_f.upload_file(path, file_name, result[0][0])

            return HttpResponse("Upload Success", content_type='text/plain')


class Files_id(APIView): 
    cursor = connection.cursor()
    
    # Download File
    def get(self, request, file_id):
        if request.method == 'GET':
            strsql = "SELECT file_name FROM File WHERE ID = {0};".format(file_id)
            self.cursor.execute(strsql)
            result = self.cursor.fetchall()
            s3_f.download_file(file_id, result[0][0])
            
        return HttpResponse("Download Success", content_type='text/plain')
    
    # Delete File
    def delete(self, request, file_id):
        if request.method == 'DELETE':

            # Delete from MYSQL DB
            strsql = "DELETE FROM File WHERE ID = {0};".format(file_id)
            self.cursor.execute(strsql)
            self.cursor.fetchall()

            # Delete from S3
            s3_f.delete_file(file_id)

        return HttpResponse("Delete Success", content_type='text/plain')

    # Update File
    def post(self, request, file_id):
        if request.method == 'POST':
            strsql = "SELECT * FROM File WHERE ID = {0};".format(file_id)
            self.cursor.execute(strsql)
            result = self.cursor.fetchall()

            Folder = request.POST.get('Folder', result[0][2])
            file_name = request.POST.get('file_name', result[0][3])
            IsPublic = request.POST.get('IsPublic', result[0][4])
            Color = request.POST.get('Color', result[0][5])

            strsql = "UPDATE File SET Folder = {0}, file_name = '{1}', IsPublic = {2}, Color = {3} WHERE ID = {4};".format(Folder, file_name, IsPublic, Color, file_id)
            self.cursor.execute(strsql)
            self.cursor.fetchall()
            
            return HttpResponse("Update Success", content_type='text/plain')
            
    # # Update File
    # def put(self, request, file_id):
    #     if request.method == 'PUT':
    #         strsql = "SELECT * FROM File WHERE ID = {0};".format(file_id)
    #         self.cursor.execute(strsql)
    #         result = self.cursor.fetchall()

    #         Folder = request.PUT.get['Folder', result[0][2]]
    #         file_name = request.PUT.get['file_name', result[0][3]]
    #         IsPublic = request.PUT.get('IsPublic', result[0][4])
    #         Color = request.PUT.get('Color', result[0][5])

    #         strsql = "UPDATE File SET Folder = {}, file_name = {}, IsPublic = {}, Color = {} WHERE ID = {};".format(Folder, file_name, IsPublic, Color, file_id)
    #         self.cursor.execute(strsql)
    #         result = self.cursor.fetchall()
            
    #         return HttpResponse("Update Success", content_type='text/plain')
           