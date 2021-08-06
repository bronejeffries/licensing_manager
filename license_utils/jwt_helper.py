import jwt
from .constants import LICENSE_ISSUER, AUDIENC_PREFIX, JWT_ALGORITHM
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
