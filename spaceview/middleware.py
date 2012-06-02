from __future__ import absolute_import

from django.core.urlresolvers import get_urlconf, get_resolver
from django.utils.importlib import import_module
from django.utils.translation import get_language

from .conf import settings


def load_space(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing space %s: "%s"' % (path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing space. Is SPACEVIEW_NAMESPACES a correctly defined list or tuple?')
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" space' % (module, attr))
    
    try:
        app_name = getattr(cls, 'app_name')
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define app_namespace' % (module, attr))
    
    try:
        as_space = getattr(cls, 'as_space')
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define as_namespace, Is the module subclass of SpaceView' % (module, attr))
    
    return app_name(), as_space()


def get_resolve(path, urlconf=None):
    if urlconf is None:
        urlconf = get_urlconf()
    
    resolver = get_resolver(urlconf)
    app_list = resolver.app_dict
    
    resolve = resolver.resolve(path)
    resolve.app_list = app_list
    
    return resolve


def get_spaceview_dict():
    spaceview_dict = {}
    
    for view_path in settings.SPACEVIEW_SPACES:
        app_name, space_func = load_space(view_path)
        spaceview_dict[app_name] = space_func
    
    return spaceview_dict


def namespace_to_appname(namespace, app_dict):
    for app_name, app_instances in app_dict.iteritems():
        if namespace in app_instances:
            return app_name
    
    return None


class SpaceviewMiddleware(object):
    
    def process_view(self, request, func, *args, **kwargs):
        
        def get_space(request, _args, _kwargs, app_name, spaceview_dict):
            if app_name in spaceview_dict.keys():
                space_func = spaceview_dict[app_name]
                return space_func(request, *_args, **_kwargs)
            else:
                return None
        
        def get_spaces_dict(request, _args, _kwargs, app_dict, namespaces, spaceview_dict):
            spaces = {}
            for ns in namespaces:
                app_name = namespace_to_appname(ns, app_dict)
                spaces[app_name] = get_space(request, _args, _kwargs, app_name, spaceview_dict)
            return spaces
        
        _args, _kwargs = args[0], args[1]
        resolve = get_resolve(request.path_info)
        namespace = resolve.namespace
        app_name = resolve.app_name
        
        if namespace:
            namespaces = resolve.namespaces
            app_dict = resolve.app_list
            spaceview_dict = get_spaceview_dict()
            
            space = get_space(request, _args, _kwargs, app_name, spaceview_dict)
            spaces = {namespace:space} if space else {}
            
            if len(namespaces) > 1:
                spaces.update(
                    get_spaces_dict(request, _args, _kwargs, app_dict, namespaces[1:], spaceview_dict)
                )
            
            request.space = space
            request.spaces = spaces
        request.resolve = resolve
    
    def process_template_response(self, request, response):
        spaces = request.spaces
        resolve = request.resolve
        namespace = resolve.namespace
        namespaces = resolve.namespaces
        app_dict = resolve.app_list
        
        if namespaces:
            context = {'current_app': namespace}
            
            for ns in reversed(namespaces):
                app_name = namespace_to_appname(ns, app_dict)
                
                if app_name in spaces.keys():
                    context.update(spaces[app_name].context)
            
            context.update(response.context_data)
            response.context_data = context
        
        return response
