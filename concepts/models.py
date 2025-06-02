from django.db import models
from django.contrib.auth.models import User

class Concept(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="concepts")
    title = models.CharField(max_length=100)  # 概念名（例：愛とは何か、仕事とは）
    description = models.TextField()  # ユーザーが記述した内容（自由記述）
    
    # GPTなどによって生成された要約や意味の埋め込み（オプション）
    system_summary = models.TextField(blank=True, null=True)

    # 公開範囲
    VISIBILITY_CHOICES = [
        ('private', '自分のみ'),
        ('shared', '選択ユーザーと共有'),
        ('public', '全体公開'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}（{self.user.username}）"
    

class ConceptChat(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='chats')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
