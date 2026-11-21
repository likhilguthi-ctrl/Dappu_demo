const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9266;
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

  // Ensure English and Dark Theme
  await send('Runtime.evaluate', { expression: "localStorage.setItem('ott_theme', 'dark'); localStorage.setItem('ott_demo_lang', 'en'); location.reload();" });
  await wait(2000);

  // 1. English Hero Section with Category Quick Nav
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_hero.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_hero.png");

  // 2. English Rails: Culture & Personalities
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 520)" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_rails_culture.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_rails_culture.png");

  // 3. English Rails: Education & Films
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 1150)" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_rails_education_films.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_rails_education_films.png");

  // 4. English Modal: Culture Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const cultureCard = document.querySelector('#section-sec_culture .content-card-wrap');
    if (cultureCard) cultureCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_modal_culture.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_modal_culture.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 5. English Modal: Education Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const eduCard = document.querySelector('#section-sec_education .content-card-wrap');
    if (eduCard) eduCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_modal_education.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_modal_education.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 6. English Modal: Films Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const filmCard = document.querySelector('#section-sec_films .content-card-wrap');
    if (filmCard) filmCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_en_modal_films.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_en_modal_films.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 7. SWITCH TO TELUGU
  await send('Runtime.evaluate', { expression: "window.switchLanguage('te'); window.scrollTo(0, 0);" });
  await wait(1500);

  // 8. Telugu Hero Section
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_hero.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_hero.png");

  // 9. Telugu Rails: Culture & Personalities
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 520)" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_rails_culture.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_rails_culture.png");

  // 10. Telugu Rails: Education & Films
  await send('Runtime.evaluate', { expression: "window.scrollTo(0, 1150)" });
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_rails_education_films.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_rails_education_films.png");

  // 11. Telugu Modal: Culture Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const teCultureCard = document.querySelector('#section-sec_culture .content-card-wrap');
    if (teCultureCard) teCultureCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_modal_culture.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_modal_culture.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 12. Telugu Modal: Education Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const teEduCard = document.querySelector('#section-sec_education .content-card-wrap');
    if (teEduCard) teEduCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_modal_education.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_modal_education.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  // 13. Telugu Modal: Films Item (Landscape Backdrop)
  await send('Runtime.evaluate', { expression: `
    const teFilmCard = document.querySelector('#section-sec_films .content-card-wrap');
    if (teFilmCard) teFilmCard.click();
  `});
  await wait(1000);
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'verify_te_modal_films.png'), Buffer.from(shot.data, 'base64'));
  console.log("Saved verify_te_modal_films.png");

  // Close modal
  await send('Runtime.evaluate', { expression: "document.getElementById('modalCloseBtn').click()" });
  await wait(600);

  console.log("All complete!");
  ws.close();
  chromeProc.kill();
}

run().catch(e => {
  console.error("Test failed:", e);
  process.exit(1);
});
