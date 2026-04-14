import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import AIService

service = AIService()

@csrf_exempt
def ask_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        return JsonResponse(service.ask(prompt))

    return JsonResponse({"error": "POST only"}, status=405)


@csrf_exempt
def train_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question")
        answer = data.get("answer")
        return JsonResponse(service.train(question, answer))

    return JsonResponse({"error": "POST only"}, status=405)


def search_view(request):
    query = request.GET.get("q", "")
    return JsonResponse(service.ask(query))


def feeds_view(request):
    return JsonResponse({"feeds": service.feeds()})
