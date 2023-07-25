from services.docusign import Docusign, ContractData
from typing import Optional
from utilities.types import HelperData
from typing import Dict


class ContractManager():

    def create_contract(self,
                        contract_type: str,
                        num_additional_chairs: int,
                        artist_phone_number: int,
                        signer_name: str,
                        signer_email: str,
                        helpers: Optional[HelperData]) -> Dict[str, str]:

        # TODO need to discuss spec for dealer contract
        if contract_type == "dealer":
            raise NotImplementedError

        # TODO randomly select admin from DB and assign as approver.
        approver_email = "TEST@gmail.com"
        approver_name = "test"

        data = ContractData(
            num_additional_chairs=num_additional_chairs,
            artist_phone_number=artist_phone_number,
            helpers=helpers,
            signer_name=signer_name,
            signer_email=signer_email,
            approver_name=approver_name,
            approver_email=approver_email,
        )

        docusign = Docusign()

        return {'contractId': docusign.create_contract(data)}
