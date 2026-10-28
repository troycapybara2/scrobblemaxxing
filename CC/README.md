# lastfm-mcp

A tiny, read-only Last.fm connector for Claude. It runs free on Cloudflare Workers and lets the Command Center read your scrobbles as they happen.

Tools it exposes:
- `recent_scrobbles` (everything since a timestamp, newest first, plus what's playing now)
- `now_playing`
- `user_summary` (total scrobbles)

## 1. Deploy (about 10 minutes)

You need Node 18+ and a free Cloudflare account.

```bash
cd lastfm-mcp
# put your Last.fm username in wrangler.toml (LASTFM_USER)
npx wrangler login
npx wrangler secret put LASTFM_API_KEY     # paste your Last.fm API key when asked
openssl rand -hex 16                       # copy the output, this is your path secret
npx wrangler secret put PATH_SECRET        # paste that random string
npx wrangler deploy
```

Wrangler prints your URL, something like `https://lastfm-mcp.<you>.workers.dev`.
Your connector URL is that plus `/mcp/<your path secret>`.

Keep the API key and the full connector URL out of chats and out of git. The random path is what keeps strangers from using your API key.

## 2. Check it works

```bash
curl -s -X POST "https://lastfm-mcp.<you>.workers.dev/mcp/<secret>" \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"now_playing","arguments":{}}}'
```

You should see your current or last track.

## 3. Add it to Claude

On claude.ai (web or desktop): Settings, Connectors, Add custom connector.
- Name: **Last.fm** (use exactly this so the Command Center finds it)
- URL: your connector URL from step 1

## 4. Tell Claude it's connected

Claude will make one real call to see the response, then wire the Command Center to it.
