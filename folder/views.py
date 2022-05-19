from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from django.contrib.auth.models import User
from folder.models import Folder
from folder.serializers import FolderSerializer, FolderInfoSerializer


class FolderAPI(APIView):
    def get(self, request):
        return JsonResponse({"message":"folder api ok"}, status=200)
    

    def post(self, request):
        try:
            #TODO: Auth check, get token info
            serializer = FolderSerializer(data=request.data)
            user = User.objects.get(id=1)

            if serializer.is_valid(raise_exception=True):
                if 'parent' in request.data:
                    parent = Folder.objects.get(id=request.data['parent'])
                    serializer.save(user=user, parent=parent)
                
                else:
                    serializer.save(user=user)
                
                return JsonResponse(serializer.data, status=200)

        except Folder.DoesNotExist:
            return JsonResponse({"message":"parent folder not found"}, status=404)
        
        except Exception as e:
            print(e)
            return JsonResponse({"message":"bad request"}, status=400)



class FolderIdAPI(APIView):
    def get(self, request, folderID):
        try:
            #TODO: Auth check, get token info
            folder = Folder.objects.get(id=folderID)
            serializer = FolderInfoSerializer(folder)
            #TODO: Folder permission check (owner check)

            return JsonResponse(serializer.data, status=200)
        
        except Folder.DoesNotExist:
            return JsonResponse({"message":"folder not found"}, status=404)
    

    def delete(self, request, folderID):
        try:
            #TODO: Auth check, get token info
            folder = Folder.objects.get(id=folderID)
            serializer = FolderInfoSerializer(folder)
            #TODO: Folder permission check (owner check)

            #TODO: Folder Empty check
            #TODO: S3 request

            folder.delete()

            response = {"id":folderID, "name":serializer.data['name'], "message":"success"}
            return JsonResponse(response, status=200)
        
        except Folder.DoesNotExist:
            return JsonResponse({"message":"folder not found"}, status=404)
        
        except Exception as e:
            print(e)
            return JsonResponse({"message":"bad request"}, status=400)
    

    def put(self, request, folderID):
        try:
            #TODO: Auth check, get token info
            folder = Folder.objects.get(id=folderID)
            serializer = FolderSerializer(instance=folder, data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                if 'parent' in request.data:
                    if request.data['parent'] == "null":
                        serializer.save(parent=None)
                    
                    else:
                        parent = Folder.objects.get(id=request.data['parent'])
                        serializer.save(parent=parent)
                else:
                    serializer.save()
                
                return JsonResponse(serializer.data, status=200)
        
        except Folder.DoesNotExist:
            return JsonResponse({"message":"folder not found"}, status=404)
        
        except Exception as e:
            print(e)
            return JsonResponse({"message":"bad request"}, status=400)