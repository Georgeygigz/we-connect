from hashlib import blake2b

from config import AppConfig


def hash_pin(pin):
    """Hash pin/password to ensure security

    Args:
        pin/password (str): a 4 digit pin
    Return:
        (str): return hashed data
    """
    hash_ = blake2b(key=AppConfig.SECRET_KEY.encode("utf-8"), digest_size=32)
    hash_.update(pin.encode('utf-8'))
    return hash_.hexdigest()


def verify_pin(pin, user_pin_hash):
    """Verify pin

    Args:
        pin (str): a 4 digit pin
        user_pin_hash (str): hashed user pin
    Returns:
        False/True if pin/password is corret of incorrect
    """
    unverified_hash = hash_pin(pin)
    is_correct = False if unverified_hash != user_pin_hash else True
    return is_correct
