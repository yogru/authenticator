import asyncio

from src.dependencies import get_user_auth_sync_usecase


async def main():
    print("create user")
    username = input("username: ")
    password = input("password: ")
    password2 = input("verify password: ")
    if password != password2:
        print("passwords don't match")
        return

    service_name = input("service name: ")

    user_auth_sync_usecase = await get_user_auth_sync_usecase()
    res = await user_auth_sync_usecase.sync_user(
        username=username,
        password=password,
        service_name=service_name,
    )
    print("생성> ", res.id)


if __name__ == '__main__':
    asyncio.run(main())
