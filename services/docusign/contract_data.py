from docusign_esign import EnvelopeDefinition, TemplateRole, Tabs, Text, Number
from .env import CONTRACT_TEMPLATE_ID
from typing import Optional
from utilities.types import HelperData, Helper
from dataclasses import dataclass
import datetime
from typing import Dict, List, Union, Optional

@dataclass
class ContractData:

    num_additional_chairs: int
    artist_phone_number: int
    helpers: Optional[HelperData]
    signer_name: str
    signer_email: str
    approver_name: str
    approver_email: str
        
    def generate_envelope(self) -> EnvelopeDefinition:
        env = EnvelopeDefinition(
            status="sent",
            template_id=CONTRACT_TEMPLATE_ID
        )

        envelope_keys = ["signer_email", "signer_name", "num_additional_chairs", "artist_phone_number"]
        text_envelope_args : List[Dict[str, List[Text]]] = []
        number_envelope_args : List[Dict[str, List[Number]]] = []
        
        for key in envelope_keys:
            if type(getattr(self, key, None)) == str:
                text_envelope_args.append(Text(tab_label=key, value=getattr(self, key)))
            elif type(getattr(self, key, None)) == int:
                number_envelope_args.append(Number(tab_label=key, value=getattr(self,key)))
        
        # Add helper badge information
        if (self.helpers):
            number_envelope_args.append(Number(tab_label="num_helper_badges", value=len(self.helpers)))
        
            for helper_num in range(0,3): #TODO dynamically add helpers based on config
                if type(self.helpers[helper_num]) == Helper:
                    text_envelope_args.append(Text(tab_label=f"helper{helper_num}_name", value=self.helpers[helper_num]['name']))
                    number_envelope_args.append(Number(tab_label=f"helper{helper_num}_phone_number", value=self.helpers[helper_num]['phoneNumber']))
                else:
                    raise ValueError("Invalid Helper Data")

        # Generate date for contract
        current_date = datetime.datetime.now()
        day = int(current_date.strftime('%d'))
        month = current_date.strftime('%B')
        shortened_year = int(current_date.strftime('%Y')[2:])

        # Add date to envelope
        text_envelope_args.append(Text(tab_label="month", value=month))
        number_envelope_args.append(Number(tab_label="day", value=day))
        number_envelope_args.append(Number(tab_label="shortened_year", value=shortened_year))

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
        signer.tabs = Tabs(text_tabs=text_envelope_args, number_tabs=number_envelope_args)
        env.template_roles = [signer, approver]

        return env