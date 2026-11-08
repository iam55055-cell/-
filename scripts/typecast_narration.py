#!/usr/bin/env python3
"""뉴과 나레이션 생성기 (타입캐스트 · 민욱).

녹음 원고 전체를 타입캐스트 API로 읽혀서, 끊김 없는 파일 하나로 만든다.

- 목소리는 이름(기본 "민욱")으로 찾는다. --voice-id 로 직접 지정할 수도 있다.
- API는 한 번에 2,000자까지만 받으므로 문단 단위로 나눠 보낸다.
  모든 구간을 같은 목소리·모델·감정·속도로 생성해서 톤을 맞춘다.
- 구간들을 이어 붙여 WAV 하나로 저장한다. ffmpeg가 있으면 MP3도 만든다.

필요한 것: 파이썬 3.8 이상. 추가 설치 없음 (표준 라이브러리만 사용).
API 키: 환경 변수 TYPECAST_API_KEY

사용법:
    python scripts/typecast_narration.py docs/episode-01-recording.txt
    python scripts/typecast_narration.py docs/episode-01-recording.txt --tempo 0.95
    python scripts/typecast_narration.py docs/episode-01-recording.txt --dry-run
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

API_HOST = "https://api.typecast.ai"
MAX_CHARS = 2000  # 타입캐스트 text-to-speech 한 번에 받는 최대 글자 수


def api_key() -> str:
    key = os.environ.get("TYPECAST_API_KEY", "").strip()
    if not key:
        sys.exit(
            "TYPECAST_API_KEY 환경 변수가 없습니다.\n"
            "  Windows:  set TYPECAST_API_KEY=발급받은키\n"
            "  macOS:    export TYPECAST_API_KEY=발급받은키\n"
            "키는 https://typecast.ai/developers/api 의 API Keys 탭에 있습니다."
        )
    return key


def request(method: str, path: str, key: str, body: dict | None = None,
            params: dict | None = None) -> bytes:
    url = API_HOST + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-API-KEY", key)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            if e.code == 429 and attempt < 3:
                time.sleep(2 ** (attempt + 1))
                continue
            hints = {
                401: "API 키가 틀렸거나 API 요금제 키가 아닙니다 (웹 요금제와 API 요금제는 별개).",
                402: "API 크레딧이 부족합니다.",
                403: "예전(Starter) API 키이거나 휴면 계정입니다. 새 API 키를 발급받으세요.",
                404: "목소리 ID를 찾을 수 없습니다.",
            }
            sys.exit(f"타입캐스트 오류 {e.code}: {detail}\n→ {hints.get(e.code, '')}")
    sys.exit("타입캐스트 요청이 계속 실패했습니다 (요청 한도 초과).")


def find_voice(key: str, name: str, model: str) -> str:
    raw = request("GET", "/v3/voices", key, params={"model": model})
    voices = json.loads(raw)
    exact, partial = [], []
    for v in voices:
        vn = v.get("voice_name") or {}
        names = [vn.get("kor", ""), vn.get("eng", "")] if isinstance(vn, dict) else [str(vn)]
        if name in names:
            exact.append(v)
        elif any(name in n for n in names if n):
            partial.append(v)
    hits = exact or partial
    if not hits:
        sys.exit(f"'{name}' 목소리를 {model} 모델에서 찾지 못했습니다. --model ssfm-v21 로 바꿔 보거나 --voice-id 로 직접 지정하세요.")
    v = hits[0]
    vn = v.get("voice_name")
    print(f"목소리: {vn} → {v['voice_id']}")
    if len(hits) > 1:
        others = ", ".join(f"{h.get('voice_name')}={h['voice_id']}" for h in hits[1:5])
        print(f"  (같은 이름 후보가 더 있습니다: {others})")
    return v["voice_id"]


def split_text(text: str, limit: int = MAX_CHARS) -> list[str]:
    """빈 줄(문단) 경계에서 limit 이하로 자른다. 문장 중간에서는 자르지 않는다."""
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(p) > limit:
            # 문단 하나가 너무 길면 줄 단위로 자른다
            for line in p.split("\n"):
                cand = (cur + "\n" + line).strip() if cur else line
                if len(cand) > limit:
                    chunks.append(cur)
                    cur = line
                else:
                    cur = cand
            continue
        cand = (cur + "\n\n" + p) if cur else p
        if len(cand) > limit:
            chunks.append(cur)
            cur = p
        else:
            cur = cand
    if cur:
        chunks.append(cur)
    return chunks


def tts(key: str, voice_id: str, text: str, args) -> bytes:
    body = {
        "voice_id": voice_id,
        "text": text,
        "model": args.model,
        "language": "kor",
        "output": {
            "audio_format": "wav",
            "audio_tempo": args.tempo,
            "audio_pitch": args.pitch,
            "volume": 100,
        },
    }
    if args.model == "ssfm-v21":
        body["prompt"] = {"emotion_preset": args.emotion, "emotion_intensity": args.intensity}
    else:
        body["prompt"] = {
            "emotion_type": "preset",
            "emotion_preset": args.emotion,
            "emotion_intensity": args.intensity,
        }
    return request("POST", "/v1/text-to-speech", key, body=body)


def join_wavs(parts: list[bytes], out: Path, gap_sec: float) -> float:
    params = None
    frames = []
    for b in parts:
        with wave.open(io.BytesIO(b)) as w:
            if params is None:
                params = w.getparams()
            elif (w.getnchannels(), w.getsampwidth(), w.getframerate()) != (
                params.nchannels, params.sampwidth, params.framerate):
                sys.exit("구간마다 오디오 형식이 달라서 이어 붙일 수 없습니다.")
            frames.append(w.readframes(w.getnframes()))
    silence = b"\x00" * int(params.framerate * gap_sec) * params.sampwidth * params.nchannels
    with wave.open(str(out), "wb") as w:
        w.setnchannels(params.nchannels)
        w.setsampwidth(params.sampwidth)
        w.setframerate(params.framerate)
        for i, f in enumerate(frames):
            if i:
                w.writeframes(silence)
            w.writeframes(f)
        n = w.getnframes() if hasattr(w, "getnframes") else None
    with wave.open(str(out)) as r:
        return r.getnframes() / r.getframerate()


def main() -> None:
    ap = argparse.ArgumentParser(description="타입캐스트로 뉴과 나레이션 전체를 한 파일로 생성")
    ap.add_argument("script", type=Path, help="녹음 원고 텍스트 파일")
    ap.add_argument("--voice-name", default="민욱")
    ap.add_argument("--voice-id", help="목소리 ID를 직접 지정 (tc_로 시작)")
    ap.add_argument("--model", default="ssfm-v30", choices=["ssfm-v21", "ssfm-v30", "ssfm-v31"])
    ap.add_argument("--emotion", default="normal")
    ap.add_argument("--intensity", type=float, default=1.0)
    ap.add_argument("--tempo", type=float, default=1.0, help="속도 0.5~2.0 (기본 1.0)")
    ap.add_argument("--pitch", type=int, default=0, help="음높이 -12~12")
    ap.add_argument("--gap", type=float, default=0.6, help="구간 사이 쉼(초)")
    ap.add_argument("--out", type=Path, help="저장할 WAV 경로")
    ap.add_argument("--dry-run", action="store_true", help="API를 부르지 않고 나누기 결과만 보기")
    args = ap.parse_args()

    text = args.script.read_text(encoding="utf-8")
    chunks = split_text(text)
    print(f"원고 {len(text)}자 → {len(chunks)}개 구간: " + ", ".join(str(len(c)) for c in chunks))
    if args.dry_run:
        return

    key = api_key()
    voice_id = args.voice_id or find_voice(key, args.voice_name, args.model)

    out = args.out or Path("outputs") / (args.script.stem + "-" + args.voice_name + ".wav")
    out.parent.mkdir(parents=True, exist_ok=True)
    parts_dir = out.parent / (out.stem + "_parts")
    parts_dir.mkdir(exist_ok=True)

    parts = []
    for i, c in enumerate(chunks, 1):
        part = parts_dir / f"{i:02d}.wav"
        if part.exists() and part.stat().st_size > 0:
            print(f"[{i}/{len(chunks)}] 이미 있음, 건너뜀")
        else:
            print(f"[{i}/{len(chunks)}] 생성 중 ({len(c)}자)…")
            part.write_bytes(tts(key, voice_id, c, args))
        parts.append(part.read_bytes())

    sec = join_wavs(parts, out, args.gap)
    print(f"완료: {out}  ({int(sec // 60)}분 {int(sec % 60)}초)")

    if shutil.which("ffmpeg"):
        mp3 = out.with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out),
                        "-codec:a", "libmp3lame", "-b:a", "192k", str(mp3)], check=True)
        print(f"MP3:  {mp3}")


if __name__ == "__main__":
    main()
