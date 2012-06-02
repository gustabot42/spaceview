=========
spaceview
=========


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

create the variable SPACEVIEW_SPACES as a list of space views

    # settings.py
    ...
    
    SPACEVIEW_SPACES = [
        'myproject.apps.myapp.views.MyappSpace',
        ...
    ]
    
    ...


Create the Space View in your reusable app and treat it like a Detail View (Class Base View)

    # myapp/views.py
    from __future__ import absolute_import
    from spaceview.views import SpaceView
    from .models import Myapp
    
    class ProjectSpace(SpaceView):
        
        namespace = 'myapp'
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


Read namespace url in django docs ;)

    # myapp/urls.py
    ...
    urlpatterns = patterns('',
        ...
        url(r"^(?P<myapp_slug>[-\w]+)/reusableapp/", include(ReusableAapp, namespace='myapp', app_name='reusableapp')),
    )

Now you can access to space objects in reusable app views

    # reusableapp/view.py
    ...
    
    class ReusableappView(FooView):
    
    model = ReusableApp
    context_object_name = "reusableapp"
    template_name = "reusableapp/reusableapp_foo.html"
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        space = request.space.object
        
        if not space.foo_permission():
            HttpResponseForbidden()
        
        return super(MemberUpdateSetView, self).dispatch(request, *args, **kwargs)


Variables
---------


        request.resolve, url resolve object
        request.space, space-view object relative to last namespace resolve in url
        request.spaces, dict of namespace an space-view object