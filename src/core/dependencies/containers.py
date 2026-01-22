# src/core/dependencies/containers.py
from dependency_injector import containers, providers
from src.features.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.features.auth.infrastructure.services.security.password_hasher import PasswordHasher
from src.features.auth.infrastructure.services.security.jwt_handler import JWTService
from src.features.auth.application.use_cases.login_user import LoginUserUseCase
from src.features.auth.application.use_cases.register_user import RegisterUserUseCase
from src.features.apiaries.infrastructure.repositories.apiary_repository_impl import ApiaryRepositoryImpl
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary

# from src.features.auth.application.use_cases.refresh_token import RefreshTokenUseCase
# from src.features.auth.application.use_cases.logout_user import LogoutUserUseCase
# from src.features.auth.application.use_cases.verify_token import VerifyTokenUseCase

from src.features.apiaries.infrastructure.repositories.apiary_repository_impl import ApiaryRepositoryImpl
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary

class MainContainer(containers.DeclarativeContainer):
    """Contenedor principal"""
    
    # Configuración
    config = providers.Configuration()
    
    # Database session (compartida entre features)
    db_session = providers.Dependency()
    
    # Repositorios de Auth
    user_repository = providers.Factory(
        UserRepositoryImpl,
        db_session=db_session
    )
    
    # Servicios de Auth
    password_hasher = providers.Singleton(
        PasswordHasher,
        algorithm=config.AUTH.password_algorithm
    )
    
    jwt_service = providers.Singleton(
        JWTService,
        secret_key=config.AUTH.jwt_secret_key,
        algorithm=config.AUTH.jwt_algorithm,
        issuer=config.AUTH.jwt_issuer,
        audience=config.AUTH.jwt_audience
    )
    
    # Casos de uso de Auth
    login_use_case = providers.Factory(
        LoginUserUseCase,
        user_repository=user_repository,
        token_service=jwt_service,
        password_hasher=password_hasher
    )
    
    register_use_case = providers.Factory(
        RegisterUserUseCase,
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=jwt_service
    )
    
    # Repositorios de Apiaries
    apiary_repository = providers.Factory(
        ApiaryRepositoryImpl,
        db_session=db_session
    )
    
    # Casos de uso de Apiaries
    create_apiary_use_case = providers.Factory(
        CreateApiary,
        apiary_repository=apiary_repository
    )
    
    get_apiary_by_id_use_case = providers.Factory(
        GetApiaryById,
        apiary_repository=apiary_repository
    )
    
    get_all_apiaries_use_case = providers.Factory(
        GetAllApiaries,
        apiary_repository=apiary_repository
    )
    
    update_apiary_use_case = providers.Factory(
        UpdateApiary,
        apiary_repository=apiary_repository
    )
    
    delete_apiary_use_case = providers.Factory(
        DeleteApiary,
        apiary_repository=apiary_repository
    )
    
    # Repositorios de Apiary
    apiary_repository = providers.Factory(
        ApiaryRepositoryImpl,
        db_session=db_session
    )

    # Casos de uso de Apiary
    create_apiary_use_case = providers.Factory(
        CreateApiary,
        apiary_repository=apiary_repository
    )

    get_apiary_by_id_use_case = providers.Factory(
        GetApiaryById,
        apiary_repository=apiary_repository
    )

    get_all_apiaries_use_case = providers.Factory(
        GetAllApiaries,
        apiary_repository=apiary_repository
    )

    update_apiary_use_case = providers.Factory(
        UpdateApiary,
        apiary_repository=apiary_repository
    )

    delete_apiary_use_case = providers.Factory(
        DeleteApiary,
        apiary_repository=apiary_repository
    )
    
    # refresh_token_use_case = providers.Factory(
    #     RefreshTokenUseCase,
    #     user_repository=user_repository,
    #     token_service=jwt_service
    # )
    
    # logout_use_case = providers.Factory(
    #     LogoutUserUseCase,
    #     user_repository=user_repository,
    #     token_service=jwt_service
    # )
    
    # verify_token_use_case = providers.Factory(
    #     VerifyTokenUseCase,
    #     token_service=jwt_service
    # )