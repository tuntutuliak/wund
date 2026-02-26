# Патч для совместимости Django 4.2 с Python 3.14:
# в BaseContext.__copy__() исправляем copy(super()) -> создание копии через __new__
# иначе при рендере админки (context.new()) возникает:
# AttributeError: 'super' object has no attribute 'dicts'
import django.template.context

_base_context_copy_orig = django.template.context.BaseContext.__copy__


def _base_context_copy_fixed(self):
    duplicate = object.__new__(type(self))
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate


django.template.context.BaseContext.__copy__ = _base_context_copy_fixed
