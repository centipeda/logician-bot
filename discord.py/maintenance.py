"""Various checks and updates to make sure Logic is capable of running
smoothly."""

def update(bot):
    """Runs all currently added checks."""
    update_server_list(bot)

def update_server_list(bot):
    """Updates list of servers in database."""
    print("Updating server list...")
    connectedServers = [s for s in bot.servers]
    c = bot.db.cursor()
    storedServers = c.execute("SELECT server_id, server_name from servers;").fetchall()
    serverIds = [str(s[0]) for s in storedServers]
    for server in connectedServers:
        if server.id not in serverIds:
            bot.db.execute("INSERT INTO servers (server_id, server_name) VALUES (?,?)", (server.id,server.name))
            print("New server {} added.".format(server.name))
        for storedServer in storedServers:
            if storedServer[0] == server.id:
                if not storedServer[1] == server.name:
                    bot.db.execute("UPDATE servers SET server_name = ? WHERE server_id = ?",(server.name,server.id))
                    s = "Changed server name from {} to {}".format(
                                                            storedServer[0],
                                                            server.name)
                    print(s)
    bot.db.commit()
