from .contract_data import ContractData
from .docusign import Docusign


def main():
    data = ContractData(
        month="January", 
        helper_badge_qt=2,
        additional_chairs_qt=4,
        artist_number=1234567890,
        helper1_number=1234567890,
        shortened_year=22,
        day=14,
        signer_name="Kevin Ha",
        signer_email="kh220kh@gmail.com",
        approver_name="joe",
        approver_email="kevtaco123@gmail.com"
    )
    
    print(Docusign.create_contract(data))
    
main()