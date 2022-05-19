from rest_framework import serializers
from file.models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'uploaduser', 'folder', 'url', 'file_name', 'color']


