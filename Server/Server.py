# -*- coding:ISO-8859-1 -*-

import grpc
import time

class Server:

    def __init__(self, PORT_SERVER=5555):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Agenda_pb2_grpc.add_AgendaServicer_to_server(AgendaServicer(), server)
        # server.add_insecure_port('[::]:50051')
        server.add_insecure_port(PORT_SERVER)
        server.start()
        print("Server inicializado em " + sys.argv[1])

        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)

        pass

# ----------- END OF CLASS ----------- #

Server(5555)
