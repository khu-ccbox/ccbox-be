from django.db import models


class Account(models.Model):
    name = models.CharField(max_length = 50) # 이름
    password = models.CharField(max_length= 200) # 패스워드
    created_at = models.DateTimeField(auto_now_add=True) # 생성시간
    updated_at = models.DateTimeField(auto_now=True) # 수정시간

    class Meta:
        db_table = 'accounts' # table명
