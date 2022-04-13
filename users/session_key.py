from django.conf import settings

def current_user_session_id(request):
	if not request.session.exists(request.session.session_key):
		request.session.create() 
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

	return session_key