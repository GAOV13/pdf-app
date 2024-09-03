# PDF Management Web Application

## Descripción del Proyecto

Esta es una aplicación web para el manejo de archivos PDF. Los usuarios pueden subir archivos PDF después de crear una cuenta con un correo electrónico y utilizar la autenticación de doble factor (2FA) con tokens. Actualmente, solo los usuarios registrados pueden acceder a la aplicación.

### Módulos Principales

1. **Módulo de Autenticación**: Maneja el registro, inicio de sesión y autenticación de doble factor de los usuarios.
2. **Módulo de Documentos**: Permite a los usuarios subir, editar, eliminar y visualizar archivos PDF.

## Instalación

Para correr el proyecto, primero necesitas instalar las dependencias listadas en el archivo `requirements.txt`. Puedes hacerlo utilizando `pip`:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

- **templates/**: Contiene las plantillas HTML utilizadas para el frontend de la aplicación.

## Uso

1. Regístrate con un correo electrónico válido.
2. Inicia sesión utilizando tu correo electrónico y contraseña.
3. Configura la autenticación de doble factor (2FA) utilizando una aplicación de autenticación.
4. Sube, edita, elimina y visualiza archivos PDF desde la interfaz de usuario.

## Pasos para Iniciar la Aplicación

1. Corre el archivo `init_db.py` para inicializar la base de datos.
2. Corre el archivo `run.py` para iniciar la aplicación.

## Dependencias

Las dependencias del proyecto están especificadas en el archivo `requirements.txt`.

## Mejoras

El proyecto fue pensado para tener 7 módulos.

1. **User Authentication & Authorization Module**
   - **Nombre**: AuthModule
   - **Responsabilidad**: Gestionar la autenticación y autorización de los usuarios. Este módulo manejará el registro de usuarios, el inicio de sesión con doble factor (Google Authenticator), y la gestión de permisos de acceso.
   - **Razón**: La autenticación es la primera línea de defensa para proteger la aplicación. Separar esta funcionalidad en un módulo dedicado permite manejar la seguridad de forma centralizada y facilita la escalabilidad y el mantenimiento.

2. **User Management Module**
   - **Nombre**: UserManagementModule
   - **Responsabilidad**: Manejar la gestión de usuarios, incluyendo la edición de perfiles, asignación de roles, y la funcionalidad específica para la asignación de aprobadores de documentos.
   - **Razón**: Separar la gestión de usuarios de la autenticación permite un manejo más flexible y detallado de las capacidades y roles dentro de la aplicación, lo que facilita la implementación de nuevas funcionalidades relacionadas con los usuarios.

3. **Document Management Module**
   - **Nombre**: DocumentModule
   - **Responsabilidad**: Implementar el CRUD de documentos PDF. Este módulo incluirá funcionalidades para subir, editar, eliminar, listar y previsualizar documentos. También gestionará la asignación de títulos, descripciones, y usuarios aprobadores.
   - **Razón**: Centralizar toda la lógica relacionada con los documentos en un solo módulo permite un desarrollo más cohesivo y facilita la implementación de futuras mejoras o cambios en la gestión de documentos.

4. **Approval Workflow Module**
   - **Nombre**: ApprovalModule
   - **Responsabilidad**: Implementar el flujo de aprobación para los documentos. Este módulo permitirá a los usuarios aprobadores visualizar, aprobar o rechazar documentos pendientes, y mostrará a los usuarios los documentos en los que están involucrados.
   - **Razón**: Separar el flujo de aprobación del CRUD de documentos permite un mejor manejo de los estados y permisos relacionados con la aprobación, además de facilitar la incorporación de lógicas de negocio más complejas en el futuro.

5. **Security Module**
   - **Nombre**: SecurityModule
   - **Responsabilidad**: Gestionar todas las medidas de seguridad adicionales como la protección contra accesos no autorizados, encriptación de datos sensibles, y asegurar que las interacciones del usuario sean seguras.
   - **Razón**: Un módulo dedicado a la seguridad permite que las mejores prácticas y actualizaciones de seguridad se implementen de forma uniforme en toda la aplicación.

6. **UI/UX Module**
   - **Nombre**: UIModule
   - **Responsabilidad**: Implementar el diseño de la interfaz de usuario y la experiencia de usuario (UI/UX) de la aplicación. Este módulo se encargará de crear una interfaz intuitiva, amigable y accesible para los usuarios finales.
   - **Razón**: Separar la lógica de presentación de la lógica de negocio asegura que las mejoras y cambios en la interfaz de usuario no afecten la funcionalidad del sistema y permite que el diseño sea escalable y fácil de modificar.

7. **Notification Module**
   - **Nombre**: NotificationModule
   - **Responsabilidad**: Gestionar las notificaciones dentro de la aplicación, incluyendo notificaciones por correo electrónico para aprobaciones, cambios en los documentos, y otras acciones importantes.
   - **Razón**: Centralizar la lógica de notificaciones permite gestionar eficientemente la comunicación dentro de la aplicación y asegura que las notificaciones estén alineadas con el flujo de trabajo y la seguridad.

De esos solo 3 han sido implementados que son el módulo de autentificación, el módulo de documentos y la UI. Como trabajos futuros se realizará el módulo de administradores que es el que maneja la asignación de usuarios para aprobar los documentos y permite los cambios de perfiles. Como también listar los PDF para ser aprobados.

Eso actualmente se está asignando automáticamente por la aplicación a usuarios creados dentro de la misma sin ellos tener la posibilidad de visualizarlos. También se desea mejorar la interfaz, ya que es una interfaz muy básica que no es responsive, como tampoco está bien optimizada para su visualización.

El módulo de autentificación tiende a fallar con el doble factor token, a veces no toma bien la contraseña temporal, por lo que también es una mejora. Junto con mejorar las respuestas a posibles errores dentro del registro. Como escribir mal el correo, no escribir la contraseña correcta o no ser un email válido.
