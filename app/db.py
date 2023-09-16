"""database relate"""

import os
import sqlite3

DB_PATH = "post_sys.db"


def build_db():
    """create database if DB_PATH is not exist"""
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS post_info (
        post_name TEXT PRIMARY KEY,
        url TEXT,
        username TEXT,
        status TEXT
        )"""
    )
    conn.commit()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_info (
        name TEXT PRIMARY KEY,
        passwd BLOB,
        full_name TEXT DEFAULT Nont,
        email TEXT DEFAULT None,
        disable BOOL DEFAULT 1
        )"""
    )
    conn.commit()
    conn.close()


def check_username_is_available(name: str):
    """check username is available of not before add a new user into database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user_info WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()

    return result is None


def insert_user(name: str, passwd, full_name: str, email: str):
    """add a new user with information into database"""
    if not check_username_is_available(name):
        raise ValueError(
            "The chosen user name is already taken, please choose a different one."
        )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_info (name, passwd, full_name, email) VALUES (?, ?, ?, ?)",
        (name, passwd, full_name, email),
    )
    conn.commit()
    conn.close()


def delete_user(name: str):
    """delete user from database"""
    if check_username_is_available(name):
        raise ValueError("The chosen username is not in our database.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_info WHERE name = ?", (name,))
    conn.commit()
    conn.close()


def update_user_status(name: str, disable: bool):
    """update user status"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("Update user_info SET disable = ? WHERE name = ?", (disable, name))
    conn.commit()
    conn.close()


def get_passwd(name: str):
    """get hashed password of target user"""

    if check_username_is_available(name):
        raise ValueError("User not found.")

    try:
        result = get_user_info(name)[1]
        if result:
            return result
        raise ValueError("User information not found.")
    except ValueError as error:
        raise ValueError(str(error)) from error


def get_user_info(name: str):
    """get user information from database"""
    if check_username_is_available(name):
        raise ValueError("User not found.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, passwd, full_name, email, disable FROM user_info WHERE name = ?",
        (name,),
    )
    result = cursor.fetchall()
    conn.close()

    if result:
        return result[0]
    raise ValueError("User information not found.")


def check_post_name_is_available(post_name: str):
    """check post name is available of not before adding a new post into database"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM post_info WHERE code = ?", (post_name,))
    result = cursor.fetchone()
    conn.close()

    return result is None


def insert_post(post_name: str, url: str, username: str, status):
    """add a post into database"""
    if not check_post_name_is_available(post_name):
        raise ValueError(
            "The chosen post name is already taken, Please choose a different post name."
        )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO post_info (post_name, url, username, status) VALUES (?, ?, ?, ?)",
        (post_name, url, username, status),
    )
    conn.commit()
    conn.close()


def update_status(post_name: str, status: str):
    """update status"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE post_info SET status = ? WHERE post_name = ?", (status, post_name)
    )
    conn.commit()
    conn.close()


def list_url(status: str):
    """list out all post with chose status"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT post_name, url FROM post_info WHERE status = ?", (status,))

    all_post = cursor.fetchone()
    cursor.close()

    return all_post
