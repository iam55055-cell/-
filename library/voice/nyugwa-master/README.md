# 뉴과 마스터 보이스 (등록 2026-11-08)

뉴과의 모든 나레이션은 이 목소리와 이 설정으로만 만든다. 새 회차 음원이 이 기준과 다르게 들리면 이 폴더의 레퍼런스와 비교해서 맞춘다.

| 항목 | 값 |
|---|---|
| 목소리 | 타입캐스트 · **민욱** (Minuk) |
| voice_id | `tc_68f0727fd62a5934102f7ec0` |
| 모델 · 감정 | ssfm-v30 · normal 1.0 |
| 최종 속도 | **0.9** (타입캐스트 tempo 0.85로 생성 → 음높이 유지한 채 5.9% 빠르게) |
| 음높이 | 0 |
| 말투 | 대화체. 문단마다 “자,”, “네,”, “아,”, “음,”, “그런데요,” 한두 개 |
| 음량 | −16 LUFS (유튜브 기준), 압축으로 문장 끝 처짐을 고르게 |

## 들어 있는 파일

| 파일 | 내용 |
|---|---|
| `preset.json` | 생성 설정. 스크립트가 그대로 읽는다 |
| `reference-1min.mp3` | **마스터 레퍼런스** (1분 5초). 훅·설명·메인 킥·펀치라인·루프·클로징 톤이 다 들어 있다 |
| `reference-1min.txt` | 위 레퍼런스의 대본 |
| `reference-full-episode01.mp3` | 긴 호흡 레퍼런스. 1화 전체 나레이션 v2 (11분 41초) |

## 새 회차 만들기

```
python scripts/typecast_narration.py docs/episode-02-recording.txt --preset library/voice/nyugwa-master/preset.json
```

- API 키는 환경 변수 `TYPECAST_API_KEY`에서 읽는다. 클라우드 환경에서는 저장된 키가 자동으로 붙으므로 `TYPECAST_API_KEY=proxy-injected`로 실행한다
- 결과: `outputs/<원고 이름>-민욱-master.wav`, `.mp3`
- 원고는 먼저 대화체로 다듬는다 (1화 예: `docs/episode-01-recording-v2.txt`)

## 지킬 것

- 이 목소리를 다른 서비스(Higgsfield, ElevenLabs 등)에 복제 등록하지 않는다. 타입캐스트 성우 목소리는 타입캐스트 안에서만 쓴다 (`docs/narrator-voice-master.md` 7-1장)
- 설정을 바꾸면 `preset.json`과 이 표를 함께 고치고, 레퍼런스도 새로 만든다
