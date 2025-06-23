# Importando el libería de encriptación
from hashlib import sha1


def make_password(raw_password: str) -> str:
    """
    Make a password compatible with metin2 database
    if raw_password is none then generate a password
    """
    if raw_password is None:
        return
    
    mysql_hash = "*" + sha1(sha1(raw_password.encode()).digest()).hexdigest()
    mysql_hash = mysql_hash.upper()
    return mysql_hash


def validate_password(mysql_hash: str, raw_password: str) -> bool:
    """
    Validate a mysql_hash with a raw_password
    
    :param mysql_hash: The hashed password from the database
    :param raw_password: The raw password to validate
    :return: True if the password is valid, False otherwise
    """
    hash_password = make_password(raw_password)
    return mysql_hash == hash_password
