from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import BasicInfoSerializer, DetailInfoSerializer
from rest_framework.response import Response
import requests
import re
import json
from datetime import datetime
from .models import Project, Commit
from rest_framework import status


def home(request):
    return render(request, "core/home.html")


class AddProjectView(APIView):
    def post(self, request):
        if request.data:
            if request.data["url"]:
                url = request.data["url"]
                api_url = re.sub("github.com/", "api.github.com/repos/", url)
                github_request = requests.request("GET", api_url)
                if github_request.text:
                    json_data = json.loads(github_request.text)
                    url_json = json_data["html_url"]
                    name = json_data["name"]
                    org = json_data["owner"]["login"]
                    language = json_data["language"]
                    stars = json_data["stargazers_count"]
                    now = datetime.now()
                    last_updated = now
                    download_link = f"{api_url}/zipball/"
                    commits_url = f"{api_url}/commits"
                    commits_request = requests.request("GET", commits_url)
                    commits_data = json.loads(commits_request.text)
                    author = commits_data[0]["commit"]["author"]["name"]
                    date = commits_data[0]["commit"]["author"]["date"]
                    message = commits_data[0]["commit"]["message"]
                    try:
                        project_name = Project.objects.get(name=name)
                    except Project.DoesNotExist:
                        project_name = None
                    if project_name:
                        return Response(
                            {"Error": "Project with this name already exists"}, status=status.HTTP_409_CONFLICT
                        )
                    else:
                        commit_obj = Commit.objects.create(author=author, date=date, message=message)
                        Project.objects.create(
                            url=url_json,
                            name=name,
                            org=org,
                            commit=commit_obj,
                            language=language,
                            stars=stars,
                            last_updated=last_updated,
                            download_link=download_link,
                        )

            return Response(200)
        else:
            return Response(400)


"""
def testcall(request):
    user = request.user
    social = user.social_auth.get(provider='github')
    payload = ""
    headers = {
    Authorization': f'Bearer {social.extra_data["access_token"]}',
    }
    headers = {
        'Authorization': 'Bearer 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',
    }
    response = requests.request("GET", 'https://api.github.com/repos/RafalPer/books', headers=headers, data=payload)
    return HttpResponse(response)
"""


class DetailInfoViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Project.objects.all()
    serializer_class = DetailInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data_link = request.data.get("download_link")
        project_id = request.data["id"]
        commit_id = request.data["commit"]["id"]
        pattern = r"\/zipball\/"
        repo_link = re.sub(pattern, "", data_link)
        github_request = requests.request("GET", repo_link)
        if github_request.text:
            json_data = json.loads(github_request.text)
            language = json_data["language"]
            stars = json_data["stargazers_count"]
            now = datetime.now()
            last_updated = now
            commits_url = f"{repo_link}/commits"
            print(commits_url)
            commits_request = requests.request("GET", commits_url)
            commits_data = json.loads(commits_request.text)
            author = commits_data[0]["commit"]["author"]["name"]
            date = commits_data[0]["commit"]["author"]["date"]
            message = commits_data[0]["commit"]["message"]
            Project.objects.filter(id=project_id).update(language=language, stars=stars, last_updated=last_updated)
            Commit.objects.filter(id=commit_id).update(author=author, date=date, message=message)

        return Response(200)


class BasicInfoViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Project.objects.all()
    serializer_class = BasicInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
