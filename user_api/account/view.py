import json # Http 통신으로 Json파일 데이터 주고받기

from .models import Account

from django.views import View
from django.http import HttpResponse, JsonResponse

# 데이터 주고 받기
class AccountView(View):
    def post(self, request): # post 메서드로 요청 받을 시 name, password 저장
        data = json.loads(request.body)
        Account.objects.create(
            name=data['name'],
            password=data['password']
        )

        return HttpResponse(status=200)

    def get(self, request): # get 메서드로 요청 받을 시, account 테이블 리스트 출력
        Account_data = Account.objects.values()
        return JsonResponse({'accounts' : list(Account_data)}, status=200)


class SignView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(name = data['name']).exists():
                user = Account.objects.get(name=data['name'])

                if user.password == data['password']: # DB내에 저장되어 있는 사용자면
                    return HttpResponse(status=200) # 200(ok)반환
                return HttpResponse(status=401)
            return HttpResponse(status=400) # 로그인 실패 시 400에러 반환

        except KeyError: # 키에러 시
            return JsonResponse({'message' : "INVALID_KEYS"}, status=400)

