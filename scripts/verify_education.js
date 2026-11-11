const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9231;
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

class CdpClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.msgId = 1;
    this.callbacks = new Map();
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.callbacks.has(msg.id)) {
          const cb = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) cb.reject(msg.error);
          else cb.resolve(msg.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.msgId++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expr) {
    const res = await this.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    return res && res.result ? res.result.value : undefined;
  }

  async screenshot(outPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(outPath, Buffer.from(res.data, 'base64'));
    console.log('Saved screenshot:', path.basename(outPath));
  }
}

async function run() {
  const chromeProcess = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1920,1080',
    '--hide-scrollbars',
    'http://localhost:5173/'
  ]);

  try {
    let wsUrl = null;
    for (let i = 0; i < 20; i++) {
      await wait(500);
      try {
        const list = await fetchJson(`http://127.0.0.1:${PORT}/json`);
        if (list && list.length > 0 && list[0].webSocketDebuggerUrl) {
          wsUrl = list[0].webSocketDebuggerUrl;
          break;
        }
      } catch (e) {}
    }

    if (!wsUrl) throw new Error('Could not connect to Chrome debugging target');

    const cdp = new CdpClient(wsUrl);
    await cdp.connect();
    await cdp.send('Page.enable');
    await wait(2000);

    // 1. Language English -> Scroll to Education Section
    await cdp.eval(`
      window.localStorage.setItem('ott_demo_language', 'en');
      location.reload();
    `);
    await wait(2500);

    // Scroll directly to Education section
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      if (sec) {
        window.scrollTo({ top: sec.offsetTop - 70, behavior: 'instant' });
      }
    `);
    await wait(1000);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'rail_education_english.png'));

    // 2. Open Gogu Shyamala modal
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      const cards = sec.querySelectorAll('.content-card-wrap');
      cards[0].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    `);
    await wait(1200);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'modal_edu_gogu_english.png'));

    // Close modal
    await cdp.eval(`
      const btn = document.getElementById('modalCloseBtn');
      if (btn) btn.click();
    `);
    await wait(600);

    // 3. Open Endluri Sudhakar modal
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      const cards = sec.querySelectorAll('.content-card-wrap');
      cards[1].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    `);
    await wait(1200);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'modal_edu_endluri_english.png'));

    // Close modal
    await cdp.eval(`
      const btn = document.getElementById('modalCloseBtn');
      if (btn) btn.click();
    `);
    await wait(600);

    // 4. Switch to Telugu Language
    await cdp.eval(`
      const item = document.querySelector('.lang-option-item[data-lang="te"]');
      if (item) item.click();
    `);
    await wait(1500);

    // Scroll to Education section in Telugu
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      if (sec) {
        window.scrollTo({ top: sec.offsetTop - 70, behavior: 'instant' });
      }
    `);
    await wait(1000);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'rail_education_telugu.png'));

    // Open Gogu Shyamala modal in Telugu
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      const cards = sec.querySelectorAll('.content-card-wrap');
      cards[0].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    `);
    await wait(1200);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'modal_edu_gogu_telugu.png'));

    // Close modal
    await cdp.eval(`
      const btn = document.getElementById('modalCloseBtn');
      if (btn) btn.click();
    `);
    await wait(600);

    // Open Endluri Sudhakar modal in Telugu
    await cdp.eval(`
      const sec = document.getElementById('section-sec_education');
      const cards = sec.querySelectorAll('.content-card-wrap');
      cards[1].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    `);
    await wait(1200);
    await cdp.screenshot(path.join(ARTIFACT_DIR, 'modal_edu_endluri_telugu.png'));

    console.log("Verification completed successfully!");
  } finally {
    chromeProcess.kill();
  }
}

run().catch(console.error);
