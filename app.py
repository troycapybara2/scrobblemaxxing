import streamlit as st
import streamlit.components.v1 as components

try:
    import voice
except Exception:
    voice = None


# ---- leaderboard semantic colors (the heart of the app) ----
# Brightened for a dark canvas so they pop, but blue/red/green identity kept.
COLOR_ACTIVE = "#1FB6FF"   # active artist (blue) — close to the original deepskyblue
COLOR_RISING = "#21D07A"   # rising (green)
COLOR_FALLEN = "#FF5470"   # fallen (red)
COLOR_FLAT = "#5B6172"     # unchanged / unknown (muted slate)


def _vtext(name, default):
    return getattr(voice, name, default) if voice else default


def _vlist(name):
    v = getattr(voice, name, None) if voice else None
    return v if isinstance(v, list) else []


def _vfmt(s, **kw):
    try:
        return s.format(**kw)
    except Exception:
        return s


def inject_theme():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{
  --neon:#00E5FF; --neon-dim:rgba(0,229,255,.5);
  --surface:#15151F; --muted:#8b93a7;
}
.stApp{
  background:
    radial-gradient(1200px 620px at 18% -12%, rgba(0,229,255,.06), transparent 60%),
    radial-gradient(1000px 520px at 102% -4%, rgba(127,90,240,.08), transparent 55%),
    #0A0A12;
}
/* headings get the display font + a neon underglow accent */
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3{
  font-family:'Space Grotesk',sans-serif; letter-spacing:.4px; color:#fff;
}
.stMarkdown h1{ text-shadow:0 0 18px rgba(0,229,255,.45); }
.stMarkdown h2,.stMarkdown h3{ position:relative; padding-bottom:.32em; }
.stMarkdown h2::after,.stMarkdown h3::after{
  content:""; position:absolute; left:0; bottom:0; height:2px; width:52px;
  background:linear-gradient(90deg,var(--neon),transparent);
  box-shadow:0 0 10px var(--neon-dim);
}
/* buttons: thin neon, glow on hover */
.stButton > button{
  background:rgba(0,229,255,.06); border:1px solid rgba(0,229,255,.35);
  color:#bff6ff; border-radius:10px; font-weight:600; letter-spacing:.3px;
  transition:all .15s ease;
}
.stButton > button:hover{
  border-color:var(--neon); color:#fff; transform:translateY(-1px);
  box-shadow:0 0 16px rgba(0,229,255,.35);
}
/* alerts become insight cards */
[data-testid="stAlert"]{
  background:linear-gradient(90deg,rgba(0,229,255,.08),rgba(21,21,31,.55));
  border:1px solid rgba(0,229,255,.22); border-left:3px solid var(--neon);
  border-radius:10px; box-shadow:0 0 24px rgba(0,229,255,.08);
}
/* metric numbers glow */
[data-testid="stMetricValue"]{
  color:var(--neon); text-shadow:0 0 14px rgba(0,229,255,.4);
  font-family:'Space Grotesk',sans-serif;
}
/* dividers as neon hairlines */
hr{ border:none; height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,229,255,.4),transparent); }
/* tables + expanders: dark surfaces, faint neon edge */
[data-testid="stDataFrame"]{ border:1px solid rgba(0,229,255,.12); border-radius:10px; overflow:hidden; }
[data-testid="stExpander"]{ border:1px solid rgba(0,229,255,.14); border-radius:10px; background:rgba(21,21,31,.4); }
/* sidebar */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0d0d18,#0a0a12);
  border-right:1px solid rgba(0,229,255,.12);
}
/* input focus */
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:var(--neon)!important; box-shadow:0 0 0 1px var(--neon)!important;
}
/* masthead */
.smx-mast{ padding:4px 0 2px; margin-bottom:8px; }
.smx-title{
  font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:2.1rem;
  letter-spacing:1px; color:#fff; text-shadow:0 0 22px rgba(0,229,255,.5);
  animation:smxpulse 5s ease-in-out infinite;
}
@keyframes smxpulse{ 0%,100%{text-shadow:0 0 22px rgba(0,229,255,.45);} 50%{text-shadow:0 0 30px rgba(0,229,255,.72);} }
.smx-tag{ color:var(--muted); font-size:.95rem; letter-spacing:.3px; margin-top:0; }
.smx-rule{ height:2px; margin-top:8px; max-width:280px;
  background:linear-gradient(90deg,var(--neon),transparent); box-shadow:0 0 12px var(--neon-dim); }
</style>
""", unsafe_allow_html=True)


def render_masthead():
    title = _vtext("APP_TITLE", "Scrobblemaxxing")
    tag = _vtext("APP_TAGLINE", "")
    html = "<div class='smx-mast'><div class='smx-title'>%s</div>" % title
    if tag:
        html += "<div class='smx-tag'>%s</div>" % tag
    html += "<div class='smx-rule'></div></div>"
    st.markdown(html, unsafe_allow_html=True)
import requests
import plotly.graph_objects as go
import random
from streamlit_autorefresh import st_autorefresh
import json
import os
from datetime import datetime
import hashlib
import base64
import time
import networkx as nx

# -------------------------
# App Config + Constants
# -------------------------
st.set_page_config(page_title="Scrobblemaxxing", layout="wide")

ERA_OPTIONS = ["", "60s", "70s", "80s", "90s", "00s", "10s", "2020s"]
ENERGY_MIN, ENERGY_MAX = 1, 5

# repo-relative paths (GitHub-backed storage, not Drive anymore)
CACHE_FILE = "lastfm_cache/leaderboard_cache.json"
HISTORY_FILE = "lastfm_cache/leaderboard_history.json"
META_FILE = "lastfm_cache/artist_meta.json"

API_KEY = st.secrets.get("LASTFM_API_KEY", "")

GH_TOKEN = st.secrets.get("GH_TOKEN", "")
GH_REPO = st.secrets.get("GH_REPO", "")
GH_BRANCH = st.secrets.get("GH_BRANCH", "main")

# files committed immediately on every write (irreplaceable). Everything else
# is buffered and pushed on an interval to avoid a commit every refresh.
PROTECTED_FILES = {META_FILE}
FLUSH_INTERVAL_SECONDS = 300  # how often cache/history get pushed to GitHub

# one-time bulk baseline importer (sub-500 artists from screenshots)
BASELINE_IMPORT_FILE = "baseline_import.json"
BASELINE_DONE_FILE = "baseline_imports_done.json"


def safe_widget_key(prefix: str, raw: str) -> str:
    raw = (raw or "").strip()
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _gh_enabled():
    return bool(GH_TOKEN and GH_REPO)


def _gh_headers():
    return {"Authorization": "token %s" % GH_TOKEN,
            "Accept": "application/vnd.github+json"}


def _gh_url(path):
    return "https://api.github.com/repos/%s/contents/%s" % (GH_REPO, path)


def _store():
    if "_gh_store" not in st.session_state:
        st.session_state._gh_store = {}
    return st.session_state._gh_store


def _gh_fetch(path):
    try:
        r = requests.get(_gh_url(path), headers=_gh_headers(),
                         params={"ref": GH_BRANCH}, timeout=20)
    except Exception:
        return None, None
    if r.status_code == 404:
        return "", None
    if r.status_code != 200:
        return None, None
    data = r.json()
    sha = data.get("sha")
    content_b64 = data.get("content", "")

    # small file (<=1 MB): content is inline base64
    if content_b64:
        try:
            return base64.b64decode(content_b64).decode("utf-8"), sha
        except Exception:
            pass

    # large file (>1 MB): Contents API leaves content empty -> fetch the blob by sha
    if sha:
        try:
            rb = requests.get(
                "https://api.github.com/repos/%s/git/blobs/%s" % (GH_REPO, sha),
                headers=_gh_headers(), timeout=30,
            )
            if rb.status_code == 200:
                bdata = rb.json()
                if bdata.get("encoding") == "base64":
                    return base64.b64decode(bdata.get("content", "")).decode("utf-8"), sha
        except Exception:
            pass

    return None, sha


def _gh_put(path, text, sha, message):
    payload = {
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "branch": GH_BRANCH,
    }
    if sha:
        payload["sha"] = sha
    try:
        r = requests.put(_gh_url(path), headers=_gh_headers(),
                         json=payload, timeout=30)
    except Exception:
        return None
    if r.status_code in (200, 201):
        return r.json().get("content", {}).get("sha")
    return None


def ensure_dir_for(path):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def _load_text(path):
    store = _store()
    if path in store:
        return store[path]["text"]

    text, sha = "", None
    if _gh_enabled():
        text, sha = _gh_fetch(path)
        if text is None:  # network/API failure -- fall back to local mirror
            text = ""
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    text = ""
    elif os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            text = ""

    store[path] = {"text": text, "sha": sha, "dirty": False}
    return text


def _save_text(path, text, message, force_commit=False):
    store = _store()
    entry = store.get(path, {"text": "", "sha": None, "dirty": False})
    entry["text"] = text
    store[path] = entry

    # always mirror locally so reruns within the same container stay consistent
    try:
        ensure_dir_for(path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass

    if not _gh_enabled():
        return

    if force_commit or path in PROTECTED_FILES:
        new_sha = _gh_put(path, text, entry.get("sha"), message)
        if new_sha:
            entry["sha"], entry["dirty"] = new_sha, False
        else:
            entry["dirty"] = True
    else:
        entry["dirty"] = True
        _maybe_flush()


def _maybe_flush(force=False):
    if not _gh_enabled():
        return
    now = time.time()
    last = st.session_state.get("_gh_last_flush", 0)
    if not force and (now - last) < FLUSH_INTERVAL_SECONDS:
        return
    for path, entry in _store().items():
        if entry.get("dirty"):
            new_sha = _gh_put(path, entry["text"], entry.get("sha"),
                              "update %s" % path)
            if new_sha:
                entry["sha"], entry["dirty"] = new_sha, False
    st.session_state._gh_last_flush = now


def read_json(path, default):
    text = _load_text(path)
    if not text:
        return default
    try:
        return json.loads(text)
    except Exception:
        return default


def write_json(path, obj, indent=None):
    _save_text(path, json.dumps(obj, indent=indent),
               "update %s" % os.path.basename(path))

def get_top_artists(username, limit=500):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.gettopartists",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
        "period": "overall",
    }
    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200:
        return []
    data = r.json()
    return data.get("topartists", {}).get("artist", []) or []


def get_artist_playcount(username, artist_name):
    top_artists = get_top_artists(username, limit=500)
    for a in top_artists:
        if a.get("name", "").lower() == (artist_name or "").lower():
            try:
                return int(a.get("playcount", 0))
            except (TypeError, ValueError):
                return 0
    return 0


def get_recent_artist(username):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "limit": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=20)
    except Exception as e:
        st.error(f"Last.fm request failed: {e}")
        return None, 0, None, None

    if response.status_code != 200:
        st.error(f"Last.fm API error: {response.status_code}")
        st.code(response.text[:1000])
        return None, 0, None, None

    data = response.json()

    if "error" in data:
        st.error(f"Last.fm error {data.get('error')}: {data.get('message')}")
        return None, 0, None, None

    tracks = data.get("recenttracks", {}).get("track", [])

    if isinstance(tracks, dict):
        tracks = [tracks]

    if not tracks:
        st.warning("Last.fm returned zero recent tracks.")
        return None, 0, None, None

    recent_track = tracks[0]
    artist_obj = recent_track.get("artist", {})

    if isinstance(artist_obj, dict):
        recent_artist = artist_obj.get("#text") or artist_obj.get("name")
    else:
        recent_artist = str(artist_obj)

    recent_track_name = recent_track.get("name")
    album_art_url = (recent_track.get("image") or [{}])[-1].get("#text")

    recent_artist_playcount = get_artist_playcount(username, recent_artist)

    return recent_artist, recent_artist_playcount, recent_track_name, album_art_url

def get_recent_tracks(username, limit=100):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
        "extended": 1,  # adds more fields (nice to have)
    }
    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200:
        return []

    data = r.json()
    tracks = data.get("recenttracks", {}).get("track", []) or []
    out = []

    for t in tracks:
        artist = (t.get("artist") or {}).get("#text") if isinstance(t.get("artist"), dict) else t.get("artist")
        name = t.get("name") or ""
        album = (t.get("album") or {}).get("#text") if isinstance(t.get("album"), dict) else ""
        images = t.get("image") or []
        art_url = ""
        if images:
            # usually last item is largest
            art_url = (images[-1] or {}).get("#text") or ""

        # now playing flag sometimes present
        now_playing = ((t.get("@attr") or {}).get("nowplaying") == "true")

        out.append({
            "artist": artist or "",
            "track": name,
            "album": album or "",
            "art": art_url,
            "now_playing": now_playing,
        })

    return out

def load_history_entries():
    text = _load_text(HISTORY_FILE)
    if not text:
        return []
    entries = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not (line.startswith("{") and '"timestamp"' in line and '"data"' in line):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("data"), dict):
            entries.append(obj)
    return entries


def load_long_term_baseline():
    entries = load_history_entries()
    if not entries:
        cached = load_previous_leaderboard()
        return cached if isinstance(cached, dict) else {}

    baselines = {}
    entries_sorted = sorted(entries, key=lambda e: e.get("timestamp", ""))

    for entry in entries_sorted:
        snapshot = entry.get("data", {})
        if not isinstance(snapshot, dict) or not snapshot:
            continue
        for artist, info in snapshot.items():
            if artist not in baselines and isinstance(info, dict):
                baselines[artist] = info

    return baselines

def load_previous_leaderboard():
    return read_json(CACHE_FILE, {})


def save_current_leaderboard(data):
    write_json(CACHE_FILE, data, indent=None)


def log_leaderboard_snapshot(snapshot_data):
    # skip near-duplicate snapshots from rapid reruns (interactions, not just refreshes)
    last = st.session_state.get("_last_snapshot_ts", 0)
    if time.time() - last < 30:
        return
    st.session_state._last_snapshot_ts = time.time()

    entry = {
        "timestamp": datetime.now().isoformat(timespec="milliseconds"),
        "data": snapshot_data,
    }
    text = _load_text(HISTORY_FILE) or ""
    if text and not text.endswith("\n"):
        text += "\n"
    text += json.dumps(entry) + "\n"
    _save_text(HISTORY_FILE, text, "append snapshot")  # throttled, not every refresh


def log_manual_entry(artist_name, playcount, rank, when_dt):
    # one manual data point for a sub-500 artist, written as its own history line.
    # force-committed immediately (deliberate action, shouldn't wait on the timer).
    entry = {
        "timestamp": when_dt.isoformat(timespec="milliseconds"),
        "data": {artist_name: {"playcount": int(playcount), "rank": rank}},
        "manual": True,
    }
    text = _load_text(HISTORY_FILE) or ""
    if text and not text.endswith("\n"):
        text += "\n"
    text += json.dumps(entry) + "\n"
    _save_text(HISTORY_FILE, text, "manual entry: %s" % artist_name, force_commit=True)


def maybe_run_baseline_import(full_top_artists, overall_ranks):
    # One-time bulk import: reads baseline_import.json from the repo, writes all
    # its artists into history as a single dated baseline snapshot, then records
    # the import_id so it never runs again. Skips anyone currently in the live
    # Top 500 (the API already tracks them).
    data = read_json(BASELINE_IMPORT_FILE, None)
    if not isinstance(data, dict):
        return
    artists = data.get("artists")
    if not isinstance(artists, dict) or not artists:
        return

    import_id = data.get("import_id") or "unnamed-baseline"
    done = read_json(BASELINE_DONE_FILE, [])
    if not isinstance(done, list):
        done = []
    if import_id in done:
        return  # already imported

    live = set(overall_ranks.keys())
    snap = {}
    skipped = 0
    for name, pc in artists.items():
        if name in live:
            skipped += 1
            continue
        try:
            snap[name] = {"playcount": int(pc), "rank": None}
        except Exception:
            continue

    if snap:
        ts = data.get("date") or datetime.now().isoformat(timespec="milliseconds")
        entry = {"timestamp": ts, "data": snap, "manual": True, "bulk_baseline": True}
        text = _load_text(HISTORY_FILE) or ""
        if text and not text.endswith("\n"):
            text += "\n"
        text += json.dumps(entry) + "\n"
        _save_text(HISTORY_FILE, text,
                   "bulk baseline import: %s (%d artists)" % (import_id, len(snap)),
                   force_commit=True)

    # record completion immediately so a restart can't re-import
    done.append(import_id)
    _save_text(BASELINE_DONE_FILE, json.dumps(done, indent=2),
               "mark baseline import done: %s" % import_id, force_commit=True)

    st.sidebar.success("Imported %d baseline artists (skipped %d already in Top 500)."
                       % (len(snap), skipped))


def get_artist_history_points(artist_name):
    # all logged (date, playcount, rank) points for one artist, oldest first.
    pts = []
    for e in load_history_entries():
        info = (e.get("data") or {}).get(artist_name)
        if isinstance(info, dict) and info.get("playcount") is not None:
            dt = parse_ts(e.get("timestamp"))
            if dt:
                pts.append((dt, int(info["playcount"]), info.get("rank")))
    pts.sort(key=lambda x: x[0])
    return pts


def render_manual_tracker(artist_name, track_name, album_art_url):
    st.markdown("### Not in your Top 500 right now")
    st.markdown("**Now playing:** %s — %s" % (artist_name, track_name or ""))
    if album_art_url:
        st.image(album_art_url, width=200)
    st.caption(
        "Log this artist's current playcount to track them over time. "
        "If they climb into your Top 500 later, this gives them a real baseline "
        "instead of reading flat."
    )

    ak = safe_widget_key("manual", artist_name)
    with st.form("manual_form_%s" % ak):
        plays = st.number_input("Playcount right now", min_value=0, step=1, value=0,
                                key="manual_plays_%s" % ak)
        when = st.date_input("Date of this count", value=datetime.now().date(),
                             key="manual_date_%s" % ak)
        submitted = st.form_submit_button("Log entry")

    if submitted:
        if plays <= 0:
            st.warning("Enter a playcount above 0.")
        else:
            when_dt = datetime.combine(when, datetime.now().time())
            log_manual_entry(artist_name, int(plays), None, when_dt)
            st.success("Logged %s: %d plays on %s." % (
                artist_name, int(plays), when.isoformat()))

    prior = get_artist_history_points(artist_name)
    if prior:
        st.markdown("#### Logged history for %s" % artist_name)
        rows = [{"Date": dt.strftime("%Y-%m-%d %H:%M"), "Plays": pc}
                for dt, pc, r in prior]
        st.dataframe(rows, use_container_width=True, hide_index=True,
                     key="manual_hist_%s" % ak)
        if len(prior) >= 2:
            gain = prior[-1][1] - prior[0][1]
            span_days = max((prior[-1][0] - prior[0][0]).total_seconds() / 86400.0, 1.0)
            st.caption("Net change since first log: %+d plays over %.0f days." % (gain, span_days))


def load_leaderboard_history():
    entries = load_history_entries()
    history = {}
    for e in entries:
        ts = e.get("timestamp")
        data = e.get("data", {})
        if ts and isinstance(data, dict):
            history[ts] = data
    return history

from datetime import datetime, timedelta
import statistics

def parse_ts(ts: str):
    if not ts:
        return None
    try:
        # supports "2025-..." isoformat; also strips a trailing Z if present
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception:
        return None

def get_history_window(days=7):
    history = load_leaderboard_history()
    now = datetime.now()
    cutoff = now - timedelta(days=int(days))

    items = []
    for ts, snap in history.items():
        dt = parse_ts(ts)
        if not dt:
            continue
        if dt >= cutoff and isinstance(snap, dict):
            items.append((dt, snap))

    items.sort(key=lambda x: x[0])
    return items

def compute_momentum_and_volatility(window_items):
    if len(window_items) < 2:
        return [], []

    artists = set()
    for _, snap in window_items:
        artists.update(snap.keys())

    momentum_rows = []
    volatility_rows = []

    start_dt = window_items[0][0]
    end_dt = window_items[-1][0]
    elapsed_days = max((end_dt - start_dt).total_seconds() / 86400.0, 1e-9)

    for artist in artists:
        ranks = []
        plays = []
        times = []

        for dt, snap in window_items:
            info = snap.get(artist)
            if not isinstance(info, dict):
                continue
            r = info.get("rank")
            p = info.get("playcount")
            if r is None and p is None:
                continue
            times.append(dt)
            ranks.append(r)
            plays.append(p)

        if len(plays) >= 2 and plays[0] is not None and plays[-1] is not None:
            play_gain = int(plays[-1]) - int(plays[0])
        else:
            play_gain = None

        if len(ranks) >= 2 and ranks[0] is not None and ranks[-1] is not None:
            # positive means rank improved (moved up)
            rank_delta = int(ranks[0]) - int(ranks[-1])
        else:
            rank_delta = None

        if play_gain is not None and play_gain != 0:
            momentum_rows.append({
                "Artist": artist,
                "Play gain": play_gain,
                "Plays/day": round(play_gain / elapsed_days, 2),
                "Rank Δ": rank_delta if rank_delta is not None else "—",
                "First seen": times[0].strftime("%m/%d %H:%M"),
                "Last seen": times[-1].strftime("%m/%d %H:%M"),
            })

        clean_ranks = [r for r in ranks if isinstance(r, int)]
        if len(clean_ranks) >= 3:
            r_min = min(clean_ranks)
            r_max = max(clean_ranks)
            r_range = r_max - r_min
            r_std = statistics.pstdev(clean_ranks)


            diffs = []
            for i in range(1, len(clean_ranks)):
                diffs.append(clean_ranks[i] - clean_ranks[i - 1])

            signs = []
            for d in diffs:
                if d > 0:
                    signs.append(1)
                elif d < 0:
                    signs.append(-1)
                else:
                    signs.append(0)

            compressed = [s for s in signs if s != 0]
            flips = 0
            for i in range(1, len(compressed)):
                if compressed[i] != compressed[i - 1]:
                    flips += 1

            volatility_rows.append({
                "Artist": artist,
                "Rank std dev": round(r_std, 2),
                "Rank range": r_range,
                "Direction flips": flips,
            })

    momentum_rows.sort(key=lambda x: x["Play gain"], reverse=True)
    volatility_rows.sort(key=lambda x: (x["Rank std dev"], x["Rank range"], x["Direction flips"]), reverse=True)

    return momentum_rows, volatility_rows

def compute_artist_loyalty_index(window_items, min_obs=3):
    if not window_items:
        return []

    ranks_by_artist = {}
    latest_play_by_artist = {}
    latest_dt_by_artist = {}

    for dt, snap in window_items:
        if not isinstance(snap, dict):
            continue
        for artist, info in snap.items():
            if not isinstance(info, dict):
                continue
            r = info.get("rank")
            p = info.get("playcount")

            if isinstance(r, int):
                ranks_by_artist.setdefault(artist, []).append(r)

            # keep the latest playcount we observe (by timestamp)
            if isinstance(p, int):
                prev_dt = latest_dt_by_artist.get(artist)
                if prev_dt is None or dt >= prev_dt:
                    latest_dt_by_artist[artist] = dt
                    latest_play_by_artist[artist] = p

    rows = []
    for artist, ranks in ranks_by_artist.items():
        if len(ranks) < min_obs:
            continue
        avg_rank = sum(ranks) / len(ranks)
        latest_play = latest_play_by_artist.get(artist)

        if latest_play is None or avg_rank <= 0:
            continue

        loyalty_score = latest_play / avg_rank

        rows.append({
            "Artist": artist,
            "Loyalty score": round(loyalty_score, 2),
            "Latest plays": latest_play,
            "Avg rank": round(avg_rank, 2),
            "Observations": len(ranks),
        })

    rows.sort(key=lambda x: x["Loyalty score"], reverse=True)
    return rows

def build_top_artist_maps(full_top_artists):
    rank_map = {}
    play_map = {}
    for i, a in enumerate(full_top_artists):
        name = a.get("name")
        if not name:
            continue
        rank_map[name] = i + 1
        try:
            play_map[name] = int(a.get("playcount", 0))
        except (TypeError, ValueError):
            play_map[name] = None
    return rank_map, play_map


def get_leaderboard_surrounding_artists(username, recent_artist, limit=500):
    top_artists = get_top_artists(username, limit=limit)
    pairs = []
    for a in top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pairs.append((name, int(a.get("playcount", 0))))
        except Exception:
            continue

    for i, (name, _) in enumerate(pairs):
        if name.lower() == (recent_artist or "").lower():
            start_index = max(0, i - 5)
            end_index = min(len(pairs), i + 6)
            return dict(pairs[start_index:end_index]), top_artists

    return {}, top_artists


def compute_artist_progress(baselines, full_top_artists):
    progress = {}
    for i, artist_obj in enumerate(full_top_artists):
        name = artist_obj.get("name")
        if not name:
            continue

        curr_rank = i + 1
        try:
            curr_play = int(artist_obj.get("playcount", 0))
        except Exception:
            curr_play = 0

        base = baselines.get(name)
        if not isinstance(base, dict):
            continue

        base_rank = base.get("rank")
        base_play = base.get("playcount")
        if base_rank is None or base_play is None:
            continue

        progress[name] = {
            "baseline_rank": base_rank,
            "current_rank": curr_rank,
            "rank_change": base_rank - curr_rank,
            "baseline_playcount": base_play,
            "current_playcount": curr_play,
            "play_change": curr_play - base_play,
        }
    return progress


def compute_biggest_movers(artist_progress, top_n=10):
    items = list(artist_progress.items())
    risers = sorted(items, key=lambda x: x[1]["rank_change"], reverse=True)[:top_n]
    fallers = sorted(items, key=lambda x: x[1]["rank_change"])[:top_n]
    return risers, fallers


def make_leaderboard_fig(artists, playcounts, ranked_artists, bar_colors, height=450, title=""):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=playcounts[::-1],
            y=ranked_artists[::-1],
            orientation="h",
            marker_color=bar_colors[::-1],
            hoverinfo="skip",
            text=[str(pc) for pc in playcounts[::-1]],
            textposition="outside",
            insidetextanchor="start",
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Playcount",
        yaxis_title="",
        margin=dict(l=100, r=30, t=50, b=30),
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8ECF4"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_traces(marker_line_width=0)
    return fig

def load_artist_meta():
    return read_json(META_FILE, {})


def save_artist_meta(meta):
    write_json(META_FILE, meta, indent=2)


def get_tag_library(meta):
    tags = set()
    moods = set()
    for _, info in meta.items():
        for t in info.get("tags", []) or []:
            tags.add(t)
        for m in info.get("moods", []) or []:
            moods.add(m)
    return sorted(tags), sorted(moods)


def auto_favorite_from_rank(rank):
    if rank is None:
        return 40
    try:
        r = int(rank)
    except (TypeError, ValueError):
        return 40

    if r <= 10:
        return 100
    if r <= 15:
        return 95
    if r <= 30:
        return 90
    if r <= 75:
        return 80
    if r <= 150:
        return 70
    if r <= 350:
        return 60
    if r <= 500:
        return 50
    return 40


def computed_favorite(meta, artist_name, overall_ranks):
    info = meta.get(artist_name, {})
    fav = info.get("favorite_override")
    if fav is None:
        fav = auto_favorite_from_rank(overall_ranks.get(artist_name))
    return int(fav)

def render_artist_tagger(recent_artist, overall_ranks, meta):
    artist_meta = meta.get(
        recent_artist,
        {
            "tags": [],
            "moods": [],
            "energy": 3,
            "era": "",
            "favorite_override": None,
            "listen_more": False,
            "notes": "",
        },
    )

    tag_library, mood_library = get_tag_library(meta)
    ak = safe_widget_key("artist", recent_artist)

    st.markdown("### 🏷️ Tag and Rate This Artist")
    c1, c2 = st.columns(2)

    with c1:
        selected_tags = st.multiselect(
            "Tags",
            options=tag_library,
            default=artist_meta.get("tags", []),
            key=f"artist_tags_{ak}",
        )
        new_tag = st.text_input("Add a new tag (optional)", key=f"artist_newtag_{ak}")

        selected_moods = st.multiselect(
            "Moods",
            options=mood_library,
            default=artist_meta.get("moods", []),
            key=f"artist_moods_{ak}",
        )
        new_mood = st.text_input("Add a new mood (optional)", key=f"artist_newmood_{ak}")

    with c2:
        curr_rank = overall_ranks.get(recent_artist)
        auto_fav = auto_favorite_from_rank(curr_rank)

        override_on = st.checkbox(
            "Override auto favorite score",
            value=artist_meta.get("favorite_override") is not None,
            key=f"artist_fav_override_on_{ak}",
        )

        if override_on:
            favorite_override = st.slider(
                "Favorite score (override)",
                1,
                100,
                value=int(artist_meta.get("favorite_override") or auto_fav),
                key=f"artist_fav_override_{ak}",
            )
        else:
            favorite_override = None
            rank_txt = curr_rank if curr_rank is not None else "—"
            st.caption(f"Auto favorite score: **{auto_fav}** (based on current rank {rank_txt})")

        energy = st.slider(
            "Energy (1 = low, 5 = high)",
            min_value=ENERGY_MIN,
            max_value=ENERGY_MAX,
            value=int(artist_meta.get("energy", 3)),
            key=f"artist_energy_{ak}",
        )

        era_val = artist_meta.get("era", "")
        if era_val not in ERA_OPTIONS:
            era_val = ""
        era = st.selectbox(
            "Era",
            options=ERA_OPTIONS,
            index=ERA_OPTIONS.index(era_val),
            key=f"artist_era_{ak}",
        )

        listen_more = st.checkbox(
            "Want to listen to more",
            value=bool(artist_meta.get("listen_more", False)),
            key=f"artist_listenmore_{ak}",
        )

        notes = st.text_area(
            "Notes (optional)",
            value=artist_meta.get("notes", ""),
            height=90,
            key=f"artist_notes_{ak}",
        )

    if st.button("Save artist tags and preferences", key=f"artist_save_{ak}"):
        if new_tag and new_tag.strip():
            selected_tags = list(dict.fromkeys(selected_tags + [new_tag.strip()]))
        if new_mood and new_mood.strip():
            selected_moods = list(dict.fromkeys(selected_moods + [new_mood.strip()]))

        meta[recent_artist] = {
            "tags": selected_tags,
            "moods": selected_moods,
            "energy": int(energy),
            "era": era,
            "favorite_override": favorite_override,
            "listen_more": bool(listen_more),
            "notes": notes.strip(),
        }
        save_artist_meta(meta)
        st.success("Saved.")

    return meta

def get_top_playcount_rows(full_top_artists, baseline_data, top_n=25):
    rows = []

    for i, a in enumerate(full_top_artists[:top_n], start=1):
        name = a.get("name")

        try:
            playcount = int(a.get("playcount", 0))
        except Exception:
            playcount = 0

        # Current rank is just position in full_top_artists
        current_rank = i

        # Baseline rank (first appearance)
        base_info = baseline_data.get(name, {})
        baseline_rank = base_info.get("rank")

        # Rank change calculation
        if baseline_rank is None:
            rank_change = "—"
        else:
            delta = baseline_rank - current_rank
            if delta > 0:
                rank_change = f"↑ {delta}"
            elif delta < 0:
                rank_change = f"↓ {abs(delta)}"
            else:
                rank_change = "• 0"

        rows.append({
            "Current rank": current_rank,
            "Artist": name,
            "Initial rank": baseline_rank if baseline_rank is not None else "—",
            "Δ rank": rank_change,
            "Playcount": playcount
        })

    return rows

def build_playcount_gainers_rows(artist_progress, top_n=25):
    items = list(artist_progress.items())

    # Sort by playcount gain (descending)
    items_sorted = sorted(items, key=lambda x: x[1].get("play_change", 0), reverse=True)[:top_n]

    rows = []
    for idx, (name, p) in enumerate(items_sorted, start=1):
        base_rank = p.get("baseline_rank")
        curr_rank = p.get("current_rank")
        rank_change = p.get("rank_change")

        if rank_change is None:
            rank_txt = "—"
        else:
            if rank_change > 0:
                rank_txt = f"↑ {rank_change}"
            elif rank_change < 0:
                rank_txt = f"↓ {abs(rank_change)}"
            else:
                rank_txt = "• 0"

        rows.append({
            "#": idx,
            "Artist": name,
            "Initial rank": base_rank if base_rank is not None else "—",
            "Current rank": curr_rank if curr_rank is not None else "—",
            "Δ rank": rank_txt,
            "Initial plays": p.get("baseline_playcount", "—"),
            "Current plays": p.get("current_playcount", "—"),
            "Playcount gain": p.get("play_change", "—"),
        })

    return rows

def normalize_list(xs):
    return [str(x).strip().lower() for x in (xs or []) if str(x).strip()]

def score_artist_for_query(artist_info, q_tags, q_moods, q_era):
    a_tags = set(normalize_list(artist_info.get("tags", [])))
    a_moods = set(normalize_list(artist_info.get("moods", [])))
    a_era = (artist_info.get("era") or "").strip()

    tag_hits = len(a_tags & q_tags)
    mood_hits = len(a_moods & q_moods)
    era_hit = 1 if (q_era and a_era == q_era) else 0

    # Big weight to tags, medium to moods, tiny to era
    score = (tag_hits * 10) + (mood_hits * 4) + (era_hit * 1)

    return score, tag_hits, mood_hits, era_hit

def recommend_artists_from_query(meta, query_tags, query_moods, query_era="", top_n=10, exclude=None):
    q_tags = set(normalize_list(query_tags))
    q_moods = set(normalize_list(query_moods))
    exclude = set([exclude]) if exclude else set()

    scored = []
    for artist, info in (meta or {}).items():
        if artist in exclude:
            continue
        if not isinstance(info, dict):
            continue

        score, tag_hits, mood_hits, era_hit = score_artist_for_query(info, q_tags, q_moods, query_era)

        # Don’t return totally unrelated artists
        if score <= 0:
            continue

        scored.append((artist, score, tag_hits, mood_hits, era_hit, info))

    # Sort: score desc, then tag hits desc, then mood hits desc, then era hit desc, then name
    scored.sort(key=lambda x: (x[1], x[2], x[3], x[4], x[0].lower()), reverse=True)

    results = []
    for artist, score, tag_hits, mood_hits, era_hit, info in scored[:top_n]:
        results.append({
            "Artist": artist,
            "Score": score,
            "Tag hits": tag_hits,
            "Mood hits": mood_hits,
            "Era match": "Yes" if era_hit else "No",
            "Tags": ", ".join(info.get("tags", []) or [])[:120],
            "Moods": ", ".join(info.get("moods", []) or [])[:120],
            "Era": info.get("era", "") or "—",
        })
    return results

def generate_insight(meta, window_items, loyalty_rows=None):
    candidates = []

    energies = []
    for _, snap in window_items:
        for artist, info in snap.items():
            a_meta = meta.get(artist, {})
            e = a_meta.get("energy")
            if isinstance(e, int):
                energies.append(e)

    if len(energies) >= 5:
        avg_energy = sum(energies) / len(energies)
        if avg_energy <= 2.5:
            candidates.extend(_vlist("INSIGHTS_ENERGY_LOW"))
        elif avg_energy >= 4:
            candidates.extend(_vlist("INSIGHTS_ENERGY_HIGH"))

    if loyalty_rows:
        top_loyal = loyalty_rows[0]
        if top_loyal["Avg rank"] > 5:
            for s in _vlist("INSIGHTS_LOYAL_NOT_TOP"):
                candidates.append(_vfmt(s, artist=top_loyal["Artist"]))

    for row in loyalty_rows or []:
        if row["Avg rank"] > 10 and row["Loyalty score"] > 100:
            for s in _vlist("INSIGHTS_QUIET_DEVOTION"):
                candidates.append(_vfmt(s, artist=row["Artist"]))
            break

    if not candidates:
        return None

    return random.choice(candidates)

import math
from datetime import datetime, timedelta
import time

def _normalize_artist_name(x: str) -> str:
    return (x or "").strip().lower()


@st.cache_data(ttl=300)  # cache 5 minutes
def get_recent_artist_counts(username: str, days: int = 7) -> dict:
    url = "http://ws.audioscrobbler.com/2.0/"
    to_ts = int(time.time())
    from_ts = to_ts - int(days) * 86400

    params = {
        "method": "user.getweeklyartistchart",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "from": from_ts,
        "to": to_ts,
    }

    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200:
        return {}

    data = r.json()
    chart = data.get("weeklyartistchart", {}).get("artist", []) or []

    counts = {}
    for a in chart:
        name = a.get("name")
        if not name:
            continue
        try:
            counts[name] = int(a.get("playcount", 0))
        except (TypeError, ValueError):
            counts[name] = 0

    return counts

def build_power_ranking_rows(
    full_top_artists,
    recent_counts,
    top_n=50,
    w_total=0.3,
    w_recent=0.7,
):

    rows = []

    for a in full_top_artists or []:
        name = a.get("name") or ""
        if not name:
            continue

        try:
            total_plays = int(a.get("playcount", 0))
        except Exception:
            total_plays = 0

        recent_plays = recent_counts.get(
            _normalize_artist_name(name), 0
        )

        power_score = (
            math.log10(total_plays + 1) * w_total
            + recent_plays * w_recent
        )

        rows.append({
            "Artist": name,
            "Total plays": total_plays,
            "Plays (last 7d)": recent_plays,
            "Power score": round(power_score, 2),
        })

    rows.sort(key=lambda x: x["Power score"], reverse=True)
    return rows[:top_n]

def _norm(s: str) -> str:
    return (s or "").strip().lower()

@st.cache_data(ttl=600)  # cache 10 minutes
def get_recent_scrobbles(username, days=14, per_page=200, max_pages=15):
    url = "http://ws.audioscrobbler.com/2.0/"
    cutoff_dt = datetime.now() - timedelta(days=int(days))
    cutoff_ts = int(cutoff_dt.timestamp())

    events = []

    for page in range(1, max_pages + 1):
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": per_page,
            "page": page,
            "from": cutoff_ts,
            "extended": 1,
        }
        r = requests.get(url, params=params, timeout=20)
        if r.status_code != 200:
            break

        tracks = r.json().get("recenttracks", {}).get("track", []) or []
        if not tracks:
            break

        for t in tracks:
            if not isinstance(t, dict):
                continue
            uts = ((t.get("date") or {}).get("uts"))
            if not uts:
                continue

            artist = t.get("artist", {})
            artist_name = artist.get("#text") if isinstance(artist, dict) else str(artist or "")
            track_name = t.get("name") or ""

            try:
                ts = int(uts)
            except Exception:
                continue

            events.append({
                "ts": ts,
                "artist": artist_name,
                "track": track_name,
            })

        time.sleep(0.05)

    # sort ascending by time
    events.sort(key=lambda x: x["ts"])
    return events


def attached_artists_for_anchor(events, anchor_artist, window_minutes=60, min_anchor_plays=5, top_n=15):
    if not events or not anchor_artist:
        return []

    A = _norm(anchor_artist)
    win = int(window_minutes) * 60

    # Build quick index by time
    ts_list = [e["ts"] for e in events]
    artists = [_norm(e["artist"]) for e in events]
    artists_raw = [e["artist"] for e in events]

    # positions where artist == A
    anchor_idxs = [i for i, a in enumerate(artists) if a == A]
    nA = len(anchor_idxs)
    if nA < min_anchor_plays:
        return []

    # For each A occurrence, look forward while within time window
    hit_counts = {}           # B -> number of anchor occurrences that had at least one B in window
    first_hit_ts = {}         # optional: earliest timestamp seen for B
    for idx in anchor_idxs:
        t0 = ts_list[idx]
        seen_in_window = set()

        j = idx + 1
        while j < len(ts_list) and (ts_list[j] - t0) <= win:
            b = artists[j]
            if b and b != A:
                seen_in_window.add(b)
                if b not in first_hit_ts:
                    first_hit_ts[b] = ts_list[j]
            j += 1

        for b in seen_in_window:
            hit_counts[b] = hit_counts.get(b, 0) + 1

    # Build rows with probabilities
    # Map normalized -> a representative display name (first one we saw)
    display_name = {}
    for raw in artists_raw:
        k = _norm(raw)
        if k and k not in display_name:
            display_name[k] = raw

    rows = []
    for b, hits in hit_counts.items():
        p = hits / nA
        rows.append({
            "Artist B": display_name.get(b, b),
            "P(B within 60m | A)": round(p, 3),
            "Anchors (A plays)": nA,
            "Windows with B": hits,
        })

    rows.sort(key=lambda x: x["P(B within 60m | A)"], reverse=True)
    return rows[:top_n]


def correlation_matrix(events, anchor_artist, attached_rows, window_minutes=60):
    labels = [anchor_artist] + [r["Artist B"] for r in attached_rows]
    # compute P(B|A) for each label as anchor
    mats = []
    for a in labels:
        rows = attached_artists_for_anchor(events, a, window_minutes=window_minutes, min_anchor_plays=1, top_n=200)
        prob_map = {_norm(r["Artist B"]): r["P(B within 60m | A)"] for r in rows}
        row_probs = []
        for b in labels:
            if _norm(a) == _norm(b):
                row_probs.append(1.0)
            else:
                row_probs.append(float(prob_map.get(_norm(b), 0.0)))
        mats.append(row_probs)
    return labels, mats

import math
import random

def jaccard(a_set, b_set):
    if not a_set and not b_set:
        return 0.0
    inter = len(a_set & b_set)
    union = len(a_set | b_set)
    return inter / union if union else 0.0

def get_artist_features_for_galaxy(top_artists, meta, recent_counts, top_n=500):
    out = []
    for a in (top_artists or [])[:top_n]:
        name = a.get("name") or ""
        if not name:
            continue
        info = (meta or {}).get(name, {}) if isinstance(meta, dict) else {}
        tags = set([t.strip().lower() for t in (info.get("tags") or []) if str(t).strip()])
        moods = set([m.strip().lower() for m in (info.get("moods") or []) if str(m).strip()])

        # skip entirely if no tags and no moods
        if not tags and not moods:
            continue

        try:
            playcount = int(a.get("playcount", 0))
        except Exception:
            playcount = 0

        recent_plays = recent_counts.get(_normalize_artist_name(name), 0)

        out.append({
            "name": name,
            "playcount": playcount,
            "recent_plays": recent_plays,
            "tags": tags,
            "moods": moods,
            "tagged": True,
        })
    return out

def build_similarity_edges(items, meta, use="tags+moods", min_sim=0.35):
    corr = make_seed_corr()

    idxs = [i for i, it in enumerate(items) if it.get("tagged")]
    adj = {i: [] for i in idxs}

    def weights_for_mode(mode: str):
        if mode == "moods":
            return 0.90, 0.10
        if mode == "tags":
            return 0.15, 0.85
        # tags+moods
        return 0.75, 0.25

    mood_w, tag_w = weights_for_mode(use)

    # cache meta lookups
    info_cache = {}
    for i in idxs:
        name = items[i]["name"]
        info_cache[i] = (meta or {}).get(name, {}) if isinstance(meta, dict) else {}

    for ii in range(len(idxs)):
        for jj in range(ii + 1, len(idxs)):
            a = idxs[ii]
            b = idxs[jj]
            sim = artist_similarity(
                info_cache[a],
                info_cache[b],
                corr=corr,
                mood_weight=mood_w,
                tag_weight=tag_w
            )
            if sim >= min_sim:
                adj[a].append(b)
                adj[b].append(a)

    return adj

def assign_galaxy_positions(items, adj, seed=42):
    rng = random.Random(seed)
    n = len(items)
    x = [0.0] * n
    y = [0.0] * n

    if n == 0:
        return x, y

    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in adj.get(i, []):
            G.add_edge(i, j)

    if G.number_of_edges() > 0:
        pos = nx.spring_layout(G, seed=seed, k=1.8, iterations=300)
        for i, (px, py) in pos.items():
            x[i] = float(px)
            y[i] = float(py)
    else:
        # no edges at all — spread in a loose circle so nothing piles up
        for i in range(n):
            ang = (i / max(n, 1)) * 2 * math.pi
            r = 1.0 + rng.uniform(-0.2, 0.2)
            x[i] = r * math.cos(ang)
            y[i] = r * math.sin(ang)

    # nudge any nodes still sitting exactly at origin
    for i in range(n):
        if x[i] == 0.0 and y[i] == 0.0:
            ang = rng.random() * 2 * math.pi
            r = rng.uniform(0.3, 0.8)
            x[i] = r * math.cos(ang)
            y[i] = r * math.sin(ang)

    return x, y

def scale_marker_size(playcount):
    # log scaling keeps sizes sane
    return 6 + (math.log10(max(playcount, 1)) * 6)

def tail_vector(recent_plays):
    # movement illusion: more recent plays => longer tail
    # (kept subtle so it isn't noisy)
    mag = min(max(recent_plays, 0), 30) / 30.0
    return mag

def _k(s: str) -> str:
    return (s or "").strip().lower()

def make_seed_corr():
    corr = {}

    def link(a, b, w):
        a, b = _k(a), _k(b)
        if not a or not b or a == b:
            return
        corr[(a, b)] = max(corr.get((a, b), 0), w)
        corr[(b, a)] = max(corr.get((b, a), 0), w)

    # --- Your explicit preferences ---
    link("pop", "girlypop", 0.95)

    link("indie", "indie pop", 0.92)
    link("indie", "indie rock", 0.92)
    link("indie pop", "indie rock", 0.85)

    link("nostalgic", "elder emo", 0.95)
    link("nostalgic", "scene kid", 0.90)
    link("nostalgic", "angsty", 0.85)
    link("elder emo", "scene kid", 0.95)
    link("elder emo", "angsty", 0.90)
    link("scene kid", "angsty", 0.90)

    # pop punk closer to alternative than emo pop
    link("pop punk", "alternative", 0.82)
    link("pop punk", "emo pop", 0.58)

    # michigan rap and mumble rap less so
    link("michigan rap", "mumble rap", 0.25)

    # --- Extra structure you explicitly wanted earlier ---
    link("rock", "alternative", 0.85)  # rock ~ alternative (strong)
    link("alternative", "indie rock", 0.75)

    return corr

def best_soft_match(a_set: set, b_set: set, corr: dict) -> float:
    if not a_set or not b_set:
        return 0.0
    best = 0.0
    for a in a_set:
        for b in b_set:
            if a == b:
                continue
            best = max(best, corr.get((a, b), 0.0))
    return best

def artist_similarity(a_info: dict, b_info: dict, corr: dict,
                      mood_weight=0.75, tag_weight=0.25):
    a_moods = set(_k(x) for x in (a_info.get("moods") or []) if _k(x))
    b_moods = set(_k(x) for x in (b_info.get("moods") or []) if _k(x))

    a_tags = set(_k(x) for x in (a_info.get("tags") or []) if _k(x))
    b_tags = set(_k(x) for x in (b_info.get("tags") or []) if _k(x))

    mood_overlap = jaccard(a_moods, b_moods)
    tag_overlap = jaccard(a_tags, b_tags)

    mood_soft = best_soft_match(a_moods, b_moods, corr)
    tag_soft = best_soft_match(a_tags, b_tags, corr)

    # exact match dominates, but correlations help pull things together
    mood_score = max(mood_overlap, 0.85 * mood_soft)
    tag_score = max(tag_overlap, 0.70 * tag_soft)

    return (mood_weight * mood_score) + (tag_weight * tag_score)

def make_bump_chart(history: dict, artists: list, overall_ranks: dict, recent_artist: str, top_n: int = 12) -> go.Figure:
    from datetime import datetime

    def _parse(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except Exception:
            return None

    # Sort snapshots chronologically
    snapshots = sorted(
        [(dt, snap) for ts, snap in history.items()
         if (dt := _parse(ts)) and isinstance(snap, dict)],
        key=lambda x: x[0],
    )

    if len(snapshots) < 2:
        return None

    # Decide which artists to plot: surrounding list, capped at top_n by current rank
    candidates = sorted(
        [a for a in artists if overall_ranks.get(a) is not None],
        key=lambda a: overall_ranks[a],
    )[:top_n]

    if not candidates:
        return None

    # Build a time series of ranks per artist
    # {artist: [(datetime, rank), ...]}
    series = {a: [] for a in candidates}
    for dt, snap in snapshots:
        for a in candidates:
            info = snap.get(a)
            if isinstance(info, dict) and info.get("rank") is not None:
                series[a].append((dt, int(info["rank"])))

    # Drop artists with fewer than 2 observations
    series = {a: pts for a, pts in series.items() if len(pts) >= 2}
    if not series:
        return None

    # Color palette — enough for 12 artists
    PALETTE = [
        "#7F77DD", "#1D9E75", "#D85A30", "#D4537E",
        "#BA7517", "#378ADD", "#639922", "#888780",
        "#534AB7", "#0F6E56", "#993C1D", "#993556",
    ]
    color_map = {}
    palette_i = 0
    for a in series:
        if a.lower() == recent_artist.lower():
            color_map[a] = "#00BFFF"  # deepskyblue — matches your existing highlight
        else:
            color_map[a] = PALETTE[palette_i % len(PALETTE)]
            palette_i += 1

    fig = go.Figure()

    for a, pts in series.items():
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        color = color_map[a]
        is_current = a.lower() == recent_artist.lower()

        # Main line — spline smoothing gives the bezier-curve look
        fig.add_trace(go.Scatter(
            x=xs,
            y=ys,
            mode="lines+markers",
            name=a,
            line=dict(
                color=color,
                width=3.5 if is_current else 2,
                shape="spline",
                smoothing=0.8,
            ),
            marker=dict(
                color=color,
                size=7 if is_current else 5,
                line=dict(color="white", width=1.5),
            ),
            hovertemplate=f"<b>{a}</b><br>Rank: %{{y}}<br>%{{x|%b %d %H:%M}}<extra></extra>",
            showlegend=False,
        ))

        # Left-side name annotation (at first observation)
        first_x, first_y = xs[0], ys[0]
        fig.add_annotation(
            x=first_x,
            y=first_y,
            text=a,
            xanchor="right",
            xshift=-10,
            showarrow=False,
            font=dict(size=11, color=color),
        )

        # Right-side name + net delta annotation (at last observation)
        last_x, last_y = xs[-1], ys[-1]
        first_rank = ys[0]
        delta = first_rank - last_y  # positive = risen
        arrow = " ↑" if delta > 0 else " ↓" if delta < 0 else ""
        fig.add_annotation(
            x=last_x,
            y=last_y,
            text=f"{a}{arrow}",
            xanchor="left",
            xshift=10,
            showarrow=False,
            font=dict(size=11, color=color),
        )

    fig.update_yaxes(
        autorange="reversed",       # rank 1 at the top
        title="Overall rank",
        dtick=1,
        gridcolor="rgba(128,128,128,0.15)",
    )
    fig.update_xaxes(
        title="Snapshot time",
        gridcolor="rgba(128,128,128,0.10)",
    )
    fig.update_layout(
        title="Rank over time (surrounding artists)",
        height=420,
        margin=dict(l=140, r=140, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="closest",
    )

    return fig

def make_rank_gravity_fig(full_top_artists):
    if not full_top_artists:
        return None

    ranks = []
    playcounts = []
    for i, a in enumerate(full_top_artists):
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        ranks.append(i + 1)
        playcounts.append(pc)

    if not playcounts:
        return None

    # play count gaps between consecutive ranks
    gaps = [0] + [playcounts[i - 1] - playcounts[i] for i in range(1, len(playcounts))]

    # band boundaries and labels
    band_cutoffs = [10, 25, 50, 100, 200, 300, 500]
    band_colors = {
        10:  "#7F77DD",
        25:  "#1D9E75",
        50:  "#D85A30",
        100: "#D4537E",
        200: "#BA7517",
        300: "#378ADD",
        500: "#639922",
    }

    def get_band(rank):
        for cutoff in band_cutoffs:
            if rank <= cutoff:
                return cutoff
        return band_cutoffs[-1]

    colors = [band_colors[get_band(r)] for r in ranks]

    fig = go.Figure()

    # main playcount line
    fig.add_trace(go.Scatter(
        x=ranks,
        y=playcounts,
        mode="lines",
        name="Playcount",
        line=dict(color="#7F77DD", width=2),
        hovertemplate="Rank %{x}<br>Plays: %{y:,}<extra></extra>",
    ))

    # band boundary vertical lines + annotations
    prev_cutoff = 0
    for cutoff in band_cutoffs:
        if cutoff > len(playcounts):
            break
        boundary_play = playcounts[cutoff - 1]
        prev_play = playcounts[prev_cutoff] if prev_cutoff < len(playcounts) else playcounts[0]
        drop = prev_play - boundary_play

        fig.add_vline(
            x=cutoff,
            line=dict(color=band_colors[cutoff], width=1, dash="dot"),
        )
        fig.add_annotation(
            x=cutoff,
            y=boundary_play,
            text=f"#{cutoff}<br>{boundary_play:,} plays",
            showarrow=False,
            yshift=14,
            font=dict(size=10, color=band_colors[cutoff]),
            bgcolor="rgba(0,0,0,0.4)",
        )
        prev_cutoff = cutoff

    # gap bar chart on a secondary y axis — shows the cliffs
    fig.add_trace(go.Bar(
        x=ranks,
        y=gaps,
        name="Gap to next rank",
        marker_color=colors,
        opacity=0.4,
        yaxis="y2",
        hovertemplate="Rank %{x}<br>Gap: %{y:,} plays<extra></extra>",
    ))

    fig.update_layout(
        title="Rank gravity: play count curve + gaps",
        xaxis=dict(
            title="Rank",
            rangeslider=dict(visible=True),
            range=[1, 200],
        ),
        yaxis=dict(
            title="Playcount",
            gridcolor="rgba(128,128,128,0.15)",
        ),
        yaxis2=dict(
            title="Gap to next rank",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        height=480,
        margin=dict(l=60, r=60, t=50, b=60),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.15),
        hovermode="x unified",
    )

    return fig

def make_play_club_fig(full_top_artists):
    tiers = [
        (1000, "1000 club", "#7F77DD"),
        (500,  "500 club",  "#1D9E75"),
        (250,  "250 club",  "#D85A30"),
        (100,  "100 club",  "#D4537E"),
    ]

    tier_artists = {}
    for threshold, label, color in tiers:
        tier_artists[threshold] = []

    for a in full_top_artists:
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            continue
        name = a.get("name", "")
        for threshold, label, color in tiers:
            if pc >= threshold:
                tier_artists[threshold].append((name, pc))
                break

    # counts per tier (exclusive — only the highest tier they qualify for)
    counts = [len(tier_artists[t]) for t, _, _ in tiers]
    labels = [label for _, label, _ in tiers]
    colors = [color for _, _, color in tiers]

    fig = go.Figure()

    # horizontal bars — widest at bottom (100 club), narrowest at top (1000 club)
    for i, (threshold, label, color) in enumerate(tiers):
        members = tier_artists[threshold]
        count = len(members)
        if count == 0:
            continue

        # tooltip lists the artists in that tier
        artist_list = "<br>".join(f"{n} ({pc:,})" for n, pc in members[:30])
        if len(members) > 30:
            artist_list += f"<br>...and {len(members) - 30} more"

        fig.add_trace(go.Bar(
            x=[count],
            y=[label],
            orientation="h",
            marker_color=color,
            text=str(count),
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=f"<b>{label}</b> ({count} artists)<br><br>{artist_list}<extra></extra>",
            showlegend=False,
        ))

    fig.update_layout(
        title="Play count club membership",
        xaxis=dict(
            title="Number of artists",
            gridcolor="rgba(128,128,128,0.15)",
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[label for _, label, _ in reversed(tiers)],
        ),
        height=280,
        margin=dict(l=80, r=40, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        barmode="relative",
    )

    return fig, tier_artists, tiers

import numpy as np
from datetime import datetime, timedelta

def compute_rank_projections(history, full_top_artists, top_n=500):
    def _parse(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except Exception:
            return None

    # build per-artist time series from history
    series = {}
    for ts, snap in history.items():
        dt = _parse(ts)
        if not dt or not isinstance(snap, dict):
            continue
        for artist, info in snap.items():
            if not isinstance(info, dict):
                continue
            pc = info.get("playcount")
            if pc is not None:
                series.setdefault(artist, []).append((dt, int(pc)))

    # only keep top_n artists by current rank
    candidates = sorted(
        [a.get("name") for a in full_top_artists if a.get("name")],
        key=lambda a: full_top_artists[[x.get("name") for x in full_top_artists].index(a)].get("playcount", 0) if a in [x.get("name") for x in full_top_artists] else 0,
        reverse=True,
    )[:top_n]

    results = {}
    now = datetime.now()
    one_year = now + timedelta(days=365)
    two_years = now + timedelta(days=730)
    five_years = now + timedelta(days=365 * 5)

    for artist in candidates:
        pts = series.get(artist)
        if not pts or len(pts) < 3:
            continue

        pts_sorted = sorted(pts, key=lambda x: x[0])
        # convert to numeric days since first observation
        t0 = pts_sorted[0][0]
        xs = np.array([(p[0] - t0).total_seconds() / 86400.0 for p in pts_sorted])
        ys = np.array([p[1] for p in pts_sorted])

        # linear regression
        coeffs = np.polyfit(xs, ys, 1)
        slope, intercept = coeffs

        current_y = float(ys[-1])

        def predict(dt, _t0=t0, _slope=slope, _intercept=intercept, _floor=current_y):
            x = (dt - _t0).total_seconds() / 86400.0
            return max(_floor, _slope * x + _intercept)

        # residuals for confidence band
        y_pred = np.polyval(coeffs, xs)
        residuals = ys - y_pred
        std_err = np.std(residuals)

        results[artist] = {
            "pts": pts_sorted,
            "slope": max(slope, 0.0),
            "intercept": intercept,
            "t0": t0,
            "std_err": std_err,
            "predict": predict,
            "projected_1y": predict(one_year),
            "projected_5y": predict(five_years),
            "current_playcount": current_y,
        }

    return results

def hex_to_rgba(hex_color, alpha=0.08):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "rgba(%d,%d,%d,%s)" % (r, g, b, alpha)

def make_rank_projection_fig(projections, overall_ranks, selected_artists):
    PALETTE = [
        "#7F77DD", "#1D9E75", "#D85A30", "#D4537E",
        "#BA7517", "#378ADD", "#639922", "#534AB7",
        "#0F6E56", "#993C1D", "#993556", "#888780",
    ]

    fig = go.Figure()
    now = datetime.now()
    one_year = now + timedelta(days=365)
    two_years = now + timedelta(days=730)
    five_years = now + timedelta(days=365 * 5)

    for idx, artist in enumerate(selected_artists):
        proj = projections.get(artist)
        if not proj:
            continue

        color = PALETTE[idx % len(PALETTE)]
        pts = proj["pts"]
        xs_actual = [p[0] for p in pts]
        ys_actual = [p[1] for p in pts]

        # actual history — solid line
        fig.add_trace(go.Scatter(
            x=xs_actual,
            y=ys_actual,
            mode="lines+markers",
            name=artist,
            line=dict(color=color, width=2),
            marker=dict(size=4),
            legendgroup=artist,
            hovertemplate=f"<b>{artist}</b><br>%{{x|%b %d %Y}}<br>Plays: %{{y:,}}<extra></extra>",
        ))

        # projection line — dashed
        proj_end = five_years
        proj_xs = [pts[-1][0], proj_end]
        proj_ys = [proj["predict"](dt) for dt in proj_xs]

        fig.add_trace(go.Scatter(
            x=proj_xs,
            y=proj_ys,
            mode="lines",
            name=f"{artist} (projected)",
            line=dict(color=color, width=1.5, dash="dash"),
            legendgroup=artist,
            showlegend=False,
            hovertemplate=f"<b>{artist}</b> projected<br>%{{x|%b %d %Y}}<br>~%{{y:,.0f}} plays<extra></extra>",
        ))

        # confidence band — widens over time
        std = proj["std_err"]
        band_xs = [pts[-1][0]] + [now + timedelta(days=d) for d in range(30, 365 * 5 + 1, 30)]
        band_upper = [proj["predict"](dt) + std * float(abs((dt - now).total_seconds() / 86400.0 / 30)) ** 0.5
                      for dt in band_xs]
        band_lower = [max(0.0, proj["predict"](dt) - std * float(abs((dt - now).total_seconds() / 86400.0 / 30)) ** 0.5)
                      for dt in band_xs]

        fig.add_trace(go.Scatter(
            x=band_xs + band_xs[::-1],
            y=band_upper + band_lower[::-1],
            fill="toself",
            fillcolor=hex_to_rgba(color),
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            legendgroup=artist,
        ))

    # marker lines for 1y and 5y
    fig.add_vline(x=one_year, line=dict(color="rgba(255,255,255,0.2)", width=1, dash="dot"))
    fig.add_vline(x=two_years, line=dict(color="rgba(255,255,255,0.15)", width=1, dash="dot"))
    fig.add_annotation(x=one_year, y=1, yref="paper", text="1 year", showarrow=False,
                       font=dict(size=10, color="rgba(255,255,255,0.4)"), yshift=8)
    fig.add_annotation(x=two_years, y=1, yref="paper", text="2 years", showarrow=False,
                       font=dict(size=10, color="rgba(255,255,255,0.4)"), yshift=8)

    fig.update_layout(
        title="Playcount projection (at current pace)",
        xaxis=dict(title="Date", gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(title="Playcount", gridcolor="rgba(128,128,128,0.15)"),
        height=500,
        margin=dict(l=60, r=40, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.15),
    )

    return fig


def find_top50_candidates(projections, overall_ranks, full_top_artists, rank_window=(51, 300)):
    # current playcount at rank 50
    sorted_artists = sorted(full_top_artists, key=lambda a: int(a.get("playcount", 0)), reverse=True)
    if len(sorted_artists) < 50:
        return []

    top50_threshold = int(sorted_artists[49].get("playcount", 0))

    now = datetime.now()
    six_months = now + timedelta(days=182)

    candidates = []
    for artist, proj in projections.items():
        rank = overall_ranks.get(artist)
        if rank is None:
            continue
        if not (rank_window[0] <= rank <= rank_window[1]):
            continue

        projected_6m = proj["predict"](six_months)
        current_pc = proj["current_playcount"]
        gap = top50_threshold - current_pc
        days_needed = gap / proj["slope"] if proj["slope"] > 0 else None

        if projected_6m >= top50_threshold:
            candidates.append({
                "Artist": artist,
                "Current rank": rank,
                "Current plays": f"{int(current_pc):,}",
                "Top 50 threshold": f"{top50_threshold:,}",
                "Gap": f"{int(gap):,}",
                "Projected plays (6mo)": f"{int(projected_6m):,}",
                "Est. days to top 50": int(days_needed) if days_needed and days_needed > 0 else "—",
            })

    candidates.sort(key=lambda x: x["Current rank"])
    return candidates, top50_threshold

def compute_velocity_tiers(full_top_artists, history, top_n=100):
    def _parse(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except Exception:
            return None

    # find first snapshot date per artist
    first_seen = {}
    for ts, snap in history.items():
        dt = _parse(ts)
        if not dt or not isinstance(snap, dict):
            continue
        for artist in snap:
            if artist not in first_seen or dt < first_seen[artist]:
                first_seen[artist] = dt

    now = datetime.now()
    candidates = [a.get("name") for a in full_top_artists[:top_n] if a.get("name")]
    tiers = {"Cheetah": [], "Cardinal": [], "Mountain Goat": [], "Kitty Cat": [], "Snail": [], "Sloth": [], "Fading": []}

    baseline_for_tiers = load_long_term_baseline()

    for a in full_top_artists[:top_n]:
        name = a.get("name")
        if not name:
            continue
        try:
            curr_plays = int(a.get("playcount", 0))
        except Exception:
            curr_plays = 0

        first_dt = first_seen.get(name)
        if not first_dt:
            tiers["Sloth"].append({"Artist": name, "Plays/day": 0.0})
            continue

        days_since = max((now - first_dt).total_seconds() / 86400.0, 1.0)

        base = baseline_for_tiers.get(name, {})
        base_plays = base.get("playcount")
        if base_plays is None:
            play_gain = curr_plays
        else:
            play_gain = max(0, curr_plays - int(base_plays))

        slope = round(play_gain / days_since, 2)

        row = {"Artist": name, "Plays/day": slope}

        if slope >= 1.0:
            tiers["Cheetah"].append(row)
        elif slope >= 0.59:
            tiers["Cardinal"].append(row)
        elif slope >= 0.35:
            tiers["Mountain Goat"].append(row)
        elif slope >= 0.19:
            tiers["Kitty Cat"].append(row)
        elif slope >= 0.06:
            tiers["Snail"].append(row)
        else:
            tiers["Sloth"].append(row)

    for k in tiers:
        tiers[k].sort(key=lambda x: x["Plays/day"], reverse=True)

    return tiers


def compute_era_density(full_top_artists, meta):
    era_plays = {}
    era_artists = {}

    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0

        info = meta.get(name, {})
        era = (info.get("era") or "").strip()
        if not era:
            era = "Untagged"

        era_plays[era] = era_plays.get(era, 0) + pc
        era_artists[era] = era_artists.get(era, 0) + 1

    rows = []
    for era in era_plays:
        rows.append({
            "Era": era,
            "Total plays": era_plays[era],
            "Artist count": era_artists[era],
            "Avg plays/artist": round(era_plays[era] / max(era_artists[era], 1)),
        })

    rows.sort(key=lambda x: x["Total plays"], reverse=True)
    return rows


def make_era_density_fig(rows):
    if not rows:
        return None

    eras = [r["Era"] for r in rows]
    plays = [r["Total plays"] for r in rows]
    counts = [r["Artist count"] for r in rows]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=eras,
        y=plays,
        name="Total plays",
        marker_color="#7F77DD",
        hovertemplate="<b>%{x}</b><br>Total plays: %{y:,}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=eras,
        y=counts,
        name="Artist count",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color="#D85A30", width=2),
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b><br>Artists: %{y}<extra></extra>",
    ))

    fig.update_layout(
        title="Era density: plays and artist count by decade",
        xaxis=dict(title="Era"),
        yaxis=dict(title="Total plays", gridcolor="rgba(128,128,128,0.15)"),
        yaxis2=dict(title="Artist count", overlaying="y", side="right", showgrid=False),
        height=360,
        margin=dict(l=60, r=60, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2),
        barmode="group",
    )

    return fig


def compute_displacement(baseline_data, full_top_artists, min_rise=10):
    current_rank = {}
    for i, a in enumerate(full_top_artists):
        name = a.get("name")
        if name:
            current_rank[name] = i + 1

    rows = []
    for name, curr_r in current_rank.items():
        base = baseline_data.get(name, {})
        base_r = base.get("rank")
        if base_r is None:
            continue
        rise = base_r - curr_r
        if rise < min_rise:
            continue

        # find who currently occupies ranks between curr_r and base_r
        displaced = []
        for other, other_curr in current_rank.items():
            if other == name:
                continue
            other_base = (baseline_data.get(other) or {}).get("rank")
            if other_base is None:
                continue
            if curr_r <= other_base <= base_r and other_curr > other_base:
                displaced.append(other)

        rows.append({
            "Artist": name,
            "Was": base_r,
            "Now": curr_r,
            "Rose": rise,
            "Displaced": ", ".join(displaced[:4]) if displaced else "—",
        })

    rows.sort(key=lambda x: x["Rose"], reverse=True)
    return rows


def compute_genre_momentum(history, full_top_artists, meta, days=14):
    def _parse(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except Exception:
            return None

    now = datetime.now()
    cutoff = now - timedelta(days=days)

    # build play totals per artist at start and end of window
    window_snaps = sorted(
        [(dt, snap) for ts, snap in history.items()
         if (dt := _parse(ts)) and isinstance(snap, dict) and dt >= cutoff],
        key=lambda x: x[0]
    )

    if len(window_snaps) < 2:
        return []

    first_snap = window_snaps[0][1]
    last_snap = window_snaps[-1][1]

    # build tag -> play gain mapping
    tag_gains = {}
    tag_artist_counts = {}

    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue

        first_info = first_snap.get(name, {})
        last_info = last_snap.get(name, {})
        if not isinstance(first_info, dict) or not isinstance(last_info, dict):
            continue

        first_pc = first_info.get("playcount")
        last_pc = last_info.get("playcount")
        if first_pc is None or last_pc is None:
            continue

        gain = int(last_pc) - int(first_pc)
        if gain <= 0:
            continue

        tags = meta.get(name, {}).get("tags") or []
        for tag in tags:
            tag = tag.strip()
            if not tag:
                continue
            tag_gains[tag] = tag_gains.get(tag, 0) + gain
            tag_artist_counts[tag] = tag_artist_counts.get(tag, 0) + 1

    rows = []
    for tag, gain in tag_gains.items():
        rows.append({
            "Tag": tag,
            "Play gain": gain,
            "Artists contributing": tag_artist_counts.get(tag, 0),
            "Avg gain/artist": round(gain / max(tag_artist_counts.get(tag, 1), 1), 1),
        })

    rows.sort(key=lambda x: x["Play gain"], reverse=True)
    return rows


def make_genre_momentum_fig(rows, top_n=15):
    if not rows:
        return None

    rows = rows[:top_n]
    tags = [r["Tag"] for r in rows]
    gains = [r["Play gain"] for r in rows]
    counts = [r["Artists contributing"] for r in rows]

    PALETTE = [
        "#7F77DD", "#1D9E75", "#D85A30", "#D4537E",
        "#BA7517", "#378ADD", "#639922", "#534AB7",
        "#0F6E56", "#993C1D", "#993556", "#888780",
        "#7F77DD", "#1D9E75", "#D85A30",
    ]
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(tags))]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=gains,
        y=tags,
        orientation="h",
        marker_color=colors,
        text=[str(g) for g in gains],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Play gain: %{x}<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        title="Genre momentum: play gains by tag",
        xaxis=dict(title="Play gain", gridcolor="rgba(128,128,128,0.15)"),
        yaxis=dict(title="", categoryorder="total ascending"),
        height=max(300, len(tags) * 32 + 80),
        margin=dict(l=120, r=60, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def compute_crowded_neighborhoods(full_top_artists, window=10):
    plays = []
    names = []

    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        names.append(name)
        plays.append(pc)

    def get_neighborhoods(plays_slice, names_slice, rank_offset=0):
        neighborhoods = []
        for i in range(len(plays_slice) - window + 1):
            band = plays_slice[i:i + window]
            band_names = names_slice[i:i + window]
            spread = band[0] - band[-1]
            avg = sum(band) / len(band)
            neighborhoods.append({
                "Start rank": i + 1 + rank_offset,
                "End rank": i + window + rank_offset,
                "Play spread": spread,
                "Avg plays": round(avg),
                "Artists": ", ".join(band_names[:5]) + ("..." if len(band_names) > 5 else ""),
            })
        neighborhoods.sort(key=lambda x: x["Play spread"])
        return neighborhoods[:20]

    city_a = get_neighborhoods(plays[:200], names[:200], rank_offset=0)
    city_b = get_neighborhoods(plays[200:], names[200:], rank_offset=200)

    return city_a, city_b


def make_crowded_neighborhood_fig(full_top_artists, top_neighborhoods, highlight_n=3):
    if not full_top_artists:
        return None

    ranks = list(range(1, len(full_top_artists) + 1))
    plays = []
    for a in full_top_artists:
        try:
            plays.append(int(a.get("playcount", 0)))
        except Exception:
            plays.append(0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ranks,
        y=plays,
        mode="lines",
        name="Playcount",
        line=dict(color="#7F77DD", width=2),
        hovertemplate="Rank %{x}<br>Plays: %{y:,}<extra></extra>",
    ))

    for i, n in enumerate(top_neighborhoods[:highlight_n]):
        start = n["Start rank"]
        end = n["End rank"]
        start_play = plays[start - 1] if start - 1 < len(plays) else 0
        end_play = plays[end - 1] if end - 1 < len(plays) else 0
        mid_play = (start_play + end_play) / 2

        fig.add_shape(
            type="rect",
            x0=start, x1=end,
            y0=end_play * 0.98, y1=start_play * 1.02,
            fillcolor="rgba(215,90,48,0.12)",
            line=dict(color="#D85A30", width=1, dash="dot"),
        )
        fig.add_annotation(
            x=(start + end) / 2,
            y=start_play * 1.04,
            text=f"#{start}-{end}<br>{n['Play spread']} play spread",
            showarrow=False,
            font=dict(size=9, color="#D85A30"),
            bgcolor="rgba(0,0,0,0.4)",
        )

        fig.update_layout(
            title="Crowded neighborhoods (tightest rank bands)",
            xaxis=dict(
                title="Rank",
                rangeslider=dict(visible=True),
            ),
            yaxis=dict(title="Playcount", gridcolor="rgba(128,128,128,0.15)"),
            height=350,
            margin=dict(l=60, r=40, t=40, b=60),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

    return fig


def make_taste_fingerprint_fig(full_top_artists, meta, top_tags=10):
    tag_plays = {}

    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0

        tags = meta.get(name, {}).get("tags") or []
        for tag in tags:
            tag = tag.strip()
            if tag:
                tag_plays[tag] = tag_plays.get(tag, 0) + pc

    if not tag_plays:
        return None

    sorted_tags = sorted(tag_plays.items(), key=lambda x: x[1], reverse=True)[:top_tags]
    labels = [t[0] for t in sorted_tags]
    values = [t[1] for t in sorted_tags]

    # close the radar loop
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(127,119,221,0.15)",
        line=dict(color="#7F77DD", width=2),
        marker=dict(size=6, color="#7F77DD"),
        hovertemplate="<b>%{theta}</b><br>Total plays: %{r:,}<extra></extra>",
    ))

    fig.update_layout(
        title="Taste fingerprint (plays by tag)",
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor="rgba(128,128,128,0.2)",
                tickfont=dict(size=9),
            ),
            angularaxis=dict(
                gridcolor="rgba(128,128,128,0.2)",
                tickfont=dict(size=11),
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=450,
        margin=dict(l=60, r=60, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return fig


def make_head_to_head_fig(projections, overall_ranks, artist_a, artist_b):
    if artist_a not in projections or artist_b not in projections:
        return None, None

    proj_a = projections[artist_a]
    proj_b = projections[artist_b]

    now = datetime.now()
    five_years = now + timedelta(days=365 * 5)

    def plays_at(proj, dt):
        return float(proj["predict"](dt))

    curr_a = plays_at(proj_a, now)
    curr_b = plays_at(proj_b, now)
    slope_a = float(proj_a["slope"])
    slope_b = float(proj_b["slope"])

    # find crossover: curr_a + slope_a*t = curr_b + slope_b*t
    crossover_date = None
    crossover_msg = None
    if abs(slope_a - slope_b) > 0.001:
        t_cross = (curr_b - curr_a) / (slope_a - slope_b)
        if 0 < t_cross < 365 * 5:
            crossover_date = now + timedelta(days=t_cross)
            chaser = artist_a if curr_a < curr_b else artist_b
            leader = artist_b if curr_a < curr_b else artist_a
            crossover_msg = "At current pace, **%s** passes **%s** in approximately **%d days** (%s)" % (
                chaser, leader, int(t_cross),
                crossover_date.strftime("%b %d, %Y")
            )

    proj_end = crossover_date + timedelta(days=120) if crossover_date else five_years

    fig = go.Figure()

    for artist, proj, color in [
        (artist_a, proj_a, "#7F77DD"),
        (artist_b, proj_b, "#D85A30"),
    ]:
        pts = proj["pts"]
        xs_actual = [p[0] for p in pts]
        ys_actual = [p[1] for p in pts]

        fig.add_trace(go.Scatter(
            x=xs_actual,
            y=ys_actual,
            mode="lines+markers",
            name=artist,
            line=dict(color=color, width=2.5),
            marker=dict(size=5, color=color),
            hovertemplate="<b>" + artist + "</b><br>%{x|%b %d %Y}<br>Plays: %{y:,}<extra></extra>",
        ))

        # project from now to proj_end in monthly steps so the line is smooth
        proj_dates = [now + timedelta(days=d) for d in range(0, int((proj_end - now).days) + 1, 7)]
        proj_ys = [plays_at(proj, dt) for dt in proj_dates]

        fig.add_trace(go.Scatter(
            x=proj_dates,
            y=proj_ys,
            mode="lines",
            name=artist + " (projected)",
            line=dict(color=color, width=1.5, dash="dash"),
            showlegend=False,
            hovertemplate="<b>" + artist + "</b> projected<br>%{x|%b %d %Y}<br>~%{y:,.0f} plays<extra></extra>",
        ))

    if crossover_date:
        crossover_y = (plays_at(proj_a, crossover_date) + plays_at(proj_b, crossover_date)) / 2
        fig.add_vline(
            x=crossover_date,
            line=dict(color="rgba(255,255,255,0.3)", width=1.5, dash="dot"),
        )
        fig.add_annotation(
            x=crossover_date,
            y=crossover_y,
            text="Crossover",
            showarrow=True,
            arrowhead=2,
            font=dict(size=11, color="rgba(255,255,255,0.7)"),
            bgcolor="rgba(0,0,0,0.5)",
            ay=-40,
        )

    # y axis range: bracket both artists with some padding
    all_ys = (
        [p[1] for p in proj_a["pts"]] +
        [p[1] for p in proj_b["pts"]] +
        [plays_at(proj_a, proj_end), plays_at(proj_b, proj_end)]
    )
    y_min = max(0, min(all_ys) * 0.95)
    y_max = max(all_ys) * 1.05

    fig.update_layout(
        title=artist_a + " vs " + artist_b,
        xaxis=dict(title="Date", gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(
            title="Playcount",
            gridcolor="rgba(128,128,128,0.15)",
            range=[y_min, y_max],
        ),
        height=460,
        margin=dict(l=60, r=40, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.15),
    )

    return fig, crossover_msg



# =========================================================
# Manually tracked artists (sub-500), random tagger, extra stats
# =========================================================

def get_manual_artists_latest(exclude_names=None):
    # latest logged playcount per manually-tracked artist, excluding any now in Top 500
    exclude = set((n or "").lower() for n in (exclude_names or []))
    latest = {}  # name -> (dt, playcount)
    for e in load_history_entries():
        if not e.get("manual"):
            continue
        dt = parse_ts(e.get("timestamp"))
        if not dt:
            continue
        for name, info in (e.get("data") or {}).items():
            if not isinstance(info, dict):
                continue
            pc = info.get("playcount")
            if pc is None or name.lower() in exclude:
                continue
            prev = latest.get(name)
            if prev is None or dt >= prev[0]:
                latest[name] = (dt, int(pc))
    rows = [(name, pc) for name, (dt, pc) in latest.items()]
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows


def make_manual_leaderboard_fig(rows):
    # rows: list of (name, playcount), already sorted desc. Pseudo-ranks start at 501.
    labels = []
    plays = []
    for i, (name, pc) in enumerate(rows):
        labels.append("%d. %s" % (501 + i, name))
        plays.append(pc)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=plays[::-1],
        y=labels[::-1],
        orientation="h",
        marker_color="#BA7517",
        text=[format(p, ",") for p in plays[::-1]],
        textposition="outside",
        hoverinfo="skip",
    ))
    fig.update_layout(
        title="Manually tracked artists (beyond your Top 500)",
        xaxis_title="Playcount",
        height=max(220, len(rows) * 34 + 90),
        margin=dict(l=170, r=50, t=50, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig.update_traces(marker_line_width=0)
    return fig


def render_manual_tracked_section(full_top_artists):
    st.markdown("### Manually Tracked Artists")
    st.caption("Sub-500 artists you've logged by hand, ranked by playcount and numbered from 501 down. "
               "An artist drops off this list automatically once they climb into your real Top 500.")

    current_names = set(a.get("name") for a in full_top_artists if a.get("name"))
    rows = get_manual_artists_latest(exclude_names=current_names)

    if not rows:
        st.info("Nothing logged yet. When a sub-500 artist plays, use the entry form to log its playcount "
                "and it'll show up here.")
        return

    fig = make_manual_leaderboard_fig(rows)
    st.plotly_chart(fig, use_container_width=True, key="manual_tracked_chart")

    table = [{"Pseudo-rank": 501 + i, "Artist": name, "Plays": pc}
             for i, (name, pc) in enumerate(rows)]
    st.dataframe(table, use_container_width=True, hide_index=True, key="manual_tracked_table")


def render_random_tagger(full_top_artists, overall_ranks):
    st.markdown("### Random Artist Tagger")
    st.caption("10 random artists from your Top 500. Fill in tags, moods, era, energy, and the listen-more flag "
               "for the artists that rarely surface while you're listening. Hit a new batch anytime.")

    names = [a.get("name") for a in full_top_artists if a.get("name")]
    if not names:
        st.caption("No artists loaded.")
        return

    if st.button("New batch", key="rt_new_batch") or "rt_batch" not in st.session_state:
        st.session_state.rt_batch = random.sample(names, min(10, len(names)))

    meta = load_artist_meta()
    tag_library, mood_library = get_tag_library(meta)

    done = 0
    for name in st.session_state.rt_batch:
        info = meta.get(name, {})
        has_meta = bool(info.get("tags") or info.get("moods"))
        if has_meta:
            done += 1

    st.caption("This batch: %d of %d already have tags or moods." % (done, len(st.session_state.rt_batch)))

    for name in st.session_state.rt_batch:
        info = meta.get(name, {})
        ak = safe_widget_key("rt", name)
        marker = "\u2705" if (info.get("tags") or info.get("moods")) else "\u2b1c"
        rnk = overall_ranks.get(name, "\u2014")
        with st.expander("%s  %s  (rank %s)" % (marker, name, rnk)):
            sel_tags = st.multiselect("Tags", options=tag_library,
                                      default=info.get("tags", []), key="rt_tags_%s" % ak)
            new_tag = st.text_input("New tag", key="rt_newtag_%s" % ak, placeholder="add a tag\u2026")
            sel_moods = st.multiselect("Moods", options=mood_library,
                                       default=info.get("moods", []), key="rt_moods_%s" % ak)
            new_mood = st.text_input("New mood", key="rt_newmood_%s" % ak, placeholder="add a mood\u2026")
            energy = st.slider("Energy", ENERGY_MIN, ENERGY_MAX,
                               value=int(info.get("energy", 3)), key="rt_energy_%s" % ak)
            era_val = info.get("era", "")
            if era_val not in ERA_OPTIONS:
                era_val = ""
            era = st.selectbox("Era", options=ERA_OPTIONS,
                               index=ERA_OPTIONS.index(era_val), key="rt_era_%s" % ak)
            listen_more = st.checkbox("Want to listen to more",
                                      value=bool(info.get("listen_more", False)), key="rt_listen_%s" % ak)
            if st.button("Save", key="rt_save_%s" % ak):
                m = load_artist_meta()
                existing = dict(m.get(name, {}))
                tags = list(sel_tags)
                moods = list(sel_moods)
                if new_tag and new_tag.strip():
                    tags = list(dict.fromkeys(tags + [new_tag.strip()]))
                if new_mood and new_mood.strip():
                    moods = list(dict.fromkeys(moods + [new_mood.strip()]))
                existing.update({
                    "tags": tags, "moods": moods, "energy": int(energy),
                    "era": era, "listen_more": bool(listen_more),
                })
                existing.setdefault("favorite_override", None)
                existing.setdefault("notes", "")
                m[name] = existing
                save_artist_meta(m)
                st.success("Saved %s." % name)


# ---------------- extra stats ----------------

def _stats_parse(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception:
        return None


def compute_period_leaders(history, period="quarter", top_n=15):
    # bucket snapshots by calendar period, gain = (last seen - first seen) within the bucket
    buckets = {}
    for ts, snap in history.items():
        dt = _stats_parse(ts)
        if not dt or not isinstance(snap, dict):
            continue
        if period == "quarter":
            key = "%d Q%d" % (dt.year, (dt.month - 1) // 3 + 1)
        elif period == "month":
            key = dt.strftime("%Y-%m")
        else:
            key = "%d" % dt.year
        buckets.setdefault(key, []).append((dt, snap))

    results = {}
    for key, items in buckets.items():
        items.sort(key=lambda x: x[0])
        first_snap, last_snap = items[0][1], items[-1][1]
        gains = {}
        for name in set(list(first_snap.keys()) + list(last_snap.keys())):
            f = first_snap.get(name, {})
            l = last_snap.get(name, {})
            fp = f.get("playcount") if isinstance(f, dict) else None
            lp = l.get("playcount") if isinstance(l, dict) else None
            if fp is None or lp is None:
                continue
            g = int(lp) - int(fp)
            if g > 0:
                gains[name] = g
        ranked = sorted(gains.items(), key=lambda x: x[1], reverse=True)[:top_n]
        if ranked:
            results[key] = ranked
    return results


def compute_milestone_watch(full_top_artists, within=15):
    rows = []
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            continue
        step = 25 if pc < 100 else (50 if pc < 500 else 100)
        nxt = ((pc // step) + 1) * step
        gap = nxt - pc
        if gap <= within:
            rows.append({"Artist": name, "Plays": pc, "Next milestone": nxt, "Plays away": gap})
    rows.sort(key=lambda x: x["Plays away"])
    return rows


def compute_biggest_binges(history, top_n=15, max_hours=48):
    series = {}
    for ts, snap in history.items():
        dt = _stats_parse(ts)
        if not dt or not isinstance(snap, dict):
            continue
        for name, info in snap.items():
            if isinstance(info, dict) and info.get("playcount") is not None:
                series.setdefault(name, []).append((dt, int(info["playcount"])))

    rows = []
    for name, pts in series.items():
        pts.sort(key=lambda x: x[0])
        best, best_span = 0, None
        for i in range(1, len(pts)):
            jump = pts[i][1] - pts[i - 1][1]
            hours = (pts[i][0] - pts[i - 1][0]).total_seconds() / 3600.0
            if jump > best and 0 < hours <= max_hours:
                best, best_span = jump, (pts[i][0], hours)
        if best > 0 and best_span:
            rows.append({"Artist": name, "Jump (plays)": best,
                         "Over (hrs)": round(best_span[1], 1),
                         "When": best_span[0].strftime("%m/%d %H:%M")})
    rows.sort(key=lambda x: x["Jump (plays)"], reverse=True)
    return rows[:top_n]


def compute_debuts(baseline_data, full_top_artists, top_n=50):
    rows = []
    for i, a in enumerate(full_top_artists):
        name = a.get("name")
        if not name:
            continue
        if name not in baseline_data:
            try:
                pc = int(a.get("playcount", 0))
            except Exception:
                pc = 0
            rows.append({"Current rank": i + 1, "Artist": name, "Plays": pc})
    rows.sort(key=lambda x: x["Current rank"])
    return rows[:top_n]


# ---------------- More Stats: expansion batch ----------------

def compute_consistency(history, full_top_artists, min_obs=4, top_n=25):
    # who gains plays the most steadily (low variance in per-snapshot gain) vs spiky
    series = {}
    for ts, snap in history.items():
        dt = _stats_parse(ts)
        if not dt or not isinstance(snap, dict):
            continue
        for name, info in snap.items():
            if isinstance(info, dict) and info.get("playcount") is not None:
                series.setdefault(name, []).append((dt, int(info["playcount"])))
    rows = []
    for name, pts in series.items():
        if len(pts) < min_obs:
            continue
        pts.sort(key=lambda x: x[0])
        gains = [pts[i][1] - pts[i - 1][1] for i in range(1, len(pts))]
        pos = [g for g in gains if g > 0]
        if len(pos) < 2:
            continue
        mean = sum(pos) / len(pos)
        var = sum((g - mean) ** 2 for g in pos) / len(pos)
        sd = var ** 0.5
        cv = (sd / mean) if mean else 0  # coefficient of variation: low = steady
        rows.append({"Artist": name, "Steadiness": round(1 / (1 + cv), 3),
                     "Avg gain/snapshot": round(mean, 2), "Observations": len(pts)})
    rows.sort(key=lambda x: x["Steadiness"], reverse=True)
    return rows[:top_n]


def compute_share_of_plays(full_top_artists, top_buckets=(1, 5, 10, 25, 50, 100)):
    plays = []
    for a in full_top_artists:
        try:
            plays.append(int(a.get("playcount", 0)))
        except Exception:
            plays.append(0)
    total = sum(plays) or 1
    rows = []
    for b in top_buckets:
        share = sum(plays[:b]) / total * 100
        rows.append({"Top N artists": b, "Share of all plays": "%.1f%%" % share})
    return rows, total


def compute_tag_leaderboard(full_top_artists, meta, top_n=25):
    tag_plays, tag_count = {}, {}
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        for t in (meta.get(name, {}).get("tags") or []):
            t = t.strip()
            if not t:
                continue
            tag_plays[t] = tag_plays.get(t, 0) + pc
            tag_count[t] = tag_count.get(t, 0) + 1
    rows = []
    for t, p in tag_plays.items():
        c = tag_count[t]
        rows.append({"Tag": t, "Total plays": p, "Artists": c,
                     "Avg plays/artist": round(p / max(c, 1))})
    rows.sort(key=lambda x: x["Total plays"], reverse=True)
    return rows[:top_n]


def compute_mood_leaderboard(full_top_artists, meta, top_n=25):
    mood_plays, mood_count = {}, {}
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        for m in (meta.get(name, {}).get("moods") or []):
            m = m.strip()
            if not m:
                continue
            mood_plays[m] = mood_plays.get(m, 0) + pc
            mood_count[m] = mood_count.get(m, 0) + 1
    rows = []
    for m, p in mood_plays.items():
        c = mood_count[m]
        rows.append({"Mood": m, "Total plays": p, "Artists": c,
                     "Avg plays/artist": round(p / max(c, 1))})
    rows.sort(key=lambda x: x["Total plays"], reverse=True)
    return rows[:top_n]


def compute_energy_profile(full_top_artists, meta):
    buckets = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    plays_b = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_e, n_e = 0, 0
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        e = meta.get(name, {}).get("energy")
        if isinstance(e, int) and 1 <= e <= 5:
            buckets[e] += 1
            plays_b[e] += pc
            total_e += e * pc
            n_e += pc
    rows = [{"Energy": k, "Artists": buckets[k], "Plays": plays_b[k]} for k in sorted(buckets)]
    weighted = (total_e / n_e) if n_e else None
    return rows, weighted


def compute_decade_distribution(full_top_artists, meta):
    era_plays, era_artists = {}, {}
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        era = (meta.get(name, {}).get("era") or "").strip() or "Untagged"
        era_plays[era] = era_plays.get(era, 0) + pc
        era_artists[era] = era_artists.get(era, 0) + 1
    rows = [{"Era": e, "Plays": era_plays[e], "Artists": era_artists[e]} for e in era_plays]
    rows.sort(key=lambda x: x["Plays"], reverse=True)
    return rows


def compute_listen_more_watchlist(full_top_artists, meta, overall_ranks):
    rows = []
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        info = meta.get(name, {})
        if not info.get("listen_more"):
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        rows.append({"Artist": name, "Rank": overall_ranks.get(name, "\u2014"),
                     "Plays": pc, "Tags": ", ".join(info.get("tags", []) or [])[:60]})
    rows.sort(key=lambda x: (x["Plays"]))
    return rows


def compute_underplayed_gems(full_top_artists, meta, overall_ranks, top_n=25):
    # high favorite/energy but relatively low plays -> "you rate them, you don't spin them"
    rows = []
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        info = meta.get(name, {})
        fav = info.get("favorite_override")
        if fav is None:
            fav = auto_favorite_from_rank(overall_ranks.get(name))
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        if pc <= 0:
            continue
        # gap score: high favorite, low plays
        gap = fav / (math.log10(pc + 1) + 1)
        rows.append({"Artist": name, "Favorite": int(fav), "Plays": pc,
                     "Rank": overall_ranks.get(name, "\u2014"),
                     "Underplay score": round(gap, 1)})
    rows.sort(key=lambda x: x["Underplay score"], reverse=True)
    return rows[:top_n]


def compute_round_numbers(full_top_artists):
    # artists sitting exactly on a milestone right now (satisfying)
    hits = []
    for a in full_top_artists:
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            continue
        if pc >= 100 and pc % 100 == 0:
            hits.append({"Artist": name, "Plays": pc, "Milestone": "%d (round hundred)" % pc})
        elif pc >= 50 and pc % 50 == 0:
            hits.append({"Artist": name, "Plays": pc, "Milestone": "%d (round fifty)" % pc})
    hits.sort(key=lambda x: x["Plays"], reverse=True)
    return hits


def compute_collection_summary(full_top_artists, meta, history):
    total_plays = 0
    for a in full_top_artists:
        try:
            total_plays += int(a.get("playcount", 0))
        except Exception:
            pass
    n = len(full_top_artists)
    tagged = sum(1 for a in full_top_artists
                 if (meta.get(a.get("name"), {}).get("tags")))
    # snapshot span
    dts = [d for d in (_stats_parse(ts) for ts in history.keys()) if d]
    span_days = 0
    if len(dts) >= 2:
        span_days = (max(dts) - min(dts)).days
    return {
        "total_plays": total_plays,
        "artists": n,
        "avg_plays": round(total_plays / max(n, 1)),
        "tagged": tagged,
        "tagged_pct": round(tagged / max(n, 1) * 100),
        "snapshots": len(history),
        "span_days": span_days,
    }


def render_more_stats(full_top_artists, baseline_data, overall_ranks):
    st.markdown("### More Stats")

    meta = load_artist_meta()
    history = load_leaderboard_history()

    # at-a-glance collection summary
    cs = compute_collection_summary(full_top_artists, meta, history)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total plays", format(cs["total_plays"], ","))
    m2.metric("Artists", cs["artists"])
    m3.metric("Avg plays/artist", cs["avg_plays"])
    m4.metric("Tagged", "%d%%" % cs["tagged_pct"])
    n1, n2 = st.columns(2)
    n1.metric("Snapshots logged", format(cs["snapshots"], ","))
    n2.metric("History span (days)", cs["span_days"])
    st.divider()

    st.markdown("#### Milestone watch")
    st.caption("Artists closing in on a round-number playcount. Works off today's numbers.")
    mw = compute_milestone_watch(full_top_artists, within=15)
    if mw:
        st.dataframe(mw[:30], use_container_width=True, hide_index=True, key="milestone_table")
    else:
        st.caption("No artists within 15 plays of a milestone right now.")

    st.divider()
    st.markdown("#### New to the Top 500")
    st.caption("Artists in your current Top 500 that weren't in your earliest baseline \u2014 the debuts.")
    debuts = compute_debuts(baseline_data, full_top_artists, top_n=50)
    if debuts:
        st.dataframe(debuts, use_container_width=True, hide_index=True, key="debuts_table")
    else:
        st.caption("No debuts versus baseline yet (or baseline already covers everyone).")

    st.divider()
    st.markdown("#### Binge detector")
    st.caption("Biggest single jump in playcount between two snapshots within ~2 days \u2014 your listening spikes.")
    binges = compute_biggest_binges(history, top_n=15)
    if binges:
        st.dataframe(binges, use_container_width=True, hide_index=True, key="binge_table")
    else:
        st.caption("Not enough close-together snapshots yet to spot a binge.")

    st.divider()
    st.markdown("#### Period leaders")
    st.caption("Top play-gainers per calendar period. This grows richer as months and quarters accumulate "
               "(your 2026 / 2027 splits will fill in here). Reflects artists captured in your snapshots.")
    period = st.radio("Bucket by", ["quarter", "month", "year"], horizontal=True, key="period_leaders_bucket")
    pl = compute_period_leaders(history, period=period, top_n=15)
    if not pl:
        st.caption("Not enough history yet for period leaders.")
    else:
        for key in sorted(pl.keys(), reverse=True):
            with st.expander("%s \u2014 top gainers" % key):
                rows = [{"Artist": n, "Play gain": g} for n, g in pl[key]]
                st.dataframe(rows, use_container_width=True, hide_index=True,
                             key="period_%s" % safe_widget_key("pl", key))

    st.divider()
    st.markdown("#### Play concentration")
    st.caption("How much of your total listening is carried by your very top artists.")
    share_rows, grand_total = compute_share_of_plays(full_top_artists)
    st.caption("Grand total across your Top 500: %s plays." % format(grand_total, ","))
    st.dataframe(share_rows, use_container_width=True, hide_index=True, key="share_table")

    st.divider()
    st.markdown("#### Tag leaderboard")
    st.caption("Your genres ranked by total plays \u2014 the real shape of your taste, by the numbers.")
    tl = compute_tag_leaderboard(full_top_artists, meta, top_n=30)
    if tl:
        st.dataframe(tl, use_container_width=True, hide_index=True, key="tag_lb_table")
    else:
        st.caption("Tag some artists to populate this.")

    st.divider()
    st.markdown("#### Mood leaderboard")
    st.caption("Same idea, by mood.")
    ml = compute_mood_leaderboard(full_top_artists, meta, top_n=30)
    if ml:
        st.dataframe(ml, use_container_width=True, hide_index=True, key="mood_lb_table")
    else:
        st.caption("Add moods to some artists to populate this.")

    st.divider()
    st.markdown("#### Energy profile")
    st.caption("How your tagged artists spread across the 1\u20135 energy scale, and your play-weighted average.")
    erows, weighted_e = compute_energy_profile(full_top_artists, meta)
    if weighted_e is not None:
        st.metric("Play-weighted average energy", "%.2f / 5" % weighted_e)
    if any(r["Artists"] for r in erows):
        st.dataframe(erows, use_container_width=True, hide_index=True, key="energy_profile_table")
    else:
        st.caption("Set energy on some artists to populate this.")

    st.divider()
    st.markdown("#### Decade distribution")
    st.caption("Plays and artist counts by the era you tagged.")
    drows = compute_decade_distribution(full_top_artists, meta)
    st.dataframe(drows, use_container_width=True, hide_index=True, key="decade_dist_table")

    st.divider()
    st.markdown("#### Underplayed gems")
    st.caption("Artists you rate highly but don't actually spin much \u2014 high favorite, low plays. Candidates to revisit.")
    gems = compute_underplayed_gems(full_top_artists, meta, overall_ranks, top_n=25)
    if gems:
        st.dataframe(gems, use_container_width=True, hide_index=True, key="gems_table")
    else:
        st.caption("Not enough favorite data yet.")

    st.divider()
    st.markdown("#### Listen-more watchlist")
    st.caption("Everyone you flagged as 'want to listen to more,' lowest plays first \u2014 work down the list.")
    lmw = compute_listen_more_watchlist(full_top_artists, meta, overall_ranks)
    if lmw:
        st.dataframe(lmw, use_container_width=True, hide_index=True, key="listen_more_table")
    else:
        st.caption("Flag some artists with 'want to listen to more' to build this list.")

    st.divider()
    st.markdown("#### Steadiest climbers")
    st.caption("Artists whose plays tick up most consistently over time, rather than in spikes. Steadiness 1.0 = perfectly even.")
    cons = compute_consistency(history, full_top_artists, min_obs=4, top_n=25)
    if cons:
        st.dataframe(cons, use_container_width=True, hide_index=True, key="consistency_table")
    else:
        st.caption("Need a few more snapshots per artist to measure steadiness.")

    st.divider()
    st.markdown("#### Sitting on a round number")
    st.caption("Artists parked exactly on a milestone playcount right now.")
    rn = compute_round_numbers(full_top_artists)
    if rn:
        st.dataframe(rn[:30], use_container_width=True, hide_index=True, key="round_numbers_table")
    else:
        st.caption("Nobody's sitting exactly on a round number at the moment.")


# ---------------- mobile view ----------------

def _mobile_label(rank, name, is_current, max_len=16):
    short = name if len(name) <= max_len else name[:max_len - 1] + "\u2026"
    rank_txt = ("%d. " % rank) if rank else ""
    prefix = "\u25b8 " if is_current else ""
    return (prefix + rank_txt + short).strip()


def make_mobile_leaderboard_fig(playcounts, ranked_artists, bar_colors):
    n = max(len(ranked_artists), 1)
    height = 70 + n * 34
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=playcounts[::-1],
        y=ranked_artists[::-1],
        orientation="h",
        marker_color=bar_colors[::-1],
        hoverinfo="skip",
        text=[format(pc, ",") for pc in playcounts[::-1]],
        textposition="auto",
        textfont=dict(size=10),
        insidetextanchor="middle",
    ))
    fig.update_layout(
        margin=dict(l=140, r=10, t=8, b=8),
        height=height,
        bargap=0.22,
        xaxis=dict(visible=False),
        yaxis=dict(tickfont=dict(size=11)),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig.update_traces(marker_line_width=0)
    return fig


def render_mobile_tagger(recent_artist, overall_ranks, meta):
    existing = meta.get(recent_artist, {})
    tag_library, mood_library = get_tag_library(meta)
    ak = safe_widget_key("m_artist", recent_artist)

    st.markdown("#### Tag this artist")
    selected_tags = st.multiselect("Tags", options=tag_library,
                                   default=existing.get("tags", []), key="m_tags_%s" % ak)
    new_tag = st.text_input("New tag", key="m_newtag_%s" % ak, placeholder="add a tag\u2026")
    selected_moods = st.multiselect("Moods", options=mood_library,
                                    default=existing.get("moods", []), key="m_moods_%s" % ak)
    new_mood = st.text_input("New mood", key="m_newmood_%s" % ak, placeholder="add a mood\u2026")
    energy = st.slider("Energy", ENERGY_MIN, ENERGY_MAX,
                       value=int(existing.get("energy", 3)), key="m_energy_%s" % ak)
    era_val = existing.get("era", "")
    if era_val not in ERA_OPTIONS:
        era_val = ""
    era = st.selectbox("Era", options=ERA_OPTIONS,
                       index=ERA_OPTIONS.index(era_val), key="m_era_%s" % ak)
    listen_more = st.checkbox("Want to listen to more",
                              value=bool(existing.get("listen_more", False)), key="m_listenmore_%s" % ak)

    if st.button("Save", key="m_save_%s" % ak, use_container_width=True):
        if new_tag and new_tag.strip():
            selected_tags = list(dict.fromkeys(selected_tags + [new_tag.strip()]))
        if new_mood and new_mood.strip():
            selected_moods = list(dict.fromkeys(selected_moods + [new_mood.strip()]))
        merged = dict(existing)
        merged.update({
            "tags": selected_tags, "moods": selected_moods,
            "energy": int(energy), "era": era, "listen_more": bool(listen_more),
        })
        merged.setdefault("favorite_override", None)
        merged.setdefault("notes", "")
        meta[recent_artist] = merged
        save_artist_meta(meta)
        st.success("Saved \u2713")
    return meta


def render_mobile_view(username, recent_artist, recent_track_name, recent_playcount,
                       album_art_url, full_top_artists, overall_ranks,
                       baseline_data, in_top500):
    st.markdown("<style>.block-container{padding-top:0.8rem;padding-left:0.6rem;"
                "padding-right:0.6rem;max-width:100%;}</style>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2.4])
    with c1:
        if album_art_url:
            st.image(album_art_url, use_container_width=True)
    with c2:
        st.markdown("**%s**" % recent_artist)
        st.caption(recent_track_name or "")
        cr = overall_ranks.get(recent_artist)
        if cr:
            st.caption("Rank #%d \u00b7 %s plays" % (cr, format(recent_playcount, ",")))
        else:
            st.caption("%s plays" % format(recent_playcount, ","))

    if not in_top500:
        render_manual_tracker(recent_artist, recent_track_name, album_art_url)
        return

    leaderboard, _ = get_leaderboard_surrounding_artists(username, recent_artist, limit=500)
    artists, playcounts = [], []
    if leaderboard:
        leaderboard_sorted = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        artists = [a for a, _ in leaderboard_sorted]
        playcounts = [c for _, c in leaderboard_sorted]
        current_data = {a: {"playcount": leaderboard[a], "rank": overall_ranks.get(a)}
                        for a in artists}
        save_current_leaderboard(current_data)
        log_leaderboard_snapshot(current_data)

    ranked_artists, bar_colors = [], []
    for a in artists:
        cr = overall_ranks.get(a)
        is_cur = a.lower() == recent_artist.lower()
        ranked_artists.append(_mobile_label(cr, a, is_cur))
        base_rank = (baseline_data.get(a) or {}).get("rank")
        if is_cur:
            color = COLOR_ACTIVE
        elif base_rank is None or cr is None:
            color = COLOR_FLAT
        elif cr < base_rank:
            color = COLOR_RISING
        elif cr > base_rank:
            color = COLOR_FALLEN
        else:
            color = COLOR_FLAT
        bar_colors.append(color)

    if artists:
        fig = make_mobile_leaderboard_fig(playcounts, ranked_artists, bar_colors)
        st.plotly_chart(fig, use_container_width=True, key="mobile_leaderboard",
                        config={"displayModeBar": False})

    st.divider()
    meta = load_artist_meta()
    render_mobile_tagger(recent_artist, overall_ranks, meta)




# =========================================================
# Galaxy v2 — synthwave nebula star map (custom canvas)
# =========================================================

SYNTH_PALETTE = [
    "#ff2d95", "#00e5ff", "#b14aed", "#2de2e6", "#ff6ec7",
    "#7b5cff", "#ff8b3d", "#3df5ff", "#f72585", "#4cc9f0",
]


def _galaxy_tag_color(tag):
    h = int(hashlib.sha1((tag or "").encode("utf-8")).hexdigest()[:8], 16)
    return SYNTH_PALETTE[h % len(SYNTH_PALETTE)]


def build_galaxy_data(full_top_artists, meta, recent_counts):
    play_of, rank_of = {}, {}
    for i, a in enumerate(full_top_artists):
        name = a.get("name")
        if not name:
            continue
        try:
            pc = int(a.get("playcount", 0))
        except Exception:
            pc = 0
        play_of[name] = pc
        rank_of[name] = i + 1

    artists = []
    for name, pc in play_of.items():
        info = meta.get(name, {}) if isinstance(meta, dict) else {}
        tags = [t.strip() for t in (info.get("tags") or []) if str(t).strip()]
        moods = [m.strip() for m in (info.get("moods") or []) if str(m).strip()]
        if not tags:  # tagged-only map
            continue
        artists.append({
            "name": name, "plays": pc, "rank": rank_of.get(name),
            "tags": tags, "moods": moods,
            "recent": int(recent_counts.get(_normalize_artist_name(name), 0)),
        })

    if not artists:
        return {"territories": [], "stars": []}

    tag_plays = {}
    for ar in artists:
        for t in ar["tags"]:
            tag_plays[t] = tag_plays.get(t, 0) + ar["plays"]
    tags_used = list(tag_plays.keys())

    corr = make_seed_corr()
    G = nx.Graph()
    for t in tags_used:
        G.add_node(t)
    for ar in artists:  # co-occurrence pulls tags together
        ts = ar["tags"]
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                a_, b_ = ts[i], ts[j]
                prev = G.get_edge_data(a_, b_, {}).get("weight", 0)
                G.add_edge(a_, b_, weight=prev + 1.0)
    for i in range(len(tags_used)):  # your hand-built correlations pull harder
        for j in range(i + 1, len(tags_used)):
            a_, b_ = tags_used[i], tags_used[j]
            c = corr.get((a_.lower(), b_.lower()), 0.0)
            if c > 0:
                prev = G.get_edge_data(a_, b_, {}).get("weight", 0)
                if G.has_edge(a_, b_):
                    G[a_][b_]["weight"] = prev + c * 3.0
                else:
                    G.add_edge(a_, b_, weight=c * 3.0)

    if G.number_of_nodes() == 1:
        centers = {tags_used[0]: (0.0, 0.0)}
    else:
        # higher k = more space between territories; gives genres room to separate
        pos = nx.spring_layout(G, seed=7, k=2.6, iterations=400, weight="weight")
        centers = {t: (float(p[0]), float(p[1])) for t, p in pos.items()}

    xs = [c[0] for c in centers.values()]
    ys = [c[1] for c in centers.values()]
    cx0 = (min(xs) + max(xs)) / 2.0
    cy0 = (min(ys) + max(ys)) / 2.0
    # single shared scale for BOTH axes -> preserves the real shape of the
    # layout instead of squashing it flat into the wide canvas
    span = max(max(xs) - min(xs), max(ys) - min(ys), 1e-9) / 2.0

    def _norm_pt(x, y):
        return ((x - cx0) / span * 0.92, (y - cy0) / span * 0.92)

    centers = {t: _norm_pt(x, y) for t, (x, y) in centers.items()}

    max_tagplays = max(tag_plays.values())
    territories = []
    for t in tags_used:
        cx, cy = centers[t]
        territories.append({
            "tag": t, "x": cx, "y": cy,
            "weight": tag_plays[t] / max_tagplays,
            "color": _galaxy_tag_color(t),
        })

    max_plays = max(a["plays"] for a in artists) or 1
    max_recent = max((a["recent"] for a in artists), default=0) or 1
    logmax = math.log10(max_plays + 1)
    stars = []
    for ar in artists:
        cxs = [centers[t][0] for t in ar["tags"] if t in centers]
        cys = [centers[t][1] for t in ar["tags"] if t in centers]
        bx, by = sum(cxs) / len(cxs), sum(cys) / len(cys)
        h = int(hashlib.sha1(ar["name"].encode("utf-8")).hexdigest()[:8], 16)
        ang = (h % 360) * math.pi / 180.0
        rad = ((h >> 9) % 1000) / 1000.0 * 0.22
        bx += math.cos(ang) * rad
        by += math.sin(ang) * rad
        lp = math.log10(ar["plays"] + 1) / logmax if logmax else 0.5
        primary = max(ar["tags"], key=lambda t: tag_plays.get(t, 0))
        stars.append({
            "name": ar["name"], "x": bx, "y": by,
            "size": 0.28 + lp, "bright": 0.4 + 0.6 * lp,
            "color": _galaxy_tag_color(primary),
            "recent": (ar["recent"] / max_recent) if max_recent else 0.0,
            "plays": ar["plays"], "rank": ar["rank"],
            "tags": ar["tags"][:6], "moods": ar["moods"][:6],
            "phase": (h % 628) / 100.0,
        })

    return {"territories": territories, "stars": stars}


def render_galaxy_canvas(data, height=720):
    payload = json.dumps(data)
    html = r"""<!doctype html><html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#07030f;overflow:hidden;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}
  #wrap{position:relative;width:100%;height:__H__px;}
  #c{display:block;width:100%;height:100%;}
  #tt{position:absolute;pointer-events:none;opacity:0;transition:opacity .12s;
    background:rgba(10,4,22,.92);border:1px solid rgba(255,45,149,.55);
    box-shadow:0 0 18px rgba(255,45,149,.35),0 0 40px rgba(0,229,255,.18);
    border-radius:10px;padding:9px 12px;color:#eafcff;font-size:12.5px;
    max-width:240px;z-index:5;backdrop-filter:blur(3px);}
  #tt b{color:#fff;font-size:13.5px;letter-spacing:.3px;}
  #tt .pc{color:#00e5ff;} #tt .rk{color:#ff8b3d;}
  #tt .tg{color:#ff6ec7;} #tt .md{color:#b9a8ff;}
  #hint{position:absolute;left:14px;bottom:12px;color:rgba(180,200,230,.40);
    font-size:11px;letter-spacing:.5px;pointer-events:none;}
</style></head><body>
<div id="wrap"><canvas id="c"></canvas><div id="tt"></div>
<div id="hint">hover a star · territories are your genres</div></div>
<script>
const DATA = __PAYLOAD__;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const tt = document.getElementById('tt'), wrap = document.getElementById('wrap');
let W=0,H=0,DPR=1,PAD=70;

function glow(color,r){
  const s=document.createElement('canvas'); s.width=s.height=r*2;
  const g=s.getContext('2d'); const grd=g.createRadialGradient(r,r,0,r,r,r);
  grd.addColorStop(0,color); grd.addColorStop(.12,color);
  grd.addColorStop(.5,'rgba(0,0,0,0)'); grd.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=grd; g.beginPath(); g.arc(r,r,r,0,7); g.fill(); return s;
}
const glowCache={}, nebCache={};
function getGlow(c){ if(!glowCache[c]) glowCache[c]=glow(c,64); return glowCache[c]; }
function getNeb(c){
  if(nebCache[c]) return nebCache[c];
  const r=180,s=document.createElement('canvas'); s.width=s.height=r*2;
  const g=s.getContext('2d'); const grd=g.createRadialGradient(r,r,0,r,r,r);
  grd.addColorStop(0,c); grd.addColorStop(.3,c); grd.addColorStop(1,'rgba(0,0,0,0)');
  g.globalAlpha=.32; g.fillStyle=grd; g.beginPath(); g.arc(r,r,r,0,7); g.fill();
  nebCache[c]=s; return s;
}
function hexA(hex,a){const n=parseInt(hex.slice(1),16);
  return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}

let bgStars=[];
function setup(){
  DPR=Math.min(window.devicePixelRatio||1,2);
  W=wrap.clientWidth; H=wrap.clientHeight;
  cv.width=W*DPR; cv.height=H*DPR; ctx.setTransform(DPR,0,0,DPR,0,0);
  bgStars=[]; const n=Math.floor(W*H/9000);
  for(let i=0;i<n;i++) bgStars.push({x:Math.random()*W,y:Math.random()*H,
    r:Math.random()*1.1+.2,a:Math.random()*.5+.15,p:Math.random()*6.28});
}
function TX(x){ const s=Math.min(W-2*PAD,H-2*PAD)/2; return W/2 + x*s; }
function TY(y){ const s=Math.min(W-2*PAD,H-2*PAD)/2; return H*0.40 + y*s*0.82; }

let hovered=null;
function pick(mx,my){
  let best=null,bd=999;
  for(const s of DATA.stars){
    const dx=mx-TX(s.x), dy=my-TY(s.y), d=Math.hypot(dx,dy);
    const hit=8+s.size*9;
    if(d<hit && d<bd){bd=d;best=s;}
  }
  return best;
}
cv.addEventListener('mousemove',e=>{
  const r=cv.getBoundingClientRect();
  const mx=e.clientX-r.left, my=e.clientY-r.top;
  hovered=pick(mx,my);
  if(hovered){
    tt.style.opacity=1;
    let tx=mx+16, ty=my+14;
    if(tx>W-250) tx=mx-236; if(ty>H-120) ty=my-110;
    tt.style.left=tx+'px'; tt.style.top=ty+'px';
    tt.innerHTML='<b>'+hovered.name+'</b><br>'+
      '<span class="pc">'+hovered.plays.toLocaleString()+' plays</span>'+
      (hovered.rank?' · <span class="rk">#'+hovered.rank+'</span>':'')+
      (hovered.tags.length?'<br><span class="tg">'+hovered.tags.join(' · ')+'</span>':'')+
      (hovered.moods.length?'<br><span class="md">'+hovered.moods.join(' · ')+'</span>':'');
  } else { tt.style.opacity=0; }
});
cv.addEventListener('mouseleave',()=>{hovered=null;tt.style.opacity=0;});

function drawGrid(t){
  const horizon=H*0.66, vpx=W/2;
  ctx.save(); ctx.globalCompositeOperation='lighter';
  ctx.strokeStyle='rgba(255,45,149,.18)'; ctx.lineWidth=1;
  for(let i=0;i<=14;i++){            // verticals converging to vanishing point
    const fx=(i/14-.5)*W*2.2;
    ctx.beginPath(); ctx.moveTo(vpx+fx,H); ctx.lineTo(vpx+fx*0.05,horizon); ctx.stroke();
  }
  ctx.strokeStyle='rgba(0,229,255,.16)';
  const scroll=(t*0.04)%1;
  for(let i=0;i<18;i++){             // horizontals receding, scrolling toward viewer
    const f=(i+scroll)/18; const y=horizon+(f*f)*(H-horizon);
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke();
  }
  // horizon glow line
  ctx.strokeStyle='rgba(255,110,199,.5)'; ctx.lineWidth=2;
  ctx.shadowColor='#ff2d95'; ctx.shadowBlur=18;
  ctx.beginPath(); ctx.moveTo(0,horizon); ctx.lineTo(W,horizon); ctx.stroke();
  ctx.restore();
}

function frame(ts){
  const t=ts/1000;
  // background
  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#0a0418'); bg.addColorStop(.6,'#0b0320'); bg.addColorStop(1,'#140a2e');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);
  // bg starfield
  ctx.save(); ctx.globalCompositeOperation='lighter';
  for(const b of bgStars){ const tw=.6+.4*Math.sin(t*1.5+b.p);
    ctx.fillStyle='rgba(200,220,255,'+(b.a*tw)+')';
    ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }
  ctx.restore();

  drawGrid(t);

  // nebula territories
  ctx.save(); ctx.globalCompositeOperation='lighter';
  for(const tr of DATA.territories){
    const x=TX(tr.x), y=TY(tr.y);
    const dx=Math.sin(t*0.2+tr.x*3)*6, dy=Math.cos(t*0.17+tr.y*3)*6;
    const R=(50+tr.weight*150);
    ctx.globalAlpha=.09+tr.weight*0.15;
    const neb=getNeb(tr.color);
    ctx.drawImage(neb,x-R+dx,y-R+dy,R*2,R*2);
  }
  ctx.globalAlpha=1; ctx.restore();

  // territory labels
  ctx.save(); ctx.textAlign='center';
  for(const tr of DATA.territories){
    if(tr.weight<0.10) continue;
    const x=TX(tr.x), y=TY(tr.y);
    ctx.font=(tr.weight>0.4?'700 15px':'600 12px')+' "Segoe UI",sans-serif';
    ctx.fillStyle=hexA(tr.color,.92); ctx.shadowColor=tr.color; ctx.shadowBlur=10;
    ctx.fillText(tr.tag.toUpperCase(), x, y-6);
  }
  ctx.restore();

  // stars
  ctx.save(); ctx.globalCompositeOperation='lighter';
  for(const s of DATA.stars){
    const bx=TX(s.x)+Math.sin(t*0.5+s.phase)*1.6;
    const by=TY(s.y)+Math.cos(t*0.4+s.phase)*1.6;
    const tw=0.72+0.28*Math.sin(t*2.0+s.phase);
    const r=(4+s.size*8)*(1+s.recent*0.4);
    ctx.globalAlpha=(0.32+0.4*s.bright)*tw*(0.7+s.recent*0.3);
    ctx.drawImage(getGlow(s.color),bx-r,by-r,r*2,r*2);
  }
  // bright cores
  for(const s of DATA.stars){
    const bx=TX(s.x)+Math.sin(t*0.5+s.phase)*1.6;
    const by=TY(s.y)+Math.cos(t*0.4+s.phase)*1.6;
    const tw=0.72+0.28*Math.sin(t*2.0+s.phase);
    ctx.globalAlpha=Math.min(1,0.45+s.bright*0.5)*tw;
    ctx.fillStyle='#ffffff';
    ctx.beginPath(); ctx.arc(bx,by,0.9+s.size*1.3,0,7); ctx.fill();
  }
  ctx.restore();

  // hovered ring
  if(hovered){
    const bx=TX(hovered.x), by=TY(hovered.y);
    ctx.save(); ctx.globalCompositeOperation='lighter';
    ctx.strokeStyle=hovered.color; ctx.lineWidth=2; ctx.shadowColor=hovered.color;
    ctx.shadowBlur=16; ctx.globalAlpha=.9;
    ctx.beginPath(); ctx.arc(bx,by,12+hovered.size*10,0,7); ctx.stroke();
    ctx.restore();
  }
  requestAnimationFrame(frame);
}

window.addEventListener('resize',setup);
setup(); requestAnimationFrame(frame);
</script></body></html>"""
    html = html.replace("__PAYLOAD__", payload).replace("__H__", str(int(height)))
    components.html(html, height=height + 6, scrolling=False)

# -------------------------
# Main App
# -------------------------
def main():
    inject_theme()
    render_masthead()
    col, _ = st.columns([1, 2])
    with col:
        username = st.text_input("Enter your Last.fm username:", value="troycapybara")

    st_autorefresh(interval=85600, limit=None, key="refresh")

    if not username:
        return

    now = datetime.now()

    if "session_start" not in st.session_state:
        st.session_state.session_start = now

    if "last_insight_time" not in st.session_state:
        st.session_state.last_insight_time = None

    runtime = now - st.session_state.session_start
    hours, rem = divmod(int(runtime.total_seconds()), 3600)
    minutes, _ = divmod(rem, 60)
    st.sidebar.caption(f"⏱️ Session: {hours}h {minutes}m")

    if st.sidebar.button("💾 Sync to GitHub now"):
        _maybe_flush(force=True)
        st.sidebar.success("Synced.")

    SESSION_WARMUP_SECONDS = 3600
    INSIGHT_COOLDOWN_SECONDS = 3600

    time_since_start = (now - st.session_state.session_start).total_seconds()
    time_since_last = (
        None if st.session_state.last_insight_time is None
        else (now - st.session_state.last_insight_time).total_seconds()
    )

    can_show_insight = (
        time_since_start >= SESSION_WARMUP_SECONDS and
        (
            st.session_state.last_insight_time is None
            or time_since_last >= INSIGHT_COOLDOWN_SECONDS
        )
    )

    with st.spinner("Fetching your data..."):
        recent_artist, recent_playcount, recent_track_name, album_art_url = get_recent_artist(username)

    if not recent_artist:
        st.warning("Could not find a recent track for that user.")
        return

    # Top 500 only
    full_top_artists = get_top_artists(username, limit=500)
    overall_ranks, top_playcounts = build_top_artist_maps(full_top_artists)
    in_top500 = overall_ranks.get(recent_artist) is not None

    # one-time bulk baseline import (no-op after it's run once)
    maybe_run_baseline_import(full_top_artists, overall_ranks)

    # mobile bookmark support: open the app URL with ?m=1 to land in the phone view
    try:
        _mp = st.query_params.get("m", "")
    except Exception:
        _mp = ""
    force_mobile = str(_mp).lower() in ("1", "true", "yes", "y", "m")

    view_options = [
        "\U0001f4f1 Mobile",
        "Leaderboard (default)",
        "Now Playing",
        "Album Art Gallery",
        "Stats",
        "More Stats",
        "Velocity Index",
        "Manual Tracker",
        "Random Tagger",
        "Galaxy (beta)",
    ]
    view_mode = st.sidebar.radio("View", view_options, index=(0 if force_mobile else 1))

    if view_mode == "\U0001f4f1 Mobile":
        baseline_data = load_long_term_baseline()
        render_mobile_view(
            username=username,
            recent_artist=recent_artist,
            recent_track_name=recent_track_name,
            recent_playcount=recent_playcount,
            album_art_url=album_art_url,
            full_top_artists=full_top_artists,
            overall_ranks=overall_ranks,
            baseline_data=baseline_data,
            in_top500=in_top500,
        )
        return

    if view_mode == "Manual Tracker":
        render_manual_tracked_section(full_top_artists)
        return

    if view_mode == "Random Tagger":
        render_random_tagger(full_top_artists, overall_ranks)
        return

    if view_mode == "More Stats":
        baseline_data = load_long_term_baseline()
        render_more_stats(full_top_artists, baseline_data, overall_ranks)
        return

    if view_mode == "Album Art Gallery":
        st.markdown("Last 100 Tracks (Album Art)")

        recent_100 = get_recent_tracks(username, limit=100)
        if not recent_100:
            st.warning("Could not load recent tracks.")
            return

        cols_per_row = st.slider("Covers per row", 4, 10, 6, key="gallery_cols")

        for start in range(0, len(recent_100), cols_per_row):
            row = recent_100[start:start + cols_per_row]
            cols = st.columns(cols_per_row)
            for col, t in zip(cols, row):
                with col:
                    if t.get("art"):
                        st.image(t["art"], use_container_width=True)
                    else:
                        st.caption("No art")
                    # minimal text
                    st.caption(t.get("track", ""))

        return

    if view_mode == "Stats":
        st.markdown("Stats")
        st.caption("Based on your leaderboard snapshots (surrounding artists) saved over time.")

        days = st.slider("Window (days)", 1, 30, 7, key="stats_window_days")
        window_items = get_history_window(days=days)

        if len(window_items) < 2:
            st.info("Not enough history in this window yet. Keep the app running to collect snapshots.")
            return

        momentum_rows, volatility_rows = compute_momentum_and_volatility(window_items)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"Momentum (last {days} days)")
            if momentum_rows:
                st.dataframe(momentum_rows[:25], use_container_width=True, hide_index=True, key="stats_momentum_table")
            else:
                st.caption("No play gains recorded in this window.")

        with c2:
            st.markdown(f"Rank Volatility (last {days} days)")
            if volatility_rows:
                st.dataframe(volatility_rows[:25], use_container_width=True, hide_index=True, key="stats_volatility_table")
            else:
                st.caption("Not enough repeated rank observations yet to measure volatility.")

        st.divider()
        st.markdown("Artist velocity tiers")
        st.caption("Plays/day = total plays divided by days since first snapshot.")

        history_for_velocity = load_leaderboard_history()
        velocity_tiers = compute_velocity_tiers(full_top_artists, history_for_velocity, top_n=100)

        tier_colors = {
            "Cheetah": "#D85A30",
            "Cardinal": "#D4537E",
            "Mountain Goat": "#1D9E75",
            "Kitty Cat": "#378ADD",
            "Snail": "#BA7517",
            "Sloth": "#888780",
            "Fading": "#993556",
        }
        tier_desc = {
            "Cheetah": "1+ plays/day",
            "Cardinal": "0.59-0.99 plays/day",
            "Mountain Goat": "0.35-0.58 plays/day",
            "Kitty Cat": "0.19-0.34 plays/day",
            "Snail": "0.06-0.18 plays/day",
            "Sloth": "0-0.05 plays/day",
            "Fading": "negative slope",
        }

        t1, t2 = st.columns(2)
        t3, t4 = st.columns(2)
        t5, t6 = st.columns(2)
        t7, _ = st.columns(2)
        cols_map = {
            "Cheetah": t1, "Cardinal": t2,
            "Mountain Goat": t3, "Kitty Cat": t4,
            "Snail": t5, "Sloth": t6,
            "Fading": t7,
        }

        for tier_name, col in cols_map.items():
            with col:
                members = velocity_tiers.get(tier_name, [])
                st.markdown("**%s** — %s (%d artists)" % (tier_name, tier_desc[tier_name], len(members)))
                if members:
                    for row in members[:15]:
                        st.caption("%s  %+.2f" % (row["Artist"], row["Plays/day"]))
                else:
                    st.caption("None right now.")

        st.divider()
        st.markdown("Era density")
        meta_for_era = load_artist_meta()
        era_rows = compute_era_density(full_top_artists, meta_for_era)
        era_fig = make_era_density_fig(era_rows)
        if era_fig:
            st.plotly_chart(era_fig, use_container_width=True, key="era_density_chart")
            st.dataframe(era_rows, use_container_width=True, hide_index=True, key="era_density_table")
        else:
            st.caption("Tag some artists with an era to see this.")

        st.divider()

        st.markdown("Displacement tracker")
        st.caption("Artists who rose 10+ spots and who they pushed down.")

        baseline_data_for_displacement = load_long_term_baseline()
        displacement_rows = compute_displacement(baseline_data_for_displacement, full_top_artists, min_rise=10)

        if displacement_rows:
            for dr in displacement_rows:
                with st.expander("%s — rose %d spots (was %d, now %d)" % (dr["Artist"], dr["Rose"], dr["Was"], dr["Now"])):
                    if dr["Displaced"] and dr["Displaced"] != "—":
                        st.caption("Displaced: %s" % dr["Displaced"])
                    else:
                        st.caption("No direct displacements identified.")
        else:
            st.caption("No artists have risen 10+ spots since your baseline yet.")

        st.divider()
        st.markdown("Crowded neighborhoods")
        st.caption("Tightest rank bands — one session reshuffles everything. Split into two cities: your top 200 and ranks 201-500.")

        city_a, city_b = compute_crowded_neighborhoods(full_top_artists, window=10)

        st.markdown("**City A — ranks 1-200**")
        neighborhood_fig_a = make_crowded_neighborhood_fig(
            full_top_artists[:200], city_a, highlight_n=3
        )
        if neighborhood_fig_a:
            st.plotly_chart(neighborhood_fig_a, use_container_width=True, key="neighborhood_chart_a")
        st.dataframe(city_a[:10], use_container_width=True, hide_index=True, key="neighborhood_table_a")

        st.markdown("**City B — ranks 201-500**")
        neighborhood_fig_b = make_crowded_neighborhood_fig(
            full_top_artists[200:], city_b, highlight_n=3
        )
        if neighborhood_fig_b:
            st.plotly_chart(neighborhood_fig_b, use_container_width=True, key="neighborhood_chart_b")
        st.dataframe(city_b[:10], use_container_width=True, hide_index=True, key="neighborhood_table_b")

        st.divider()
        st.markdown("Taste fingerprint")
        meta_for_fp = load_artist_meta()
        fp_top_n = st.slider("Tags to show", 5, 20, 10, key="fp_top_n")
        fp_fig = make_taste_fingerprint_fig(full_top_artists, meta_for_fp, top_tags=fp_top_n)
        if fp_fig:
            st.plotly_chart(fp_fig, use_container_width=True, key="taste_fingerprint_chart")
        else:
            st.caption("Tag some artists to see your taste fingerprint.")

        st.divider()
        st.markdown("Head-to-head projection")
        st.caption("Pick two artists and see when one overtakes the other at current pace.")

        history_for_h2h = load_leaderboard_history()
        projections_for_h2h = compute_rank_projections(history_for_h2h, full_top_artists, top_n=100)

        if not projections_for_h2h:
            st.caption("Not enough snapshot history yet.")
        else:
            h2h_options = sorted(projections_for_h2h.keys(), key=lambda a: overall_ranks.get(a, 9999))
            h2h_col1, h2h_col2 = st.columns(2)
            with h2h_col1:
                h2h_a = st.selectbox("Artist A", options=h2h_options, index=0, key="h2h_artist_a")
            with h2h_col2:
                default_b = h2h_options[1] if len(h2h_options) > 1 else h2h_options[0]
                h2h_b = st.selectbox("Artist B", options=h2h_options, index=1, key="h2h_artist_b")

            if h2h_a and h2h_b and h2h_a != h2h_b:
                h2h_fig, crossover_msg = make_head_to_head_fig(
                    projections_for_h2h, overall_ranks, h2h_a, h2h_b
                )
                if crossover_msg:
                    st.info(crossover_msg)
                if h2h_fig:
                    st.plotly_chart(h2h_fig, use_container_width=True, key="h2h_chart")
            elif h2h_a == h2h_b:
                st.caption("Pick two different artists.")

        st.markdown("Rank gravity")
        gravity_fig = make_rank_gravity_fig(full_top_artists)
        if gravity_fig:
            st.plotly_chart(gravity_fig, use_container_width=True, key="rank_gravity_chart")
        else:
            st.caption("Not enough data yet.")

        st.divider()

        st.markdown("Play count clubs")
        club_fig, tier_artists, tiers = make_play_club_fig(full_top_artists)
        if club_fig:
            st.plotly_chart(club_fig, use_container_width=True, key="play_club_chart")

            # expandable roster for each tier
            for threshold, label, color in tiers:
                members = tier_artists.get(threshold, [])
                if not members:
                    continue
                with st.expander(f"{label} — {len(members)} artists"):
                    for name, pc in members:
                        st.markdown(f"**{name}** — {pc:,} plays")

        st.divider()

        st.markdown("Artist Power Ranking")

        days = st.slider(
            "Recency window (days)",
            min_value=3,
            max_value=30,
            value=7,
            key="power_days",
        )

        top_n = st.slider(
            "Show top",
            min_value=10,
            max_value=200,
            value=50,
            key="power_top_n",
        )

        c1, c2 = st.columns(2)
        with c1:
            w_recent = st.slider(
                "Weight: Recency",
                0.0,
                1.0,
                0.7,
                0.05,
                key="power_weight_recent",
            )
        with c2:
            w_total = round(1.0 - w_recent, 2)
            st.caption(f"Weight: Total plays = {w_total}")

        recent_counts = get_recent_artist_counts(
            username=username,
            days=days,
        )

        power_rows = build_power_ranking_rows(
            full_top_artists=full_top_artists,
            recent_counts=recent_counts,
            top_n=top_n,
            w_total=w_total,
            w_recent=w_recent,
        )

        st.dataframe(
            power_rows,
            use_container_width=True,
            hide_index=True,
            key="power_ranking_table",
        )

        st.divider()
        st.markdown("Rank projection")
        st.caption("Linear regression on your snapshot history, extrapolated forward. Confidence band widens over time.")

        history = load_leaderboard_history()
        projections = compute_rank_projections(history, full_top_artists, top_n=500)

        if not projections:
            st.caption("Not enough snapshot history yet for projections. Keep the app running.")
        else:
            artist_options = sorted(projections.keys(),
                                    key=lambda a: overall_ranks.get(a, 9999))
            selected = st.multiselect(
                "Artists to project",
                options=artist_options,
                default=artist_options[:5],
                key="proj_artist_select",
            )

            if selected:
                proj_fig = make_rank_projection_fig(projections, overall_ranks, selected)
                st.plotly_chart(proj_fig, use_container_width=True, key="rank_projection_chart")

                summary = []
                now_p = datetime.now()
                for a in selected:
                    p = projections.get(a)
                    if not p:
                        continue
                    summary.append({
                        "Artist": a,
                        "Current rank": overall_ranks.get(a, "—"),
                        "Current plays": f"{int(p['current_playcount']):,}",
                        "Projected 1 year": f"{int(p['predict'](now_p + timedelta(days=365))):,}",
                        "Projected 2 years": f"{int(p['predict'](now_p + timedelta(days=730))):,}",
                        "Projected 5 years": f"{int(p['predict'](now_p + timedelta(days=1825))):,}",
                        "Projected 10 years": f"{int(p['predict'](now_p + timedelta(days=3650))):,}",
                        "Plays/day pace": f"{p['slope']:.1f}",
                    })
                st.dataframe(summary, use_container_width=True, hide_index=True,
                            key="proj_summary_table")

            st.divider()
            st.markdown("Top 50 candidates (ranked 51-300)")
            st.caption("Artists on pace to crack your top 50 within 6 months at current rate.")

            result = find_top50_candidates(projections, overall_ranks, full_top_artists,
                                          rank_window=(51, 300))
            if isinstance(result, tuple):
                top50_candidates, top50_threshold = result
                if top50_candidates:
                    st.caption(f"Current top 50 threshold: {top50_threshold:,} plays")
                    st.dataframe(top50_candidates, use_container_width=True, hide_index=True,
                                key="top50_candidates_table")
                else:
                    st.caption("No artists in ranks 51-300 are currently on pace to crack your top 50 within 6 months.")
            else:
                st.caption("Not enough data.")

        st.divider()

        st.markdown("Artist Loyalty Index")

        min_obs = st.slider("Minimum observations", 2, 20, 3, key="loyalty_min_obs")
        loyalty_rows = compute_artist_loyalty_index(window_items, min_obs=min_obs)

        if not loyalty_rows:
            st.caption("Not enough repeat appearances in this window yet. Try a larger window or lower the minimum observations.")
        else:
            st.dataframe(loyalty_rows[:25], use_container_width=True, hide_index=True, key="loyalty_table")

        st.divider()

        st.markdown("Attached Artists (within the next hour)")

        days = st.slider("Lookback window (days)", 7, 60, 14, key="corr_days")
        window_minutes = st.slider("Time window (minutes)", 15, 120, 60, key="corr_window")
        top_n = st.slider("Show top attached artists", 5, 30, 15, key="corr_topn")

        events = get_recent_scrobbles(username, days=days)

        # anchor on the now playing artist
        anchor = recent_artist

        rows = attached_artists_for_anchor(
            events=events,
            anchor_artist=anchor,
            window_minutes=window_minutes,
            min_anchor_plays=5,
            top_n=top_n,
        )

        if not rows:
            st.info("Not enough recent scrobbles for this artist to compute correlations yet. Try increasing lookback days.")
        else:
            st.caption(f"Anchor artist: **{anchor}**")
            st.dataframe(rows, use_container_width=True, hide_index=True, key="attached_artists_table")

            show_matrix = st.checkbox("Show mini correlation matrix (anchor + top attached)", value=False, key="corr_show_matrix")
            if show_matrix:
                labels, mat = correlation_matrix(events, anchor, rows, window_minutes=window_minutes)
                fig = go.Figure(
                    data=go.Heatmap(
                        z=mat,
                        x=labels,
                        y=labels,
                        zmin=0.0,
                        zmax=1.0,
                        hovertemplate="P(%{x} | %{y}) = %{z:.3f}<extra></extra>",
                    )
                )
                fig.update_layout(
                    height=520,
                    margin=dict(l=60, r=20, t=30, b=60),
                )
                st.plotly_chart(fig, use_container_width=True, key="corr_heatmap")

    if view_mode == "Galaxy (beta)":
        st.markdown("### Artist Galaxy")
        st.caption("Your taste as a star map. Each glowing region is a tag; related genres sit as neighbors. "
                   "Stars are your tagged artists \u2014 brighter and bigger means more plays. Hover any star for details.")

        gc1, gc2 = st.columns([1, 3])
        with gc1:
            gal_days = st.slider("Recent-glow window (days)", 7, 60, 14, key="galv2_days")

        meta_g = load_artist_meta()
        recent_counts_g = get_recent_artist_counts(username, days=gal_days)
        gdata = build_galaxy_data(full_top_artists, meta_g, recent_counts_g)

        if not gdata["stars"]:
            st.info("No tagged artists in your current Top 500 yet. Tag a few artists "
                    "(try the Random Tagger) and they'll appear as stars here.")
        else:
            render_galaxy_canvas(gdata, height=720)
            st.caption("%d artists across %d genre territories. Tag more artists to grow the map."
                       % (len(gdata["stars"]), len(gdata["territories"])))
        return

    if view_mode == "Velocity Index":
      st.markdown("Velocity Index")
      st.caption("All 500 artists ranked by total plays. Tier based on plays/day slope from snapshot history. Click any column header to sort.")

      vi_period = st.radio("Lookback window", ["All time", "7 days", "30 days", "60 days", "90 days"], horizontal=True, key="vi_period")

      history_for_vi = load_leaderboard_history()
      if vi_period == "All time":
          history_vi_filtered = history_for_vi
      else:
          vi_days_map = {"7 days": 7, "30 days": 30, "60 days": 60, "90 days": 90}
          vi_cutoff = datetime.now() - timedelta(days=vi_days_map[vi_period])
          history_vi_filtered = {
              ts: snap for ts, snap in history_for_vi.items()
              if parse_ts(ts) and parse_ts(ts) >= vi_cutoff
          }

      def _parse_vi(ts):
          try:
              return datetime.fromisoformat(ts.replace("Z", ""))
          except Exception:
              return None

      vi_series = {}
      for ts, snap in history_vi_filtered.items():
          dt = _parse_vi(ts)
          if not dt or not isinstance(snap, dict):
              continue
          for artist, info in snap.items():
              if not isinstance(info, dict):
                  continue
              pc = info.get("playcount")
              if pc is not None:
                  vi_series.setdefault(artist, []).append((dt, int(pc)))

      baseline_for_vi_slope = load_long_term_baseline()

      def get_slope(artist):
          first_dt = None
          for ts, snap in history_vi_filtered.items():
              dt = _parse_vi(ts)
              if dt and isinstance(snap, dict) and artist in snap:
                  if first_dt is None or dt < first_dt:
                      first_dt = dt
          if not first_dt:
              return 0.0
          now_vi = datetime.now()
          days_since = max((now_vi - first_dt).total_seconds() / 86400.0, 1.0)
          base = baseline_for_vi_slope.get(artist, {})
          base_plays = base.get("playcount")
          curr_plays = next((int(a.get("playcount", 0)) for a in full_top_artists if a.get("name") == artist), 0)
          if base_plays is None:
              play_gain = curr_plays
          else:
              play_gain = max(0, curr_plays - int(base_plays))
          return round(play_gain / days_since, 2)

      def get_tier(slope):
          if slope >= 1.0:
              return "Cheetah"
          elif slope >= 0.59:
              return "Cardinal"
          elif slope >= 0.35:
              return "Mountain Goat"
          elif slope >= 0.19:
              return "Kitty Cat"
          elif slope >= 0.06:
              return "Snail"
          else:
              return "Sloth"

      tier_colors_vi = {
          "Cheetah": "#D85A30",
          "Cardinal": "#D4537E",
          "Mountain Goat": "#1D9E75",
          "Kitty Cat": "#378ADD",
          "Snail": "#BA7517",
          "Sloth": "#888780",
          "Fading": "#993556",
      }

      baseline_for_vi = load_long_term_baseline()

      vi_rows = []
      for i, a in enumerate(full_top_artists):
          name = a.get("name")
          if not name:
              continue
          try:
              curr_plays = int(a.get("playcount", 0))
          except Exception:
              curr_plays = 0

          curr_rank = i + 1
          base = baseline_for_vi.get(name, {})
          base_rank = base.get("rank")

          if base_rank is None:
              rank_delta = "—"
          else:
              d = base_rank - curr_rank
              if d > 0:
                  rank_delta = "+%d" % d
              elif d < 0:
                  rank_delta = str(d)
              else:
                  rank_delta = "0"

          slope = get_slope(name)
          tier = get_tier(slope)

          vi_rows.append({
              "Rank": curr_rank,
              "Artist": name,
              "Tier": tier,
              "Plays": curr_plays,
              "Δ rank": rank_delta,
              "Plays/day": round(slope, 2),
          })

      import pandas as pd

      df_vi = pd.DataFrame(vi_rows)

      tier_order = ["Cheetah", "Cardinal", "Mountain Goat", "Kitty Cat", "Snail", "Sloth", "Fading"]

      def color_tier_row(row):
          color = tier_colors_vi.get(row["Tier"], "#888780")
          return ["color: %s" % color if col == "Tier" else "" for col in row.index]

      styled = df_vi.style.apply(color_tier_row, axis=1).format({
          "Plays": "{:,}",
          "Plays/day": "{:+.2f}",
      })

      st.dataframe(styled, use_container_width=True, hide_index=True, key="velocity_index_table")

      st.divider()
      st.markdown("Tier breakdown")
      tier_summary = []
      for tier in tier_order:
          count = len(df_vi[df_vi["Tier"] == tier])
          if count > 0:
              avg_slope = df_vi[df_vi["Tier"] == tier]["Plays/day"].mean()
              tier_summary.append({
                  "Tier": tier,
                  "Artists": count,
                  "Avg plays/day": round(avg_slope, 2),
              })
      st.dataframe(tier_summary, use_container_width=True, hide_index=True, key="vi_tier_summary")

      return

    baseline_data = load_long_term_baseline()

    # Surrounding leaderboard + log snapshot (only when in top 500)
    artists, playcounts = [], []
    if in_top500:
        leaderboard, _ = get_leaderboard_surrounding_artists(username, recent_artist, limit=500)
        if leaderboard:
            leaderboard_sorted = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
            artists = [a for a, _ in leaderboard_sorted]
            playcounts = [c for _, c in leaderboard_sorted]

            current_data = {
                artist: {"playcount": leaderboard[artist], "rank": overall_ranks.get(artist)}
                for artist in artists
            }
            save_current_leaderboard(current_data)
            log_leaderboard_snapshot(current_data)

    if not in_top500:
        render_manual_tracker(recent_artist, recent_track_name, album_art_url)
        return

    # Progress
    artist_progress = compute_artist_progress(baseline_data, full_top_artists)

    if can_show_insight:
      meta_for_insight = load_artist_meta()
      window_items = get_history_window(days=7)

      # Only compute loyalty rows if you have the function available
      loyalty_rows = []
      try:
          loyalty_rows = compute_artist_loyalty_index(window_items, min_obs=3)
      except Exception:
          loyalty_rows = []

      insight = generate_insight(
          meta=meta_for_insight,
          window_items=window_items,
          loyalty_rows=loyalty_rows
      )

      if insight:
          st.info(insight)
          st.session_state.last_insight_time = now

    # -------------------------
    # Leaderboard UI
    # -------------------------
    ranked_artists, bar_colors = [], []
    for artist in artists:
        curr_rank = overall_ranks.get(artist)
        label = f"{curr_rank}. {artist}" if curr_rank else artist
        if artist.lower() == recent_artist.lower():
            label += " (current)"
        ranked_artists.append(label)

        base_rank = (baseline_data.get(artist) or {}).get("rank")
        if base_rank is None or curr_rank is None:
            color = COLOR_FLAT
        else:
            if curr_rank < base_rank:
                color = COLOR_RISING
            elif curr_rank > base_rank:
                color = COLOR_FALLEN
            else:
                color = COLOR_FLAT

        if artist.lower() == recent_artist.lower():
            color = COLOR_ACTIVE

        bar_colors.append(color)

    hero_fig = make_leaderboard_fig(
        artists=artists,
        playcounts=playcounts,
        ranked_artists=ranked_artists,
        bar_colors=bar_colors,
        height=450,
        title="Leaderboard: Surrounding Artists (colors vs baseline)",
    )

    mini_fig = make_leaderboard_fig(
        artists=artists,
        playcounts=playcounts,
        ranked_artists=ranked_artists,
        bar_colors=bar_colors,
        height=260,
        title="",
    )
    mini_fig.update_layout(margin=dict(l=70, r=10, t=10, b=10), xaxis_title="")
    mini_fig.update_xaxes(showticklabels=False)
    mini_fig.update_yaxes(tickfont=dict(size=11))

    curr_rank_for_artist = overall_ranks.get(recent_artist)
    curr_play_for_artist = top_playcounts.get(recent_artist)

    if view_mode == "Leaderboard (default)":
        st.plotly_chart(hero_fig, use_container_width=True, key="hero_leaderboard")
        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Track: **{recent_track_name}**")
            st.markdown(f"**Artist:** {recent_artist}")
            st.markdown(f"**Overall rank:** {curr_rank_for_artist}")
            st.markdown(f"**Playcount:** {recent_playcount}")
        with col2:
            if album_art_url:
                st.image(album_art_url, width=160)

    elif view_mode == "Now Playing":
        left, right = st.columns([1.1, 1.9], vertical_alignment="top")
        with left:
            if album_art_url:
                st.image(album_art_url, use_container_width=True)
            else:
                st.caption("No album art found for this track.")
            st.markdown("")
            st.markdown(f"## {recent_artist}")
            st.markdown(f"**{recent_track_name}**")
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Overall rank", value=curr_rank_for_artist if curr_rank_for_artist else "—")
            with m2:
                st.metric("Artist playcount", value=curr_play_for_artist if curr_play_for_artist is not None else "—")
        with right:
            st.markdown("### Leaderboard (mini)")
            st.plotly_chart(mini_fig, use_container_width=True, key="mini_leaderboard", config={"displayModeBar": False})
        st.divider()

    # -------------------------
    # Meta Sections
    # -------------------------
    meta = load_artist_meta()
    meta = render_artist_tagger(recent_artist, overall_ranks, meta)

    st.divider()

    # Trend chart for current artist (from history)
    history = load_leaderboard_history()


    st.divider()

    trend_tab, bump_tab = st.tabs(["Rank / Playcount over time", "Bump chart"])

    with trend_tab:
        metric = st.radio("View over time:", ["Rank", "Playcount"], horizontal=True, key="trend_metric")
        show_surrounding = st.toggle("Show surrounding artists", value=False, key="trend_show_surrounding")

        plot_artists = [recent_artist]
        if show_surrounding and artists:
            plot_artists = list(artists)

        fig_metric = go.Figure()
        series_added = 0

        def _parse_ts(ts):
            try:
                return datetime.fromisoformat(ts.replace("Z", ""))
            except Exception:
                return None

        snapshots = []
        for ts, snap in history.items():
            dt = _parse_ts(ts)
            if not dt or not isinstance(snap, dict):
                continue
            snapshots.append((dt, snap))
        snapshots.sort(key=lambda x: x[0])

        for a in plot_artists:
            xs, ys = [], []
            for dt, snap in snapshots:
                info = snap.get(a)
                if not isinstance(info, dict):
                    continue
                val = info.get("rank") if metric == "Rank" else info.get("playcount")
                if val is None:
                    continue
                xs.append(dt)
                ys.append(val)

            if len(xs) >= 2:
                fig_metric.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=a))
                series_added += 1

        if series_added == 0:
            st.caption("Not enough history yet. Keep the app running to collect snapshots.")
        else:
            if metric == "Rank":
                fig_metric.update_yaxes(autorange="reversed")
                y_label = "Overall Rank"
                title = "Surrounding Artists: Rank Over Time" if show_surrounding else f"{recent_artist} Rank Over Time"
            else:
                y_label = "Playcount"
                title = "Surrounding Artists: Playcount Over Time" if show_surrounding else f"{recent_artist} Playcount Over Time"

            fig_metric.update_layout(
                title=title,
                xaxis_title="Snapshot Time",
                yaxis_title=y_label,
                margin=dict(l=60, r=30, t=50, b=40),
                height=380,
                legend_title_text="Artist (click to isolate)",
            )
            st.plotly_chart(fig_metric, use_container_width=True, key="trend_chart")

    with bump_tab:
        bump_top_n = st.slider("Artists to show", 5, 15, 10, key="bump_top_n")
        bump_fig = make_bump_chart(
            history=history,
            artists=artists,
            overall_ranks=overall_ranks,
            recent_artist=recent_artist,
            top_n=bump_top_n,
        )
        if bump_fig is None:
            st.caption("Not enough snapshot history yet to draw a bump chart. Keep the app running to collect data.")
        else:
            st.plotly_chart(bump_fig, use_container_width=True, key="bump_chart")

    # Choose which artists to plot
    plot_artists = [recent_artist]
    if show_surrounding and artists:
        # 'artists' is your current surrounding list
        plot_artists = list(artists)

    # Build series for each artist
    fig_metric = go.Figure()
    series_added = 0

    def _parse_ts(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except Exception:
            return None

    # Pre-sort snapshots by datetime
    snapshots = []
    for ts, snap in history.items():
        dt = _parse_ts(ts)
        if not dt or not isinstance(snap, dict):
            continue
        snapshots.append((dt, snap))
    snapshots.sort(key=lambda x: x[0])

    for a in plot_artists:
        xs, ys = [], []
        for dt, snap in snapshots:
            info = snap.get(a)
            if not isinstance(info, dict):
                continue
            val = info.get("rank") if metric == "Rank" else info.get("playcount")
            if val is None:
                continue
            xs.append(dt)
            ys.append(val)

        # Only plot if we have enough points
        if len(xs) >= 2:
            fig_metric.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=a))
            series_added += 1

    if series_added == 0:
        if show_surrounding:
            st.caption("Not enough history yet to plot surrounding artists. Keep the app running to collect snapshots.")
        else:
            st.caption(f"Not enough history to plot {recent_artist}'s trend over time.")
    else:
        if metric == "Rank":
            fig_metric.update_yaxes(autorange="reversed")
            y_label = "Overall Rank"
            title = "Surrounding Artists: Rank Over Time" if show_surrounding else f"{recent_artist} Rank Over Time"
        else:
            y_label = "Playcount"
            title = "Surrounding Artists: Playcount Over Time" if show_surrounding else f"{recent_artist} Playcount Over Time"

        fig_metric.update_layout(
            title=title,
            xaxis_title="Snapshot Time",
            yaxis_title=y_label,
            margin=dict(l=60, r=30, t=50, b=40),
            height=380,
            legend_title_text="Artist (click to isolate)",
        )

    st.divider()
    st.markdown("### Δ Rank vs baseline (surrounding artists)")

    delta_rows = []
    for a in artists:
        r = overall_ranks.get(a)
        base_r = (baseline_data.get(a) or {}).get("rank")
        if r is None or base_r is None:
            delta_txt = "—"
        else:
            d = base_r - r
            delta_txt = f"{'↑' if d > 0 else '↓' if d < 0 else '•'} {abs(d)}" if d != 0 else "• 0"

        delta_rows.append(
            {
                "Rank": r if r is not None else "—",
                "Artist": a,
                "Δ vs baseline": delta_txt,
                "Plays": (top_playcounts.get(a) if top_playcounts.get(a) is not None else "—"),
            }
        )

    st.dataframe(delta_rows, use_container_width=True, hide_index=True, key="baseline_delta_table")

    st.divider()

    top_n = st.slider("Rows to show", 25, 200, 100, 25, key="gainers_top_n")
    st.markdown(f"### 📈 Biggest Playcount Gains Since Baseline (Top {top_n})")

    gainer_rows = build_playcount_gainers_rows(artist_progress, top_n=top_n)

    st.dataframe(
        gainer_rows,
        use_container_width=True,
        hide_index=True,
        key="playcount_gainers_since_baseline",
    )

    st.divider()

    risers, fallers = compute_biggest_movers(artist_progress, top_n=10)

    st.markdown("### 🏆 Biggest Movers Since First Appearance")

    st.markdown("#### Biggest Risers")
    for name, p in risers:
        st.markdown(f"- **{name}**: up {p['rank_change']} spots (plays +{p['play_change']})")

    st.markdown("#### Biggest Fallers")
    for name, p in fallers:
        st.markdown(f"- **{name}**: down {abs(p['rank_change'])} spots (plays {p['play_change']:+d})")

    st.markdown("### 🔎 Discover Artists by Tags + Moods")

    tag_library, mood_library = get_tag_library(meta)

    cA, cB, cC = st.columns([2, 2, 1])

    with cA:
        query_tags = st.multiselect(
            "Search / select tags",
            options=tag_library,
            default=[],
            key="discover_query_tags",
        )

    with cB:
        query_moods = st.multiselect(
            "Search / select moods",
            options=mood_library,
            default=[],
            key="discover_query_moods",
        )

    with cC:
        query_era = st.selectbox(
            "Era (tiebreaker)",
            options=ERA_OPTIONS,
            index=0,
            key="discover_query_era",
        )

    top_n = st.slider("How many recommendations?", 5, 30, 12, key="discover_top_n")

    exclude_current = st.checkbox("Exclude current artist", value=True, key="discover_exclude_current")

    if st.button("Recommend artists", key="discover_btn"):
        if not query_tags and not query_moods:
            st.warning("Pick at least one tag or mood to get recommendations.")
        else:
            recs = recommend_artists_from_query(
                meta=meta,
                query_tags=query_tags,
                query_moods=query_moods,
                query_era=query_era,
                top_n=top_n,
                exclude=recent_artist if exclude_current else None,
            )

            if not recs:
                st.info("No matches yet. Tag a few more artists, or broaden your tag/mood selection.")
            else:
                st.dataframe(recs, use_container_width=True, hide_index=True, key="discover_results_table")


    st.divider()

if __name__ == "__main__":
    main()
