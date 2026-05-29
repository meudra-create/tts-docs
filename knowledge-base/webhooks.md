# Webhooks

> **Summary**: TTS OpenAI delivers job results asynchronously via HTTP POST webhooks. You register a URL, and the API calls it with job status and the audio download URL when processing completes.
> **Related**: [endpoints.md](./endpoints.md), [authentication.md](./authentication.md)

---

## Setup

1. Register your webhook URL at:
   `https://ttsopenai.com/profile/integration/webhook`
2. The URL must be publicly accessible and accept `POST` requests.
3. Your server must respond `200 OK`. Any other status triggers a retry.

**Retry policy**: 3 attempts, 1-hour delay between each. Total window: ~2 hours after original delivery.

---

## Signature verification

Each webhook request includes an `x-signature` header containing an HMAC-SHA256 signature of the request body signed with TTS OpenAI's private key.

**Always verify this signature** before processing the payload. Unverified webhooks can be spoofed.

### Verification steps

1. Download the public key: `https://docs.ttsopenai.com/assets/uapi_public_key.pem`
2. Compute MD5 hash of the `event` UUID from the request body.
3. Verify the `x-signature` header against that hash using RSA-SHA256.

```python
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from hashlib import md5

def verify_signature(event_uuid: str, signature_hex: str, public_key_path: str) -> bool:
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    event_hash = md5(event_uuid.encode()).digest()
    try:
        public_key.verify(bytes.fromhex(signature_hex), event_hash, padding.PKCS1v15(), hashes.SHA256())
        return True
    except Exception:
        return False
```

If verification fails, discard the request.

---

## Payload shape

```json
{
  "event": "TTS_TEXT_SUCCESS",
  "uuid": "<event-uuid>",
  "data": {
    "uuid": "<job-uuid>",
    "media_url": "https://...",
    "tts_input": "...",
    "voice_id": "OA001",
    "speed": 1,
    "status": 2,
    "model": "tts-1",
    "used_credit": 54,
    "speaker_name": "Alloy",
    "error_message": "",
    "status_percentage": 100,
    "created_at": "2024-11-21T12:48:40",
    "updated_at": "2024-11-21T12:48:40"
  }
}
```

`data.uuid` matches the `uuid` returned by the original endpoint response — use it to correlate with your local records.

`media_url` is the download URL for the audio file. Present only when `event` is a `_SUCCESS` type.

---

## Event types

| Event | Trigger |
|-------|---------|
| `TTS_TEXT_SUCCESS` | `/text-to-speech` job completed |
| `TTS_TEXT_FAILED` | `/text-to-speech` job failed |
| `TTS_DOCUMENT_SUCCESS` | `/document-to-speech` job completed |
| `TTS_DOCUMENT_FAILED` | `/document-to-speech` job failed |

_Note: Story Maker and Emotion webhook event names are not yet documented._

---

## Testing

You can send a test webhook event from the integration settings page:
`https://ttsopenai.com/profile/integration/webhook`

You can also use [RequestBin](https://requestbin.com/) to inspect raw webhook payloads during development.
