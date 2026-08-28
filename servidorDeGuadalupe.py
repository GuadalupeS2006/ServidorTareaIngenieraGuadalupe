import json
from wsgiref.simple_server import make_server

tasks = {}
cuenta_id=1

def app(environ, start_response):

    global cuenta_id
    
    metodo = environ.get("REQUEST_METHOD")
    path = environ.get("PATH_INFO")
    ruta = path.strip("/").split("/")

    #GET
    if metodo == "GET" and len(ruta) ==  1 and ruta[0] == "tasks":
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)

        return[json.dumps(tasks).encode("utf-8")]
            
    #POST

    
    elif metodo == "POST" and len(ruta) == 1 and ruta[0] == "tasks":
        tam_contenido = int(environ.get("CONTENT_LENGTH",0))
        cuerpo_bt = environ["wsgi.input"].read(tam_contenido)

        data = json.loads(cuerpo_bt.decode("utf-8"))

        new_id = str(cuenta_id)
        
        cuenta_id+=1

        tasks[new_id]=data

        #DEVUELVE TAREA Y SU ID

        response_body = json.dumps({"id":new_id, "tarea":data})
        status = "201 created "
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)

        return[response_body.encode("utf-8")]

    #GET/DELETE/PATH 
    elif len(ruta) == 2 and ruta[0] == "tasks":
        aux_tarea = ruta[1]

        if metodo == "GET":
    
        #BUSCAR ID
            if aux_tarea in tasks:
                status = "200 OK"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps(tasks[aux_tarea]).encode("utf-8")]
            else:
            #NO EXISTE
                status = "404 Not Found"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps({"error": "No se ha encontrado la tarea"}).encode("utf-8")]

        if metodo == "DELETE":
           
            if aux_tarea in tasks:

                tarea_delete = tasks.pop(aux_tarea)
                status = "200 OK"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps({"mensaje":"Tarea eliminada","tarea": tarea_delete }).encode("utf-8")]
            else:
                #NO EXISTE
                    status = "404 Not Found"
                    headers = [("Content-Type", "application/json")]
                    start_response(status, headers)
                    return [json.dumps({"error": "No se pudo eliminar la tarea"}).encode("utf-8")]

        if metodo == "PATCH":
            #BUSCAR ID
            if aux_tarea in tasks:
                tam_contenido = int(environ.get("CONTENT_LENGTH",0))
                cuerpo_bt = environ["wsgi.input"].read(tam_contenido)
                
                data = json.loads(cuerpo_bt.decode("utf-8"))
                tasks[aux_tarea].update(data)

                status = "200 OK"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                body = json.dumps(tasks[aux_tarea]).encode("utf-8")
                return [body]
            else:
                #NO EXISTE
                status = "404 Not Found"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps({"error": "No se ha encontrado la tarea"}).encode("utf-8")]
            
    #OTRO
    else:
        status = "404 Not Found"
        headers = [("Content-Type", "text/plain")]
        start_response(status,headers)

        return[b"Page Not Found"]


with make_server("",9292,app) as server:
    print("Listening on http://localhost:9292")
    server.serve_forever()

    