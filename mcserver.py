from mcstatus import MinecraftServer
def mc_check(ipadd):
    server = MinecraftServer.lookup(ipadd)
    try:
        status = server.status()
        print("Server Online")
    except:
        print("Server Offline")
mc_check("192.168.0.90")
