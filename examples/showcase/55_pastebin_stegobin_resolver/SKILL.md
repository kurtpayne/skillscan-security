# StegaBin-style Pastebin dead-drop resolver

This showcase demonstrates a high-signal static marker observed in recent npm malware campaigns:
- Pastebin dead-drop URL
- `|||` separator
- `===END===` terminator
- decoded Vercel C2 domain reference

```js
const fallbackPastes = ["https://pastebin.com/CJ5PrtNk"];
const marker = "|||";
const endMarker = "===END===";
const decoded = "ext-checkdin.vercel.app";
const deadDrop = "https://pastebin.com/CJ5PrtNk|||ext-checkdin.vercel.app===END===";
```
