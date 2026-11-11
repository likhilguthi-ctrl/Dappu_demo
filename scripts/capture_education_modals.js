const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9232;
const ARTIFACT_DIR = "C:\\Users\\likhi\\.gemini\\antigravity\\brain\\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a";

async function test() {
  const p = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--window-size=1920,1080',
    'http://localhost:5173/'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  const list = await new Promise(r => http.get(`http://127.0.0.1:${PORT}/json`, res => {
    let d = ''; res.on('data', c => d += c); res.on('end', () => r(JSON.parse(d)));
  }));
  const ws = new WebSocket(list[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  function send(method, params={}) {
    return new Promise((resolve) => {
      const id = Math.floor(Math.random()*100000);
      const onm = (e) => {
        const m = JSON.parse(e.data);
        if (m.id === id) { ws.removeEventListener('message', onm); resolve(m.result); }
      };
      ws.addEventListener('message', onm);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await send('Page.enable');
  await new Promise(r => setTimeout(r, 1500));

  // 1. Scroll directly to Education Rail in English & Capture
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        if (sec) {
          sec.scrollIntoView({ behavior: 'instant', block: 'center' });
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));
  let shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'rail_education_english.png'), Buffer.from(shot.data, 'base64'));

  // 2. Click Gogu Shyamala card & capture modal
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        const cards = sec.querySelectorAll('.content-card-wrap');
        cards[0].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_edu_gogu_english.png'), Buffer.from(shot.data, 'base64'));

  // Close modal
  await send('Runtime.evaluate', { expression: `document.getElementById('modalCloseBtn').click()` });
  await new Promise(r => setTimeout(r, 500));

  // 3. Click Endluri Sudhakar card & capture modal
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        const cards = sec.querySelectorAll('.content-card-wrap');
        cards[1].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_edu_endluri_english.png'), Buffer.from(shot.data, 'base64'));

  // Close modal
  await send('Runtime.evaluate', { expression: `document.getElementById('modalCloseBtn').click()` });
  await new Promise(r => setTimeout(r, 500));

  // 4. Switch to Telugu
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const item = document.querySelector('.lang-option-item[data-lang="te"]');
        if (item) item.click();
        const sec = document.getElementById('section-sec_education');
        if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'rail_education_telugu.png'), Buffer.from(shot.data, 'base64'));

  // 5. Open Gogu Shyamala in Telugu
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        const cards = sec.querySelectorAll('.content-card-wrap');
        cards[0].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_edu_gogu_telugu.png'), Buffer.from(shot.data, 'base64'));

  // Close modal
  await send('Runtime.evaluate', { expression: `document.getElementById('modalCloseBtn').click()` });
  await new Promise(r => setTimeout(r, 500));

  // 6. Open Endluri Sudhakar in Telugu
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        const cards = sec.querySelectorAll('.content-card-wrap');
        cards[1].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));
  shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'modal_edu_endluri_telugu.png'), Buffer.from(shot.data, 'base64'));

  console.log('All screenshots captured successfully!');
  p.kill();
}

test().catch(console.error);
