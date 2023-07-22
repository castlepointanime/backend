from docusign_esign import EnvelopeDefinition, TemplateRole, Tabs, Text, Number
from .env import CONTRACT_TEMPLATE_ID
from typing import Optional
from utilities.types import HelperData
from dataclasses import dataclass
import datetime
from typing import Dict, List, Union

@dataclass
class ContractData:

    num_additional_chairs: int
    artist_phone_number: int
    helpers: HelperData
    signer_name: str
    signer_email: str
    approver_name: str
    approver_email: str
        
    def generate_envelope(self):
        env = EnvelopeDefinition(
            status="sent",
            template_id=CONTRACT_TEMPLATE_ID
        )

        envelope_keys["signer_email", "signer_name", "num_additional_chairs", "artist_phone_number"]
        envelope_args = {
            "text": list(),
            "number": list()
        }
        
        for key in envelope_keys:
            if type(getattr(self, key, None)) == str:
                envelope_args["text"].append(Text(tab_label=key, value=getattr(self, key)))
            elif type(getattr(self, key, None)) == int:
                envelope_args["number"].append(Number(tab_label=key, value=getattr(self,key)))
        
        # Add helper badge information
        envelope_args["number"].append(Number(tab_label="num_helper_badges", value=len(self.helpers)))
        
        for helper_num in range(0,3): #TODO dynamically add helpers based on config
            envelope_args["text"].append(Text(tab_label=f"helper{helper_num}_name", value=helpers[helper_num]['name']))
            envelope_args["number"].append(Number(tab_label=f"helper{helper_num}_phone_number", value=helpers[helper_num]['phoneNumber']))

        # Generate date for contract
        current_date = datetime.datetime.now()
        day = int(current_date.strftime('%d'))
        month = current_date.strftime('%B')
        shortened_year = int(current_date.strftime('%Y')[2:])

        # Add date to envelope
        envelope_args["text"].append(Text(tab_label="month", value=month))
        envelope_args["number"].append(Number(tab_label="day", value=day))
        envelope_args["number"].append(Number(tab_label="shortened_year", value=shortened_year))

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
