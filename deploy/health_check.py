import xmlrpc.client
from time import sleep

if __name__ == "__main__":
    try:
        sleep(10)
        with xmlrpc.client.ServerProxy("http://localhost:9005/RPC2") as server:
            info = server.supervisor.getAllProcessInfo()
            error_states = list(filter(lambda x: x["state"] != 20, info))
            exit(len(error_states))
    except Exception as e:
        print(e.with_traceback())
        exit(1)
