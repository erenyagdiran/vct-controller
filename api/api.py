from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import patterns, url
from django.utils import six
from django.utils.encoding import smart_str, force_unicode
from django.utils.importlib import import_module
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(APIView):
    """ 
    This is the entry point for the REST API.
    
    Follow the hyperinks each resource offers to explore the API.
    
    Note that you can also explore the API from the command line, for instance 
    using the curl command-line tool.
    
    For example: `curl -X GET https://your_domain.net/api/ 
    -H "Accept: application/json; indent=4"`
    """
    def get(base_view, request, format=None):
        output = {}
        for model in api._registry:
            name = force_unicode(model._meta.verbose_name)
            name_plural = force_unicode(model._meta.verbose_name_plural)
            output.update({'%s_uri' % name_plural: reverse('%s-list' % name,
                args=[], request=request)})
        return Response(output)


class RestApi(object):
    def __init__(self):
        self._registry = {}
    
    def register(self, *args):
        model = args[0].model
        self._registry.update({model: args})
    
    def base(self):
        try: api_root = settings.COMMON_API_ROOT
        except AttributeError: api_root = ApiRoot
        else: 
            mod, inst = api_root.rsplit('.', 1)
            mod = import_module(mod)
            api_root = getattr(mod, inst)
        return api_root.as_view()
    
    @property
    def urls(self):
        return self.get_urls()
    
    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.base(), name='base'),)
        
        for model, resource in six.iteritems(self._registry):
            # TODO Support for nested resources on urls /api/nodes/1111/ctl
            name = force_unicode(model._meta.verbose_name)
            name_plural = force_unicode(model._meta.verbose_name_plural)
            urlpatterns += patterns('',
                url(r'^%s/$' % name_plural,
                    resource[0].as_view(),
                    name='%s-list' % name),
                url(r'^%s/(?P<pk>[0-9]+)$' % name_plural, 
                    resource[1].as_view(),
                    name="%s-detail" % name),
            )
        return urlpatterns
    
    def autodiscover(self):
        """ Auto-discover INSTALLED_APPS api.py and serializers.py modules """
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try: import_module('%s.api' % app)
            except ImportError: pass
            try: import_module('%s.serializers' % app)
            except ImportError: pass
    
    def aggregate(self, model, field, name):
        """ Dynamically add new fields to an existing serializer """
        # TODO provide support for hooking with nested serializers
        if model in self._registry:
            self._registry[model][0].serializer_class.base_fields.update({name: field()})
            self._registry[model][1].serializer_class.base_fields.update({name: field()})


# singleton
api = RestApi()
