from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt
from .base_controller import BaseController
from utilities.types import FlaskResponseType
from utilities.flask_responses import FlaskResponses
from managers import MeManager


class MeController(BaseController):

    @cognito_auth_required
    # @swag_from()  # TODO
    def get(self) -> FlaskResponseType:
        self.verify_id_token()
        result = MeManager().get_user(current_user, current_cognito_jwt)
        return FlaskResponses().success(result)

    @cognito_auth_required
    # @swag_from  # TODO
    def patch(self) -> FlaskResponseType:
        return FlaskResponses().not_implemented_yet()  # TODO
