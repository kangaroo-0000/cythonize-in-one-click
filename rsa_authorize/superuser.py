
# load_dotenv 一定要在最前
from dotenv import load_dotenv
load_dotenv(".env")
from utils.fast_verify.jwt_method import hash_password
from apps.rsa_authorize.sql.sqlite_database import SessionLocal, engine
from apps.rsa_authorize.sql.sqlite_curd import SuperUserHandler, Session
import apps.rsa_authorize.sql.sqlite_models as models
import click
import os


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@click.command()
@click.option("-U", "--username", "username", default="admin")
@click.option("-P", "--password", "password", default="admin123")
@click.option("-E", "--email", "email", default="admin@gmail.com")
def create_user(username, password, email, db: Session = get_db()):
    try:
        db = next(db)
        superuser_handler = SuperUserHandler(db)

        data = {
            "username": username,
            "password": password,
            "email": email
        }

        data["hashed_password"] = hash_password(data["password"])
        data.pop("password")

        res = superuser_handler.Create_New_User(data)

        if(res):
            print(True)
        else:
            print(False)
    except Exception as e:
        print("create_user 發生預期外錯誤")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    create_user()
