#!/usr/bin/env node
/**
 * Driver for tts-docs (Nuxt 3 docs site).
 * Usage: node driver.mjs <command> [args...]
 *
 * Commands:
 *   start               — start dev server (background), wait until ready
 *   stop                — kill dev server
 *   screenshot <url> <out.png>  — navigate and screenshot (default: / → /tmp/ss.png)
 *   navigate  <url> <out.png>  — alias for screenshot
 *   text      <url>            — dump visible text to stdout
 *   smoke                      — full smoke run: home + getting-started + resources page
 *
 * Environment:
 *   PORT                — dev server port (default 3001)
 *   PLAYWRIGHT_BROWSERS_PATH — path to playwright browser cache
 *   CHROMIUM_PATH       — explicit chromium binary path
 */

import { spawn, execSync } from 'child_process';
import { existsSync, writeFileSync, readFileSync } from 'fs';
import pkg from '/tmp/node_modules/playwright/index.js';
const { chromium } = pkg;
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../../..');  // tts-docs/
const PORT = process.env.PORT || 3001;
const BASE = `http://localhost:${PORT}`;
const PID_FILE = '/tmp/tts-docs-server.pid';

// ── Browser factory ──────────────────────────────────────────────────────────
async function getBrowser() {
  // Try explicit path first, then auto-detect installed Playwright chromium
  const candidates = [
    process.env.CHROMIUM_PATH,
    '/tmp/pw-browsers/chromium-1194/chrome-linux/chrome',
    '/tmp/pw-browsers/chromium_headless_shell-1194/chrome-linux/chrome-headless-shell',
  ].filter(Boolean);

  let executablePath;
  for (const p of candidates) {
    if (p && existsSync(p)) { executablePath = p; break; }
  }

  return chromium.launch({
    executablePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
  });
}

// ── Server helpers ────────────────────────────────────────────────────────────
async function waitReady(maxMs = 60_000) {
  const start = Date.now();
  while (Date.now() - start < maxMs) {
    try {
      const r = await fetch(BASE);
      if (r.status < 500) return true;
    } catch {}
    await new Promise(r => setTimeout(r, 1000));
  }
  throw new Error(`Server not ready after ${maxMs}ms`);
}

function startServer() {
  if (existsSync(PID_FILE)) {
    const pid = parseInt(readFileSync(PID_FILE, 'utf8'));
    try { process.kill(pid, 0); console.log(`Server already running (pid ${pid})`); return; } catch {}
  }
  const child = spawn('pnpm', ['dev'], {
    cwd: ROOT,
    env: { ...process.env, PORT: String(PORT) },
    detached: true,
    stdio: 'ignore',
  });
  child.unref();
  writeFileSync(PID_FILE, String(child.pid));
  console.log(`Dev server started (pid ${child.pid}) on ${BASE}`);
}

function stopServer() {
  if (!existsSync(PID_FILE)) { console.log('No PID file — server may not be running'); return; }
  const pid = parseInt(readFileSync(PID_FILE, 'utf8'));
  try {
    // Kill the whole process group (pnpm spawns nuxt as a child)
    process.kill(-pid, 'SIGTERM');
  } catch {
    try { process.kill(pid, 'SIGTERM'); } catch {}
  }
  execSync(`rm -f ${PID_FILE}`);
  console.log(`Server stopped (pid ${pid})`);
}

// ── Screenshot / navigate ────────────────────────────────────────────────────
async function screenshot(url, out) {
  url  = url  || BASE;
  out  = out  || '/tmp/ss.png';
  if (!url.startsWith('http')) url = BASE + (url.startsWith('/') ? url : '/' + url);

  const browser = await getBrowser();
  const page    = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30_000 });
  await page.screenshot({ path: out, fullPage: false });
  await browser.close();
  console.log(`Screenshot: ${out}`);
}

async function pageText(url) {
  url = url || BASE;
  if (!url.startsWith('http')) url = BASE + (url.startsWith('/') ? url : '/' + url);
  const browser = await getBrowser();
  const page    = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30_000 });
  const text = await page.evaluate(() => document.body.innerText);
  await browser.close();
  console.log(text);
}

// ── Smoke test ───────────────────────────────────────────────────────────────
async function smoke() {
  console.log('=== Smoke test: tts-docs ===');
  await waitReady();

  const routes = [
    ['/', '/tmp/ss-home.png'],
    ['/getting-started', '/tmp/ss-getting-started.png'],
    ['/getting-started/authentication', '/tmp/ss-auth.png'],
    ['/resources/tts-text', '/tmp/ss-resources.png'],
  ];

  for (const [route, out] of routes) {
    await screenshot(BASE + route, out);
  }

  console.log('=== Smoke test PASSED ===');
  console.log('Screenshots:', routes.map(r => r[1]).join(', '));
}

// ── CLI dispatch ─────────────────────────────────────────────────────────────
const [,, cmd, ...args] = process.argv;

switch (cmd) {
  case 'start':
    startServer();
    console.log('Waiting for server...');
    await waitReady();
    console.log('Ready.');
    break;
  case 'stop':
    stopServer();
    break;
  case 'screenshot':
  case 'navigate':
    await screenshot(args[0], args[1]);
    break;
  case 'text':
    await pageText(args[0]);
    break;
  case 'smoke':
    await smoke();
    break;
  case 'wait':
    await waitReady();
    console.log('Server ready.');
    break;
  default:
    console.log(`Usage: node driver.mjs <start|stop|screenshot|navigate|text|smoke|wait> [url] [out.png]`);
    process.exit(0);
}
