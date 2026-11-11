const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9226;
const ARTIFACT_DIR = "C:\\Users\\likhi\\.gemini\\antigravity\\brain\\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a";

async function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function run() {
  console.log("Launching headless Chrome on port", PORT);
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100',
    '--hide-scrollbars',
    'http://127.0.0.1:5173/'
  ]);

  await wait(2500);

  const targets = await fetchJson(`http://127.0.0.1:${PORT}/json`);
  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget) {
    console.error("No page target found");
    chromeProc.kill();
    return;
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();

  ws.onmessage = (event) => {
    const res = JSON.parse(event.data);
    if (res.id && pending.has(res.id)) {
      const { resolve, reject } = pending.get(res.id);
      pending.delete(res.id);
      if (res.error) reject(res.error);
      else resolve(res.result);
    }
  };

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await new Promise(resolve => {
    if (ws.readyState === 1) resolve();
    else ws.onopen = resolve;
  });
  console.log("Connected to Chrome CDP WebSocket.");

  await wait(2000);

  // 1. English Podcasts rail
  await send('Runtime.evaluate', {
    expression: `
      const sec = document.getElementById('section-sec_podcast');
      if (sec) {
        window.scrollTo({ top: sec.offsetTop - 70, behavior: 'instant' });
      }
    `
  });
  await wait(1200);
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'rail_podcasts_english.png'), Buffer.from(shot.data, 'base64'));
  console.log("Captured rail_podcasts_english.png");

  // 2. Open Podcast 5 modal in English (Manda Krishna Madiga)
  await send('Runtime.evaluate', {
    expression: `
      const cards = document.querySelectorAll('#section-sec_podcast .content-card-wrap');
      if (cards.length > 4) cards[4].click();
    `
  });
  await wait(1200);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_podcast_5_english.png'), Buffer.from(shot.data, 'base64'));
  console.log("Captured modal_podcast_5_english.png");

  // 3. Close modal and switch to Telugu
  await send('Runtime.evaluate', {
    expression: `
      const closeBtn = document.getElementById('modalCloseBtn');
      if (closeBtn) closeBtn.click();
      const teOption = document.querySelector('.lang-option-item[data-lang="te"]');
      if (teOption) teOption.click();
    `
  });
  await wait(1500);

  // 4. Telugu Podcasts rail
  await send('Runtime.evaluate', {
    expression: `
      const sec = document.getElementById('section-sec_podcast');
      if (sec) {
        window.scrollTo({ top: sec.offsetTop - 70, behavior: 'instant' });
      }
    `
  });
  await wait(1200);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'rail_podcasts_telugu.png'), Buffer.from(shot.data, 'base64'));
  console.log("Captured rail_podcasts_telugu.png");

  ws.close();
  chromeProc.kill();
  console.log("Screenshots captured successfully!");
  process.exit(0);
}

run().catch(err => {
  console.error("Capture error:", err);
  process.exit(1);
});
