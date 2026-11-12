const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9240;
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

async function captureTelugu() {
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

  // Switch language to Telugu
  await send('Runtime.evaluate', {
    expression: `
      const teOption = document.querySelector('.lang-option-item[data-lang="te"]');
      if (teOption) {
        teOption.click();
      } else {
        localStorage.setItem('ott_demo_lang', 'te');
        location.reload();
      }
    `
  });
  await wait(1800);

  // Capture Desktop Hero Telugu
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'new_hero_desktop_te.png'), Buffer.from(shot.data, 'base64'));

  // Open Modal in Telugu
  await send('Runtime.evaluate', { expression: "document.getElementById('heroInfoActionBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'new_modal_desktop_te.png'), Buffer.from(shot.data, 'base64'));

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // Mobile Telugu
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'new_hero_mobile_te.png'), Buffer.from(shot.data, 'base64'));

  console.log("Telugu captures completed!");
  ws.close();
  chromeProc.kill();
  await wait(800);
}

captureTelugu().catch(console.error);
