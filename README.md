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

### Ejecución de la práctica
Para poder ejecutar de una manera semiautomatica el programa hemos añadido un script. Cuando lo ejecutamos nos mostrará el siguiente menu:
Practica 2 Seguridad en Redes 2022
What do you want to do? 
1. Signup
2. Login
3. Get the contents of a file 
4. Create a file 
5. Change the contents of a file 
6. Delete file 
7. Exit

- La primera opción ejecutará el comando curl con el verbo post para la creación de un nuevo usuario.
- La segunda opción ejecutará el comando curl con el verbo post para la autenticación de un usuario ya existente.
- La tercera opción ejecutará el comando curl con el verbo get para obtener el contenido del archivo existente en el directorio del usuario.
- La cuarta opción ejecutará el comando curl con el verbo post para la creación de un archivo y el directorio correspondiente al usuario.
- La quinta opción ejecutará el comando curl con el verbo put para la actualización del contenido de un archivo ya existente
- La sexta opción ejecutará el comando curl con el verbo delete para la eliminación de un archivo existente.
- La séptima opción terminará la ejecución del script.