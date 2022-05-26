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

### Ejemplos curl
- curl http://myserver.local:5000/signup -d '{"username":"Aaron Peces", "password":"segred2022"}' -X POST -H 'Content-Type: application/json'
- curl http://myserver.local:5000/login -d '{"username":"Aaron Peces", "password":"segred2022"}' -X POST -H 'Content-Type: application/json'
- curl http://myserver.local:5000/username/doc_id -X GET -H 'Content-Type: application/json' -H 'Authentication: token "token del usuario"'

