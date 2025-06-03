from django.db import models
from django.contrib.auth.models import User

PARAMETER_CHOICES = [
    ('violet', 'Emotion（感情）'),
    ('indigo', 'Self-control（自己制御）'),
    ('blue', 'Social（社会的関係）'),
    ('green', 'Well-being（ウェルビーイング）'),
    ('yellow', 'Economy（経済）'),
    ('orange', 'Knowledge（知識）'),
    ('red', 'Physical（身体）'),
]

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    emotion = models.PositiveIntegerField(default=0)        # Violet
    self_control = models.PositiveIntegerField(default=0)   # Indigo
    social = models.PositiveIntegerField(default=0)         # Blue
    well_being = models.PositiveIntegerField(default=0)     # Green
    economy = models.PositiveIntegerField(default=0)        # Yellow
    knowledge = models.PositiveIntegerField(default=0)      # Orange
    physical = models.PositiveIntegerField(default=0)       # Red

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_exp(self):
        return (
            self.emotion + self.self_control + self.social +
            self.well_being + self.economy + self.knowledge +
            self.physical
        )

    def level(self):
        return self.total_exp() // 100  # 100EXPごとに1レベルアップ

    def __str__(self):
        return f"{self.user.username}'s UserStatus (Lv.{self.level()})"


class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=20, choices=PARAMETER_CHOICES)
    description = models.TextField()
    exp = models.PositiveIntegerField(default=10)  # デフォルト経験値
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.parameter} +{self.exp}EXP"
