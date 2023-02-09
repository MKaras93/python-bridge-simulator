from server.fast_api_server.fast_api_server import PythonBridgeSimulatorHttpServer

server_class = PythonBridgeSimulatorHttpServer
server = server_class()
server.run()
