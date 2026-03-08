# src/core/dependencies/containers.py
from dependency_injector import containers, providers
from src.features.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl as AuthUserRepositoryImpl
from src.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl as UserFeatureRepositoryImpl
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
from src.features.user.application.use_cases.get_user_full_data import GetUserFullDataUseCase

from src.features.auth.application.use_cases.forgot_password import ForgotPasswordUseCase
from src.features.auth.application.use_cases.reset_password import ResetPasswordUseCase
from src.features.auth.application.interfaces.services.email_service import IEmailService
from src.features.auth.infrastructure.services.password_service_impl import PasswordServiceImpl
from config import get_config
from src.features.beehive.infrastructure.repositories.beehive_repository_impl import BeehiveRepositoryImpl
from src.features.beehive.application.use_cases.create_beehive import CreateBeehiveUseCase
from src.features.beehive.application.use_cases.get_beehive_by_id import GetBeehiveByIdUseCase
from src.features.beehive.application.use_cases.get_all_beehives_by_apiary_id import GetAllBeehivesByApiaryIdUseCase
from src.features.beehive.application.use_cases.update_beehive import UpdateBeehiveUseCase
from src.features.beehive.application.use_cases.delete_beehive import DeleteBeehiveUseCase
from src.features.treatments.infrastructure.repositories.treatment_repository_impl import TreatmentRepositoryImpl
from src.features.treatments.application.use_cases.create_treatment import CreateTreatmentUseCase
from src.features.treatments.application.use_cases.get_treatments import GetTreatmentsByHiveUseCase
from src.features.treatments.application.use_cases.get_treatment_by_id import GetTreatmentByIdUseCase
from src.features.treatments.application.use_cases.update_treatment import UpdateTreatmentUseCase
from src.features.treatments.application.use_cases.delete_treatment import DeleteTreatmentUseCase
from src.features.treatments.application.use_cases.create_followup import CreateFollowupUseCase
from src.features.treatments.application.use_cases.update_followup import UpdateFollowupUseCase
from src.features.treatments.application.use_cases.delete_followup import DeleteFollowupUseCase
from src.features.inventory.application.dependency_injection import InventoryContainer

from src.features.questions.infrastructure.repositories.sqlalchemy_question_repository import SQLAlchemyQuestionRepository
from src.features.questions.application.use_cases.initialize_apiary_questions import InitializeApiaryQuestions
from src.features.questions.application.use_cases.initialize_hive_questions import InitializeHiveQuestions
from src.features.questions.application.use_cases.get_hive_questions import GetHiveQuestions
from src.features.questions.application.use_cases.update_hive_question import UpdateHiveQuestion

from src.features.ai_agent.infrastructure.services.ai_service_impl import MockAIServiceImpl
from src.features.ai_agent.infrastructure.services.openai_service_impl import OpenAIServiceImpl
from src.features.ai_agent.infrastructure.services.deepseek_service_impl import DeepSeekServiceImpl
from src.features.ai_agent.infrastructure.services.gemini_service_impl import GeminiServiceImpl
from src.features.ai_agent.infrastructure.services.ai_provider_registry import AIProviderRegistry
from src.features.ai_agent.infrastructure.services.session_repository_impl import InMemoryAISessionRepository
from src.features.ai_agent.application.use_cases.process_ai_prompt import ProcessAIPromptUseCase

config_obj = get_config()

class MainContainer(containers.DeclarativeContainer):
    """Contenedor principal"""

    config = providers.Configuration()
    db_session = providers.Dependency()

    inventory_container = providers.Container(
        InventoryContainer,
        db_session=db_session,
        apiary_repository=providers.Factory(
            ApiaryRepositoryImpl,
            db_session=db_session
        )
    )

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

    question_repository = providers.Factory(
        SQLAlchemyQuestionRepository,
        db_session=db_session
    )

    initialize_apiary_questions_use_case = providers.Factory(
        InitializeApiaryQuestions,
        question_repository=question_repository
    )

    initialize_hive_questions_use_case = providers.Factory(
        InitializeHiveQuestions,
        question_repository=question_repository
    )

    get_hive_questions_use_case = providers.Factory(
        GetHiveQuestions,
        question_repository=question_repository
    )

    update_hive_question_use_case = providers.Factory(
        UpdateHiveQuestion,
        question_repository=question_repository
    )

    create_apiary_use_case = providers.Factory(
        CreateApiary,
        apiary_repository=apiary_repository,
        create_inventory_use_case=inventory_container.create_inventory_use_case,
        initialize_apiary_questions_use_case=initialize_apiary_questions_use_case
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

    beehive_repository = providers.Factory(
        BeehiveRepositoryImpl,
        db_session=db_session
    )

    create_beehive_use_case = providers.Factory(
        CreateBeehiveUseCase,
        repository=beehive_repository,
        initialize_hive_questions_use_case=initialize_hive_questions_use_case
    )

    get_beehive_by_id_use_case = providers.Factory(
        GetBeehiveByIdUseCase,
        repository=beehive_repository
    )

    get_all_beehives_by_apiary_id_use_case = providers.Factory(
        GetAllBeehivesByApiaryIdUseCase,
        repository=beehive_repository
    )

    update_beehive_use_case = providers.Factory(
        UpdateBeehiveUseCase,
        repository=beehive_repository
    )

    delete_beehive_use_case = providers.Factory(
        DeleteBeehiveUseCase,
        repository=beehive_repository
    )

    treatment_repository = providers.Factory(
        TreatmentRepositoryImpl,
        db_session=db_session
    )

    create_treatment_use_case = providers.Factory(
        CreateTreatmentUseCase,
        repository=treatment_repository
    )

    get_treatments_by_hive_use_case = providers.Factory(
        GetTreatmentsByHiveUseCase,
        repository=treatment_repository
    )

    get_treatment_by_id_use_case = providers.Factory(
        GetTreatmentByIdUseCase,
        repository=treatment_repository
    )

    update_treatment_use_case = providers.Factory(
        UpdateTreatmentUseCase,
        repository=treatment_repository
    )

    delete_treatment_use_case = providers.Factory(
        DeleteTreatmentUseCase,
        repository=treatment_repository
    )

    create_followup_use_case = providers.Factory(
        CreateFollowupUseCase,
        repository=treatment_repository
    )

    update_followup_use_case = providers.Factory(
        UpdateFollowupUseCase,
        repository=treatment_repository
    )

    delete_followup_use_case = providers.Factory(
        DeleteFollowupUseCase,
        repository=treatment_repository
    )

    get_user_full_data_use_case = providers.Factory(
        GetUserFullDataUseCase,
        get_user_use_case=get_user_use_case,
        get_apiaries_use_case=get_apiaries_by_user_id_use_case,
        get_beehives_use_case=get_all_beehives_by_apiary_id_use_case,
        get_inventories_use_case=inventory_container.get_inventories_by_apiary_use_case
    )

    mock_ai_service = providers.Singleton(MockAIServiceImpl)
    
    openai_service = providers.Singleton(
        OpenAIServiceImpl,
        api_key=config.AI.openai_api_key
    )

    deepseek_service = providers.Singleton(
        DeepSeekServiceImpl,
        api_key=config.AI.deepseek_api_key
    )

    gemini_service = providers.Singleton(
        GeminiServiceImpl,
        api_key=config.AI.gemini_api_key
    )

    ai_provider_registry = providers.Singleton(
        AIProviderRegistry,
        providers=providers.Dict({
            "mock": mock_ai_service,
            "openai": openai_service,
            "deepseek": deepseek_service,
            "gemini": gemini_service
        }),
        default_provider=config.AI.default_provider
    )

    session_repository = providers.Singleton(
        InMemoryAISessionRepository
    )

    process_ai_prompt_use_case = providers.Factory(
        ProcessAIPromptUseCase,
        provider_registry=ai_provider_registry,
        session_repository=session_repository
    )
