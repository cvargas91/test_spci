from django.contrib.auth import login
from django.contrib.auth.models import User

def MyMiddleware(get_response):
    def middleware(request):
        if not request.user.is_authenticated :
            login(request, User.objects.get(email='jose.espina@uaysen.cl'))
            request.session['perfil'] = "Auditoría"
        response = get_response(request)
        return response
    return middleware