**Usagi Bot**

某エンジョイゲームサーバー用の便利Bot

- マルチサーバー情報の管理

**Commands**

|  コマンド名  |  引数  |  処理内容  |
| ---- | ---- | ---- |
|  /server  |  slug  |  登録名からサーバー情報を呼び出し表示する  |
|  /server-list  |  なし  |  登録されているサーバー情報を一覧表示する  |
|  /server-add  |  slug, title, host, port, password, message  |  サーバー情報を登録する  |
|  /server-remove  |  slug  |  指定した登録名のサーバー情報を削除する  |

--

**Requirements**

```
Python 3.8.*
SQLite3
```

**CentOS7 Setup**

```
yum install -y git
yum install -y centos-release-scl
yum install -y rh-python38 which
scl enable rh-python38 bash
python3 -m pip install python-dotenv
python3 -m pip install git+https://github.com/Rapptz/discord.py
```

