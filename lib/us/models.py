from django.conf import settings
from django.db.models.fields import Field

class USStateField(Field): 
    def get_internal_type(self): 
        return "USStateField" 
        
    def db_type(self):
        if settings.DATABASE_ENGINE == 'oracle':
            return 'CHAR(2)'
        else:
            return 'varchar(2)'
    
    def formfield(self, **kwargs): 
        from applyform.lib.us.forms import USStateSelect 
        defaults = {'widget': USStateSelect} 
        defaults.update(kwargs) 
        return super(USStateField, self).formfield(**defaults)