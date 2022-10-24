# django_bulk_hook_manager

This package can help you to hook some function on bulk operations.

## Installation

Not yet packaged to pip.

```shell

```

## Usage:

```python
# hooks.py

def demo_hook1(queryset, res, *args, **kwargs):
    pass


def demo_hook2(queryset, res, *args, **kwargs):
    pass
```

```python
# models.py

from django.db import models
from django_bulk_hook_manager.managers import BulkHookManager

from hooks import demo_hook1, demo_hook2


class DemoModel(models.Model):
    # Just hook `demo_hook1` on `update`:
    objects = BulkHookManager('update', demo_hook1)

    # Hook `demo_hook1` on `update` and `bulk_update`:
    objects = BulkHookManager(
        ['update', 'bulk_update'], demo_hook1
    )

    # Hook different functions on different original functions: 
    objects = BulkHookManager({
        'update': demo_hook1,
        'bulk_update': demo_hook2
    })

    demo_field = models.IntegerField()
```

```python
# demo.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YourProjectName.settings')
django.setup()

if __name__ == '__main__':
    from demo.models import DemoModel
    
    for i in range(20):
        x = i % 4
        DemoModel.objects.create(x=x)

    demo_model = DemoModel.objects.filter(x=3)

    demo_model.update(x=2)  # Will call the hook function in this.

```