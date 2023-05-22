def caesar_encrypt(message: str, n: int) -> str:
    """
    Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    result = ""
    for letter in message:
        if letter.isalpha():
            num = ord(letter)
            if letter.isupper():
                num = (num - ord('A') + n) % 26 + ord('A')
            else:
                num = (num - ord('a') + n) % 26 + ord('a')
            result += chr(num)
        else:
            result += letter
    return result
