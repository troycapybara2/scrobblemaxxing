// Last.fm MCP server for Capy's Command Center.
// Remote MCP over Streamable HTTP (stateless JSON responses), runs on Cloudflare Workers.
// Read-only: it only reads your public Last.fm listening data.

const SERVER_INFO = { name: "lastfm-capy", version: "1.0.0" };
const SUPPORTED = ["2025-06-18", "2025-03-26", "2024-11-05"];
const API = "https://ws.audioscrobbler.com/2.0/";

const TOOLS = [
  {
    name: "recent_scrobbles",
    title: "Recent scrobbles",
    description:
      "Scrobbles for the configured Last.fm user, newest first. Pass since_uts (Unix seconds) to get everything after that moment. Each scrobble is [uts, artist, album, track]. Also returns what is playing right now, if anything.",
    inputSchema: {
      type: "object",
      properties: {
        since_uts: { type: "integer", description: "Only scrobbles after this Unix timestamp (seconds)." },
        limit: { type: "integer", minimum: 1, maximum: 2000, description: "Max scrobbles to return (default 200, max 2000)." },
      },
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  {
    name: "now_playing",
    title: "Now playing",
    description: "The track the configured Last.fm user is playing right now, or the last one scrobbled.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  {
    name: "user_summary",
    title: "User summary",
    description: "Total scrobble count and registration date for the configured Last.fm user.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
];

async function lastfm(env, params) {
  const u = new URL(API);
  for (const [k, v] of Object.entries({ ...params, user: env.LASTFM_USER, api_key: env.LASTFM_API_KEY, format: "json" }))
    if (v !== undefined && v !== null) u.searchParams.set(k, String(v));
  const r = await fetch(u, { headers: { "User-Agent": "capy-command-center/1.0" } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.error) throw new Error(`Last.fm error ${j.error || r.status}: ${j.message || r.statusText}`);
  return j;
}
const arr = (x) => (Array.isArray(x) ? x : x ? [x] : []);
const txt = (x) => (x && (x["#text"] ?? x.name)) || "";

function splitTracks(list) {
  let now = null;
  const done = [];
  for (const t of arr(list)) {
    const row = { artist: txt(t.artist), album: txt(t.album), track: t.name || "" };
    if (t["@attr"] && t["@attr"].nowplaying === "true") now = row;
    else if (t.date && t.date.uts) done.push([Number(t.date.uts), row.artist, row.album, row.track]);
  }
  return { now, done };
}

async function recentScrobbles(env, args) {
  const limit = Math.min(Math.max(parseInt(args.limit ?? 200, 10) || 200, 1), 2000);
  const since = args.since_uts ? Math.floor(Number(args.since_uts)) + 1 : undefined;
  let page = 1, pages = 1, total = 0, now = null;
  const out = [];
  while (out.length < limit && page <= pages && page <= 10) {
    const j = await lastfm(env, { method: "user.getrecenttracks", limit: 200, page, from: since });
    const rt = j.recenttracks || {};
    pages = Number(rt["@attr"]?.totalPages || 1);
    total = Number(rt["@attr"]?.total || 0);
    const s = splitTracks(rt.track);
    if (page === 1) now = s.now;
    out.push(...s.done);
    page++;
  }
  const scrobbles = out.slice(0, limit);
  return { now_playing: now, total_matching: total, returned: scrobbles.length, truncated: total > scrobbles.length, scrobbles };
}

async function nowPlaying(env) {
  const j = await lastfm(env, { method: "user.getrecenttracks", limit: 1 });
  const s = splitTracks(j.recenttracks?.track);
  const last = s.done[0];
  return { now_playing: s.now, last_scrobble: last ? { uts: last[0], artist: last[1], album: last[2], track: last[3] } : null };
}

async function userSummary(env) {
  const j = await lastfm(env, { method: "user.getinfo" });
  const u = j.user || {};
  return { user: u.name, playcount: Number(u.playcount || 0), registered_uts: Number(u.registered?.unixtime || u.registered?.["#text"] || 0) };
}

async function callTool(env, name, args) {
  if (name === "recent_scrobbles") return recentScrobbles(env, args || {});
  if (name === "now_playing") return nowPlaying(env);
  if (name === "user_summary") return userSummary(env);
  throw Object.assign(new Error(`Unknown tool: ${name}`), { rpc: -32602 });
}

async function handleRpc(env, msg) {
  const { id, method, params } = msg || {};
  const ok = (result) => ({ jsonrpc: "2.0", id, result });
  const err = (code, message) => ({ jsonrpc: "2.0", id: id ?? null, error: { code, message } });
  if (!method) return err(-32600, "Invalid request");
  if (id === undefined || id === null) return null; // notification, no reply
  try {
    if (method === "initialize") {
      const want = params?.protocolVersion;
      return ok({
        protocolVersion: SUPPORTED.includes(want) ? want : SUPPORTED[0],
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER_INFO,
        instructions: "Read-only access to one Last.fm user's scrobbles. Use recent_scrobbles with since_uts to catch up on new listening.",
      });
    }
    if (method === "ping") return ok({});
    if (method === "tools/list") return ok({ tools: TOOLS });
    if (method === "tools/call") {
      try {
        const data = await callTool(env, params?.name, params?.arguments);
        return ok({ content: [{ type: "text", text: JSON.stringify(data) }], structuredContent: data, isError: false });
      } catch (e) {
        if (e.rpc) return err(e.rpc, e.message);
        return ok({ content: [{ type: "text", text: String(e.message || e) }], isError: true });
      }
    }
    return err(-32601, `Method not found: ${method}`);
  } catch (e) {
    return err(-32603, String(e.message || e));
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!env.PATH_SECRET || url.pathname !== `/mcp/${env.PATH_SECRET}`) return new Response("Not found", { status: 404 });
    if (request.method === "GET" || request.method === "DELETE") return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
    let body;
    try { body = await request.json(); } catch { return Response.json({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }, { status: 400 }); }
    if (Array.isArray(body)) {
      const replies = (await Promise.all(body.map((m) => handleRpc(env, m)))).filter(Boolean);
      return replies.length ? Response.json(replies) : new Response(null, { status: 202 });
    }
    const reply = await handleRpc(env, body);
    return reply ? Response.json(reply) : new Response(null, { status: 202 });
  },
};
