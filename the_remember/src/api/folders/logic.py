from the_remember.src.api.folders.db_model import FolderORM
from the_remember.src.api.folders.dto import CreateFolderAsTreeDTO
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.modules.dto import CreateModuleAsTreeDTO
from the_remember.src.api.sentences.db_model import SentenceORM
from the_remember.src.api.sentences.dto import CreateSentenceAsTreeDTO
from the_remember.src.api.terms.db_model import TermORM
from the_remember.src.api.terms.dtos.dto import CreateTermAsTreeDTO
from the_remember.src.api.users.dto import UserDTO


def recourse_tree_to_db_models(
        obj: CreateFolderAsTreeDTO | CreateModuleAsTreeDTO | CreateTermAsTreeDTO | CreateSentenceAsTreeDTO,
        current_user: UserDTO,
        __deep: int = 0
) -> FolderORM | ModuleORM | TermORM | SentenceORM:
    if isinstance(obj, CreateFolderAsTreeDTO):
        return FolderORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(
                user_id=current_user.id,
                sub_folders=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_folders],
                sub_modules=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_modules],
            ))
        )

    elif isinstance(obj, CreateModuleAsTreeDTO):
        return ModuleORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(
                author_id=current_user.id,
                sub_terms=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_terms],

            ))
        )
    elif isinstance(obj, CreateTermAsTreeDTO):
        if obj.sub_sentences is None:
            print("ERROR!!!!!!!!!!!!! obj.sub_sentences is None", obj)
        return TermORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(
                sub_sentences=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_sentences or []],
            ))
        )
    elif isinstance(obj, CreateSentenceAsTreeDTO):
        return SentenceORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(

            ))
        )
    else:
        raise NotImplementedError()
