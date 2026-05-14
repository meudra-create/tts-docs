<template>
  <div class="not-prose my-8 overflow-x-auto">
    <svg
      width="705"
      height="230"
      viewBox="0 0 705 230"
      xmlns="http://www.w3.org/2000/svg"
      style="font-family: 'DM Sans', ui-sans-serif, system-ui, sans-serif; display: block;"
      role="img"
      aria-label="TTS Query Status Flow"
    >
      <defs>
        <marker id="qg-arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon class="qg-arr-main" points="0 0, 8 3, 0 6" />
        </marker>
        <marker id="qg-arr-amber" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon class="qg-arr-amber" points="0 0, 8 3, 0 6" />
        </marker>
        <marker id="qg-arr-red" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon class="qg-arr-red" points="0 0, 8 3, 0 6" />
        </marker>
      </defs>

      <!-- Background -->
      <rect x="0.5" y="0.5" width="704" height="229" rx="12" class="qg-bg" />

      <!-- Label -->
      <text x="352.5" y="16" text-anchor="middle" dominant-baseline="middle" class="qg-title">Query Status Flow</text>

      <!-- ── MAIN FLOW NODES (top=30, height=52, center_y=56) ── -->

      <!-- API Request (blue) -->
      <rect x="15" y="30" width="85" height="52" rx="7" class="qg-node-start" />
      <text x="57.5" y="48" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">API</text>
      <text x="57.5" y="64" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Request</text>

      <!-- Arrow → -->
      <line x1="100" y1="56" x2="115" y2="56" class="qg-line" stroke-width="1.5" marker-end="url(#qg-arr)" />

      <!-- Converting (status 1) -->
      <rect x="115" y="30" width="100" height="52" rx="7" class="qg-node-proc" />
      <text x="165" y="48" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Converting</text>
      <text x="165" y="64" text-anchor="middle" dominant-baseline="middle" class="qg-text-status">status: 1</text>

      <!-- Arrow → -->
      <line x1="215" y1="56" x2="230" y2="56" class="qg-line" stroke-width="1.5" marker-end="url(#qg-arr)" />

      <!-- Joining Audio (status 12) -->
      <rect x="230" y="30" width="100" height="52" rx="7" class="qg-node-proc" />
      <text x="280" y="42" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Joining</text>
      <text x="280" y="56" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Audio</text>
      <text x="280" y="70" text-anchor="middle" dominant-baseline="middle" class="qg-text-status">status: 12</text>

      <!-- Arrow → -->
      <line x1="330" y1="56" x2="345" y2="56" class="qg-line" stroke-width="1.5" marker-end="url(#qg-arr)" />

      <!-- Merging Audio (status 13) -->
      <rect x="345" y="30" width="100" height="52" rx="7" class="qg-node-proc" />
      <text x="395" y="42" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Merging</text>
      <text x="395" y="56" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Audio</text>
      <text x="395" y="70" text-anchor="middle" dominant-baseline="middle" class="qg-text-status">status: 13</text>

      <!-- Arrow → -->
      <line x1="445" y1="56" x2="460" y2="56" class="qg-line" stroke-width="1.5" marker-end="url(#qg-arr)" />

      <!-- Downloading Audio (status 14) -->
      <rect x="460" y="30" width="115" height="52" rx="7" class="qg-node-proc" />
      <text x="517.5" y="42" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Downloading</text>
      <text x="517.5" y="56" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Audio</text>
      <text x="517.5" y="70" text-anchor="middle" dominant-baseline="middle" class="qg-text-status">status: 14</text>

      <!-- Arrow → -->
      <line x1="575" y1="56" x2="590" y2="56" class="qg-line" stroke-width="1.5" marker-end="url(#qg-arr)" />

      <!-- Completed (status 2) -->
      <rect x="590" y="30" width="100" height="52" rx="7" class="qg-node-success" />
      <text x="640" y="48" text-anchor="middle" dominant-baseline="middle" class="qg-text-success">Completed</text>
      <text x="640" y="64" text-anchor="middle" dominant-baseline="middle" class="qg-text-success-status">status: 2  ✓</text>

      <!-- ── BRANCH: Reworking (below Converting) ── -->

      <!-- Down arrow: Converting bottom → Reworking top -->
      <line x1="165" y1="82" x2="165" y2="140" class="qg-line-amber" stroke-width="1.5" marker-end="url(#qg-arr-amber)" />

      <!-- Reworking (status 11) -->
      <rect x="115" y="140" width="100" height="50" rx="7" class="qg-node-retry" />
      <text x="165" y="158" text-anchor="middle" dominant-baseline="middle" class="qg-text-main">Reworking</text>
      <text x="165" y="174" text-anchor="middle" dominant-baseline="middle" class="qg-text-retry-status">status: 11</text>

      <!-- Loop arrow: Reworking left → Converting left -->
      <path d="M 115 165 C 88 165, 88 56, 115 56" class="qg-path-amber" stroke-width="1.5" fill="none" marker-end="url(#qg-arr-amber)" />

      <!-- ── BRANCH: Error (below Merging Audio) ── -->

      <!-- Down dashed arrow: Merging Audio bottom → Error top -->
      <line x1="395" y1="82" x2="395" y2="140" class="qg-line-red" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#qg-arr-red)" />

      <!-- Error (status 3) -->
      <rect x="345" y="140" width="100" height="50" rx="7" class="qg-node-error" />
      <text x="395" y="158" text-anchor="middle" dominant-baseline="middle" class="qg-text-error">Error</text>
      <text x="395" y="174" text-anchor="middle" dominant-baseline="middle" class="qg-text-error-status">status: 3  ✕</text>

      <!-- Note -->
      <text x="352.5" y="212" text-anchor="middle" dominant-baseline="middle" class="qg-note">Any processing stage can result in an error</text>
    </svg>
  </div>
</template>

<style scoped>
/* Background */
.qg-bg { fill: #f9fafb; stroke: #e5e7eb; stroke-width: 1; }
:global(.dark) .qg-bg { fill: #111827; stroke: #1f2937; }

/* Title */
.qg-title { fill: #9ca3af; font-size: 9.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; }
:global(.dark) .qg-title { fill: #6b7280; }

/* ── Nodes ── */
.qg-node-start  { fill: #eff6ff; stroke: #93c5fd; stroke-width: 1.5; }
:global(.dark) .qg-node-start  { fill: #1e3a5f; stroke: #3b82f6; }

.qg-node-proc   { fill: #fffbeb; stroke: #fcd34d; stroke-width: 1.5; }
:global(.dark) .qg-node-proc   { fill: #2d1f00; stroke: #d97706; }

.qg-node-success { fill: #f0fdf4; stroke: #86efac; stroke-width: 1.5; }
:global(.dark) .qg-node-success { fill: #052e16; stroke: #16a34a; }

.qg-node-retry  { fill: #fff7ed; stroke: #fdba74; stroke-width: 1.5; }
:global(.dark) .qg-node-retry  { fill: #2d1200; stroke: #ea580c; }

.qg-node-error  { fill: #fef2f2; stroke: #fca5a5; stroke-width: 1.5; }
:global(.dark) .qg-node-error  { fill: #2d0000; stroke: #dc2626; }

/* ── Text ── */
.qg-text-main         { fill: #1f2937; font-size: 11px; font-weight: 600; }
:global(.dark) .qg-text-main   { fill: #f3f4f6; }

.qg-text-status       { fill: #92400e; font-size: 9.5px; }
:global(.dark) .qg-text-status { fill: #fcd34d; }

.qg-text-success      { fill: #14532d; font-size: 11px; font-weight: 600; }
:global(.dark) .qg-text-success { fill: #bbf7d0; }

.qg-text-success-status       { fill: #15803d; font-size: 9.5px; }
:global(.dark) .qg-text-success-status { fill: #4ade80; }

.qg-text-retry-status         { fill: #c2410c; font-size: 9.5px; }
:global(.dark) .qg-text-retry-status   { fill: #fb923c; }

.qg-text-error        { fill: #7f1d1d; font-size: 11px; font-weight: 600; }
:global(.dark) .qg-text-error  { fill: #fecaca; }

.qg-text-error-status         { fill: #b91c1c; font-size: 9.5px; }
:global(.dark) .qg-text-error-status   { fill: #f87171; }

.qg-note { fill: #9ca3af; font-size: 9.5px; font-style: italic; }
:global(.dark) .qg-note { fill: #4b5563; }

/* ── Lines ── */
.qg-line       { stroke: #9ca3af; }
:global(.dark) .qg-line       { stroke: #6b7280; }

.qg-line-amber { stroke: #d97706; }
:global(.dark) .qg-line-amber { stroke: #f59e0b; }

.qg-path-amber { stroke: #d97706; }
:global(.dark) .qg-path-amber { stroke: #f59e0b; }

.qg-line-red   { stroke: #dc2626; }
:global(.dark) .qg-line-red   { stroke: #ef4444; }

/* ── Arrow marker fills ── */
.qg-arr-main  { fill: #9ca3af; }
:global(.dark) .qg-arr-main  { fill: #6b7280; }

.qg-arr-amber { fill: #d97706; }
:global(.dark) .qg-arr-amber { fill: #f59e0b; }

.qg-arr-red   { fill: #dc2626; }
:global(.dark) .qg-arr-red   { fill: #ef4444; }
</style>
