"""
Guildmages' Forum Post Management Discord Bot
"""
import json
import os
import sqlite3

import discord
from discord.ext import commands

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
    conn.close()


def check_post_name_is_available(post_name: str):
    """check post name is available of not before adding a new post into database"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT post_name FROM post_info WHERE post_name = ?", (post_name,))
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


def update_status_in_ddb(post_name: str, status: str):
    """update status"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE post_info SET status = ? WHERE post_name = ?", (status, post_name)
    )
    conn.commit()
    conn.close()


def list_post(status: str):
    """list out all post with chose status"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT post_name, url FROM post_info WHERE status = ?", (status,))

    all_post = cursor.fetchall()
    cursor.close()

    return all_post


def list_all_post_in_ddb():
    """List all post in ddb"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_info")
    all_post = cursor.fetchall()
    cursor.close()

    res = "```\n"
    for i in all_post:
        res = res + f"{i[0]} {i[1]} {i[2]} {i[3]}\n"
    res = res + "```\n"

    return res


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def new_post_tmp(args1, args2, args3, args4):
    """New Post tmp"""
    try:
        insert_post(args1, args2, args3, args4)
        return "文章 " + args1 + " 成功加入資料庫"
    except ValueError:
        return "文章已在資料庫中，請檢查網址是否錯誤"


@bot.event
async def on_ready():
    """When bot is ready to use, let me know"""
    print("Bot in ready.")


@bot.command()
async def New_Post(ctx, args1, args2, args3, args4):  # pylint: disable=C0103
    """Add a new post into ddb"""
    await ctx.send(new_post_tmp(args1, args2, args3, args4))


@bot.command()
async def new_post(ctx, args1, args2, args3, args4):
    """Add a new post into ddb"""
    await ctx.send(new_post_tmp(args1, args2, args3, args4))


@bot.command()
async def List(ctx, status):  # pylint: disable=C0103
    """Listing all post with same status"""
    res = list_post(status)
    if res is None:
        res = "無符合目標"
    await ctx.send(res)


@bot.command()
async def Update_Status(ctx, args1, args2):  # pylint: disable=C0103
    """Update post status"""
    update_status_in_ddb(args1, args2)
    await ctx.send("已成功更新文章狀態")


@bot.command()
async def update_status(ctx, args1, args2):
    """Update post status"""
    update_status_in_ddb(args1, args2)
    await ctx.send("已成功更新文章狀態")


@bot.command()
async def Help(ctx):  # pylint: disable=C0103
    """List all command"""
    await ctx.send(
        "!New_Post [文章名稱] [hackmd 網址] [作者名稱] [文章狀態]：將新文章加入資料庫\n"
        + "!List [狀態]：列出目前所有符合 [狀態] 的文章\n"
        + "!Update_Status [文章名稱] [文章狀態]：更新文章狀態\n"
        + "!List_All_Post：列出所有文章"
    )


@bot.command()
async def List_All_Post(ctx):  # pylint: disable=C0103
    """List all post"""
    await ctx.send(list_all_post_in_ddb())


@bot.command()
async def list_all_post(ctx):
    """List all post"""
    await ctx.send(list_all_post_in_ddb())


build_db()
TOKEN = ""
with open("token.json", "r") as f:  # pylint: disable=W1514
    TOKEN = json.load(f)["token"]
bot.run(TOKEN)
