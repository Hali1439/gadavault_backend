from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "Products app is alive!"})
