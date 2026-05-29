# Errors

> **Summary**: The API uses standard HTTP status codes plus a structured JSON error body with `error_code` and `message`. Most errors are caller mistakes, not server faults.
> **Related**: [authentication.md](./authentication.md), [api-overview.md](./api-overview.md)

---

## Error response shape

```json
{
  "detail": {
    "error_code": "API_KEY_NOT_FOUND",
    "message": "Api key is not found"
  }
}
```

Use `error_code` for programmatic handling; `message` for logging.

---

## HTTP status codes

| Code | Meaning | Common cause |
|------|---------|--------------|
| `200` | OK | Request succeeded |
| `400` | Bad Request | Invalid input, missing required field, or malformed body |
| `401` | Unauthorized | Missing or invalid API key |
| `403` | Forbidden | Valid key, but no permission for this resource |
| `404` | Not Found | Endpoint or resource does not exist |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server-side fault — retry later |
| `503` | Service Unavailable | Server overload or maintenance |

---

## Error codes

### Auth errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `API_KEY_REQUIRED` | 401 | `x-api-key` header absent | Add the header |
| `API_KEY_NOT_FOUND` | 401 | Key string not recognized | Check for typos; regenerate if needed |
| `USER_NOT_FOUND` | 401 | Account linked to key not found | Re-check account status |
| `FORBIDDEN` | 403 | Key valid, no permission | Check plan or contact support |

### Credit errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `NOT_ENOUGH_CREDIT` | 402 | Balance below job cost | Top up account |
| `NOT_ENOUGH_AND_LOCK_CREDIT` | 402 | Credit is locked | Check transaction history |

### Input errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `TEXT_TOO_LONG` | 400 | Input exceeds 10,000 characters | Split the text |
| `MAXIMUM_FILE_SIZE_EXCEED` | 400 | File too large | Reduce file size |
| `FILE_TYPE_NOT_ALLOWED` | 400 | Unsupported file extension | Use `.txt`, `.docx`, `.pdf`, or `.srt` |
| `PDF_MORE_THAN_400_PAGES` | 400 | PDF over 400 pages | Split the PDF |

### Plan/quota errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `PLAN_MAX_FILE_SIZE_EXCEED` | 403 | File exceeds plan's size limit | Upgrade plan |
| `PLAN_TOTAL_FILE_EXCEED` | 403 | Monthly file quota exceeded | Upgrade plan or wait for reset |
| `PREMIUM_PLAN_REQUIRED` | 403 | Feature requires premium plan | Upgrade plan |

### Voice errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `VOICE_NOT_FOUND` | 404 | `voice_id` not in system | Check [voices.md](./voices.md) for valid IDs |
| `VOICE_NOT_ACTIVE` | 403 | Voice exists but is deactivated | Activate in account settings or choose another voice |

### System errors

| Error code | HTTP | Meaning | Fix |
|-----------|------|---------|-----|
| `SYSTEM_ERROR` | 500 | Internal fault | Retry with exponential backoff; contact support if persistent |

---

## Troubleshooting checklist

1. Read the `error_code` and `message` in the response body.
2. Check `x-api-key` is present and correct.
3. Verify input data: text length, file type, file size.
4. Check account balance and plan limits.
5. For `500`/`503`: wait and retry — these are transient.
6. Contact support with the full request/response if unresolved.
