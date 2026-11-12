const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9252;
const ARTIFACT_DIR = "C:\\Users\\likhi\\.gemini\\antigravity\\brain\\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a";

async function wait(ms) { return new Promise(r => setTimeout(r, ms)); }
function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

async function run() {
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900',
    '--hide-scrollbars',
    'http://127.0.0.1:5173/'
  ]);
  await wait(2200);
  const targets = await fetchJson(`http://127.0.0.1:${PORT}/json`);
  const pageTarget = targets.find(t => t.type === 'page');
  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
  let id = 1;
  const send = (m, p={}) => new Promise(res => {
    const cur = id++;
    const handler = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === cur) { ws.removeEventListener('message', handler); res(d.result); }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: cur, method: m, params: p }));
  });
  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 2, mobile: false });
  await wait(1000);

  // 1. Click Hero "Watch Now"
  await send('Runtime.evaluate', { expression: "document.getElementById('heroPlayActionBtn').click()" });
  await wait(1000);
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'player_watch_now_clean.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved player_watch_now_clean.png");

  // 2. Click "Back to Details"
  await send('Runtime.evaluate', { expression: "document.getElementById('playerBackBtn').click()" });
  await wait(800);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_returned_to_details.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved modal_returned_to_details.png");

  // 3. Click "Play Movie" inside the modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalPlayBtn').click()" });
  await wait(800);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'player_from_modal_play.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved player_from_modal_play.png");

  ws.close();
  chromeProc.kill();
  await wait(800);
  console.log("All watch tests finished!");
}

run().catch(console.error);
