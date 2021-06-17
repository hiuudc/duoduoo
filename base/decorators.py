# from django.contrib.auth import decorators
# from django.http import HttpResponse
# from django.shortcuts import redirect


# def unauthenticated_user(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('home')
#         else:
#             return view_func(request, *args, **kwargs)

#     return wrapper_func


# def allowed_user(allowed_roll=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name:
#             if group in allowed_roll:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse("You are not authorized to view this page")
#         return wrapper_func
#     return decorator


# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = None

#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name:
#         if group == 'admin':
#             return view_func(request, *args, **kwargs)
#         # elif group == 'user':
#         #     return redirect('some-where')
#     return wrapper_func
