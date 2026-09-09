from common import constants

class Error(Exception):
    """Classe de base pour les exceptions personnalisées"""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class RequestInvalidError(Error):
    """Exception pour une requête invalide"""
    def __init__(self, message: str = constants.REQUEST_INVALID):
        super().__init__(message, 400)

class UserUnauthenticatedError(Error):
    """Exception pour un utilisateur non authentifié"""
    def __init__(self, message: str = constants.USER_UNAUTHENTICATED):
        super().__init__(message, 401)

class UserUnauthorizedError(Error):
    """Exception pour un utilisateur non autorisé"""
    def __init__(self, message: str = constants.USER_UNAUTHORIZED):
        super().__init__(message, 403)

class ResourceNotFoundError(Error):
    """Exception pour une ressource non trouvée"""
    def __init__(self, message: str = constants.RESSOURCE_NOT_FOUND):
        super().__init__(message, 404)

