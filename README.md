# CueSync
### Rekordbox Hot Cue → Memory Cue Converter

Tired of manually adding memory cues to every track in your rekordbox library? **CueSync does it automatically.**

Load your rekordbox XML, run the script, and every hot cue in your entire library becomes a memory cue — in seconds. Preserves cue names, positions, and colours.

---

> 🖥️ **Prefer a simple double-click Windows app with no terminal required?**
> **[Get CueSync for £7 → rekordtools.gumroad.com/l/iwtml](https://rekordtools.gumroad.com/l/iwtml)**

---

## How It Works

CueSync reads your rekordbox XML export and duplicates every hot cue as a memory cue. That's it. No rekordbox plugin, no reverse engineering — just standard XML in, XML out.

## Requirements

- Python 3.6+
- No external libraries needed

## Usage

**Step 1 — Export your rekordbox library**

In rekordbox: `File → Export Collection in xml format`

**Step 2 — Run the script**

```bash
# Basic usage — adds memory cues, keeps hot cues
python rekordbox_hotcue_to_memorycue.py my_collection.xml

# Custom output filename
python rekordbox_hotcue_to_memorycue.py my_collection.xml output.xml

# Remove hot cues after converting
python rekordbox_hotcue_to_memorycue.py my_collection.xml --remove-hotcues
```

**Step 3 — Import back into rekordbox**

`Preferences → Advanced → rekordbox xml` — point it at your output file and import.

## Features

- ✔ Converts unlimited hot cues to memory cues
- ✔ Preserves cue names, positions & colours
- ✔ Automatic backup before every conversion
- ✔ Works with rekordbox 5, 6 & 7
- ✔ No external dependencies

## Want Something Simpler?

This script requires Python installed and comfort with the terminal. If you'd rather just **download, double-click, and go** — the CueSync Windows app has a full GUI, automatic backups, and a live conversion log.

**[Download the Windows app — £7 (one-time)](https://rekordtools.gumroad.com/l/iwtml)**

No Python needed. No terminal. Just drag your XML in and hit Convert.

---

## License

MIT License — free to use, share, and modify. See [LICENSE](LICENSE) for details.

---

*Not affiliated with Pioneer DJ or rekordbox.*
*Built by [RekordTools](https://rekordtools.net) — DJ utilities for serious players.*
