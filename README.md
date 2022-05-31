## Práctica 2 Seguridad en Redes
### Objetivos de la práctica:
- Conocer e implementar un API RESTful sencilla
- Implementar mecanismos de identificación y autenticación de usuarios.
- Implementar mecanismos de confidencialidad utilizando HTTPS.

### Autores de la práctica:
- Aarón Peces García
- Fernando González García

### Configuracion entorno
- Configurar archivo /etc/hosts para redireccionar 127.0.0.1 a myserver.local.
- Copiar el archivo cert.pem a /usr/local/share/ca-certificates/myserver.local.crt.
- Ejecutar "sudo update-ca-certificates"
- Insalar el módulo flask con "pip install flask"
- Instalar el módulo flask-restful con "pip install flask-restful"
- Instalar el módulo httplib2 con "pip install httplib2"
- Instalar el módulo requests con "pip install requests"

### Ejecución de la práctica
Primero debemos ejecutar en una shell el main.py de la siguiente manera "python3 main.py". Para poder enviar las peticiones
al servidor hemos creado un script que actua como cliente y permite hacerlo de una manera cómoda. Para ejecutarlo pondremos
en la terminal "python3 script_app.py", y se mostrará el siguiente menu:

What do you want to do? 
0. Show app version
1. Signup
2. Login
3. Get the contents of a file 
4. Create a file 
5. Change the contents of a file 
6. Delete file 
7. Reset API 
8. Exit

- La opción "0" ejecutará el comando curl con el verbo get para obtener la versión de la app.
- La opción "1" ejecutará el comando curl con el verbo post para la creación de un nuevo usuario.
- La opción "2" ejecutará el comando curl con el verbo post para la autenticación de un usuario ya existente.
- La opción "3" ejecutará el comando curl con el verbo get para obtener el contenido del archivo existente en el directorio del usuario.
- La opción "4" ejecutará el comando curl con el verbo post para la creación de un archivo y el directorio correspondiente al usuario.
- La opción "5" ejecutará el comando curl con el verbo put para la actualización del contenido de un archivo ya existente
- La opción "6" ejecutará el comando curl con el verbo delete para la eliminación de un archivo existente.
- La opción "7" borra los subdirectorios que se hayan creado dentro del directorio de usuarios y borra el contenido del archivo .shadow.
- La opción "8" termina la ejecución del script
