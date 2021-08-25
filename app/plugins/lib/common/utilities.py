import hashlib
from datetime import datetime

class Util:
    """
    A collection of common utilities used throughout the repo
    """
    def iso_timestamp(self):
        """
        Return a ISO formatted timestamp of the current time
        """
        return datetime.now().replace(microsecond=0).isoformat()

    def sha256(self, data):
        """
        Hash a string and return a SHA256 hash
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
