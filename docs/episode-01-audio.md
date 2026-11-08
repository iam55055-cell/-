# 뉴과 1화 음원

## 🎙️ 최종본: 타입캐스트 · 민욱

### v2 (2026-11-08) — 현재 최종

- 파일: `outputs/episode-01-recording-v2-민욱-master.mp3` (12분 22초)
- 원고: `docs/episode-01-recording-v2.txt` (대화체. 내용·숫자는 v1 원고와 같고, “자,”, “네,”, “아,”, “음,” 같은 말 붙임 36곳을 넣었다)
- 설정: 민욱(`tc_68f0727fd62a5934102f7ec0`), ssfm-v30, normal, **속도 0.85**
- 음량 보정: 문장 끝이 작아지거나 소리가 잠깐 줄어드는 부분을 압축으로 고르게 하고 −16 LUFS로 맞췄다

| 측정 | 보정 전 | 보정 후 |
|---|---|---|
| 전체 음량 | −23.2 LUFS | −16.0 LUFS (유튜브 기준) |
| 음량 변화 폭 (LRA) | 4.2 LU | 2.1 LU |
| 말하는 구간 0.4초 단위 음량 차이 (10~90%) | 9.1 dB | 5.8 dB |
| 최고 레벨 | −3.9 dBFS | −1.5 dBFS |

### v1 (2026-11-08)

- `outputs/episode-01-recording-민욱.mp3` (10분 14초). 원고 v1, 속도 1.0, 음량 보정 없음
- 피드백: 속도가 빠르다, 대화하듯 자연스럽게, 중간에 음량이 잠깐씩 줄어든다 → v2에서 반영

### 다시 만드는 법

```
python scripts/typecast_narration.py docs/episode-01-recording-v2.txt --tempo 0.85
```

- API 키는 환경 변수 `TYPECAST_API_KEY`로 읽는다. 이 클라우드 환경에서는 저장된 네트워크 시크릿이 자동으로 붙으므로 `TYPECAST_API_KEY=proxy-injected`로 실행한다
- 한 번에 600자씩 보낸다 (2,000자를 보내면 서버가 502를 냈다). 모든 구간을 같은 목소리·모델·감정·속도로 생성한다
- 구간은 설정별 폴더(`outputs/<이름>_parts/<설정>/`)에 저장해서, 설정을 바꾸면 새로 만들고 같으면 건너뛴다

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--tempo` | 1.0 | 속도. 뉴과 기준은 0.85 |
| `--emotion` | normal | normal, happy, sad, angry, whisper, toneup, tonedown |
| `--intensity` | 1.0 | 감정 세기 0~2 |
| `--gap` | 0.6 | 구간 사이 쉼(초) |
| `--max-chars` | 600 | 한 번에 보내는 글자 수 |
| `--lufs` | −16 | 음량 보정 목표 |
| `--no-master` | — | 음량 보정 안 함 |
| `--dry-run` | — | API를 부르지 않고 구간 나누기만 확인 |

---

# 가이드 음원 (마커스, 임시)

## ✅ 전체 한 파일 (v2, 2026-11-08) — 이 파일을 쓴다

| 항목 | 값 |
|---|---|
| 들어보기 | [전체 듣기 (11분 5초)](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261108_035942_f95136f6-8b14-4bd7-9b92-c5f6adb4d0a1.mp3) |
| 목소리 | Marcus |
| 엔진 | Higgsfield Text to Speech V2 · seed_speech |
| 원고 | `docs/episode-01-recording.txt` 전체를 한 번에 생성 (공백 포함 5,118자) |
| 속도 | 공백 제외 3,879자 ÷ 665초 ≈ 분당 약 350자 |

v1(아래 12개 구간)은 구간마다 따로 생성해서 목소리 톤과 빠르기가 구간마다 달랐다. v2는 원고 전체를 한 번에 생성해서 처음부터 끝까지 같은 목소리, 같은 빠르기다.

한 번에 생성할 수 있는 길이: ElevenLabs 5,000자, minimax 10,000자, seed_speech 15,000자 (Higgsfield 기준). 앞으로 원고가 5,000자를 넘으면 seed_speech나 minimax로 한 번에 만든다.

**가이드 음원입니다. 최종 목소리가 아닙니다.** 최종 나레이터는 타입캐스트 · 민욱이다.

---

## v1 · 12개 구간 (참고용, 쓰지 않음)

> **가이드 음원입니다. 최종 목소리가 아닙니다.** 최종 나레이터는 타입캐스트 · 민욱이다. 타입캐스트 API 키가 인증에 실패해서, 편집 타이밍을 먼저 잡을 수 있도록 Higgsfield Seed Audio · Marcus로 만들었다.
> 생성일 2026-11-07 · 설정: 속도 −30, 높이 −1, mp3 44.1kHz · 원고: `docs/episode-01-recording.txt`

## 구간별 파일

| 파일 | 내용 | 시작 | 길이 | 분당 글자 수 | 들어보기 |
|---|---|---|---|---|---|
| 01 | 훅 | 0:00 | 30.1초 | 약 295자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_3dfd72b3-0adf-470f-834b-8450f04e38e9.mp3) |
| 02 | 질문 | 0:30 | 50.4초 | 약 151자 ⚠️ | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_381d429a-ad4d-4fe3-bb4e-f02fb6f92a96.mp3) |
| 03a | 외교관 가방 · 39호실 | 1:20 | 80.0초 | 약 316자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_2f7cf239-6331-48eb-8c4f-920f63261b0a.mp3) |
| 03b | 슈퍼노트 | 2:40 | 55.3초 | 약 304자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_d8a48487-b85e-47b9-aac6-a269661ccf54.mp3) |
| 03c | 마카오 은행 | 3:35 | 90.1초 | 약 335자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_91b446c5-a8d6-4e44-98cd-da3248c0d935.mp3) |
| 04a | 메인 킥: 해커와 평양 | 5:05 | 96.4초 | 약 227자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_fef54692-7fec-4540-8e79-7cce5f308ffd.mp3) |
| 04b | 해커 선발 · 수출산업 | 6:42 | 90.8초 | 약 254자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_24eec1f3-1f8a-40a5-b4c5-34d419ca9bf6.mp3) |
| 05a | 방글라데시 · 오타 | 8:13 | 65.1초 | 약 383자 ⚠️ | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_af253ffc-d6fe-4976-85fe-74d7a1dbd270.mp3) |
| 05b | 코인으로 · 질문의 답 | 9:18 | 75.7초 | 약 280자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_9addf456-072c-4ca8-beed-a820a0554fc5.mp3) |
| 06a | FBI 발표 이후 | 10:34 | 82.2초 | 약 237자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_3f4a1f3e-ff3e-4db7-b3f6-a41ed7a4ba67.mp3) |
| 06b | 업비트 · 같은 사건 다른 말 | 11:56 | 57.7초 | 약 297자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_067e5832-fb19-4dbf-95f9-6ff70283edf8.mp3) |
| 07 | 다음에 볼 것 · 클로징 | 12:54 | 64.0초 | 약 253자 | [재생](https://d8j0ntlcm91z4.cloudfront.net/user_3JY9ZSD8BKesC6br9SUbmuhz1DW/hf_20261107_090142_ac491878-63d2-459a-9c66-576f187b1127.mp3) |

**전체 낭독 길이: 약 13:57** (구간 사이 쉼과 화면 연출 제외)

⚠️ 표시는 분당 글자 수가 기준(약 330자)에서 크게 벗어난 구간이다. 지나치게 느리면 긴 무음이 끼었을 수 있고, 지나치게 빠르면 문장을 건너뛰었을 수 있다. 편집 전에 그 구간만 처음부터 끝까지 들어 본다. 다른 구간도 같은 설정인데 빠르기가 들쭉날쭉하다. Seed Audio가 생성할 때마다 쉼을 다르게 넣기 때문이다.

## 편집할 때

1. 파일 01부터 12까지 순서대로 타임라인에 붙인다
2. 구간 사이(02→03a, 03c→04a, 04b→05a, 05b→06a, 06b→07)에는 1.5초 쉼을 넣고 화면 전환을 건다
3. 나레이터 문서 2-3장의 후반 효과를 전체에 입힌다. 01의 “기록을 불러옵니다”에는 효과를 더 세게 건다
4. 민욱 녹음이 준비되면 같은 구간 단위로 교체한다. 타이밍은 이 가이드를 기준으로 맞춘다
