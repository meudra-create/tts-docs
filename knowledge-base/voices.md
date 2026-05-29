# Voices & Emotion System

> **Summary**: Voices are identified by `voice_id` strings with an `OA` prefix. The emotion system adds expressive layering via vibes (predefined or custom) and inline `emotion`/`custom_prompt` fields, available only with the `audio_stable` model.
> **Related**: [endpoints.md](./endpoints.md), [api-overview.md](./api-overview.md)

---

## Voice IDs

Voice IDs use the format `OA###`. Example: `OA001` (default, "Alloy").

The full catalogue is available in the Voice Library:
`https://ttsopenai.com/voice-library`

Voice IDs are accepted by all endpoints. If a voice is not found or not active, see [errors.md](./errors.md#voice-errors).

---

## Emotion system

The emotion system is layered — you can use any combination of the three controls:

| Control | Type | Where used | Effect |
|---------|------|-----------|--------|
| `vibe_id` | integer | `/text-to-speech-advanced`, story blocks | Apply a predefined emotional profile |
| `emotion` | string | `/text-to-speech-advanced`, story blocks | Name a specific emotion (e.g. `"happy"`, `"sad"`) |
| `custom_prompt` | string | `/text-to-speech-advanced` | Natural-language instruction for expression style |

All three require `model: "audio_stable"`. They are ignored by `tts-1`.

Example emotion strings: `"neutral"`, `"happy"`, `"sad"`, `"excited"`, `"calm"`, `"angry"`, `"surprised"`, `"amazed"`.

---

## Master vibes

Platform-provided vibes. Retrieved via:
`GET https://api.ttsopenai.com/uapi/v1/master-vibes`

Use `vibe_id` from this list to apply a preset emotional profile. Full list: _Not yet documented in public docs._

---

## Custom vibes

User-defined reusable emotional profiles. Backed by the custom vibes CRUD API.

### Custom vibe object

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | Used as `vibe_id` in speech requests |
| `type` | string | Always `"user_vibe"` for custom vibes |
| `vibe` | string | Human-readable name |
| `prompt` | string | Natural-language expression instruction |
| `user_id` | integer | Owner's account ID |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

### CRUD endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/uapi/v1/custom-vibes` | List all your custom vibes |
| `POST` | `/uapi/v1/custom-vibes` | Create a new vibe (`vibe` + `prompt` body) |
| `GET` | `/uapi/v1/custom-vibes/{id}` | Get a specific vibe |
| `PUT` | `/uapi/v1/custom-vibes/{id}` | Update `vibe` or `prompt` |
| `DELETE` | `/uapi/v1/custom-vibes/{id}` | Delete a vibe |

### Create request body

```json
{
  "vibe": "Motivational Coach",
  "prompt": "Speak with high energy, enthusiasm, and encouragement to inspire action"
}
```

### Example custom vibes

| Name | Prompt idea |
|------|------------|
| Professional Presenter | Confident and authoritative, as if presenting to a business audience |
| Storyteller | Warm, engaging tone with dramatic pauses and expressive inflection |
| Motivational Coach | High energy, enthusiastic, encouraging — inspires action |

---

## Story Maker: per-block voice and emotion

In the `/story-maker` endpoint, each block can have its own `voice_id`, `emotion`, and `model`. This allows mixing voices and emotional registers within a single audio piece.

See [endpoints.md](./endpoints.md#post-story-maker) for the full block schema.
