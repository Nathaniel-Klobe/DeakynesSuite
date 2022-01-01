from wtforms import Form, StringField, DecimalField, BooleanField, validators


class CompleteTicketForm(Form):
    """Validation for for completing a Ticket."""
    
    labor = DecimalField('Labor Cost')
    parts = DecimalField('Parts Cost')
    other = DecimalField('Other Cost')
    notes = StringField('Notes', [validators.length(max=250)])
    bNotified = BooleanField('Notified')