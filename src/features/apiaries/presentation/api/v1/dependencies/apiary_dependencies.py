from dependency_injector.wiring import Provide, inject
from dependency_injector import containers, providers
from fastapi import Depends
from sqlalchemy.orm import Session
from src.core.dependencies.containers import MainContainer
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary
from src.features.apiaries.infrastructure.repositories.apiary_repository_impl import ApiaryRepositoryImpl


@inject
def get_apiary_repository(
    db_session: Session = Depends(Provide[MainContainer.db_session]),
) -> ApiaryRepositoryImpl:
    return ApiaryRepositoryImpl(db_session=db_session)

@inject
def get_create_apiary_use_case(
    apiary_repository: ApiaryRepositoryImpl = Depends(get_apiary_repository),
) -> CreateApiary:
    return CreateApiary(apiary_repository=apiary_repository)

@inject
def get_get_apiary_by_id_use_case(
    apiary_repository: ApiaryRepositoryImpl = Depends(get_apiary_repository),
) -> GetApiaryById:
    return GetApiaryById(apiary_repository=apiary_repository)

@inject
def get_get_all_apiaries_use_case(
    apiary_repository: ApiaryRepositoryImpl = Depends(get_apiary_repository),
) -> GetAllApiaries:
    return GetAllApiaries(apiary_repository=apiary_repository)

@inject
def get_update_apiary_use_case(
    apiary_repository: ApiaryRepositoryImpl = Depends(get_apiary_repository),
) -> UpdateApiary:
    return UpdateApiary(apiary_repository=apiary_repository)

@inject
def get_delete_apiary_use_case(
    apiary_repository: ApiaryRepositoryImpl = Depends(get_apiary_repository),
) -> DeleteApiary:
    return DeleteApiary(apiary_repository=apiary_repository)
