from django import forms

class NullBooleanDashedSelect(forms.Select):
    '''I prefer a dashed null value instead of "unknown" for the
    NullBooleanSelect widget. This class fixes that behavior.'''
    def __init__(self, attrs=None):
        choices = ((u'1', '---------'), (u'2', 'Yes'), (u'3', 'No'))
        super(NullBooleanDashedSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        try:
            value = {True: u'2', False: u'3', u'2': u'2', u'3': u'3'}[value]
        except KeyError:
            value = u'1'
        return super(NullBooleanDashedSelect, self).render(name, value, attrs, choices)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return {u'2': True, u'3': False, True: True, False: False}.get(value, None)

    def _has_changed(self, initial, data):
        # Sometimes data or initial could be None or u'' which should be the
        # same thing as False.
        return bool(initial) != bool(data)