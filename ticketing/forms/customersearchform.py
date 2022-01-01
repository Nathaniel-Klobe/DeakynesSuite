from wtforms import Form, StringField, validators

class CustomerSearchForm(Form):
    """Validation for for customer search"""
    
    lastname = StringField('Last Name', [validators.length(min=3, max=25)])
