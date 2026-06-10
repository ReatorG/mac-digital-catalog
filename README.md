<div align="center">

  <img src="mac-catalogo-web/public/assets/mac2.png" alt="Logo del Museo de Arte Contemporáneo" width="150" />

  # MAC Digital Catalog

  **Una experiencia digital para descubrir, consultar y conectar con la colección del Museo de Arte Contemporáneo.**

  [![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
  [![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.118-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?logo=vercel&logoColor=white)](https://mac-digital-catalog.vercel.app/)
  [![Render](https://img.shields.io/badge/API-Render-46E3B7?logo=render&logoColor=black)](https://mac-digital-catalog.onrender.com/docs)

  [Ver aplicación](https://mac-digital-catalog.vercel.app/) · [Explorar API](https://mac-digital-catalog.onrender.com/docs)

</div>

---

## Sobre el proyecto

**MAC Digital Catalog** es una aplicación web full stack desarrollada para el Museo de Arte Contemporáneo (MAC). Su objetivo es transformar la consulta tradicional de una colección artística en una experiencia digital accesible, organizada e interactiva.

La plataforma permite recorrer las obras del museo, conocer a sus artistas y consultar información detallada sobre cada pieza. Además, incorpora herramientas de búsqueda, filtrado, paginación con carga infinita y una sección de comentarios que fomenta la participación de los visitantes.

El proyecto fue creado en el contexto del curso **Proyectos Interdisciplinarios III**, integrando desarrollo de software, gestión de información cultural y diseño de experiencia de usuario en una solución desplegada y funcional.

## Objetivos

- Facilitar el acceso digital al patrimonio artístico del museo.
- Centralizar la información de obras y artistas en un catálogo consultable.
- Mejorar la exploración de la colección mediante búsquedas y filtros especializados.
- Ofrecer una interfaz adaptable a computadores y dispositivos móviles.
- Promover la interacción de los usuarios por medio de comentarios sobre las obras.
- Construir una solución desacoplada, mantenible y preparada para evolucionar.

## Funcionalidades principales

### Catálogo de obras

- Visualización de obras en una cuadrícula responsiva.
- Fichas individuales con imagen, título, autor, fecha, técnica, materiales, ubicación y descripción.
- Filtros por técnica, materiales, ubicación y estado de exhibición.
- Ordenamiento y búsqueda por texto.
- Carga progresiva de resultados mediante *infinite scroll*.

### Directorio de artistas

- Exploración del listado de artistas vinculados a la colección.
- Perfil individual con datos biográficos y obras relacionadas.
- Búsqueda por nombre y navegación entre artistas y obras.
- Carga progresiva de resultados.

### Participación del visitante

- Consulta de comentarios asociados a cada obra.
- Publicación de nuevas opiniones desde la ficha de la pieza.
- Actualización inmediata de la conversación después de comentar.

### API y administración de datos

- API REST documentada automáticamente con Swagger/OpenAPI.
- Operaciones CRUD para artistas y obras.
- Creación y consulta de comentarios.
- Búsqueda independiente de obras y artistas.
- Paginación de resultados y filtros avanzados para las obras.
- Endpoint de salud para comprobar la conexión entre la API y PostgreSQL.

## Tecnologías

| Área | Tecnologías |
| --- | --- |
| Frontend | Next.js 16, React 19, JavaScript, CSS, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Base de datos | PostgreSQL, Psycopg 3 |
| Arquitectura | API REST y separación por capas: aplicación, dominio e infraestructura |
| Calidad | ESLint y validación de datos con Pydantic |
| Despliegue | Vercel para el frontend y Render para la API |

## Estructura del repositorio

```text
MAC-Digital-Catalog/
├── backend/
│   ├── src/app/
│   │   ├── artist/          # Artistas: controladores, dominio y repositorio
│   │   ├── artwork/         # Obras: controladores, dominio y repositorio
│   │   ├── comment/         # Comentarios asociados a las obras
│   │   ├── search/          # Busqueda de obras y artistas
│   │   ├── config/          # Variables de entorno y configuración CORS
│   │   ├── database.py      # Conexión e inicialización de PostgreSQL
│   │   └── main.py          # Punto de entrada de FastAPI
│   ├── requirements.txt
│   └── rundev.py
├── mac-catalogo-web/
│   ├── app/                 # Paginas y rutas con Next.js App Router
│   ├── components/          # Navegación, filtros, búsqueda y comentarios
│   ├── lib/                 # Cliente para consumir la API
│   └── public/              # Recursos estáticos e identidad visual
└── README.md
```

## Ejecución local

### Requisitos previos

- Node.js y npm
- Python 3
- PostgreSQL
- Git

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd MAC-Digital-Catalog
```

### 2. Configurar el backend

Desde la carpeta `backend`, crea y activa un entorno virtual:

```bash
cd backend
python -m venv .venv
```

En Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Crea `backend/.env` con la configuración de PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/mac_catalog
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mac_catalog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

APP_ENV=development
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=["http://localhost:3000"]
```

Crea la base de datos `mac_catalog` en PostgreSQL y ejecuta la API:

```bash
python rundev.py
```

La API quedará disponible en:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Estado del servicio: `http://localhost:8000/health`

Las tablas necesarias se crean automáticamente al iniciar el backend.

### 3. Configurar el frontend

En otra terminal:

```bash
cd mac-catalogo-web
npm install
```

Crea `mac-catalogo-web/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Inicia el servidor de desarrollo:

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en el navegador.

> Nota: algunas vistas del frontend conservan la URL de la API desplegada de forma directa. La variable `NEXT_PUBLIC_API_BASE_URL` es utilizada por el cliente central de `lib/api.js`; para trabajar completamente contra una API local, las demás llamadas deben apuntar también a esa variable.

## Endpoints principales

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/health` | Comprueba el estado de la API y la base de datos |
| `GET` | `/artists/` | Lista artistas con paginacion y filtros |
| `GET` | `/artists/{id}` | Obtiene el perfil de un artista |
| `POST` | `/artists/` | Registra un artista |
| `PUT` | `/artists/{id}` | Actualiza un artista |
| `DELETE` | `/artists/{id}` | Elimina un artista |
| `GET` | `/artworks/` | Lista obras con paginacion y filtros |
| `GET` | `/artworks/{id}` | Obtiene el detalle de una obra |
| `GET` | `/artworks/artist/{id}` | Lista las obras de un artista |
| `POST` | `/artworks/` | Registra una obra |
| `PUT` | `/artworks/{id}` | Actualiza una obra |
| `DELETE` | `/artworks/{id}` | Elimina una obra |
| `GET` | `/comments/artwork/{id}` | Lista los comentarios de una obra |
| `POST` | `/comments/` | Publica un comentario |
| `GET` | `/search/artworks` | Busca obras por texto |
| `GET` | `/search/artists` | Busca artistas por texto |

La especificación completa y los modelos de datos se pueden consultar en la [documentación interactiva de la API](https://mac-digital-catalog.onrender.com/docs).

## Retos técnicos resueltos

- Modelado de relaciones entre artistas, obras y comentarios en PostgreSQL.
- Construcción de filtros combinables y consultas dinámicas desde la API.
- Implementación de paginación y carga infinita para explorar colecciones extensas.
- Integración de un frontend desplegado independientemente con una API REST remota.
- Organización del backend por responsabilidades para facilitar mantenimiento y pruebas futuras.
- Adaptación de la experiencia de consulta a diferentes tamaños de pantalla.

## Aprendizajes

Este proyecto demuestra experiencia práctica en desarrollo full stack, diseño de APIs, modelado de bases de datos relacionales, consumo asíncrono de servicios, interfaces responsivas y despliegue de aplicaciones modernas. También refleja la capacidad de convertir una necesidad del sector cultural en un producto digital navegable y extensible.

## Estado del proyecto

El catálogo cuenta con una versión desplegada y funcional. Entre las mejoras futuras posibles se encuentran la autenticación de usuarios, moderación de comentarios, panel administrativo, pruebas automatizadas, optimización de imágenes y unificación total de la configuración de la URL de la API.

---

<div align="center">
  Desarrollado como una solución digital para acercar el arte contemporáneo a más personas.
</div>
