const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9236;
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

async function testMobileStyle(name, cssRules) {
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844',
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
  await send('Emulation.setDeviceMetricsOverride', {
    width: 390,
    height: 844,
    deviceScaleFactor: 2,
    mobile: true
  });
  await wait(1000);

  if (cssRules) {
    await send('Runtime.evaluate', {
      expression: `
        const s = document.createElement('style');
        s.id = 'test-injected-style';
        s.innerHTML = ${JSON.stringify(cssRules)};
        document.head.appendChild(s);
      `
    });
    await wait(800);
  }

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, `test_${name}.png`), Buffer.from(shot.data, 'base64'));
  console.log(`Saved test_${name}.png`);
  ws.close();
  chromeProc.kill();
  await wait(1000);
}

async function run() {
  // Test 1: background-position: right center
  await testMobileStyle('right_center', `
    .hero-banner-image { background-position: right center !important; }
  `);
  
  // Test 2: background-position: 95% center
  await testMobileStyle('pos_95', `
    .hero-banner-image { background-position: 95% center !important; }
  `);

  // Test 3: background-position: right center with stage height 300px
  await testMobileStyle('right_stage300', `
    .hero-carousel-stage { height: 300px !important; }
    .hero-banner-image { background-position: right center !important; }
  `);

  // Test 4: Pure 16:9 stage with transparent text card below or overlay
  await testMobileStyle('aspect_16_9', `
    .hero-carousel-stage { height: auto !important; aspect-ratio: 16 / 9 !important; }
    .hero-banner-image { background-position: center center !important; }
  `);
}

run().catch(console.error);
