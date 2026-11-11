-- SQLite (local, one file per project library). Times in ms/beats are integers; timestamps are ISO-8601 UTC text.
pragma foreign_keys = on;

create table projects (
  id text primary key,
  name text not null,
  settings text not null default '{}' check (json_valid(settings)),
  created_at text not null default (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  updated_at text not null default (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

create table tracks (
  id text primary key,
  source text not null default 'file' check (source in ('file','m3u','itunes','rekordbox','serato','traktor','vdj','engine')),
  path text not null unique,
  title text, artist text, duration_ms integer not null check (duration_ms > 0),
  bpm real, camelot text check (camelot is null or camelot glob '[0-9]*[AB]'),
  energy integer check (energy is null or energy between 1 and 10),
  beatgrid text not null default '[]' check (json_valid(beatgrid)),   -- first beat offset + bpm segments
  phrases text not null default '[]' check (json_valid(phrases)),
  analysis_status text not null default 'pending' check (analysis_status in ('pending','running','done','error')),
  created_at text not null default (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
create index tracks_bpm on tracks (bpm);
create index tracks_camelot on tracks (camelot);

create table presets (
  id text primary key,
  name text not null,
  curves text not null check (json_valid(curves)),   -- {volume,eq_low,eq_mid,eq_high,hp,lp,loop,fx[]}
  is_builtin integer not null default 0 check (is_builtin in (0,1)),
  is_default integer not null default 0 check (is_default in (0,1))
);
create unique index presets_one_default on presets (is_default) where is_default = 1;

create table mix_items (
  id text primary key,
  project_id text not null references projects(id) on delete cascade,
  track_id text not null references tracks(id) on delete restrict,
  position integer not null check (position >= 0),
  in_ms integer not null default 0 check (in_ms >= 0),
  out_ms integer,                      -- null = end of track
  gain_db real not null default 0,
  locked integer not null default 0 check (locked in (0,1)),
  unique (project_id, position)  -- reorder in one tx: add 1000000 to all positions, then write finals
);
create index mix_items_track on mix_items (track_id);

create table transitions (
  id text primary key,
  project_id text not null references projects(id) on delete cascade,
  from_item_id text not null references mix_items(id) on delete cascade,
  to_item_id text not null references mix_items(id) on delete cascade,
  preset_id text references presets(id) on delete set null,
  start_beat real not null,            -- on the outgoing track's grid
  length_beats real not null check (length_beats > 0),
  curves text not null default '{}' check (json_valid(curves)),  -- manual overrides per lane
  locked integer not null default 0 check (locked in (0,1)),
  unique (from_item_id, to_item_id),
  check (from_item_id <> to_item_id)
);
create index transitions_project on transitions (project_id);

create table exports (
  id text primary key,
  project_id text not null references projects(id) on delete cascade,
  kind text not null check (kind in ('audio','playlist')),
  format text not null check (format in ('mp3','wav','flac','m3u','m3u8','txt','csv','cue')),
  options text not null default '{}' check (json_valid(options)),
  output_path text, status text not null default 'queued' check (status in ('queued','running','done','error')),
  error text,
  created_at text not null default (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
create index exports_project on exports (project_id);
