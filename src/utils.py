import random
import string


def generate_random_string(length):
    """
    Generate a random string of given length
    :param length: int
    :return: str
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
