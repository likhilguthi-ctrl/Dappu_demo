const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9228;
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

async function capture(viewport, filename) {
  console.log(`Capturing ${filename} (${viewport.width}x${viewport.height})...`);
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--window-size=${viewport.width},${viewport.height}`,
    '--hide-scrollbars',
    'http://127.0.0.1:5173/'
  ]);

  await wait(2500);

  let targets;
  try {
    targets = await fetchJson(`http://127.0.0.1:${PORT}/json`);
  } catch (err) {
    console.error("Failed to fetch chrome targets:", err);
    chromeProc.kill();
    return;
  }

  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget) {
    console.error("No page target found");
    chromeProc.kill();
    return;
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(msg.error);
      else resolve(msg.result);
    }
  };

  await new Promise(resolve => ws.onopen = resolve);

  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: 2,
    mobile: !!viewport.mobile
  });

  await wait(1800);

  const screenshot = await send('Page.captureScreenshot', { format: 'png' });
  const buffer = Buffer.from(screenshot.data, 'base64');
  fs.writeFileSync(path.join(ARTIFACT_DIR, filename), buffer);
  console.log(`Saved screenshot to ${filename}`);

  ws.close();
  chromeProc.kill();
  await wait(1000);
}

async function main() {
  await capture({ width: 1440, height: 900, mobile: false }, 'dappu_logo_desktop.png');
  await capture({ width: 390, height: 844, mobile: true }, 'dappu_logo_mobile.png');
  console.log("All captures completed!");
}

main().catch(err => {
  console.error("Error in capture script:", err);
  process.exit(1);
});
