from wtforms import Form, StringField, SelectField, DateTimeField, validators

class TicketForm(Form):
    """Validation for for ticket creation."""
    
    tickettype = SelectField('Ticket Type')
    ticketdescription = StringField('Ticket Description', [validators.length(min=3, max=25)])
    ticketstatus = SelectField('Ticket Status', [validators.length(min=3, max=50)])
    promised = DateTimeField('Promised Date')
    notes = StringField('Notes', [validators.length(max=250)])