from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.core import serializers
from datetime import datetime
import json
import collections
from decimal import Decimal
from collections import Iterable
from django.core.cache import cache
import settings
from django.db import models
from discount.models import ResourceModel


def json_view( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        response = view_func( request, *args, **kwargs )
        response_code = 200
        if isinstance(response, tuple):
            resp = response[0]
            response_code = response[1]
            response = resp
        if isinstance(response, HttpResponse):
            return response
        r = HttpResponse(as_json(response), mimetype='application/json')
        r.status_code = response_code
        return r
    return _wrapped_view



def cacheable( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        if request.method == 'GET':
            key = settings.CACHE_STRING % (request.get_full_path(), 'ajax', request.is_ajax())
            cached = cache.get(key)
            if cached:
               return cached
            response = view_func( request, *args, **kwargs )
            cache.set(key, response, settings.CACHE_TIME)
            return response
        else:
            return view_func( request, *args, **kwargs )
    return _wrapped_view



#Serialization
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return str(o)
        elif isinstance(o, list):
            return [self.default(i) for i in o]
        elif isinstance(o, ResourceModel):
            return o.as_resource()
        return super(CustomEncoder, self).default(o)


def as_json(response):
    return json.dumps(response, cls = CustomEncoder)
