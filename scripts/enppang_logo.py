"""엔빵 로고 생성기. 글자와 심볼을 도형으로 그려 SVG로 내보낸다.

사용법:
    python3 scripts/enppang_logo.py library/brand/enppang/svg [태그라인용 TTF]

- '엔빵' 글자와 심볼은 모두 도형이라 글꼴이 필요 없다.
- 태그라인("내 돈 나눠 먹는 사람들")만 글꼴 윤곽선을 따서 넣는다. TTF 경로를 주지 않으면
  태그라인이 붙은 로고(lockup)는 만들지 않는다. 2026-11-22 시안은 Noto Sans KR Bold
  (SIL Open Font License)로 만들었다. fonttools가 필요하다 (pip install fonttools).
- PNG는 scripts/enppang_logo_png.js로 내보낸다.
- 'N + 0' 변형 심볼은 scripts/enppang_logo_n0.py가 이 파일의 글자 도형을 가져다 쓴다.
"""
import math, os, sys

INK = '#17130E'      # 잉크 (글자, 어두운 바탕)
GOLD = '#FFC62B'     # 동전
PAPER = '#FFF7E3'    # 영수증 종이 (밝은 바탕)

LW = 193.0           # 글자 전체 폭 (왼쪽 5.5 ~ 오른쪽 198.5 사이)
X0, PAD = 5.5, 12.0
O_SLOT = (29.5, 40.0, 24.0)   # '엔'의 ㅇ 자리: 가운데 x, y, 반지름


def rect(x, y, w, h, fill, r=1.6):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}"/>'


def ncoin(cx, cy, R, coin=GOLD, cut=INK, stem=0.27, xoff=0.43, pieces=False):
    """N 모양으로 쪼개진 동전. stem: 획 굵기(R 대비), xoff: 세로획 중심 위치(R 대비).

    pieces=False: 동전 위에 N을 cut 색으로 그린다 (밝은 바탕용).
    pieces=True : 동전 조각 네 개만 그린다. N 자리는 비어서 바탕이 보인다 (어두운 바탕용).
    잘라내기 마스크를 쓰지 않고 모양을 그대로 그린다.
    """
    hw = stem * R / 2
    a_, b_ = xoff * R + hw, xoff * R - hw          # 세로획의 바깥쪽·안쪽 x (절댓값)
    ya, yb = math.sqrt(R * R - a_ * a_), math.sqrt(R * R - b_ * b_)
    m = 2 * yb / (a_ + b_)                          # 대각선 기울기
    y_r = -yb + m * 2 * b_                          # 대각선 위쪽 변이 오른쪽 세로획에 닿는 높이
    y_l = -yb + m * 2 * hw                          # 대각선 아래쪽 변이 왼쪽 세로획에서 시작하는 높이
    A = f'A{R:.3f},{R:.3f} 0 0'
    g = f'<g transform="translate({cx:.2f} {cy:.2f})">'
    if pieces:
        d = (f'M{-a_:.3f},{-ya:.3f} {A} 0 {-a_:.3f},{ya:.3f} Z '                      # 왼쪽 조각
             f'M{a_:.3f},{-ya:.3f} {A} 1 {a_:.3f},{ya:.3f} Z '                         # 오른쪽 조각
             f'M{-b_:.3f},{-yb:.3f} {A} 1 {b_:.3f},{-yb:.3f} V{y_r:.3f} Z '            # 가운데 위 조각
             f'M{-b_:.3f},{y_l:.3f} L{b_:.3f},{yb:.3f} {A} 1 {-b_:.3f},{yb:.3f} Z')    # 가운데 아래 조각
        return g + f'<path fill="{coin}" d="{d}"/></g>'
    left = f'M{-a_:.3f},{-ya:.3f} {A} 1 {-b_:.3f},{-yb:.3f} V{yb:.3f} {A} 1 {-a_:.3f},{ya:.3f} Z'
    right = f'M{b_:.3f},{-yb:.3f} {A} 1 {a_:.3f},{-ya:.3f} V{ya:.3f} {A} 1 {b_:.3f},{yb:.3f} Z'
    diag = f'M{-b_:.3f},{-yb:.3f} L{b_:.3f},{y_r:.3f} V{yb:.3f} L{-b_:.3f},{y_l:.3f} Z'
    return g + f'<circle r="{R:.2f}" fill="{coin}"/><path fill="{cut}" d="{left} {right} {diag}"/></g>'


def letters(ink=INK, coin=GOLD, cut=INK, pieces=False, o_glyph=None):
    """'엔빵' 글자. 음절 하나가 100×100 칸이고 두 음절을 붙여 그린다.

    o_glyph: '엔'의 ㅇ 자리에 넣을 SVG 조각. 주지 않으면 N 동전을 넣는다.
    """
    s = []
    # ---- 엔: 초성 ㅇ 자리에 N 동전
    ox = 0
    cx, cy, R = O_SLOT
    s.append(o_glyph if o_glyph is not None else ncoin(ox + cx, cy, R, coin, cut, pieces=pieces))
    s.append(rect(ox + 55, 33.75, 7, 12.5, ink))       # ㅓ의 가로 삐침
    s.append(rect(ox + 60, 10, 14, 64, ink))          # ㅓ 세로획
    s.append(rect(ox + 79, 7, 14, 71, ink))           # ㅣ
    s.append(rect(ox + 22, 70, 14, 28, ink))          # ㄴ 세로
    s.append(rect(ox + 22, 84, 71, 14, ink))          # ㄴ 가로
    # ---- 빵
    ox = 100.5
    for bx in (6, 36):                                # ㅂ 두 개
        s.append(rect(ox + bx, 12, 9.5, 44, ink))
        s.append(rect(ox + bx + 16.5, 12, 9.5, 44, ink))
        s.append(rect(ox + bx, 28, 26, 8.5, ink))
        s.append(rect(ox + bx, 47, 26, 9, ink))
    s.append(rect(ox + 68, 7, 14, 56, ink))           # ㅏ 세로획
    s.append(rect(ox + 80, 28, 13, 12.5, ink))        # ㅏ 가로 삐침
    # 받침 ㅇ: 굵은 타원 고리
    s.append(f'<path fill="{ink}" fill-rule="evenodd" d="'
             f'M{ox + 17.5:.2f},81.2 a32,16.8 0 1,0 64,0 a32,16.8 0 1,0 -64,0 Z '
             f'M{ox + 33:.2f},81.2 a16.5,6.2 0 1,0 33,0 a16.5,6.2 0 1,0 -33,0 Z"/>')
    return ''.join(s)


def wordmark_viewbox():
    return (X0 - PAD, 7 - PAD, LW + 2 * PAD, 91 + 2 * PAD)


def svg(w, h, body, vb, bg=None, label='엔빵'):
    x, y, vw, vh = vb
    back = f'<rect x="{x}" y="{y}" width="{vw}" height="{vh}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x} {y} {vw} {vh}" '
            f'role="img" aria-label="{label}">{back}{body}</svg>\n')


def tagline(text, width, fill, font, tracking=0.06):
    """text를 글꼴 윤곽선으로 그려 폭 width에 맞춘다. 반환: (svg 조각, 글자 높이)."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = TTFont(font)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm
    x = 0
    parts = []
    for ch in text:
        g = cmap[ord(ch)]
        adv = gs[g].width
        if ch != ' ':
            pen = SVGPathPen(gs)
            gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
            parts.append(pen.getCommands())
        x += adv + tracking * upm
    total = x - tracking * upm
    sc = width / total
    cap = 0.78 * upm * sc
    d = ' '.join(parts)
    return f'<g transform="scale({sc:.5f})"><path d="{d}" fill="{fill}"/></g>', cap


def receipt(cx, cy, w, h, teeth=6, fill=PAPER, r=20):
    x0, y0 = cx - w / 2, cy - h / 2
    tw = w / teeth
    th = tw * 0.55
    d = f'M{x0:.1f},{y0 + r:.1f} a{r},{r} 0 0 1 {r},-{r} h{w - 2 * r:.1f} a{r},{r} 0 0 1 {r},{r} V{y0 + h:.1f} '
    for i in range(teeth):
        d += f'l{-tw / 2:.2f},{-th:.2f} l{-tw / 2:.2f},{th:.2f} '
    d += 'Z'
    return f'<path d="{d}" fill="{fill}"/>'


def nglyph(cx, cy, w, h, t, fill=INK):
    x0, y0 = cx - w / 2, cy - h / 2
    return (f'<g fill="{fill}"><rect x="{x0:.1f}" y="{y0:.1f}" width="{t}" height="{h}"/>'
            f'<rect x="{x0 + w - t:.1f}" y="{y0:.1f}" width="{t}" height="{h}"/>'
            f'<polygon points="{x0:.1f},{y0:.1f} {x0 + t:.1f},{y0:.1f} {x0 + w:.1f},{y0 + h:.1f} {x0 + w - t:.1f},{y0 + h:.1f}"/></g>')


def main(out, font=None):
    os.makedirs(out, exist_ok=True)

    def save(name, text):
        open(os.path.join(out, name), 'w', encoding='utf-8').write(text)

    # ---------- 워드마크
    vb = wordmark_viewbox()
    ratio = vb[3] / vb[2]
    save('wordmark.svg', svg(1200, round(1200 * ratio), letters(), vb))
    save('wordmark-on-dark.svg', svg(1200, round(1200 * ratio), letters(ink=PAPER, pieces=True), vb))
    # 금색 바탕에서는 동전이 묻히므로 동전을 종이색으로 바꾼다
    save('wordmark-on-gold.svg', svg(1200, round(1200 * ratio), letters(coin=PAPER), vb))

    # ---------- 태그라인 붙인 로고
    if font:
        for name, ink in (('lockup.svg', INK), ('lockup-on-dark.svg', PAPER)):
            tg, cap = tagline('내 돈 나눠 먹는 사람들', LW, ink, font)
            gapy = 13
            body = (letters(ink=ink, pieces=(ink == PAPER))
                    + f'<g transform="translate({X0} {98 + gapy + cap:.2f})">{tg}</g>')
            vb2 = (X0 - PAD, 7 - PAD, LW + 2 * PAD, 91 + gapy + cap + 4 + 2 * PAD)
            save(name, svg(1200, round(1200 * vb2[3] / vb2[2]), body, vb2, label='엔빵 | 내 돈 나눠 먹는 사람들'))

    # ---------- 심볼 A: N으로 쪼개진 동전
    save('symbol.svg', svg(800, 800, ncoin(400, 400, 328, pieces=True), (0, 0, 800, 800), bg=INK, label='엔빵 심볼'))
    save('symbol-coin-only.svg', svg(800, 800, ncoin(400, 400, 390), (0, 0, 800, 800), label='엔빵 심볼'))

    # ---------- 심볼 B: 영수증 위의 N
    b = receipt(400, 408, 350, 480)
    b += nglyph(400, 322, 214, 214, 56)
    b += f'<rect x="293" y="478" width="214" height="28" rx="4" fill="{INK}"/>'
    b += f'<rect x="293" y="530" width="132" height="28" rx="4" fill="{INK}"/>'
    save('symbol-alt-receipt.svg', svg(800, 800, b, (0, 0, 800, 800), bg=GOLD, label='엔빵 심볼 (영수증)'))

    # ---------- 심볼 C: 글자 심볼
    sc = 2.6
    body_c = letters(ink=INK, coin=PAPER, cut=INK)
    tx = 400 - (X0 + LW / 2) * sc
    ty = 400 - 52.5 * sc
    save('symbol-alt-letters.svg', svg(800, 800, f'<g transform="translate({tx:.1f} {ty:.1f}) scale({sc})">{body_c}</g>',
                                       (0, 0, 800, 800), bg=GOLD, label='엔빵 심볼 (글자)'))
    print('written to', out)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'out', sys.argv[2] if len(sys.argv) > 2 else None)
