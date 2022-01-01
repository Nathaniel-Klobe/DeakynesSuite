from wtforms import Form, StringField, EmailField, validators

class CustomerForm(Form):
    """Validation for for customer creation"""
    firstname = StringField('First Name', [validators.length(min=3, max=25)])
    lastname = StringField('Last Name', [validators.length(min=3, max=25)])
    address = StringField('Address', [validators.length(min=3, max=50)])
    phone = StringField('Phone', [validators.length(min=7, max=-10)])
    email = EmailField('Email')
    
    