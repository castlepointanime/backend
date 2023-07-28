from services.docusign import Docusign, ContractData
from typing import Optional
from utilities.types import HelperData
from typing import Dict
from database import UsersDB
from utilities import NoApproverException


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
            raise NotImplementedError()

        # Randomly get an approver
        approver = UsersDB.get_random_artist_reviewer()
        if approver is None:
            raise NoApproverException()
        approver_email = approver.get("email")
        approver_name = approver.get('name')

        assert type(approver_email) == str
        assert type(approver_name) == str

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

        contract_id = docusign.create_contract(data)

        # TODO create task to create reference of the contract in contracts DB
        # TODO create task to update the approver's entry so he has a reference of the contract

        return {'contractId': contract_id}
