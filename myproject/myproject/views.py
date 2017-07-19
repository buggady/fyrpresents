from django.shortcuts import render

def bad_request(request):
	return render(request, 'fyrpresents/400.html')

def permission_denied(request):
	return render(request, 'fyrpresents/403.html')

def not_found(request):
	return render(request, 'fyrpresents/404.html')

def server_error(request):
	return render(request, 'fyrpresents/500.html')