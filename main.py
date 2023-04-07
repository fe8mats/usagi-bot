import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
import servers
import migrate

TOKEN = os.getenv('TOKEN')

migrate.start()

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("ready...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(s)

@bot.tree.command(name="server", description="指定されたサーバー情報を表示します。")
@app_commands.describe(slug="登録名")
async def getServer(interaction: discord.Interaction, slug: str):
    info = servers.Information()
    result = info.get(slug)
    print(result)
    if result is None:
        await interaction.response.send_message(f"{interaction.user.name} 指定されたサーバー情報が見つかりません")
    else:
        row = result
        info_title = row["title"]
        embed = discord.Embed(title=f"{info_title}のサーバー情報", color=discord.Colour.from_rgb(51,152,219))
        embed.add_field(name="ホスト",value=row["host"])
        embed.add_field(name="パスワード",value=row["password"])
        embed.add_field(name="ポート",value=row["port"])
        embed.add_field(name="登録名（slug）",value=row["slug"])
        embed.add_field(name="登録者/管理者",value=row["manager"])
        if row["message"] is not None:
            embed.add_field(name="メッセージ",value=row["message"], inline=False)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server-add", description="サーバー情報を追加します")
@app_commands.describe(slug="登録名")
@app_commands.describe(title="ゲーム名")
@app_commands.describe(host="ホスト名/IPアドレス")
@app_commands.describe(port="ポート名")
@app_commands.describe(password="パスワード")
@app_commands.describe(message="メッセージ")
async def addServer(interaction: discord.Interaction, slug: str, title: str, host: str, port: str = "なし", password: str = "なし", message: str = None):
    info = servers.Information()
    info.setData(slug, title, host, port, password, message, interaction.user.name)
    result = info.insert()
    del info
    if result is True:
        await interaction.response.send_message(f"{interaction.user.name} 「{title}」のサーバー情報が登録されました。呼び出し名：{slug}")
    else:
        await interaction.response.send_message(f"{interaction.user.name} 「{title}」のサーバー情報登録に失敗しました。既に登録されている可能性があります。")

@bot.tree.command(name="server-list", description="登録されているサーバー情報を一覧表示します")
async def listServer(interaction: discord.Interaction):
    info = servers.Information()
    result = info.getList()
    embed = discord.Embed(title="サーバーリスト一覧", color=discord.Colour.from_rgb(51,152,219))
    for row in result:
        info_host = row["host"]
        info_pass = row["password"]
        info_port = row["port"]
        info_slug = row["slug"]
        info = f"```ホスト: {info_host}\nパスワード：{info_pass}\nポート：{info_port}\n登録名：{info_slug}```"
        embed.add_field(name=row["title"],value=info,inline=False)
    if len(result) < 1:
        embed.description = "登録されていません"
    del info
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server-remove", description="登録されているサーバー情報を削除します")
async def removeServer(interaction: discord.Interaction, slug: str):
    info = servers.Information()
    result = info.remove(slug)
    del info
    if result is True:
        await interaction.response.send_message(f"登録名「{slug}」の情報を削除しました。")
    else:
        await interaction.response.send_message(f"登録名「{slug}」の情報が見つかりません")

bot.run(TOKEN)