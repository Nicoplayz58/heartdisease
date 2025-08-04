
# 🧠 Heart Disease Dashboard

Este proyecto es una aplicación web interactiva construida con [Plotly Dash](https://dash.plotly.com/) que visualiza y analiza datos relacionados con enfermedades cardíacas. Utiliza una base de datos PostgreSQL y está completamente dockerizado para facilitar su despliegue.

---

## 📦 Estructura del Proyecto

```
├── app.py
├── Dockerfile
├── docker-compose.yml
├── heart.csv
├── init.sql
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo ejecutar el proyecto

1. **Clona este repositorio**

```bash
git clone https://github.com/Nicoplayz58/heartdisease.git
cd heartdisease
```

2. **Ejecuta con Docker Compose**

```bash
docker-compose up --build
```

3. **Abre el navegador en:**

```
http://localhost:8050/
```

---

## 🗃️ Base de Datos

- **Motor:** PostgreSQL
- **Nombre de la BD:** `heart`
- **Tabla creada:** `heart_data`
- **Carga inicial:** A partir del archivo `heart.csv` mediante el script SQL `init.sql`.

---

## 📊 Funcionalidades del Dashboard

- Visualización de variables cardíacas
- Análisis de distribución por edad, sexo y target
- Gráficas interactivas
- Conexión directa a la base de datos

---

## 🛠️ Requisitos

- Docker y Docker Compose instalados

Si deseas correr el script por fuera de Docker:

```bash
pip install pandas sqlalchemy psycopg2-binary
```

---

## 👨‍💻 Autor

Hecho por Nicolás  
Universidad del Norte - Ciencia de Datos
