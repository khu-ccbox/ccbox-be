from rest_framework import serializers
from folder.models import Folder

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BasicFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name']


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent = BasicFolderSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class FolderInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent = BasicFolderSerializer(read_only=True)
    folders = serializers.SerializerMethodField('get_folders')
    #TODO: files field & get_files method

    def get_folders(self, obj):
        folderQuery = Folder.objects.filter(parent=obj.id)
        serializer = BasicFolderSerializer(folderQuery, many=True)
        return serializer.data

    class Meta:
        model = Folder
        fields = '__all__'