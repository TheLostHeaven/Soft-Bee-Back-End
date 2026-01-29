# src/core/dependencies/containers.py
from dependency_injector import containers, providers
from src.features.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl as AuthUserRepositoryImpl
from src.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl as UserFeatureRepositoryImpl
from src.features.auth.infrastructure.services.security.password_hasher import PasswordHasher
from src.features.auth.infrastructure.services.security.jwt_handler import JWTService
from src.features.auth.application.use_cases.login_user import LoginUserUseCase
from src.features.auth.application.use_cases.register_user import RegisterUserUseCase

from src.features.auth.infrastructure.services.email_service_impl import EmailServiceImpl

from src.features.apiaries.infrastructure.repositories.apiary_repository_impl import ApiaryRepositoryImpl
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.get_apiaries_by_user_id import GetApiariesByUserId
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary

from src.features.user.application.use_cases.get_user import GetUserUseCase
from src.features.user.application.use_cases.update_user import UpdateUserUseCase
from src.features.user.application.use_cases.delete_user import DeleteUserUseCase

from src.features.auth.application.use_cases.forgot_password import ForgotPasswordUseCase
from src.features.auth.application.use_cases.reset_password import ResetPasswordUseCase
from src.features.auth.application.interfaces.services.email_service import IEmailService
from src.features.auth.infrastructure.services.password_service_impl import PasswordServiceImpl
from config import get_config

config_obj = get_config()

class MainContainer(containers.DeclarativeContainer):
    """Contenedor principal"""

    config = providers.Configuration()
    db_session = providers.Dependency()

    auth_user_repository = providers.Factory(
        AuthUserRepositoryImpl,
        db_session=db_session
    )

    password_service = providers.Singleton(
        PasswordServiceImpl,
        secret_key=config.auth.jwt_secret_key,
        algorithm=config.auth.jwt_algorithm,
        time_cost=config.auth.password_argon2_time_cost,
        memory_cost=config.auth.password_argon2_memory_cost,
        parallelism=config.auth.password_argon2_parallelism,
        hash_len=config.auth.password_argon2_hash_len,
        salt_len=config.auth.password_argon2_salt_len
    )

    jwt_service = providers.Singleton(
        JWTService,
        secret_key=config_obj.AUTH["jwt_secret_key"],
        algorithm=config_obj.AUTH["jwt_algorithm"],   
        issuer=config_obj.AUTH["jwt_issuer"],
        audience=config_obj.AUTH["jwt_audience"]
    )

    email_service = providers.Singleton(
        EmailServiceImpl,
        smtp_server=config.email.smtp_host,
        smtp_port=config.email.smtp_port,
        smtp_email=config.email.smtp_user,
        smtp_password=config.email.smtp_password,
        smtp_user=config.email.smtp_user,
        frontend_url=config.frontend_url
    )
    
    login_use_case = providers.Factory(
        LoginUserUseCase,
        user_repository=auth_user_repository,
        token_service=jwt_service,
        password_service=password_service
    )
    
    register_use_case = providers.Factory(
        RegisterUserUseCase,
        user_repository=auth_user_repository,
        password_service=password_service,
        token_service=jwt_service
    )
    
    forgot_password_use_case = providers.Factory(
        ForgotPasswordUseCase,
        user_repository=auth_user_repository,
        email_service=email_service,
        token_service=jwt_service
    )
    
    reset_password_use_case = providers.Factory(
        ResetPasswordUseCase,
        user_repository=auth_user_repository,
        password_service=password_service,
        token_service=jwt_service 
    )
    

    apiary_repository = providers.Factory(
        ApiaryRepositoryImpl,
        db_session=db_session
    )

    create_apiary_use_case = providers.Factory(
        CreateApiary,
        apiary_repository=apiary_repository
    )
    
    get_apiary_by_id_use_case = providers.Factory(
        GetApiaryById,
        apiary_repository=apiary_repository
    )

    get_apiaries_by_user_id_use_case = providers.Factory(
        GetApiariesByUserId,
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

    user_feature_repository = providers.Factory(
        UserFeatureRepositoryImpl,
        db_session=db_session
    )

    get_user_use_case = providers.Factory(
        GetUserUseCase,
        user_repository=user_feature_repository
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_repository=user_feature_repository
    )

    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        user_repository=user_feature_repository
    )