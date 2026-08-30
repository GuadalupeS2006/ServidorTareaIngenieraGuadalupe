# ServidorTareaIngenieraGuadalupe

Lo primero que hay que entender (antes de dar cualquier definicion), es que función cumple principalmente "task"; maquina como un diccionario, asociando las tareas con un identificador.
Ahora bien, el servidor puede soportar los siguientes verbos:
-Get: no hace ningun cambio, solo retorna la informacion (que puede ser todo el diccionario task, o, una tarea con un id particular)
-Post: Crea un nuevo registro, se guarda en el diccionario de tasks 
-Patch: Podemos modificar informacion de algun registro que ya este creado 
-Delete: Borra un registro   

Por otro lado, que algo sea idempotente, significa que si dicho algo de ejecuta x cantidad de veces, el estado final siempre es el mismo; Por ello, post no lo es!, luego de ejecutarlo, el estado final siempre es diferente, pues, el resultado de ejecutar post es crear tareas nuevas, se "altera" el servidor añadiendo info nueva.
