from faker import Faker


def test_password_hasher(faker: Faker):
    from app.lib.password_hasher import Argon2PasswordHasher

    password, salt = faker.password(), faker.password()
    hashed_password = Argon2PasswordHasher(salt).hash(password)
    assert Argon2PasswordHasher(salt).verify(password, hashed_password)
