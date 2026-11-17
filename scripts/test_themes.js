const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9260;
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
  await wait(1500);

  // Clear any existing localStorage theme so it starts in Dark mode
  await send('Runtime.evaluate', { expression: "localStorage.setItem('ott_theme', 'dark'); location.reload();" });
  await wait(2000);

  // 1. Dark Theme Desktop Hero
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_desktop.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_desktop.png");

  // 1b. Dark Theme Content Rails (Posters & Outlines)
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 520)" });
  await wait(600);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_rails.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_rails.png");
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 0)" });
  await wait(400);

  // 2. Open Details Modal in Dark Theme
  await send('Runtime.evaluate', { expression: "document.getElementById('heroInfoActionBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_modal.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_modal.png");

  // 3. Play video from modal in Dark Theme
  await send('Runtime.evaluate', { expression: "document.getElementById('modalPlayBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_player.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_player.png");

  // Close player and modal
  await send('Runtime.evaluate', { expression: "document.getElementById('playerCloseBtn').click()" });
  await wait(600);

  // 4. Switch to Light Theme
  await send('Runtime.evaluate', { expression: "document.getElementById('themeToggleBtn').click()" });
  await wait(1000);

  // 5. Light Theme Desktop Hero
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_light_desktop.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_light_desktop.png");

  // Scroll down a bit to see cards and rails in Light Theme
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 520)" });
  await wait(800);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_light_rails.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_light_rails.png");

  // Scroll back up and open Details Modal in Light Theme
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 0)" });
  await wait(600);
  await send('Runtime.evaluate', { expression: "document.getElementById('heroInfoActionBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_light_modal.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_light_modal.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 6. Test Mobile Viewports (390 x 844)
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await wait(1000);

  // Mobile Light Theme
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_light_mobile_hero.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_light_mobile_hero.png");

  // Mobile Light Modal
  await send('Runtime.evaluate', { expression: "document.getElementById('heroInfoActionBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_light_mobile_modal.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_light_mobile_modal.png");

  // Close modal and switch back to Dark on mobile
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);
  await send('Runtime.evaluate', { expression: "document.getElementById('themeToggleBtn').click()" });
  await wait(1000);

  // Mobile Dark Theme
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_mobile_hero.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_mobile_hero.png");

  // Mobile Dark Modal
  await send('Runtime.evaluate', { expression: "document.getElementById('heroInfoActionBtn').click()" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'theme_dark_mobile_modal.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved theme_dark_mobile_modal.png");

  chromeProc.kill();
  console.log("All screenshots captured successfully!");
  process.exit(0);
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
