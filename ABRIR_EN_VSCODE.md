# Abrir el proyecto en Visual Studio Code

Pasos para que cualquier persona (por ejemplo tu tutora) pueda abrir y ejecutar el proyecto en su PC con VS Code.

---

## 1. Tener el proyecto en la PC

- Copiar la carpeta del proyecto (por ejemplo `saphiro-nuevo` o `saphiro-condominio`) a una ruta conocida, por ejemplo:
  - `C:\Users\TuUsuario\Desktop\saphiro-nuevo`
- O clonar el repositorio en esa carpeta si usan Git.

---

## 2. Abrir la carpeta en VS Code

1. Abrir **Visual Studio Code**.
2. Menú **File → Open Folder** (o **Archivo → Abrir carpeta**).
3. Ir a la carpeta del proyecto (la que contiene `manage.py` y la carpeta `venv`).
4. Pulsar **Seleccionar carpeta**.

La raíz del proyecto debe ser la carpeta donde están `manage.py`, `venv`, `condominio`, `condominio_app`, etc.

---

## 3. Usar el entorno virtual (venv)

1. En VS Code, abrir la **Terminal** (menú **Terminal → New Terminal** o `` Ctrl+` ``).
2. Si el proyecto ya tiene la carpeta `venv`:
   - VS Code puede preguntar si quieres usar el intérprete de esa carpeta. Pulsa **Yes** / **Sí**.
   - O bien: `Ctrl+Shift+P` → escribir **Python: Select Interpreter** → elegir el que muestre `./venv/Scripts/python.exe` o `.\venv\Scripts\python.exe`.
3. Con **python.terminal.activateEnvironment** en la configuración, al abrir una terminal nueva dentro del proyecto se activará solo el `venv`.

Si **no** existe la carpeta `venv` en el proyecto, créala en esa misma carpeta desde la terminal de VS Code:

```cmd
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Luego en VS Code: **Python: Select Interpreter** y elige `.\venv\Scripts\python.exe`.

---

## 4. Ejecutar el servidor Django

**Opción A – Terminal (recomendado)**

En la terminal de VS Code (ya con el venv activado si configuraste el intérprete):

```cmd
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000/**

**Opción B – Botón Run / F5**

1. Ir al panel **Run and Debug** (icono de “play” con bicho o **Ctrl+Shift+D**).
2. Arriba elegir la configuración **“Django: runserver”**.
3. Pulsar el botón verde **Run** o **F5**.

El servidor se inicia y la app estará en **http://127.0.0.1:8000/**.

---

## 5. Extensión recomendada

- **Python** (Microsoft): para que funcionen el intérprete, la terminal automática y el debug de Django.

Si al usar F5 dice que falta el depurador, instala la extensión **Python** y vuelve a intentar.

---

## Resumen rápido

1. **File → Open Folder** → carpeta del proyecto (donde está `manage.py`).
2. **Python: Select Interpreter** → `.\venv\Scripts\python.exe`.
3. Terminal: `python manage.py runserver` **o** F5 con **“Django: runserver”**.
4. Navegador: **http://127.0.0.1:8000/**.
