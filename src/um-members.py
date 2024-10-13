from curses import wrapper

from app.app_context import AppContext
from app.builder import Builder
from app.repositories.member_repository import MemberRepository, MemberRepositoryInterface
from app.repositories.user_repository import UserRepository, UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.lifetimes import Lifetime
from common.logging.logger import CustomLogger, LoggerInterface
from common.smart_db.query_builder import QueryBuilder

def main(stdscr):
    builder = Builder()
    builder.add_dependency_injection()
    builder.add_service(Encoder, Encoder, Lifetime.SINGLETON)
    builder.add_service(LoggerInterface, CustomLogger, Lifetime.SINGLETON)
    builder.add_service(QueryBuilder, QueryBuilder, Lifetime.TRANSIENT)
    builder.add_secure_database_access()
    builder.add_mediator()
    builder.add_service(AppContext, AppContext, Lifetime.SINGLETON)
    builder.add_render_engine(stdscr, 10)
    builder.add_service(MemberRepositoryInterface,
                        MemberRepository, Lifetime.SCOPED)
    builder.add_service(UserRepositoryInterface,
                        UserRepository, Lifetime.SCOPED)
    builder.add_service(PasswordManager,
                        PasswordManager, Lifetime.SINGLETON)
    builder.build_app()
    builder.app.start()


if __name__ == "__main__":

    wrapper(main)
