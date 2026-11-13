# Architecture: DJ.Studio clone (scope L)

Built from `recon.md` (scope-reduced slice: local files, Harmonize, timeline + transition editor, MP3/WAV export, M3U export). Stems, video, Ableton, Mixcloud, library importers and licensing are deferred (could/skip).

## 1. Stack
The recon found a native desktop app, so the web default does not apply. No server, no auth, no payments in the slice: one user, one machine.

| layer | choice | why |
| --- | --- | --- |
| shell | Electron + TypeScript | one codebase for Windows and macOS, large audio/web ecosystem; Tauri is smaller but needs Rust for the audio side |
| UI | React + Vite, Tailwind with tokens from replica-design | boring, fast |
| timeline | canvas (Pixi or plain 2D canvas) for waveforms and automation lanes | DOM is too slow for long waveforms |
| database | SQLite via better-sqlite3 + Drizzle | local, zero setup, a project is a file |
| audio decode / render | ffmpeg (bundled, LGPL build) for decode, MP3/FLAC encode; WAV written directly | offline render faster than real time |
| DSP | offline graph in a Node worker using Web Audio `OfflineAudioContext` (in a hidden renderer) for EQ, filters, gain curves; rubberband (CLI/WASM) for time-stretch and re-pitch | avoids writing DSP from scratch |
| analysis | essentia.js (WASM) for BPM, key, beat grid; energy from loudness + spectral features | open source, runs locally |
| packaging | electron-builder | signed installers |
| licensing (later) | Stripe Checkout + a small licence-key service on Vercel/Cloudflare | only if you sell; not in the slice |

One database, no microservices, no backend in the slice.

## 2. Schema
`replica/schema.sql` (validated in SQLite): 6 tables.
`projects`, `tracks`, `presets`, `mix_items`, `transitions`, `exports`.
- Access rules: none needed (local single user). If a cloud sync is added later, add `user_id` + row level security on Postgres.
- Hard constraints: `unique (project_id, position)` stops two tracks sharing a slot; `unique (from_item_id, to_item_id)` gives one transition per pair; `length_beats > 0`; one default preset by partial unique index; `check` on every status and format.
- Deleting a track used in a mix is blocked (`restrict`); deleting a project cascades to its items, transitions and exports.
- Reordering: inside one transaction add 1000000 to all positions, then write final positions (the unique index is immediate in SQLite).
- Times: timestamps ISO UTC text; audio positions integer ms or beats (real). Money: not in the slice.
- Curves, beat grids and phrases are JSON validated with `json_valid`; their shape is a TypeScript type shared by UI and renderer.

## 3. API (IPC, main process <-> renderer; no network)
| channel | does | caller | input | output | flow |
| --- | --- | --- | --- | --- | --- |
| project:list / create / open / delete | manage projects | UI | id/name | project(s) | F01 |
| project:backup / restore | export/import project file | UI | path | path | F01 |
| library:addFiles | scan files/folders, enqueue analysis | UI | paths[] | track ids | F01 |
| library:list | tracks with filters (bpm, key, text) | UI | query | tracks | F01 |
| analysis:progress (event) | status per track | main | - | track id, % | F01 |
| mix:setOrder / add / remove / trim | edit playlist | UI | items | mix state | F01 |
| harmonize:run | order + place transitions | UI | track ids, mode (mood/fuzzy), bpmKeyWeight, lockedIds, transition defaults | new order + transitions | F01, F03 |
| harmonize:solve | bridge tracks for a clashing pair | UI | pair ids | candidates | F02 |
| transition:update / lock / savePreset | edit one transition | UI | id, curves | transition | F01, F03 |
| preset:list / save / setDefault | manage presets | UI | preset | preset | F01 |
| playback:preview | render a short window for audition | UI | range | audio stream | F01 |
| export:audio | offline render to mp3/wav (flac later) | UI | format, gain, limiter, re-pitch | file path + progress | F01 |
| export:playlist | m3u/m3u8/txt/csv | UI | format, includeAudio | file path | F04 |
Background jobs: analysis queue (worker pool, N = CPU cores - 1), export render queue (one at a time). No scheduled jobs, no webhooks. External APIs: none in the slice. Only user-owned files; no private endpoints of the original app.

## 4. Parts that bite
- **Beat grids:** wrong BPM or half/double tempo breaks every transition; allow manual grid edit and a half/double toggle early.
- **Time-stretch quality:** re-pitch vs stretch artefacts; keep render deterministic and test against reference files.
- **Offline render determinism:** the preview and the export must use the same graph, or the mix sounds different from what was audited.
- **Large files and memory:** decode in streamed chunks, cache peaks (waveform) to disk; a 2h mix at 44.1k stereo float is ~2 GB if held in RAM.
- **Clipping:** limiter on master; gain staging per item.
- **Paths:** moved or missing files on open; store path + size + hash, offer relink.
- **Codecs and licences:** ffmpeg build must be LGPL; MP3 encoding via LAME in ffmpeg; check patent/licence terms before distribution.
- **Cross-platform audio:** sample-rate and device differences; keep playback separate from rendering.
- **Harmonize search:** brute force on N tracks explodes; use beam search or DP with constraints (locks, fixed ends) and a time cap.
- **Idempotent analysis:** re-running must not duplicate tracks (unique path) or lose manual grid fixes.
- Legal: reproduce rules from the public Camelot wheel, not DJ.Studio's code, assets or copy.

## 5. Build order
1. **Vertical slice (ugly):** S02 library (add 3 files) -> analysis (BPM, key) -> S03 playlist -> S06 timeline with default crossfade -> S11 export MP3. Tables: projects, tracks, mix_items, transitions. Proves audio decode, analysis, render, packaging.
2. **Must-haves:** S04 Harmonize (Mood/Fuzzy, weight slider, auto transitions), S06 timeline drag/zoom/beat grid, S07 transition editor lanes (volume, EQ, HP/LP) + built-in presets, re-pitch/time-stretch, faster-than-real-time export, project save/open. Tables: presets, exports.
3. **Should-haves:** custom presets and default, transition lock, lock first/last in Harmonize, Solver (S05), WAV/FLAC, master gain/auto gain/limiter, M3U/CSV export (S13).
4. **Could-haves:** stems, FX, edits, video, Ableton, rekordbox cues, Mixcloud, library importers, licensing (S08-S10, S12, S14-S17).
5. **Fixes** from replica-entrepreneur once it has run.

## Riskiest parts
1. Audio engine: beatmatched time-stretch plus automation rendered offline, identical to the preview.
2. Reliable BPM/key/beat-grid analysis with manual correction.
3. Harmonize ordering at scale, with locks and a usable Solver.
