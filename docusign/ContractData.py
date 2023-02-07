from docusign_esign import EnvelopeDefinition, TemplateRole, Tabs, Text, Number
from env import CONTRACT_TEMPLATE_ID

class ContractData:
    
    def __init__(
        self,
        month: str,
        helper_badge_qt: int,
        additional_chairs_qt: int,
        artist_number: int,
        helper1_number: int,
        shortened_year: int,
        day: int,
        signer_name: str,
        signer_email: str,
        approver_name: str,
        approver_email: str
        ):
        
        self.month=month
        self.helper_badge_qt=helper_badge_qt
        self.additional_chairs_qt=additional_chairs_qt
        self.artist_number=artist_number
        self.helper1_number=helper1_number
        self.shortened_year=shortened_year
        self.day=day
        self.signer_name=signer_name
        self.signer_email=signer_email
        self.approver_name=approver_name
        self.approver_email=approver_email
        
    def generate_envelope(self):
        env = EnvelopeDefinition(
            status="sent",
            template_id=CONTRACT_TEMPLATE_ID
        )
        
        envelope_keys=["month", 
                       "helper_badge_qt", "additional_chairs_qt", "artist_number",
                       "helper1_number", "shortened_year", "day"]
        envelope_args = {
            "text": list(),
            "number": list()
        }
        
        for key in envelope_keys:
            if type(getattr(self, key)) == str:
                envelope_args["text"].append(Text(tab_label=key, value=getattr(self, key)))
            elif type(getattr(self, key)) == int:
                envelope_args["number"].append(Number(tab_label=key, value=getattr(self,key)))
                
        envelope_args["text"].append(Text(tab_label="email", value=self.signer_email))
        envelope_args["text"].append(Text(tab_label="name", value=self.signer_name))

        signer = TemplateRole(
            role_name="Artist",
            name=self.signer_name,
            email=self.signer_email
        )

        approver = TemplateRole(
            role_name="Approver",
            name=self.approver_name,
            email=self.approver_email
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(text_tabs=envelope_args["text"], number_tabs=envelope_args["number"])
        env.template_roles = [signer, approver]

        return env
