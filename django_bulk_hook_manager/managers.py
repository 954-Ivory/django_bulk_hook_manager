from django.db.models.manager import BaseManager, Manager


class BulkHookManager:
    def __new__(cls, mounts, func=None, *args, **kwargs):
        from django_bulk_hook_manager.querysets import BulkSignalQuerySet
        queryset = BulkSignalQuerySet(
            mounts, func, *args, **kwargs
        )
        cls = BaseManager.from_queryset(queryset)
        return cls()
