from .models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def read_notify(request):

    user = request.user
    action = request.POST['action']
    if action == 'read_notify':

        unread_notify = Notification.objects.filter(receiver=user).filter(is_seen=False)
        unread_notify.update(is_seen=True)
        context = {
            'status': 'success',
        }

        return JsonResponse(context)
