from django.shortcuts import redirect

def notLoggedU(view_fun):
    def wrapper_fun(request , *args, **kwargs):
        if request.user.is_authenticated:
            return view_fun(request , *args, **kwargs)
        else:
            return redirect('/')
    
    return wrapper_fun

def allowedUser(allowedGroups=[]):
    def decorator(view_fun):
        def wrapper_fun(request , *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name 
            if group in allowedGroups:
                 return view_fun(request , *args, **kwargs)
            else:
                return redirect('/jobs')

        return wrapper_fun
    return decorator