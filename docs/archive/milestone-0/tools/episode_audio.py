#!/usr/bin/env python3
"""Turn a For one script into audio with Gemini 3.8 Flash TTS.

Milestone 0 helper (optional; the AI Studio speech playground does the same by hand).

The script file has one line per turn, "Name: text", e.g.
    Karim: Okay, I have a confession.
    Mona: Oh no. How bad was it?
Blank lines and lines without "Name:" are ignored. Inline pauses such as <pause 2s> are passed through.

Usage:
    pip install google-genai          (once)
    export GEMINI_API_KEY=...         (a key from a Cloud project with billing on)
    python episode_audio.py L03-ep05.txt --voices Karim=Puck,Mona=Aoede
    python episode_audio.py storyA.txt --voices Narrator=Charon
    python episode_audio.py repeatA.txt --voices Narrator=Charon --split

Output: an .mp3 next to the input (or .wav if ffmpeg is not installed). With --split, one file per line.

Written against the Gemini API speech-generation docs of 2026-10-10 (Interactions API, model
gemini-3.8-flash-tts). It has not been run against the live API from this kit: test it once with
a two-line script before relying on it.
"""
import argparse
import base64
import io
import os
import re
import shutil
import subprocess
import sys
import wave

MODEL = "gemini-3.8-flash-tts"
TURN = re.compile(r"^\s*([A-Za-z][\w .'-]{0,30}):\s*(.+?)\s*$")


def parse_script(path):
    turns = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = TURN.match(line)
            if m:
                turns.append((m.group(1).strip(), m.group(2)))
    if not turns:
        sys.exit(f"No 'Name: text' lines found in {path}")
    return turns


def parse_voices(spec):
    voices = {}
    for part in spec.split(","):
        if "=" not in part:
            sys.exit(f"--voices needs Name=Voice pairs, got {part!r}")
        name, voice = part.split("=", 1)
        voices[name.strip()] = voice.strip()
    return voices


def tts(client, turns, voices, styles):
    """One request for a list of turns; returns raw 24 kHz mono 16-bit PCM."""
    speakers = sorted({s for s, _ in turns})
    content = []
    for speaker, text in turns:
        meta = {"type": "speech_metadata", "speaker": speaker}
        if speaker in styles:
            meta["style"] = styles[speaker]
        content.append({"type": "text", "text": text, "annotations": [meta]})
    if len(speakers) == 1:
        # Single speaker: speech_config is a list of {"voice": ...} (per the docs).
        for item in content:
            item["annotations"][0].pop("speaker", None)
            if not item["annotations"][0].get("style"):
                item.pop("annotations")
        speech_config = [{"voice": voices[speakers[0]]}]
    elif len(speakers) == 2:
        speech_config = {"speakers": [{"speaker": s, "voice": voices[s]} for s in speakers]}
    else:
        sys.exit(f"Gemini TTS takes at most 2 speakers per request; found {speakers}")
    interaction = client.interactions.create(
        model=MODEL,
        input=[{"type": "user_input", "content": content}],
        response_format={"type": "audio"},
        generation_config={"speech_config": speech_config},
    )
    audio = base64.b64decode(interaction.output_audio.data)
    if audio[:4] == b"RIFF":  # strip the WAV header so chunks can be joined
        with wave.open(io.BytesIO(audio)) as w:
            return w.readframes(w.getnframes())
    return audio


def save(pcm, out_base):
    wav_path = out_base + ".wav"
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(pcm)
    if shutil.which("ffmpeg"):
        mp3_path = out_base + ".mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
                        "-codec:a", "libmp3lame", "-b:a", "96k", mp3_path], check=True)
        os.remove(wav_path)
        return mp3_path
    return wav_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script")
    ap.add_argument("--voices", required=True, help="e.g. Karim=Puck,Mona=Aoede")
    ap.add_argument("--style", default="", help='optional per speaker, e.g. "Karim=warm and relaxed;Mona=quick and dry"')
    ap.add_argument("--chunk", type=int, default=24, help="turns per request (default 24)")
    ap.add_argument("--split", action="store_true", help="one audio file per line")
    ap.add_argument("--dry-run", action="store_true", help="parse and show the plan without calling the API")
    args = ap.parse_args()

    turns = parse_script(args.script)
    voices = parse_voices(args.voices)
    styles = {}
    for part in filter(None, args.style.split(";")):
        name, style = part.split("=", 1)
        styles[name.strip()] = style.strip()
    missing = {s for s, _ in turns} - voices.keys()
    if missing:
        sys.exit(f"No voice given for: {', '.join(sorted(missing))}")

    base = os.path.splitext(args.script)[0]
    groups = [[t] for t in turns] if args.split else [turns[i:i + args.chunk] for i in range(0, len(turns), args.chunk)]
    words = sum(len(t.split()) for _, t in turns)
    print(f"{len(turns)} turns, {words} words, about {words / 140:.1f} minutes; {len(groups)} request(s)")
    if args.dry_run:
        return

    from google import genai  # imported here so --dry-run works without the package
    client = genai.Client()  # reads GEMINI_API_KEY

    if args.split:
        for n, group in enumerate(groups, 1):
            print("saved", save(tts(client, group, voices, styles), f"{base}-{n:02d}"))
    else:
        pcm = b"".join(tts(client, g, voices, styles) for g in groups)
        print("saved", save(pcm, base))


if __name__ == "__main__":
    main()
