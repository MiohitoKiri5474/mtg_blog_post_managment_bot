"""
testing database relate
"""
import os

from app import db

USERNAME = "lltzpp"
PASSWD = b"$2b$12$doY4G1vL6Yr2LnZEUJX42eCYPDL.JHQiVg5xQXfCF0ZdH.8NuWOti"
FULL_NAME = "miohitokiri5474"
EMAIL = "lltzpp@gmail.com"


def clear_db():
    """clear previous testing data"""

    if not db.check_username_is_available("lltzpp"):
        db.delete_user("lltzpp")


def test_build():
    """testing build_db"""
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.build_db()


def test_check_insert_user():
    """testing check insert user"""
    clear_db()
    db.insert_user(USERNAME, PASSWD, FULL_NAME, EMAIL)
    assert db.check_username_is_available("lltzpp") is False


def test_update_user_status():
    """testing update_user_status"""
    clear_db()
    db.insert_user(USERNAME, PASSWD, FULL_NAME, EMAIL)
    db.update_user_status(USERNAME, False)
    assert db.get_user_info("lltzpp")[4] == 0
    db.update_user_status(USERNAME, True)
    assert db.get_user_info("lltzpp")[4]


def test_get_passwd():
    """testing get_passwd"""
    clear_db()
    db.insert_user(USERNAME, PASSWD, FULL_NAME, EMAIL)
    assert db.get_passwd(USERNAME) == PASSWD
