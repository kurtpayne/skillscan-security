---
name: emblem-ai
description: Multi-chain wallet authentication, AI-powered crypto assistant, and AI app introspection. Use when the user wants to integrate wallet authentication (Ethereum, Solana, Bitcoin, Hedera), sign transactions, add AI chat capabilities with 25+ crypto tools, display Migrate.fun token migration data, or embed AI-powered monitoring and debugging into Node.js apps. Provides React components, TypeScript SDKs, session-based authentication, and Reflexive for AI introspection. Supports trading, token analysis, DeFi operations, token migration browsing, multi-language debugging, and custom AI tool plugins.
user-invocable: true
metadata: {"clawdbot":{"emoji":"🔐","homepage":"https://emblemvault.dev","requires":{"bins":["node"]}}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: EmblemCompany/EmblemAi-SKILLS
# corpus-url: https://github.com/EmblemCompany/EmblemAi-SKILLS/blob/7dcd5506ed99e6da4275d9cb100444f7c973d40c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Emblem AI

Multi-chain wallet authentication and AI-powered crypto tools for developers.

## What You Can Build

**Authentication & Signing**
- Wallet connect flows (MetaMask, Phantom, WalletConnect, etc.)
- Multi-chain authentication (Ethereum, Solana, Bitcoin, Hedera)
- OAuth login (Google, Twitter)
- Session management with automatic JWT refresh
- Transaction signing across chains

**AI Chat & Tools**
- AI assistant with 250+ crypto tools built-in
- Streaming chat responses
- Custom tool plugins
- Trading, DeFi, token analysis, and more

**Token Migration (Migrate.fun)**
- Browse and display migrate.fun projects
- Token mint info (decimals, program, supply)
- Liquidity pool details (source, output, quote token)
- Ready-to-use `<ProjectSelect>` component

**AI App Introspection And Build Agent (Reflexive)**
- Embed Claude inside running apps to monitor, debug, and develop
- Multi-language debugging (Node.js, Python, Go, .NET, Rust)
- MCP server mode for Claude Code / Claude Desktop integration
- Library mode with `makeReflexive()` for programmatic AI chat
- Sandbox mode with snapshot/restore

## Quick Start

### Installation

```bash
# CLI for AI agent wallets
npm install -g @emblemvault/agentwallet

# Core authentication
npm install @emblemvault/auth-sdk

# React integration (includes auth)
npm install @emblemvault/emblem-auth-react

# AI chat for React
npm install @emblemvault/hustle-react

# AI chat SDK (Node.js / vanilla JS)
npm install hustle-incognito

# Token migration data (Migrate.fun)
npm install @emblemvault/migratefun-react

# AI app introspection and debugging
npm install reflexive
```

### Option A: React App (Recommended)

```tsx
import { EmblemAuthProvider, ConnectButton, useEmblemAuth } from '@emblemvault/emblem-auth-react';
import { HustleProvider, HustleChat } from '@emblemvault/hustle-react';

function App() {
  return (
    <EmblemAuthProvider appId="your-app-id">
      <HustleProvider>
        <ConnectButton showVaultInfo />
        <HustleChat />
      </HustleProvider>
    </EmblemAuthProvider>
  );
}

function MyComponent() {
  const { isAuthenticated, walletAddress, vaultId } = useEmblemAuth();

  if (!isAuthenticated) {
    return <ConnectButton />;
  }

  return <div>Connected: {walletAddress}</div>;
}
```

### Option B: Vanilla JavaScript / Node.js

```typescript
import { EmblemAuthSDK } from '@emblemvault/auth-sdk';
import { HustleIncognito } from 'hustle-incognito';

// Initialize auth
const auth = new EmblemAuthSDK({ appId: 'your-app-id' });

// Open auth modal (browser)
auth.openAuthModal();

// Listen for session
auth.on('session', (session) => {
  console.log('Authenticated:', session.user.vaultId);
});

// Initialize AI with auth
const hustle = new HustleIncognito({ auth });

// Chat with AI
const response = await hustle.chat([
  { role: 'user', content: 'What tokens are trending on Base?' }
]);
```

### Option C: CLI (Agent Wallet)

```bash
# Install globally
npm install -g @emblemvault/agentwallet

# Interactive mode -- opens browser for authentication
emblemai

# Agent mode -- single-shot queries for scripts and AI frameworks
emblemai --agent -m "What's the price of ETH?"

# Agent mode with explicit wallet identity
emblemai --agent -p "your-password-16-chars-min" -m "Show my balances across all chains"
```

Agent mode auto-generates a secure password on first run if none provided. See [references/agentwallet.md](references/agentwallet.md) for full CLI reference.

## Core Capabilities

### Wallet Authentication

**Supported Chains:**
| Chain | Auth Method | Signing Support |
|-------|-------------|-----------------|
| Ethereum/EVM | Signature verification | viem, ethers.js, web3.js |
| Solana | Signature verification | @solana/web3.js, @solana/kit |
| Bitcoin | PSBT signing | Native PSBT |
| Hedera | Signature verification | Hedera SDK |

**Additional Auth Methods:**
- OAuth (Google, Twitter)
- Email/password with OTP

**Reference**: [references/auth-sdk.md](references/auth-sdk.md)

### Transaction Signing

Convert authenticated sessions into signers for any blockchain library:

```typescript
const auth = new EmblemAuthSDK({ appId: 'your-app-id' });

// After authentication...

// EVM signing
const viemAccount = await auth.toViemAccount();
const ethersWallet = await auth.toEthersWallet(provider);
const web3Adapter = await auth.toWeb3Adapter();

// Solana signing
const solanaSigner = await auth.toSolanaWeb3Signer();
const solanaKitSigner = await auth.toSolanaKitSigner();

// Bitcoin PSBT signing
const bitcoinSigner = await auth.toBitcoinSigner();
```

**Reference**: [references/signing.md](references/signing.md)

### AI Chat Tools

25+ built-in crypto tools accessible via natural language:

**Trading & Swaps**
- Token swaps across chains
- Cross-chain bridges
- Limit orders and stop losses

**Market Research**
- Real-time prices
- Technical analysis (RSI, MACD)
- Trending tokens
- Social sentiment

**DeFi Operations**
- Liquidity pool analysis
- Yield farming opportunities
- Protocol interactions

**Token Analysis**
- Security audits
- Whale tracking
- Holder distribution

**Reference**: [references/ai-tools.md](references/ai-tools.md)

### React Components

Pre-built UI components for rapid development:

```tsx
// Auth components
<ConnectButton />           // Wallet connect button
<ConnectButton showVaultInfo />  // With vault dropdown
<AuthStatus />              // Shows connection status

// AI chat components
<HustleChat />              // Full chat interface
<HustleChatWidget />        // Floating chat widget
```

**Reference**: [references/react-components.md](references/react-components.md)

### Agent Wallet CLI

Give AI agents their own crypto wallets via a single CLI command. Zero-config agent mode auto-generates a wallet on first run. Supports 7 chains, 250+ trading tools, browser auth for humans, and password auth for agents.

```bash
# Zero-config -- auto-generates wallet, answers query, exits
emblemai --agent -m "What are my wallet addresses?"

# Explicit wallet identity
emblemai --agent -p "your-password-16-chars-min" -m "Swap $20 of SOL to USDC"

# Interactive mode with browser auth
emblemai
```

```bash
# Integrate with any agent framework (OpenClaw, CrewAI, AutoGPT)
emblemai --agent -m "Send 0.1 SOL to <address>"
emblemai --agent -m "What tokens do I hold across all chains?"

# Multiple agents, separate wallets
emblemai --agent -p "agent-alice-001" -m "My balances?"
emblemai --agent -p "agent-bob-002" -m "My balances?"
```

**Modes**: Interactive (browser auth, slash commands), Agent (single-shot, stdout)

**Plugins**: ElizaOS (default), A2A, ACP, Bridge -- managed via `/plugins`

**Reference**: [references/agentwallet.md](references/agentwallet.md)

### Migrate.fun Token Migration

React hooks and a `<ProjectSelect>` component for browsing and displaying migrate.fun projects, token mint details, and liquidity pool info.

```tsx
import { MigrateFunProvider } from '@emblemvault/migratefun-react/providers';
import { ProjectSelect } from '@emblemvault/migratefun-react/components';
import { useProject, useMintInfo } from '@emblemvault/migratefun-react/hooks';

function MigrationBrowser() {
  const [projectId, setProjectId] = useState('');
  const { project } = useProject(projectId);
  const { mintInfo } = useMintInfo(projectId);

  return (
    <MigrateFunProvider>
      <ProjectSelect value={projectId} onChange={setProjectId} />
      {project && <p>{project.oldTokenMeta?.symbol} -> {project.newTokenMeta?.symbol}</p>}
      {mintInfo && <p>Supply: {mintInfo.newToken.supplyFormatted}</p>}
    </MigrateFunProvider>
  );
}
```

**Hooks**: `useProjects`, `useProject`, `useProjectSelect`, `useMintInfo`, `usePoolInfo`

**Reference**: [references/migratefun-react.md](references/migratefun-react.md)

### AI App Introspection (Reflexive)

Embed Claude inside running applications to monitor, debug, and develop with conversational AI. Works as a CLI, embedded library, or MCP server.

```bash
# Monitor any app (read-only by default)
npx reflexive ./server.js

# Full development mode with debugging
npx reflexive --write --shell --debug --watch ./server.js

# As MCP server for Claude Code
npx reflexive --mcp --write --shell --debug ./server.js
```

```typescript
// Library mode -- embed in your app
import { makeReflexive } from 'reflexive';

const r = makeReflexive({ webUI: true, title: 'My App' });
r.setState('users.active', 42);
const analysis = await r.chat('Any anomalies in recent activity?');
```

**Modes**: CLI (local), library (`makeReflexive()`), MCP server, sandbox, hosted

**Debugging**: Node.js, Python, Go, .NET, Rust -- breakpoints with AI prompts

**Reference**: [references/reflexive.md](references/reflexive.md)

## Session Management

Emblem uses JWT-based sessions with automatic refresh:

```typescript
// Session structure
interface Session {
  authToken: string;      // JWT for API calls
  refreshToken?: string;  // For mobile/native apps
  expiresAt: number;      // Unix timestamp
  user: {
    vaultId: string;
    identifier?: string;
  };
  appId: string;
}

// Events
auth.on('session', (session) => { /* new session */ });
auth.on('sessionExpired', () => { /* handle expiry */ });
auth.on('sessionRefreshed', (session) => { /* refreshed */ });
```

Sessions auto-refresh ~60 seconds before expiry. No manual token management needed.

## Custom AI Plugins

Extend the AI with your own tools:

```typescript
const { registerPlugin } = useHustle();

await registerPlugin({
  name: 'my-plugin',
  version: '1.0.0',
  tools: [{
    name: 'get_nft_floor',
    description: 'Get NFT collection floor price',
    parameters: {
      type: 'object',
      properties: {
        collection: { type: 'string', description: 'Collection name or address' }
      },
      required: ['collection']
    }
  }],
  executors: {
    get_nft_floor: async ({ collection }) => {
      const data = await fetchFloorPrice(collection);
      return { floor: data.floorPrice, currency: 'ETH' };
    }
  }
});
```

**Reference**: [references/plugins.md](references/plugins.md)

## Common Patterns

### Auth Flow in React

```tsx
function AuthenticatedFeature() {
  const { isAuthenticated, isLoading, openAuthModal } = useEmblemAuth();

  if (isLoading) return <Spinner />;

  if (!isAuthenticated) {
    return <button onClick={openAuthModal}>Connect Wallet</button>;
  }

  return <ProtectedContent />;
}
```

### AI Chat with Streaming

```tsx
function ChatInterface() {
  const { chatStream } = useHustle();
  const [response, setResponse] = useState('');

  const handleSubmit = async (message: string) => {
    setResponse('');

    for await (const chunk of chatStream({
      messages: [{ role: 'user', content: message }]
    })) {
      setResponse(prev => prev + chunk.content);
    }
  };

  return (/* UI */);
}
```

### Programmatic Wallet Auth

```typescript
// For server-side or custom flows
const session = await auth.authenticateWallet({
  network: 'ethereum',
  message: 'Sign to authenticate with MyApp',
  signature: userSignature,
  address: userAddress
});
```

### Get Vault Info

```typescript
// After authentication
const vaultInfo = await auth.getVaultInfo();
// {
//   evmAddress: '0x...',
//   solanaAddress: '...',
//   hederaAccountId: '0.0.xxx'
// }
```

## Environment Setup

### Browser Apps

```typescript
const auth = new EmblemAuthSDK({
  appId: 'your-app-id',
  // Optional: customize modal behavior
  modalMode: 'iframe',  // or 'popup'
  authUrl: 'https://auth.emblemvault.dev'
});
```

### Node.js / Server

```typescript
const auth = new EmblemAuthSDK({
  appId: 'your-app-id',
  storage: {
    // Custom storage implementation
    get: async (key) => redis.get(key),
    set: async (key, value) => redis.set(key, value),
    remove: async (key) => redis.del(key)
  }
});
```

### Environment Variables

```bash
# For hustle-incognito CLI/server usage
HUSTLE_API_KEY=your-api-key
HUSTLE_API_URL=https://agenthustle.ai
VAULT_ID=your-vault-id
```

## Prompt Examples

### Trading
- "Buy $50 of ETH on Base"
- "Swap 0.1 SOL for USDC"
- "What's the best route to swap ETH to MATIC?"

### Market Research
- "Analyze ETH price with technical indicators"
- "What tokens are trending on Solana?"
- "Show me whale movements for PEPE"

### DeFi
- "Find the best yield for USDC"
- "Analyze Uniswap V3 ETH/USDC pool"
- "What are the top liquidity pools on Base?"

### Token Analysis
- "Is this token safe: 0x..."
- "Show holder distribution for SHIB"
- "Check if BONK has any red flags"

## Best Practices

### Security
1. Never expose API keys in client-side code
2. Use session-based auth for browser apps
3. Validate signatures server-side for sensitive operations
4. Store refresh tokens securely (httpOnly cookies recommended)

### Performance
1. Use streaming for AI responses
2. Leverage automatic session refresh (don't manually refresh)
3. Use React hooks instead of direct SDK calls in components

### UX
1. Show loading states during auth
2. Handle session expiry gracefully
3. Provide clear error messages for failed signatures

## Packages Reference

| Package | Purpose | Docs |
|---------|---------|------|
| `@emblemvault/agentwallet` | CLI for AI agent wallets | [agentwallet.md](references/agentwallet.md) |
| `@emblemvault/auth-sdk` | Core authentication | [auth-sdk.md](references/auth-sdk.md) |
| `@emblemvault/emblem-auth-react` | React auth hooks/components | [auth-react.md](references/auth-react.md) |
| `@emblemvault/hustle-react` | React AI chat | [hustle-react.md](references/hustle-react.md) |
| `hustle-incognito` | AI SDK (Node/Browser) | [hustle-incognito.md](references/hustle-incognito.md) |
| `@emblemvault/migratefun-react` | Migrate.fun React hooks/components | [migratefun-react.md](references/migratefun-react.md) |
| `reflexive` | AI app introspection & debugging | [reflexive.md](references/reflexive.md) |

## Troubleshooting

### Auth Issues
- **Modal not opening**: Check popup blockers, try `modalMode: 'iframe'`
- **Session not persisting**: Verify localStorage is available
- **Signature rejected**: Ensure correct chain is selected in wallet

### AI Issues
- **No response**: Check API key configuration
- **Tools not working**: Verify user is authenticated
- **Streaming broken**: Check network/proxy settings

### React Issues
- **Hook errors**: Ensure components are wrapped in providers
- **State not updating**: Check provider hierarchy (Auth → Hustle)

## Resources

- **Documentation**: https://emblemvault.dev/docs/auth/overview
- **App Registration**: https://emblemvault.dev/register
- **GitHub**: https://github.com/EmblemCompany
- **Discord**: https://discord.gg/Q93wbfsgBj

---

**Getting Started**: Start with `<ConnectButton />` to add wallet auth, then add `<HustleChat />` for AI capabilities.

**Need Help?**: Check the reference docs in the `references/` folder for detailed API documentation.