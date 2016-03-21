# -*- coding: utf-8 -*-

import inspect

from django.core.validators import MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ungettext_lazy

from collectionfield.converter import CollectionConverter


class ItemValidatorMixin(object):

    def __call__(self, value):
        validate = super(ItemValidatorMixin, self).__call__
        for item in value:
            validate(item)


@deconstructible
class ConvertedMaxLengthValidator(MaxLengthValidator):

    def __init__(self, limit_value, collection_type, item_type, sort,
                 unique_items, delimiter, **kwargs):
        self.collection_type = collection_type
        self.item_type = item_type
        self.sort = sort
        self.unique_items = unique_items
        self.delimiter = delimiter
        super(ConvertedMaxLengthValidator, self).__init__(
            limit_value, **kwargs
        )

    def clean(self, value):
        return super(ConvertedMaxLengthValidator, self).clean(
            CollectionConverter(
                collection_type=self.collection_type,
                item_type=self.item_type,
                sort=self.sort,
                unique_items=self.unique_items,
                delimiter=self.delimiter
            ).dump(value)
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.limit_value == other.limit_value and
            self.message == other.message and
            self.code == other.code and
            self.collection_type == other.collection_type and
            self.item_type == other.item_type and
            self.sort == other.sort and
            self.unique_items == other.unique_items and
            self.delimiter == other.delimiter
        )


@deconstructible
class MaxItemsValidator(MaxLengthValidator):
    message = ungettext_lazy(
        singular=(
            'Ensure this value has at most %(limit_value)d item '
            '(it has %(show_value)d).'
        ),
        plural=(
            'Ensure this value has at most %(limit_value)d items '
            '(it has %(show_value)d).'
        ),
        number='limit_value'
    )
    code = 'max_items'


def item_validator(validator):

    if inspect.isclass(validator):
        if issubclass(validator, ItemValidatorMixin):
            _item_validator = validator
        else:
            _item_validator = deconstructible(
                type(
                    'Item{0}'.format(validator.__name__),
                    (ItemValidatorMixin, validator)
                )
            )
    else:

        def _item_validator(value):
            for item in value:
                validator(item)

    return _item_validator


def item_validators(validators):
    return [item_validator(validator) for validator in validators]
