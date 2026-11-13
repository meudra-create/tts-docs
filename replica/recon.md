# Recon map: DJ.Studio (https://dj.studio)

## 1. Scope (defaults proposed, not yet confirmed)
- **App / platform:** DJ.Studio, native desktop app (Windows 10+, macOS Intel + Apple Silicon). No web or mobile editor. An iPhone companion app plays exported mixes via Dropbox.
- **Slice:** the core loop: import tracks -> Harmonize (auto-order) -> edit transitions on a timeline -> export a mix.
- **Audience:** your own product (assumed).
- **Method:** public pages and help center only. No account, no binary or bundle inspection, no screenshots saved (marketing images only seen as links). Every UI detail below comes from DJ.Studio's own public descriptions, so confidence is medium; the real UI must be confirmed with a trial run by you.

## 2. Sources
| source | URL | gave |
| --- | --- | --- |
| home / pitch | https://dj.studio | positioning, FAQ, integrations |
| transitions | https://dj.studio/transitions | timeline, presets, transition editor, locking |
| Harmonize | https://dj.studio/automix | auto-order, Solver, Camelot logic |
| export | https://dj.studio/export | all export targets and options |
| pricing | https://dj.studio/pricing | tiers, feature gating |
| help center | https://help.dj.studio/en/ | 12 collections (see below) |
| help: transition editor | https://help.dj.studio/en/articles/8106059-transition-editor | lanes |
| help: exporting | https://help.dj.studio/en/articles/8106079-exporting-mixes | export menu |
| help: rekordbox export | https://help.dj.studio/en/articles/8842722-export-mix-to-rekordbox | hot cues |
| help: Harmonize | https://help.dj.studio/en/articles/7878402-harmonize-previously-automix | not yet read |
| help: FX pack / stems | https://help.dj.studio/en/articles/10137876-fx-pack | not yet read |

Help center collections: Getting Started, Navigating DJ.Studio (9), Manage your DJ mixes (4), Creating & Editing Mixes (27), Exporting Mixes (8), External Software Connections (18), How-To (15), Troubleshooting (9), Billing (8), Announcements, Guides.

## 3. Screen inventory
| ID | screen | how you get there | purpose | key components | states |
| --- | --- | --- | --- | --- | --- |
| S01 | Project list / home | app launch | open, create, back up mixes | project cards, new project | empty, filled |
| S02 | Library | main tab | browse tracks from local files and connected libraries | source tree, track table (BPM, key, energy), search | empty, loading/analysing, filled |
| S03 | Playlist / Mix tab | main tab | ordered track list for the mix | track rows with BPM/key, Camelot colour + symbols, Mood/Fuzzy match column, X flag, lock icons | empty, filled, key clash (X) |
| S04 | Harmonize wizard | "Harmonize" button | auto-order tracks | Mood/Fuzzy choice, BPM/key slider, lock first/last, transitions tab (style, bars, beat-match, mix in/out), Finish | step states, running |
| S05 | Solver | click X on a clashing pair | suggest bridge tracks from library | candidate list, insert | none found |
| S06 | Studio (timeline) | "Studio" tab | DAW-style timeline of tracks and transitions | waveform lanes, beat grid, blue transition frames, drag handles, lock icon, beatmap/energy graph, video lane | playing, zoomed, locked |
| S07 | Transition editor | click a transition | edit one blend | lanes: volume, low/mid/high EQ, HP/LP filter, loop length, FX slots; preset menu; preset or manual curve | preset, manual |
| S08 | Stems / FX panel | per track (Pro+Stems) | split vocals/drums/bass/melody/instrumental, mute in transitions | stem toggles, FX pack | processing, locked by plan |
| S09 | Video tab | Studio view tab | per-track visuals | backgrounds (art, colour, image, Shadertoy, clip), spectrum/particles/waveform, text | preview |
| S10 | Export menu | "Export" top right | choose target | Record, DJ Set, Publish, Backup, Mobile | trial: disabled |
| S11 | Export > Record > Audio | export menu | MP3/WAV/FLAC render | format, master gain, auto gain, re-pitch, limiter | rendering, done |
| S12 | Export > Record > Video | export menu | MP4 up to 4K, landscape/portrait | resolution, YouTube description file | rendering |
| S13 | Export > DJ Set | export menu | playlist to live software | rekordbox/Serato/Traktor/VDJ/Engine/djay, M3U/M3U8/TXT/CSV/CUE, include audio, hot cues | none |
| S14 | Export > Ableton | export menu | .als project with automation | vertical/horizontal layout, stems flow | none |
| S15 | Publish > Mixcloud | export menu | connect account, title, description, upload | OAuth connect, tracklist timestamps | not connected, uploading |
| S16 | Settings / integrations | menu | connect rekordbox, Serato, Traktor, VDJ, Engine, djay Pro, Mixed In Key, iTunes/Apple Music, Beatport | connection list | disconnected, connected |
| S17 | Licence / trial | menu | activation, 7-day trial, plans | key entry, countdown | trial, expired, licensed |

Marketing site screens (if cloning the site, not the app): home, pricing, downloads, features pages, blog, academy, contact.

## 4. User flows
```
F01 Make a harmonised mix (core loop)
    S01 new project -> S02 pick tracks -> S03 playlist -> S04 Harmonize -> S06 timeline -> S07 refine -> S10/S11 export
    edge: missing BPM/key analysis, key clash (S05), tracks locked, file moved
F02 Fix a harmonic clash:  S03 click X -> S05 Solver -> insert bridge track -> re-run Harmonize
F03 Lock a signature transition:  S06 click lock -> re-run Harmonize -> locked pair stays
F04 Prep a live set:  S03 -> S13 export M3U or rekordbox with hot cues
F05 Publish to Mixcloud:  S15 connect -> title/description -> record+upload with timestamps
F06 YouTube video mix:  S09 set visuals -> S12 render -> description file
F07 Producer handoff:  S14 Ableton export (+ stems)
F08 Trial to purchase:  S17 -> pricing -> checkout -> activate
```
Click counts are unknown without a trial run (to measure).

## 5. Components
Track row (BPM, key, Camelot chip, energy), match indicator (Mood/Fuzzy tick, X), lock toggle, waveform lane, beat-grid timeline with zoom, transition frame with drag handles, automation lane (preset curve / manual points), preset picker + save-as-preset, FX slot, stem toggle, wizard stepper, slider (BPM/key), export format form, progress/render bar, account-connect card, countdown banner.

## 6. Inferred data model
```
Project     id, name, created_at, bpm_mode, settings (json)        evidence: .djs backup file; confidence high
Track       id, source (file|rekordbox|serato|...|beatport), path/uri, title, artist, bpm, key, energy, phrases (json), beatgrid
            evidence: track analysis section on /automix; confidence high
MixItem     id, project_id, track_id, position, start_at, in_point, out_point, locked, edits (cuts/loops/pastes)   confidence medium
Transition  id, from_item, to_item, preset_id, start_beat, length_beats, locked, curves (volume, eq_low/mid/high, hp, lp, loop, fx[]), stem_mutes
            evidence: transition editor lanes; confidence high
Preset      id, name, curves (json), is_default                      confidence high
Stem        track_id, vocals|drums|bass|melody|instrumental file ref confidence medium
VideoLane   project_id, track_id, background, visualiser, text       confidence medium
Export      id, project_id, target, format, options (json)           confidence medium
Connection  id, service (mixcloud|dropbox|libraries), token          confidence medium
License     key, plan, updates_until, machines (<=2)                 evidence: pricing FAQ; confidence high
```

## 7. Hard parts
1. **Audio engine:** beatmatching, time-stretch / re-pitch, per-transition EQ/filter/FX automation rendered offline faster than real time.
2. **Analysis + Harmonize:** BPM, key, phrase detection, Camelot scoring and ordering search with locks (the product's edge); Solver.
3. **Stem separation:** needs an ML model (open-source models exist; heavy compute).
4. Library importers (rekordbox, Serato, Traktor, VDJ, Engine), Ableton .als writer, rekordbox cue export: reverse-engineered formats, fragile.
5. Native desktop packaging (Electron/Tauri + native audio) on two OSes.

## 8. What cannot be cloned (skip)
- Beatport streaming catalogue and Mixed In Key's analysis/licensing (partner deals).
- DJ.Studio's trademarks, logos, copy, tutorials, academy content, Trustpilot reviews.
- Their analysis algorithms and Harmonize scoring: rebuild from the public Camelot-wheel rules, not their code.
- Music itself: the user brings their own files.

## 9. Size
17 screens, 8 flows, ~10 entities. **XL** as a whole. Rescope to **L** by cutting to: library (local files only), Harmonize, timeline + transition editor with EQ/volume/filters, MP3/WAV export, M3U export. Defer stems, video, Ableton, Mixcloud, library integrations.
