from license_management.models import Client

class ClientHelper(object):
    """
        provides helper methods for client model
    """
    @classmethod
    def getClientByName(cls,name):
        """
            gets registered client with the provided name
        """
        try:
            return Client.objects.get(name=name)
        except Client.DoesNotExist:
            return None