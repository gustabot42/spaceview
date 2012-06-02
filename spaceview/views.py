from functools import update_wrapper

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView


class SpaceView(DetailView):
    """
    Namespace object like class based view
    """
    app_namespace = None
    template_name_suffix = '_base'
    
    @classmethod
    def app_name(cls):
        """
        
        """
        if cls.app_namespace:
            return cls.app_namespace
        elif cls.model:
            return smart_str(cls.model.__class__.__name__.lower())
        
        raise ImproperlyConfigured(u"SpaceView %s must define app_namespace or model"
                                   % self.__class__.__name__)
    
    @classmethod
    def as_space(cls, **initkwargs):
        """
        Namespace object definition base on Class View.
        Giving access to "object" and "context" variable
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(u"You tried to pass in the %s method name as a "
                                u"keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError(u"%s() received an invalid keyword %r" % (
                    cls.__name__, key))
        
        def space(request, *args, **kwargs):
            self = cls(**initkwargs)
            
            self.request = request
            self.args = args
            self.kwargs = kwargs
            
            self.object = self.get_object()
            self.context = self.get_context_data()
            
            return self
        
        # take name and docstring from class
        update_wrapper(space, cls, updated=())

        return space
