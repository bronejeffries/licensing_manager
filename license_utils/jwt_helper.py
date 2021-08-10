import jwt
from license_utils.constants import LICENSE_ISSUER, AUDIENC_PREFIX, JWT_ALGORITHM
from datetime import datetime


class JWT_helper(object):

    @classmethod
    def create_license_for_client(cls, client, license_details=None):
        """
            creates a license key for the client
        """
        pay_load = {
            "iss": LICENSE_ISSUER,
            "aud": f"{AUDIENC_PREFIX}{client.name}",
            "iat": datetime.utcnow(),
            "license": f"licence issued for {client.name}, must be kept confindential"
        }
        return jwt.encode(pay_load, client.private_key, algorithm=JWT_ALGORITHM)
    
    @classmethod
    def create_software_initialization_token(cls,client_software_pay_load,private_key):
        """
            generate software initialization token
        """
        client_software_pay_load["iss"] = LICENSE_ISSUER
        client_software_pay_load["iat"] = datetime.utcnow()
        return jwt.encode(client_software_pay_load,private_key,algorithm=JWT_ALGORITHM)
