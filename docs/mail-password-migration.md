# Migración de contraseñas de correo

## Objetivo

Conservar las contraseñas originales de las cuentas de correo durante una migración desde cPanel hacia HestiaCP.

---

## Investigación realizada

### cPanel

Las cuentas de correo almacenan la contraseña utilizando:

```
SHA512-CRYPT
```

Ejemplo:

```
$6$TOOYO9ccHnLkRyfX$ZAqXdR2AHMvDafbl1GELLwprFnaaRzly...
```

Este hash es extraído por el parser desde el backup.

---

### HestiaCP

Las cuentas de correo se almacenan en:

```
/home/<USER>/conf/mail/<DOMAIN>/passwd
```

Ejemplo:

```
test:{BLF-CRYPT}$2y$05$LOLG6zV7Jjs5ffHu7zZ5k.0961gicM0GsIr4Doy0z3B12ektkQtie:prueba123:mail::/home/prueba123:100:userdb_quota_rule=*:storage=100M
```

Por defecto Hestia utiliza:

```
{BLF-CRYPT}
```

(Bcrypt)

---

## Prueba realizada

Se reemplazó manualmente el contenido del archivo `passwd`.

De:

```
{BLF-CRYPT}$2y$...
```

A:

```
{SHA512-CRYPT}$6$...
```

utilizando un hash original proveniente de un backup de cPanel.

Resultado:

✅ Autenticación correcta mediante Webmail.

No fue necesario convertir el hash.

---

## Conclusión

Dovecot acepta múltiples formatos de hash.

Por lo tanto el migrador puede:

1. Crear la cuenta mediante `v-add-mail-account`.
2. Reemplazar el hash generado por Hestia.
3. Copiar el Maildir.
4. Mantener la contraseña original del usuario.

---

## Flujo definitivo

```
Crear cuenta

↓

Reemplazar hash

↓

Copiar Maildir

↓

Finalizar migración
```

---

## Ventajas

- El usuario mantiene su contraseña.
- No es necesario conocer la contraseña en texto plano.
- No es necesario solicitar cambio de contraseña.
- Compatible con backups de cPanel.
