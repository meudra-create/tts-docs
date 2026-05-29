# Authentication

> **Summary**: All requests require an API key in the `x-api-key` header. Keys are managed at ttsopenai.com/profile/integration/api-keys.
> **Related**: [api-overview.md](./api-overview.md), [errors.md](./errors.md)

---

## API key

Every request must include the key as an HTTP header:

```
x-api-key: YOUR_API_KEY
```

### Obtaining a key

Create and manage keys at:
`https://ttsopenai.com/profile/integration/api-keys`

### Rotating a key

Delete the compromised key in the dashboard and create a new one.
There is no "regenerate in place" — deletion + creation is the rotation flow.

## Security rules

1. **Never expose the key client-side.** Do not embed in browser JavaScript, mobile app binaries, or public repos.
2. **Always load from an environment variable** on your backend server or from a secrets manager.
3. **Rotate immediately** if you suspect compromise.

## Error codes related to auth

| Error code | Meaning |
|-----------|---------|
| `API_KEY_REQUIRED` | Header `x-api-key` was absent from the request |
| `API_KEY_NOT_FOUND` | Key was present but not recognized |
| `USER_NOT_FOUND` | Key is valid but the associated account no longer exists |
| `FORBIDDEN` | Key is valid but lacks permission for the requested resource |

Full error reference: [errors.md](./errors.md)
