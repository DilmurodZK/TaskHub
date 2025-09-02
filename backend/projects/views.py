from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role in ["admin", "manager"]:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionError("Sizga project yaratishga ruxsat berilmagan!")

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Project.objects.all()
        return Project.objects.filter(owner=user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "assigned_to", "title"]

    def perform_create(self, serializer):
        assignee = serializer.validated_data.get("assigned_to")
        user = self.request.user

        if not assignee:
            serializer.save(assigned_to=user)
            return

        if assignee == user:
            serializer.save(assigned_to=user)
            return

        if user.role in ("admin", "manager"):
            serializer.save()
        else:
            raise PermissionDenied("Boshqa foydalanuvchiga vazifa biriktirish huquqingiz yo‘q.")


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == "admin":
            return Task.objects.all()
        elif user.role == "manager":
            return Task.objects.filter(Q(project__owner=user) | Q(assigned_to=user))
        return Task.objects.filter(assigned_to=user)

