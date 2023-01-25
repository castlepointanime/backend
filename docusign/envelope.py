from ds_config import DS_JWT
from docusign_esign import EnvelopesApi, EnvelopeDefinition, TemplateRole, Tabs, Text, Number
from jwt_config import create_api_client
from env import CONTRACT_TEMPLATE_ID

class Contract:

    @classmethod
    def worker(cls, access_token, base_path, account_id):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope()
        api_client = create_api_client(
            base_path=base_path, access_token=access_token)
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=account_id, envelope_definition=envelope_definition)
        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls):
        # create the envelope definition
        env = EnvelopeDefinition(
            status="sent",
            template_id=CONTRACT_TEMPLATE_ID
        )

        month = Text(
            tab_label="month", value="January"
        )

        signer_name = Text(
            tab_label="name", value="Kevin Ha"
        )

        email = Text(
            tab_label="email", value="kh220kh@gmail.com"
        )

        helper_badge_qt = Number(
            tab_label="helper_badge_qt", value=2
        )

        additional_chairs_qt = Number(
            tab_label="additional_chairs_qt", value=4
        )

        artist_number = Number(
            tab_label="artist_number", value=1234567890
        )
        helper1_number = Number(
            tab_label="helper1_number", value=1234567890
        )
        shortened_year = Number(
            tab_label="shortened_year", value=22
        )
        day = Number(
            tab_label="day", value=14
        )

        signer = TemplateRole(
            role_name="Artist",
            name="Kevin Ha",
            email="kh220kh@gmail.com"
        )

        approver = TemplateRole(
            role_name="Approver",
            name="joe",
            email="kevtaco123@gmail.com"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(text_tabs=[month, signer_name, email], number_tabs=[
                           helper_badge_qt, additional_chairs_qt, artist_number, helper1_number, shortened_year, day])

        env.template_roles = [signer, approver]

        return env
