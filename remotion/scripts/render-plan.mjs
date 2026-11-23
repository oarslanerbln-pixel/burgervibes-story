// Render story slots from tools/plan.json with Remotion (bundles once).
//   node scripts/render-plan.mjs --week 1 [--day Mo] [--ids W1-Mo-1 W1-Mo-2] [--placeholder]
//   node scripts/render-plan.mjs --reel plan/reels/reel-01.json
// Media is looked up by slot id in assets/selects (real footage) then assets/ai.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const assets = path.join(root, 'assets');
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const ids = args.includes('--ids') ? args.slice(args.indexOf('--ids') + 1).filter((a) => !a.startsWith('--')) : null;
const browserExecutable = process.env.REMOTION_BROWSER || undefined;

const findMedia = (id) => {
  for (const dir of ['selects', 'ai']) {
    const d = path.join(assets, dir);
    if (!fs.existsSync(d)) continue;
    const hit = fs.readdirSync(d).find((f) => f.toLowerCase().startsWith(id.toLowerCase() + '.') || f.toLowerCase().startsWith(id.toLowerCase() + '_'));
    if (hit) return `${dir}/${hit}`;
  }
  return null;
};

const serveUrl = await bundle({entryPoint: path.join(here, '..', 'src', 'index.ts'), publicDir: assets});
const outDir = path.join(root, 'output', 'remotion');
fs.mkdirSync(outDir, {recursive: true});

const render = async (id, inputProps, file) => {
  const composition = await selectComposition({serveUrl, id, inputProps, browserExecutable});
  await renderMedia({composition, serveUrl, codec: 'h264', crf: 17, outputLocation: file, inputProps, browserExecutable, muted: true});
  console.log('ok', path.relative(root, file));
};

if (opt('--reel')) {
  const reel = JSON.parse(fs.readFileSync(path.resolve(root, opt('--reel')), 'utf8'));
  await render('Reel', reel, path.join(outDir, path.basename(opt('--reel'), '.json') + '.mp4'));
} else {
  const plan = JSON.parse(fs.readFileSync(path.join(root, 'tools', 'plan.json'), 'utf8'));
  const week = opt('--week') ? Number(opt('--week')) : null;
  const day = opt('--day');
  const missing = [];
  for (const s of plan.slots) {
    if ((week && s.week !== week) || (day && s.day !== day) || (ids && !ids.includes(s.id))) continue;
    const bg = findMedia(s.id);
    if (!bg && !args.includes('--placeholder')) { missing.push(s.id); continue; }
    await render('Story', {title: s.title, sub: s.sub, scriptSub: s.script_sub, preset: s.preset, accent: s.accent, bg: bg ?? undefined}, path.join(outDir, s.id + '.mp4'));
  }
  if (missing.length) console.log('no media yet:', missing.join(' '));
}
