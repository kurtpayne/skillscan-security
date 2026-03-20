---
name: twilio-best-practises
description: Best practices for integrating Twilio communications APIs. Use when implementing SMS/MMS messaging, voice calls, WhatsApp, phone verification (Verify), webhooks, or any Twilio product. Triggers on Twilio API integration, sending SMS, making calls, OTP verification, TwiML, webhook handling, and phone number management.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: SK7zzz/skills-twilio-best-practises
# corpus-url: https://github.com/SK7zzz/skills-twilio-best-practises/blob/7a264e3a865a316b6cfa8e6eb1ad3fe57106524e/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Twilio Integration Best Practices

## Quick Reference

| Resource | URL |
|----------|-----|
| API Base | `https://api.twilio.com/2010-04-01/` |
| Console | `https://console.twilio.com/` |
| Docs | `https://www.twilio.com/docs` |

## Core Products

| Product | Use Case |
|---------|----------|
| Messaging | SMS, MMS, WhatsApp, RCS |
| Voice | Calls, IVR, conferencing, recording |
| Verify | OTP, 2FA, phone verification |
| SendGrid | Email delivery |
| Video | Video calling SDK |
| Flex | Contact center |

## Authentication

All requests use HTTP Basic Auth with Account SID and Auth Token:

```typescript
// Environment variables (NEVER hardcode)
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;

// Using Twilio SDK (recommended)
import twilio from 'twilio';
const client = twilio(accountSid, authToken);

// Manual HTTP request
const auth = Buffer.from(`${accountSid}:${authToken}`).toString('base64');
const headers = { 'Authorization': `Basic ${auth}` };
```

## SMS Messaging

### Send SMS

```typescript
const client = twilio(accountSid, authToken);

const message = await client.messages.create({
  body: 'Hello from Twilio!',
  from: '+15551234567',  // Your Twilio number
  to: '+15559876543'     // Recipient
});

console.log(message.sid); // SM...
```

### Send MMS (with media)

```typescript
const message = await client.messages.create({
  body: 'Check out this image!',
  from: '+15551234567',
  to: '+15559876543',
  mediaUrl: ['https://example.com/image.jpg']
});
```

### Receive SMS (Webhook)

```typescript
// Express webhook handler
import { twiml } from 'twilio';

app.post('/sms', (req, res) => {
  const { From, Body } = req.body;
  
  const response = new twiml.MessagingResponse();
  response.message(`You said: ${Body}`);
  
  res.type('text/xml');
  res.send(response.toString());
});
```

## Voice Calls

### Make Outbound Call

```typescript
const call = await client.calls.create({
  url: 'https://yourapp.com/voice-handler',  // TwiML URL
  to: '+15559876543',
  from: '+15551234567'
});

console.log(call.sid); // CA...
```

### Handle Incoming Call (TwiML)

```typescript
app.post('/voice', (req, res) => {
  const response = new twiml.VoiceResponse();
  
  response.say('Hello! Press 1 for sales, 2 for support.');
  response.gather({
    numDigits: 1,
    action: '/handle-key'
  });
  
  res.type('text/xml');
  res.send(response.toString());
});

app.post('/handle-key', (req, res) => {
  const digit = req.body.Digits;
  const response = new twiml.VoiceResponse();
  
  if (digit === '1') {
    response.dial('+15551111111'); // Sales
  } else if (digit === '2') {
    response.dial('+15552222222'); // Support
  }
  
  res.type('text/xml');
  res.send(response.toString());
});
```

### Record Call

```typescript
const response = new twiml.VoiceResponse();
response.say('This call will be recorded.');
response.record({
  maxLength: 60,
  action: '/handle-recording',
  transcribe: true,
  transcribeCallback: '/transcription'
});
```

## Phone Verification (Verify)

### Send OTP

```typescript
// Create verification service once
const service = await client.verify.v2.services.create({
  friendlyName: 'My App'
});

// Send verification code
const verification = await client.verify.v2
  .services(serviceId)
  .verifications.create({
    to: '+15559876543',
    channel: 'sms'  // 'sms', 'call', 'email', 'whatsapp'
  });

console.log(verification.status); // 'pending'
```

### Verify OTP

```typescript
const check = await client.verify.v2
  .services(serviceId)
  .verificationChecks.create({
    to: '+15559876543',
    code: '123456'  // User-provided code
  });

if (check.status === 'approved') {
  // Verification successful
}
```

## Webhooks

### Webhook Security (Validate Requests)

```typescript
import twilio from 'twilio';

const validateRequest = (req: Request): boolean => {
  const signature = req.headers['x-twilio-signature'] as string;
  const url = `https://${req.headers.host}${req.originalUrl}`;
  
  return twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN!,
    signature,
    url,
    req.body
  );
};

// Middleware
app.use('/webhooks/twilio', (req, res, next) => {
  if (!validateRequest(req)) {
    return res.status(403).send('Invalid signature');
  }
  next();
});
```

### Status Callbacks

```typescript
// Track message delivery
const message = await client.messages.create({
  body: 'Hello!',
  from: '+15551234567',
  to: '+15559876543',
  statusCallback: 'https://yourapp.com/status'
});

// Handle status updates
app.post('/status', (req, res) => {
  const { MessageSid, MessageStatus } = req.body;
  // Status: queued, sent, delivered, undelivered, failed
  console.log(`Message ${MessageSid}: ${MessageStatus}`);
  res.sendStatus(200);
});
```

## TwiML Reference

### Voice TwiML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice">Welcome to our service.</Say>
  <Gather numDigits="1" action="/menu">
    <Say>Press 1 for sales, 2 for support.</Say>
  </Gather>
  <Dial callerId="+15551234567">
    <Number>+15559876543</Number>
  </Dial>
  <Record maxLength="60" transcribe="true"/>
  <Play>https://example.com/audio.mp3</Play>
  <Hangup/>
</Response>
```

### Messaging TwiML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message to="+15559876543">
    <Body>Hello!</Body>
    <Media>https://example.com/image.jpg</Media>
  </Message>
</Response>
```

## Best Practices

### Security
- Store credentials in environment variables
- Validate webhook signatures (X-Twilio-Signature)
- Use HTTPS for all webhook URLs
- Enable HTTP Basic Auth for media URLs
- Rotate Auth Tokens periodically

### Error Handling

```typescript
try {
  const message = await client.messages.create({...});
} catch (error) {
  if (error.code === 21211) {
    // Invalid 'To' phone number
  } else if (error.code === 21608) {
    // Unverified number (trial accounts)
  } else if (error.code === 21614) {
    // 'To' number not SMS-capable
  }
}
```

### Rate Limits
- SMS: 1 message/second per number (can burst higher)
- Voice: 1 call/second per number
- API: 100 requests/second per account
- Implement exponential backoff on 429 errors

### Phone Number Formatting
- Always use E.164 format: `+[country code][number]`
- Example: `+14155551234` (US), `+442071234567` (UK)

### Message Delivery
- Use status callbacks to track delivery
- Handle `undelivered` and `failed` statuses
- Implement retry logic for transient failures

## Common Error Codes

| Code | Description |
|------|-------------|
| 20003 | Authentication error |
| 21211 | Invalid 'To' phone number |
| 21408 | Permission denied |
| 21608 | Unverified number (trial) |
| 21610 | Message blocked (STOP) |
| 21614 | Number not SMS-capable |
| 30003 | Unreachable destination |
| 30004 | Message blocked by carrier |
| 30005 | Unknown destination |
| 30006 | Landline or unreachable |

## WhatsApp Integration

```typescript
// Send WhatsApp message
const message = await client.messages.create({
  body: 'Hello from WhatsApp!',
  from: 'whatsapp:+14155238886',  // Twilio Sandbox or your number
  to: 'whatsapp:+15559876543'
});

// WhatsApp template message
const message = await client.messages.create({
  from: 'whatsapp:+14155238886',
  to: 'whatsapp:+15559876543',
  contentSid: 'HXXXXXXXXXXXXXXXXXXX',  // Template SID
  contentVariables: JSON.stringify({ '1': 'John', '2': 'Order #123' })
});
```

## Resources

- [Messaging Docs](https://www.twilio.com/docs/messaging)
- [Voice Docs](https://www.twilio.com/docs/voice)
- [Verify Docs](https://www.twilio.com/docs/verify)
- [TwiML Reference](https://www.twilio.com/docs/voice/twiml)
- [Error Codes](https://www.twilio.com/docs/api/errors)
- [SDKs](https://www.twilio.com/docs/libraries)