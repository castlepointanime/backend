from services.docusign import Docusign, ContractData
from typing import Optional
from utilities.types import HelperModel
from typing import Dict
from database import UsersDB
from utilities import NoApproverException
from typing import List
from database import CognitoIdentityProviderWrapper


class ContractManager():

    async def create_contract(
        self,
        user_id: str,
        contract_type: str,
        num_additional_chairs: int,
        artist_phone_number: int,
        signer_name: str,
        signer_email: str,
        helpers: Optional[List[HelperModel]]
    ) -> Dict[str, str]:

        # TODO need to discuss spec for dealer contract
        if contract_type == "dealer":
            raise NotImplementedError()

        # Randomly get an approver
        approver = await UsersDB.get_random_artist_reviewer()
        if approver is None:
            raise NoApproverException()

        # Get the email and username from CognitoDB
        assert "username" in approver
        approver_name = approver["username"]
        approver_cognito_data = CognitoIdentityProviderWrapper().get_user(approver_name)
        approver_email = approver_cognito_data.email

        # TODO the approver_name should be the user's name, not username

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

        await UsersDB().add_user_contract(user_id, contract_id)
        # TODO create task to update the approver's entry so he has a reference of the contract

        return {'contractId': contract_id}
