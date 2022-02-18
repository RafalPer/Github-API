from .models import Project, Commit
from rest_framework import serializers


class CommitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ["commits", "author", "date", "message"]


class DetailInfoSerializer(serializers.ModelSerializer):
    commits = CommitInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "org", "language", "stars", "last_updated"]
