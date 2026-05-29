# Endpoints

> **Summary**: Four main endpoints — text, document, story-maker, and emotion. All are POST requests to `https://api.ttsopenai.com/uapi/v1`. Responses are asynchronous; audio arrives via webhook.
> **Related**: [api-overview.md](./api-overview.md), [webhooks.md](./webhooks.md), [voices.md](./voices.md), [errors.md](./errors.md)

---

## Common patterns

- All endpoints require `x-api-key` header. See [authentication.md](./authentication.md).
- Responses return a `uuid`. Audio is **not** in the response — it is delivered asynchronously via webhook `media_url`. See [webhooks.md](./webhooks.md).
- `status` codes are shared across all job endpoints — see [Job status codes](#job-status-codes) below.

---

## POST /text-to-speech

Convert plain text to speech.

**URL**: `POST https://api.ttsopenai.com/uapi/v1/text-to-speech`

### Request body

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `model` | string | No | `tts-1` | `tts-1` or `tts-1-hd` |
| `voice_id` | string | No | `OA001` | See [voices.md](./voices.md) |
| `speed` | float | No | `1` | Range: 1–4 |
| `input` | string | **Yes** | — | Max 10,000 characters |

### Response body (`result` object)

| Field | Type | Notes |
|-------|------|-------|
| `uuid` | string | Job identifier — use for webhook matching |
| `voice_id` | string | Voice used |
| `speed` | float | Speed used |
| `model` | string | Model used |
| `tts_input` | string | Text submitted |
| `estimated_credit` | integer | Credit estimate before processing |
| `used_credit` | integer | Actual credits consumed |
| `status` | integer | See [Job status codes](#job-status-codes) |
| `status_percentage` | integer | Progress 0–100 |
| `error_message` | string | Non-empty on failure |
| `speaker_name` | string | Human-readable voice name |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

---

## POST /document-to-speech

Convert uploaded document files to speech.

**URL**: `POST https://api.ttsopenai.com/uapi/v1/document-to-speech`
**Content-Type**: `multipart/form-data`

### Request fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `model` | string | No | `tts-1` or `tts-1-hd` |
| `voice_id` | string | No | See [voices.md](./voices.md) |
| `speed` | float | No | Range: 1–4 |
| `file` | file | **Yes** | `.txt`, `.docx`, `.pdf`, `.srt` |
| `file_password` | string | No | For password-protected files |

Limits: max PDF size is 400 pages. Other types subject to plan file-size limits.

---

## POST /story-maker

Convert multiple text blocks into a single narrated audio story.

**URL**: `POST https://api.ttsopenai.com/uapi/v1/story-maker`

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Story name |
| `blocks` | array | Yes | One or more block objects |

Each **block** object:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Block name |
| `input` | string | Yes | Text for this block |
| `voice_id` | string | Yes | See [voices.md](./voices.md) |
| `model` | string | Yes | `tts-1` or `audio_stable` |
| `speed` | float | No | Range: 1–4 |
| `silence_before` | integer | No | Silence in seconds before block |
| `emotion` | string | No | E.g. `"neutral"`, `"happy"` |
| `duration` | integer | No | Target duration (0 = auto) |

Different blocks can use different voices and emotions within the same story.

---

## POST /text-to-speech-advanced

Emotion-expressive text-to-speech. Requires `audio_stable` model.

**URL**: `POST https://api.ttsopenai.com/uapi/v1/text-to-speech-advanced`

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `model` | string | **Yes** | Must be `audio_stable` |
| `voice_id` | string | No | See [voices.md](./voices.md) |
| `speed` | float | No | Range: 1–4 |
| `input` | string | **Yes** | Max 10,000 characters |
| `vibe_id` | number | No | ID of a master or custom vibe |
| `emotion` | string | No | E.g. `"happy"`, `"sad"`, `"excited"` |
| `custom_prompt` | string | No | Natural language expression instructions |

Response shape is the same as `/text-to-speech` plus `vibe_id`, `emotion`, and `custom_prompt` echoed back.

---

## Custom Vibes CRUD

Manage reusable emotional vibe definitions. See [voices.md](./voices.md) for the full table.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/custom-vibes` | List user's custom vibes |
| `POST` | `/custom-vibes` | Create a custom vibe |
| `GET` | `/custom-vibes/{id}` | Get a single custom vibe |
| `PUT` | `/custom-vibes/{id}` | Update a custom vibe |
| `DELETE` | `/custom-vibes/{id}` | Delete a custom vibe |
| `GET` | `/master-vibes` | List platform-provided vibes |

---

## Job status codes

Shared across all job-creating endpoints.

| Code | Name | Meaning |
|------|------|---------|
| `1` | Converting | Processing started |
| `2` | Completed | Audio ready; `media_url` available via webhook |
| `3` | Error | Processing failed; `error_message` populated |
| `11` | Reworking | Retrying a failed step |
| `12` | Joining Audio | Combining audio segments |
| `13` | Merging Audio | Merging merged segments |
| `14` | Downloading Audio | Fetching final file |

Terminal states: `2` (success) and `3` (failure). All others are intermediate.
