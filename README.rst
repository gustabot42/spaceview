=========
spaceview
=========


Father app dependency in reusable aplications.

Solution:

Url declaration using namespace

Aplication namespace (app_name) data declaration using Class Base Views

And this aplication to glue them



Install
-------


In settings.py:

Install the app:

    INSTALLED_APPS = [
        ...
        'spaceview',
        ...
    ]

add the middleware

    MIDDLEWARE_CLASSES = [
        ...
        "spaceview.middleware.SpaceviewMiddleware"
    ]

create the variable SPACEVIEW_SPACES as a list of SpaceViews clases

    # settings.py
    ...
    
    SPACEVIEW_SPACES = [
        'myproject.apps.myapp.views.MyappSpace',
        ...
    ]
    
    ...


Create the SpaceView Class in your reusable app and treat it like a Detail View (Class Base View)

    # myapp/views.py
    from __future__ import absolute_import
    from spaceview.views import SpaceView
    from .models import Myapp
    
    class MyappSpace(SpaceView):
        
        app_namespace = 'myapp'
        model = Myapp
        context_object_name = "myapp"
        slug_url_kwarg = 'myapp_slug'
        template_name = 'myapp/myapp_base.html'
        
        def get_context_data(self, **kwargs):
            context = super(ProjectSpace, self).get_context_data(**kwargs)
            context['foo'] = self.object.foo()
            
            return context


Usage
-----


Read namespace url in django docs ;) https://docs.djangoproject.com/en/dev/topics/http/urls

model (or app_namespace if declared) most be equal to app_name used in urls

    # myapp/urls.py
    ...
    urlpatterns = patterns('',
        ...
        url(r"^(?P<myapp_slug>[-\w]+)/reusableapp/", include(ReusableAapp, namespace='myapp_instance', app_name='myapp')),
    )

Now you can access to space objects in reusable app views

    # reusableapp/view.py
    ...
    
    class ReusableappView(FooView):
    
	model = ReusableApp
	context_object_name = "reusableapp"
	template_name = "reusableapp/reusableapp_foo.html"
	app_name = "myapp"
    
    
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
	    spaces = request.spaces
	    myapp_object = spaces[self.app_name].object
	    
	    if not myapp_object.foo_permission():
		HttpResponseForbidden()
	    
	    return super(MemberUpdateSetView, self).dispatch(request, *args, **kwargs)


Spaces context variables will be automaticly added

context variable "current_app" will be added equal to namespace


Variables
---------


request.resolve
    url resolve object plus app_dict variable

request.space
    spaceview object relative to last namespace resolve in url
    give access to object and context variable

request.spaces - dictionary
    aplication namespaces (app_name) : SpaceView Object


Usage Example
-------------


https://github.com/gustavodiazjaimes/narrat