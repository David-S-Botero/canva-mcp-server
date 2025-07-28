# Canva MCP Server

Un servidor MCP (Model Context Protocol) completo que expone los endpoints de la API de Canva como herramientas. Este servidor permite interactuar con Canva programáticamente a través de asistentes de IA.

## Características

### 🔐 Autenticación OAuth 2.0
- Generación de URLs de autorización con PKCE
- Intercambio de códigos de autorización por tokens de acceso
- Renovación automática de tokens de acceso
- Gestión segura de credenciales

### 📁 Gestión de Diseños
- Crear nuevos diseños
- Listar diseños existentes
- Obtener metadatos de diseños
- Gestionar páginas de diseños
- Obtener formatos de exportación disponibles

### 🖼️ Gestión de Assets
- Subir assets desde archivos locales
- Subir assets desde URLs
- Obtener metadatos de assets
- Actualizar información de assets
- Eliminar assets

### 📂 Gestión de Carpetas
- Crear carpetas
- Listar contenido de carpetas
- Actualizar metadatos de carpetas
- Mover elementos entre carpetas
- Eliminar carpetas

### 📤 Exportación
- Exportar diseños a múltiples formatos (PDF, JPG, PNG, GIF, PPTX, MP4)
- Trabajo asíncrono para exportaciones
- Seguimiento del estado de exportación

### 🎨 Plantillas de Marca
- Listar plantillas de marca
- Obtener metadatos de plantillas
- Verificar capacidades de autocompletado

### 🔄 Autocompletado
- Crear trabajos de autocompletado de diseños
- Seguimiento del estado de autocompletado
- Generación dinámica de diseños

### 💬 Comentarios
- Crear hilos de comentarios
- Responder a comentarios
- Listar respuestas de comentarios
- Obtener metadatos de comentarios

### 👤 Gestión de Usuarios
- Obtener información del usuario actual
- Obtener perfil del usuario
- Verificar capacidades del usuario

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd canva-mcp-server
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en el directorio raíz:

```env
CANVA_CLIENT_ID=tu_client_id_aqui
CANVA_CLIENT_SECRET=tu_client_secret_aqui
CANVA_REDIRECT_URI=https://tu-dominio.com/callback
```

### 4. Configurar la integración en Canva

1. Ve a [Canva Developer Portal](https://www.canva.com/developers/integrations/connect-api)
2. Crea una nueva integración
3. Configura los scopes necesarios:
   - `asset:read` - Leer assets
   - `asset:write` - Escribir assets
   - `design:meta:read` - Leer metadatos de diseños
   - `design:meta:write` - Escribir metadatos de diseños
   - `folder:read` - Leer carpetas
   - `folder:write` - Escribir carpetas
   - `comment:write` - Escribir comentarios
   - `brand_template:read` - Leer plantillas de marca
4. Configura la URL de redirección
5. Copia el Client ID y Client Secret a tu archivo `.env`

## Uso

### 1. Iniciar el servidor
```bash
python server.py
```

### 2. Flujo de autenticación

#### Paso 1: Crear URL de autorización
```python
# Usar la herramienta create_authorization_url
auth_result = create_authorization_url(
    scopes="asset:read asset:write design:meta:read folder:read"
)
# auth_result contiene:
# - authorization_url: URL para que el usuario autorice
# - code_verifier: Verificador de código para PKCE
# - state: Parámetro de estado para seguridad
```

#### Paso 2: Intercambiar código por token
```python
# Después de que el usuario autorice, recibirás un código
# Usar la herramienta exchange_code_for_token
token_result = exchange_code_for_token(
    authorization_code="código_recibido",
    code_verifier="verificador_guardado"
)
```

#### Paso 3: Usar las herramientas de la API
Una vez autenticado, puedes usar todas las herramientas disponibles.

### 3. Ejemplos de uso

#### Crear un nuevo diseño
```python
design = create_design(
    title="Mi Nuevo Diseño",
    folder_id="folder_id_opcional"
)
```

#### Listar diseños
```python
designs = list_designs(
    limit=20,
    folder_id="folder_id_opcional"
)
```

#### Subir un asset desde URL
```python
upload_job = create_url_asset_upload_job(
    url="https://ejemplo.com/imagen.jpg",
    filename="mi_imagen.jpg",
    folder_id="folder_id_opcional"
)

# Verificar estado del trabajo
job_status = get_url_asset_upload_job(upload_job["job"]["id"])
```

#### Exportar un diseño
```python
export_job = create_design_export_job(
    design_id="design_id",
    file_type="pdf",
    page_range="1-3"
)

# Verificar estado de exportación
export_status = get_design_export_job(export_job["job"]["id"])
```

#### Crear una carpeta
```python
folder = create_folder(
    name="Mi Carpeta",
    parent_folder_id="parent_folder_id_opcional"
)
```

#### Autocompletar un diseño desde plantilla de marca
```python
autofill_job = create_design_autofill_job(
    brand_template_id="template_id",
    dataset={
        "company_name": "Mi Empresa",
        "logo_url": "https://ejemplo.com/logo.png",
        "primary_color": "#FF5733"
    }
)

# Verificar estado del autocompletado
autofill_status = get_design_autofill_job(autofill_job["job"]["id"])
```

## Herramientas Disponibles

### Autenticación
- `create_authorization_url` - Crear URL de autorización OAuth
- `exchange_code_for_token` - Intercambiar código por token de acceso
- `refresh_access_token` - Renovar token de acceso
- `get_oauth_config` - Obtener configuración OAuth actual
- `clear_tokens` - Limpiar tokens almacenados

### Usuarios
- `get_current_user` - Obtener información del usuario actual
- `get_user_profile` - Obtener perfil del usuario
- `get_user_capabilities` - Obtener capacidades del usuario

### Diseños
- `create_design` - Crear nuevo diseño
- `list_designs` - Listar diseños
- `get_design` - Obtener metadatos de diseño
- `get_design_pages` - Obtener páginas de diseño
- `get_design_export_formats` - Obtener formatos de exportación

### Assets
- `create_asset_upload_job` - Crear trabajo de subida de asset
- `get_asset_upload_job` - Verificar estado de subida de asset
- `create_url_asset_upload_job` - Subir asset desde URL
- `get_url_asset_upload_job` - Verificar estado de subida desde URL
- `get_asset` - Obtener metadatos de asset
- `update_asset` - Actualizar asset
- `delete_asset` - Eliminar asset

### Carpetas
- `create_folder` - Crear carpeta
- `get_folder` - Obtener metadatos de carpeta
- `update_folder` - Actualizar carpeta
- `delete_folder` - Eliminar carpeta
- `list_folder_items` - Listar contenido de carpeta
- `move_folder_item` - Mover elemento entre carpetas

### Exportación
- `create_design_export_job` - Crear trabajo de exportación
- `get_design_export_job` - Verificar estado de exportación

### Plantillas de Marca
- `list_brand_templates` - Listar plantillas de marca
- `get_brand_template` - Obtener metadatos de plantilla
- `get_brand_template_dataset` - Obtener dataset de plantilla

### Autocompletado
- `create_design_autofill_job` - Crear trabajo de autocompletado
- `get_design_autofill_job` - Verificar estado de autocompletado

### Comentarios
- `create_comment_thread` - Crear hilo de comentarios
- `create_comment_reply` - Responder a comentario
- `get_comment_thread` - Obtener metadatos de hilo
- `list_comment_replies` - Listar respuestas de comentarios

## Configuración de Seguridad

### Variables de Entorno Requeridas
- `CANVA_CLIENT_ID` - ID del cliente de Canva
- `CANVA_CLIENT_SECRET` - Secreto del cliente de Canva
- `CANVA_REDIRECT_URI` - URI de redirección configurada

### Mejores Prácticas
1. **Nunca** compartas tus credenciales de Canva
2. Usa variables de entorno para las credenciales
3. Implementa almacenamiento seguro de tokens en producción
4. Maneja errores de autenticación apropiadamente
5. Implementa renovación automática de tokens

## Trabajos Asíncronos

Muchas operaciones en la API de Canva son asíncronas. El flujo típico es:

1. Crear un trabajo (ej: `create_asset_upload_job`)
2. Obtener un ID de trabajo
3. Verificar el estado del trabajo periódicamente
4. Usar el resultado cuando el trabajo esté completo

### Ejemplo de polling
```python
import asyncio
import time

async def wait_for_job_completion(job_id: str, check_function):
    while True:
        status = await check_function(job_id)
        if status["job"]["status"] == "success":
            return status["job"]["result"]
        elif status["job"]["status"] == "failed":
            raise Exception(f"Job failed: {status}")
        
        # Esperar antes de verificar nuevamente
        await asyncio.sleep(2)
```

## Manejo de Errores

El servidor maneja errores de la API de Canva y los propaga como excepciones. Los errores comunes incluyen:

- `401 Unauthorized` - Token inválido o expirado
- `403 Forbidden` - Permisos insuficientes
- `404 Not Found` - Recurso no encontrado
- `429 Too Many Requests` - Límite de tasa excedido

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Recursos Adicionales

- [Documentación de Canva Connect API](https://www.canva.dev/docs/connect)
- [Canva Developer Portal](https://www.canva.com/developers/integrations/connect-api)
- [Starter Kit de Canva](https://github.com/canva-sdks/canva-connect-api-starter-kit)
- [Documentación de MCP](https://modelcontextprotocol.io/) 