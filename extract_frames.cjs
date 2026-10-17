const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const server = http.createServer((req, res) => {
  const filePath = path.join(__dirname, 'public', decodeURIComponent(req.url.replace(/^\//, '')));
  if (fs.existsSync(filePath)) {
    const stat = fs.statSync(filePath);
    res.writeHead(200, {
      'Content-Length': stat.size,
      'Content-Type': filePath.endsWith('.mp4') ? 'video/mp4' : 'text/html',
      'Accept-Ranges': 'bytes'
    });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(8099, async () => {
  console.log('HTTP Server listening on 8099');
  try {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <body style="margin:0; background:#000; display:flex; justify-content:center; align-items:center; height:100vh;">
        <video id="vid" src="http://localhost:8099/assets/spiral%20menu%20satvik.mp4" style="max-width:95vw; max-height:95vh;" muted playsinline></video>
      </body>
      </html>
    `);

    const vid = page.locator('#vid');
    await page.waitForTimeout(1000);
    const duration = await vid.evaluate(v => {
      return new Promise((resolve) => {
        if (v.readyState >= 1) return resolve(v.duration);
        v.onloadedmetadata = () => resolve(v.duration);
      });
    });
    console.log('Video loaded. Duration:', duration);

    for (let t = 0; t <= Math.min(duration, 6); t += 0.5) {
      await vid.evaluate((v, time) => {
        v.currentTime = time;
      }, t);
      await page.waitForTimeout(500);
      await page.screenshot({ path: `test_output/vid_${t.toFixed(1)}.png` });
      console.log(`Saved vid_${t.toFixed(1)}.png`);
    }

    await browser.close();
  } catch (err) {
    console.error('Error during video capture:', err);
  } finally {
    server.close();
    process.exit(0);
  }
});
