import functools
from collections import Iterable

from django.db import transaction
from django.db.models import QuerySet


class BulkSignalQuerySet:
    def __new__(cls, mounts, hook_func, *args, **kwargs):
        def general_iterator(iterator):
            if isinstance(iterator, str):
                yield iterator, hook_func
            if isinstance(iterator, dict):
                for item, func in iterator.items():
                    yield item, func
            elif isinstance(iterator, (list, tuple, set)):
                for item in iterator:
                    yield item, hook_func

        def bulk_operation_decorator(func, original_func):
            @functools.wraps(original_func)
            def wrapper(self, *original_args, **original_kwargs):
                with transaction.atomic():
                    res = original_func(self, *original_args, **original_kwargs)
                    func(self, res, *original_args, **original_kwargs)
                    return res

            return wrapper

        def hook(queryset_class):
            assert isinstance(mounts, Iterable), '`mounts` must be a Iterable.'
            invalid_mounts = set()
            for mount, func in general_iterator(mounts):
                if mount in ('update', 'bulk_update', 'bulk_create'):
                    original_func = getattr(queryset_class, mount, None)
                    if callable(original_func):
                        wrapped_func = bulk_operation_decorator(
                            func, original_func
                        )
                        setattr(queryset_class, mount, wrapped_func)
                else:
                    invalid_mounts.add(mount)
            assert not invalid_mounts, f'{invalid_mounts} is not allowed.'

        cls = type(
            'HookedQuerySet',
            (QuerySet,),
            {}
        )
        hook(cls)
        return cls
