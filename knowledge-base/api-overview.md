# API Overview

> **Summary**: TTS OpenAI provides a REST API for converting text, documents, and subtitles into speech. It supports multiple languages, voices, and emotional expression.
> **Related**: [authentication.md](./authentication.md), [endpoints.md](./endpoints.md), [voices.md](./voices.md)

---

## Base URL

```
https://api.ttsopenai.com/uapi/v1
```

## Capabilities

| Capability | Description |
|-----------|-------------|
| Text-to-speech | Convert plain text to audio |
| Document-to-speech | Convert `.txt`, `.docx`, `.pdf`, `.srt` files to audio |
| Story maker | Narrate text or subtitle files as stories |
| Emotion/vibe | Express speech with emotional context (requires `audio_stable` model) |
| Custom vibes | Define reusable emotional prompts via CRUD endpoints |

## Models

| Model ID | Use case |
|----------|----------|
| `tts-1` | Standard speech generation |
| `audio_stable` | Emotion-capable speech generation |

Use `audio_stable` when passing `vibe_id`, `emotion`, or `custom_prompt` fields.
`tts-1` ignores those fields.

## Audio output

- Audio is not returned directly in the API response.
- The response contains a `uuid` to identify the job.
- The completed audio URL is delivered via **webhook** (`media_url` field).
  See [webhooks.md](./webhooks.md).

## Rate limits

_Not yet documented._ Check [ttsopenai.com](https://ttsopenai.com) or contact support.

## Credits

- Each request consumes credits from your account balance.
- Error `NOT_ENOUGH_CREDIT` fires when balance is insufficient.
- `NOT_ENOUGH_AND_LOCK_CREDIT` fires when credit is locked (check transaction history).
- See [errors.md](./errors.md) for the full credit error table.

## Supported file types (document endpoint)

`.txt`, `.docx`, `.pdf`, `.srt` — other types return `FILE_TYPE_NOT_ALLOWED`.
PDF files must be under 400 pages.
