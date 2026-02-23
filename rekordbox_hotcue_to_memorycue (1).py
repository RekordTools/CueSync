#!/usr/bin/env python3
"""
Rekordbox Hot Cue → Memory Cue Converter
=========================================
Converts all hot cues in a rekordbox XML export to memory cues.

Usage:
    python rekordbox_hotcue_to_memorycue.py <input.xml> [output.xml]

Notes:
    - rekordbox supports a maximum of 10 memory cues per track.
      If adding a converted hot cue would exceed this limit, it is skipped
      and a warning is shown so the user can manually resolve it.
"""

import xml.etree.ElementTree as ET
import sys
import os
import shutil
from datetime import datetime

MEMORY_CUE_LIMIT = 10


def convert_hotcues_to_memorycues(input_path, output_path, remove_hotcues=False):
    print(f"\n🎵 Rekordbox Hot Cue → Memory Cue Converter")
    print(f"   Input:  {input_path}")
    print(f"   Output: {output_path}")
    print(f"   Remove original hot cues: {remove_hotcues}\n")

    try:
        tree = ET.parse(input_path)
    except ET.ParseError as e:
        print(f"❌ Error parsing XML: {e}")
        sys.exit(1)

    root = tree.getroot()
    collection = root.find("COLLECTION")
    if collection is None:
        print("❌ No <COLLECTION> element found. Is this a valid rekordbox XML?")
        sys.exit(1)

    total_tracks = 0
    total_hotcues_found = 0
    total_memory_cues_added = 0
    total_hotcues_removed = 0
    total_skipped = 0
    tracks_with_warnings = []

    for track in collection.findall("TRACK"):
        track_name = track.get("Name", track.get("Location", "Unknown"))
        total_tracks += 1

        hotcues = [pm for pm in track.findall("POSITION_MARK") if int(pm.get("Num", -1)) >= 0]
        if not hotcues:
            continue

        total_hotcues_found += len(hotcues)
        track_skipped = 0

        for hc in hotcues:
            start_pos = hc.get("Start")

            # Skip if memory cue already exists at this position
            existing = any(
                pm.get("Start") == start_pos and int(pm.get("Num", -1)) == -1
                for pm in track.findall("POSITION_MARK")
            )
            if existing:
                continue

            # Count current memory cues (re-query each iteration to include newly added ones)
            current_count = sum(
                1 for pm in track.findall("POSITION_MARK")
                if int(pm.get("Num", -1)) == -1
            )

            if current_count >= MEMORY_CUE_LIMIT:
                total_skipped += 1
                track_skipped += 1
                continue

            # Create memory cue
            mem_cue = ET.Element("POSITION_MARK")
            for attr, val in hc.attrib.items():
                mem_cue.set(attr, val)
            mem_cue.set("Num", "-1")
            mem_cue.set("Type", "0")

            idx = list(track).index(hc)
            track.insert(idx, mem_cue)
            total_memory_cues_added += 1

        if track_skipped > 0:
            tracks_with_warnings.append((track_name, track_skipped))

        if remove_hotcues:
            for hc in [pm for pm in track.findall("POSITION_MARK") if int(pm.get("Num", -1)) >= 0]:
                track.remove(hc)
                total_hotcues_removed += 1

    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"✅ Done!")
    print(f"   Tracks processed:      {total_tracks}")
    print(f"   Hot cues found:        {total_hotcues_found}")
    print(f"   Memory cues added:     {total_memory_cues_added}")
    if total_skipped > 0:
        print(f"\n   ⚠️  {total_skipped} cue(s) skipped — 10 memory cue limit reached:")
        for name, count in tracks_with_warnings:
            print(f"     • {os.path.basename(name)}  ({count} skipped)")
        print(f"\n   Tip: Remove some existing memory cues on these tracks in rekordbox,")
        print(f"   then re-run CueSync to fill the remaining slots.")
    if remove_hotcues:
        print(f"   Hot cues removed:      {total_hotcues_removed}")
    print(f"\n   Output saved to: {output_path}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
        output_path = sys.argv[2]
    else:
        base, ext = os.path.splitext(input_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{base}_memory_cues_{timestamp}{ext}"

    remove_hotcues = "--remove-hotcues" in sys.argv

    backup_path = input_path + ".backup"
    if not os.path.exists(backup_path):
        shutil.copy2(input_path, backup_path)
        print(f"💾 Backup created: {backup_path}")

    convert_hotcues_to_memorycues(input_path, output_path, remove_hotcues)


if __name__ == "__main__":
    main()
