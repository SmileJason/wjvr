#coding: utf-8

from django.core.cache import cache

def cache4anonymous(ttl=None):
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            CACHE_KEY = request.path
            response = None
            if request.user.is_anonymous():
                response = cache.get(CACHE_KEY, None)
                
            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator
