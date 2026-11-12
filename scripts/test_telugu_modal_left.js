const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9248;
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

async function testTeluguModal(outFilename) {
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

  // Switch to Telugu and click Dandora card
  await send('Runtime.evaluate', {
    expression: `
      localStorage.setItem('ott_demo_lang', 'te');
      location.reload();
    `
  });
  await wait(1800);

  await send('Runtime.evaluate', {
    expression: `
      const cards = Array.from(document.querySelectorAll('.content-card-wrap'));
      // Find Dandora card or 3rd song card
      const card = cards.find(c => (c.getAttribute('data-content')||'').includes('song_3')) || cards[0];
      if (card) card.click();
    `
  });
  await wait(1200);

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, outFilename), Buffer.from(shot.data, 'base64'));
  console.log(`Saved ${outFilename}`);
  ws.close();
  chromeProc.kill();
  await wait(800);
}

testTeluguModal('modal_dandora_te_left.png').catch(console.error);
