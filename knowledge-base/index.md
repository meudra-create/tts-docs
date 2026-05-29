# TTS OpenAI API — Knowledge Base Index

Master index. Update this file whenever a page is added, renamed, or significantly changed.

## Pages

| Page | Summary | Last significant change |
|------|---------|------------------------|
| [api-overview.md](./api-overview.md) | Capabilities, models, base URL, rate limits | 2026-05-29 |
| [authentication.md](./authentication.md) | API key format, request header, security guidance | 2026-05-29 |
| [endpoints.md](./endpoints.md) | All API endpoints with parameters and response shapes | 2026-05-29 |
| [webhooks.md](./webhooks.md) | Webhook setup, signature verification, event types and payloads | 2026-05-29 |
| [errors.md](./errors.md) | HTTP status codes, error codes, troubleshooting steps | 2026-05-29 |
| [voices.md](./voices.md) | Voice IDs, language support, emotion/vibe system, custom vibes | 2026-05-29 |

## Key facts (quick reference)

- **Base URL**: `https://api.ttsopenai.com/uapi/v1`
- **Auth header**: `x-api-key: YOUR_API_KEY`
- **Models**: `tts-1` (standard), `audio_stable` (emotion-capable)
- **Max text length**: 10,000 characters
- **Max PDF size**: 400 pages
- **Webhook retries**: 3 attempts, 1-hour interval
- **Voice IDs**: prefix `OA` — see [voices.md](./voices.md)

## Known gaps

- Rate limits: not publicly documented; mark `_Not yet documented_` in [api-overview.md](./api-overview.md)
- Story endpoint: partially documented; see [endpoints.md](./endpoints.md)
- Voice list: full catalogue not in docs; only example `OA001` confirmed
