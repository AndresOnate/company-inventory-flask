class InvalidCredentialsException(Exception):
    """
    Custom exception to be raised when invalid credentials are provided.

    Args:
        message (str, optional): The error message to be associated with the exception.
            Defaults to "Invalid credentials" if no message is provided.
    
    Attributes:
        message (str): The error message that explains the reason for the exception.
    """

    def __init__(self, message="Invalid credentials"):
        """
        Initializes the InvalidCredentialsException with the specified message.

        Args:
            message (str, optional): The error message to be associated with the exception.
                Defaults to "Invalid credentials" if no message is provided.
        """
        self.message = message
        super().__init__(self.message)
