from typing import List
from app.context.member import Member
from app.context.user import User
from common.logging.log import Log


class AppContext():
    logged_in_user: User = None
    error = None
    state = None
    users: List[User] = None
    selected_user: User = None
    selected_member: Member = None
    member_list: List[Member] = None
    selected_log: Log = None
    failed_login_attempts = 0
