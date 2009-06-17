from django.conf import settings
from django.db.models.fields import Field

class ShirtSizeField(Field): 
    def get_internal_type(self): 
        return "ShirtSizeField" 
        
    def db_type(self):
        if settings.DATABASE_ENGINE == 'oracle':
            return 'CHAR(3)'
        else:
            return 'varchar(3)'
    
    def formfield(self, **kwargs): 
        from applyform.lib.shirts.forms import ShirtSizeSelect
        defaults = {'widget': ShirtSizeSelect} 
        defaults.update(kwargs) 
        return super(ShirtSizeField, self).formfield(**defaults)