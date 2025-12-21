/* global JSZip */
/* eslint-disable no-restricted-globals */

// Zip parsing in a Web Worker to avoid blocking the main thread.
// Loads JSZip from CDN (keeps show.html as a single-file app).
importScripts('https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js');

let currentZip = null;
let currentZipId = null;

function ok(id, payload) {
  postMessage({ id, ok: true, payload });
}

function fail(id, message) {
  postMessage({ id, ok: false, error: String(message || 'error') });
}

function inFinal(name) {
  return name.includes('/final/') || name.startsWith('final/');
}
function inChunk(name) {
  return name.includes('/chunk_') || name.startsWith('chunk_');
}
function chunkKeyFromPath(p) {
  const m = String(p).match(/(^|\/)(chunk_[^/]+)\//);
  return m ? m[2] : null;
}
function slideKeyFromPath(p) {
  const m = String(p).match(/(^|\/)(slide_\d+)\//i);
  return m ? m[2] : null;
}
function filenameNoExt(p) {
  const name = String(p).split('/').pop() || '';
  return name.replace(/\.[^.]+$/i, '');
}

function pickBest(items) {
  if (!items.length) return null;
  items.sort((a, b) => a.rank - b.rank);
  return items[0].name;
}

async function parsePartZip(buf, zipId) {
  const zip = new JSZip();
  const contents = await zip.loadAsync(buf);

  const fileNames = [];
  for (const [name, entry] of Object.entries(contents.files || {})) {
    if (entry && !entry.dir) fileNames.push(name);
  }

  const videoCandidates = [];
  const srtCandidates = [];
  const narFiles = [];
  const refFiles = [];
  const cropFiles = [];
  const captureById = {};
  let secManifestAligned = null;
  let secManifestPlan = null;
  let secManifestAny = null;
  let graphFinal = null;
  let graphAny = null;
  let materialsFinal = null;
  let materialsAny = null;
  let materialManifestAny = null;

  for (const name of fileNames) {
    const lower = name.toLowerCase();
    const isFinal = inFinal(name);
    const isChunk = inChunk(name);

    if (lower.endsWith('part_low.mp4')) videoCandidates.push({ rank: isFinal ? 0 : 10, name });
    else if (lower.endsWith('part_high.mp4')) videoCandidates.push({ rank: isFinal ? 1 : 11, name });
    else if (lower.endsWith('chunk_low.mp4')) videoCandidates.push({ rank: isChunk ? 2 : 12, name });
    else if (lower.endsWith('chunk_high.mp4')) videoCandidates.push({ rank: isChunk ? 3 : 13, name });

    if (lower.endsWith('part_subtitles_aligned.srt')) srtCandidates.push({ rank: isFinal ? 0 : 10, name });
    else if (lower.endsWith('part_subtitles.srt')) srtCandidates.push({ rank: isFinal ? 1 : 11, name });
    else if (lower.endsWith('chunk_subtitles_aligned.srt')) srtCandidates.push({ rank: isChunk ? 2 : 12, name });
    else if (lower.endsWith('chunk_subtitles.srt')) srtCandidates.push({ rank: isChunk ? 3 : 13, name });

    if (isFinal && lower.endsWith('section_manifest_aligned.json') && !secManifestAligned) secManifestAligned = name;
    if (isFinal && lower.endsWith('section_manifest.json') && !secManifestPlan) secManifestPlan = name;
    if (!secManifestAny && lower.endsWith('section_manifest.json')) secManifestAny = name;

    if (isFinal && /_merge_slides\/artifacts\/materials\.json$/i.test(name) && !materialsFinal) materialsFinal = name;
    if (!materialsAny && /materials\.json$/i.test(name)) materialsAny = name;
    if (!materialManifestAny && lower.endsWith('material_manifest.json')) materialManifestAny = name;

    if (isFinal && lower.endsWith('section_graph.json') && !graphFinal) graphFinal = name;
    if (!graphAny && lower.endsWith('section_graph.json')) graphAny = name;

    const mNar = name.match(/section_(.+)_narrative\.json$/i);
    if (mNar) narFiles.push({ sid: mNar[1], path: name, final: isFinal ? 1 : 0 });
    const mRef = name.match(/section_(.+)_refined\.md$/i);
    if (mRef) refFiles.push({ sid: mRef[1], path: name, final: isFinal ? 1 : 0 });

    if (/\/\d+_crop_decision\//.test(name) && lower.endsWith('step.json')) cropFiles.push(name);
    if (/\/\d+_capture_frame\//.test(name) && /slide_\d+\.png$/i.test(name)) {
      const chunkKey = chunkKeyFromPath(name);
      const slideId = filenameNoExt(name);
      if (chunkKey && slideId) captureById[`${chunkKey}/${slideId}`] = name;
    }
  }

  const srtPath = pickBest(srtCandidates);
  if (!srtPath) throw new Error('未找到字幕产物（part_subtitles_aligned.srt 或 chunk_subtitles_aligned.srt）');
  const secManifestPath = secManifestAligned || secManifestPlan || secManifestAny;
  if (!secManifestPath) throw new Error('未找到 section_manifest');

  const graphPath = graphFinal || graphAny;
  const materialsPath = materialsFinal || materialsAny;

  const srtEntry = contents.file(srtPath);
  const secEntry = contents.file(secManifestPath);
  if (!srtEntry) throw new Error('字幕文件不存在: ' + srtPath);
  if (!secEntry) throw new Error('section_manifest 不存在: ' + secManifestPath);

  const [srtText, secText] = await Promise.all([srtEntry.async('string'), secEntry.async('string')]);
  const secJson = JSON.parse(secText);
  const sections = Array.isArray(secJson.sections) ? secJson.sections : [];

  // Materials timeline
  const materialsById = {};
  const materialsEntry = materialsPath ? contents.file(materialsPath) : null;
  const materialManifestEntry = materialManifestAny ? contents.file(materialManifestAny) : null;
  if (materialsEntry) {
    try {
      const json = JSON.parse(await materialsEntry.async('string'));
      const items = Array.isArray(json.materials) ? json.materials : Array.isArray(json) ? json : [];
      items.forEach((m) => {
        if (m && m.id) materialsById[String(m.id)] = m;
      });
    } catch (_e) {}
  } else if (materialManifestEntry) {
    try {
      const json = JSON.parse(await materialManifestEntry.async('string'));
      const items = Array.isArray(json.materials) ? json.materials : Array.isArray(json) ? json : [];
      items.forEach((m) => {
        if (m && m.id) materialsById[String(m.id)] = m;
      });
    } catch (_e) {}
  }

  // Refined scripts / narratives
  const narratives = {};
  const refined = {};
  narFiles.sort((a, b) => (b.final - a.final) || a.path.localeCompare(b.path));
  refFiles.sort((a, b) => (b.final - a.final) || a.path.localeCompare(b.path));

  for (const f of narFiles) {
    if (narratives[f.sid]) continue;
    const entry = contents.file(f.path);
    if (!entry) continue;
    try {
      narratives[f.sid] = JSON.parse(await entry.async('string'));
    } catch (_e) {}
  }
  for (const f of refFiles) {
    if (refined[f.sid]) continue;
    const entry = contents.file(f.path);
    if (!entry) continue;
    try {
      refined[f.sid] = await entry.async('string');
    } catch (_e) {}
  }

  // Crops (optional)
  const crops = {};
  for (let idx = 0; idx < cropFiles.length; idx++) {
    const p = cropFiles[idx];
    const entry = contents.file(p);
    if (!entry) continue;
    let data;
    try {
      data = JSON.parse(await entry.async('string'));
    } catch (_e) {
      continue;
    }
    const chunkKey = chunkKeyFromPath(p);
    const slideId = slideKeyFromPath(p) || filenameNoExt(p);
    if (chunkKey && slideId) {
      const id = `${chunkKey}/${slideId}`;
      if (data && data.output) crops[id] = data.output;
    }
  }

  // Graph (optional)
  let graph = null;
  if (graphPath && contents.file(graphPath)) {
    try {
      const json = JSON.parse(await contents.file(graphPath).async('string'));
      graph = json.graph_data || json;
    } catch (_e) {}
  }

  // Keep zip in worker for on-demand capture extraction.
  currentZip = contents;
  currentZipId = zipId;

  return {
    srtText,
    sections,
    narratives,
    refined,
    crops,
    captures: captureById,
    materialsById,
    graph,
  };
}

async function getEntryBlob(path, zipId) {
  if (!currentZip || currentZipId !== zipId) throw new Error('zip not loaded');
  const entry = currentZip.file(path);
  if (!entry) throw new Error('entry not found: ' + path);
  return await entry.async('blob');
}

self.onmessage = async (evt) => {
  const msg = evt && evt.data ? evt.data : null;
  if (!msg || typeof msg.id !== 'number' || !msg.type) return;
  try {
    if (msg.type === 'parse_part_zip') {
      const { buf, zipId } = msg;
      const payload = await parsePartZip(buf, zipId);
      ok(msg.id, payload);
      return;
    }
    if (msg.type === 'get_entry_blob') {
      const { path, zipId } = msg;
      const blob = await getEntryBlob(path, zipId);
      ok(msg.id, { blob });
      return;
    }
    fail(msg.id, 'unknown type');
  } catch (e) {
    fail(msg.id, e && e.message ? e.message : String(e));
  }
};

