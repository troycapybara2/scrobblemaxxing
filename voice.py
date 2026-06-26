# =====================================================================
# voice.py  —  every human-facing word lives here.
#
# This is the ONLY file you touch to change how the app *talks*.
# Rewrite anything below in your own voice, commit voice.py, reboot.
# Nothing else depends on your wording — break a sentence, not the app.
#
# Rules:
#   - Keep the variable NAMES (the ALL_CAPS ones) exactly as they are.
#   - You can change, add, or delete the strings inside the lists/quotes.
#   - Where a string supports a {variable}, it's noted above it. Keep the
#     {curly_braces} spelling if you want that value to appear; drop it if
#     you don't. Any other word is yours.
#   - An empty list  []  silences that kind of line entirely.
# =====================================================================


# ---- The masthead at the very top of the app ----
APP_TITLE = "Scrobblemaxxing"
# Your one-liner under the title. This is the most "you" line in the app —
# write something that sounds like you. Leave as "" to hide it.
APP_TAGLINE = "every day i'm scrobblin..."


# ---- Insight lines ----
# These surface occasionally above the leaderboard. The app picks ONE at
# random from whichever group currently applies, so give each group a few
# variants if you want variety. Write them like notes to yourself.

# Triggered when your recent listening skews low-energy. No variables.
INSIGHTS_ENERGY_LOW = [
    "why you always sad and depressed all the time like a lil bitch?", "who's ready to cry in the shower later?", "are you overstimulated?", "slow songs feel good right now", "low energy day", "chill vibes",
]

# Triggered when your recent listening skews high-energy. No variables.
INSIGHTS_ENERGY_HIGH = [
    "BAHHHHHHHHHHHHH", "understimulation station. choo choo bitch", "let's get fired up", "i think this next song calls for a dance break", "10 push-ups? do it you won't", "so much energy"
]

# Triggered when your most-returned-to artist isn't your #1.
# Available: {artist}
INSIGHTS_LOYAL_NOT_TOP = [
    "{artist} isn't my top artist, but I keep circling back.", "{artist} is killin it on that oven", "{artist} has a massive shlong", "{artist} solved world hunger yesterday."
]

# Triggered for an artist you return to often despite a low rank.
# Available: {artist}
INSIGHTS_QUIET_DEVOTION = [
    "{artist} hasn't climbed far, yet I keep coming home to them.", "{artist} is a lowkey bop", "your lowkey favorite lately has been {artist}", "don't look now but {artist} is climbing the ranks", "the momentum is building for {artist}"
]


# ---- A couple of empty-state lines you might want in your voice ----
# (Optional — wire more in later if you like. These are here as a start.)
EMPTY_NOT_ENOUGH_HISTORY = "i just bipped right on the highway lowkey"
