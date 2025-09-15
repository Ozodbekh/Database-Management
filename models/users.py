class User:
    def __init__(
            self,
            id: int,
            full_name: str,
            phone_number: str,
            email: str,
            password: str,
            role: str
    ):
        self.id = id
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.id}: {self.full_name} ({self.role})>"
