from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt
from .base_controller import BaseController
from utilities.types import FlaskResponseType
from utilities.flask_responses import FlaskResponses
from managers import MeManager
from flasgger import swag_from


class MeController(BaseController):

    ME_POST_SCHEMA = "swagger/me/post.yaml"

    @cognito_auth_required
    @swag_from("swagger/me/get.yaml")
    def get(self) -> FlaskResponseType:
        result = MeManager().get_user(str(current_user), current_cognito_jwt)
        return FlaskResponses().success(result)

    @cognito_auth_required
    def patch(self) -> FlaskResponseType:
        return FlaskResponses().not_implemented_yet()  # TODO

    @cognito_auth_required
    @swag_from(ME_POST_SCHEMA)
    def post(self) -> FlaskResponseType:
        data = self.get_request_data(self.ME_POST_SCHEMA, "NewUserData")
        ret = MeManager().create_user(current_cognito_jwt['sub'], str(current_user), data['vendorType'])
        if not ret:
            return FlaskResponses().bad_request("Failed to make user")
        return FlaskResponses().created_resource(ret)
