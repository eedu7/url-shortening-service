import secrets


def short_code(url: str, number: int = 6) -> str:
    new_url = "".join([i for i in url if i.isalnum()])
    return "".join(secrets.choice(new_url) for _ in range(number))
