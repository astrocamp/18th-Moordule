from django.shortcuts import render, HttpResponse


def activities(request):
    return HttpResponse("這是活動頁面！")
