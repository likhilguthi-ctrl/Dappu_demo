const { spawn } = require('child_process');
const http = require('http');

async function test() {
  const p = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=9230',
    '--headless=new',
    '--window-size=1920,1080',
    'http://localhost:5173/'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  const list = await new Promise(r => http.get('http://127.0.0.1:9230/json', res => {
    let d = ''; res.on('data', c => d += c); res.on('end', () => r(JSON.parse(d)));
  }));
  const ws = new WebSocket(list[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  function send(method, params={}) {
    return new Promise((resolve) => {
      const id = Math.floor(Math.random()*10000);
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

  const res = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sec = document.getElementById('section-sec_education');
        if (!sec) return { error: 'sec not found' };
        const cards = sec.querySelectorAll('.content-card-wrap');
        if (!cards.length) return { error: 'no cards' };
        // Trigger click
        cards[0].dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        const modal = document.getElementById('detailsModal');
        return {
          cardCount: cards.length,
          modalOpen: modal.classList.contains('open'),
          modalTitle: document.getElementById('modalTitle').textContent
        };
      })()
    `,
    returnByValue: true
  });
  console.log('Result:', res.result.value);
  p.kill();
}
test().catch(console.error);
