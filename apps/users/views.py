from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "Users app is alive!"})
