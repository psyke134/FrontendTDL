import requests, json

class BackendAccess:
    invalidIP = "255.255.255.255"
    backendServerIP = "192.168.56.139"
    protocol = "http"
    port = "8888"
    headers = {'Content-Type': 'application/json'}
    timeout = 2
    wellKnownStatus = {
        200: "OK",
        201: "Created",
        400: "Request timed out",
        401: "Unauthorized",
        404: "Not found",
        405: "Method not allowed",
        409: "Conflict",
        500: "Internal server error"
    }
    wellKnowMethod = {
        "get": requests.get,
        "post": requests.post,
        "delete": requests.delete
    }

    @staticmethod
    def updateInfo(backendServerIP, port, protocol):
        BackendAccess.backendServerIP = backendServerIP
        BackendAccess.port = port
        BackendAccess.protocol = protocol

    @staticmethod
    def getServerAddress():
        return "{0}://{1}:{2}/".format(BackendAccess.protocol, BackendAccess.backendServerIP, BackendAccess.port)

    @staticmethod
    def request(url, method, data, headers, timeout):
        if BackendAccess.backendServerIP == BackendAccess.invalidIP:
            return (404, BackendAccess.wellKnownStatus[404], {"Error": "No active backend server"})

        try:
            sendMethod = BackendAccess.wellKnowMethod[method]
            response = sendMethod(url, data=data, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            return (400, BackendAccess.wellKnownStatus[400], {"Error": "Backend server took too long make response"})
        except requests.exceptions.ConnectionError:
            return (500, BackendAccess.wellKnownStatus[500], {"Error": "Backend server is not available right now"})

        data = response.json()
        status = response.status_code
        return (status, BackendAccess.wellKnownStatus.get(status, ""), data)

    @staticmethod
    def addNewTask(username, taskText):
        addr = BackendAccess.getServerAddress()
        url = addr + "backend/task/addNew/"
        data = {"username": username, "taskText": taskText}

        return BackendAccess.request(url, "post", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)

    def deleteTask(username, taskText):
        addr = BackendAccess.getServerAddress()
        url = addr + "backend/task/delete/"
        data = {"username": username, "taskText": taskText}

        return BackendAccess.request(url, "delete", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)

    def getTasksOf(username):
        addr = BackendAccess.getServerAddress()
        url = addr + "backend/task/"
        data = {"username": username}

        return BackendAccess.request(url, "get", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)

    def authenticate(username, password):
        addr = BackendAccess.getServerAddress()
        url = addr + "backend/account/authenticate/"
        data = {"username": username, "password": password}

        return BackendAccess.request(url, "post", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)

    def register(name, username, password):
        addr = BackendAccess.getServerAddress()
        url = addr + "backend/account/register/"
        data = {"accountName": name, "username": username, "password": password}

        return BackendAccess.request(url, "post", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)
