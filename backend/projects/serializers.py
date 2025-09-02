from rest_framework import serializers
from .models import Project, Task
from accounts.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("owner",)


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True)# required=False qilib, validation bosqichida xato chiqishini to‘xtatamiz

    class Meta:
        model = Task
        fields = "__all__"

