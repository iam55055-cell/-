"""엔빵 로고 'N빵' 꼴을 SVG로 내보낸다. 심볼이 N 자리에 서고, 그 옆에 '빵'이 붙는다.

사용법:
    python3 scripts/enppang_logo_nppang.py library/brand/enppang/svg/nppang [태그라인용 TTF]
    node scripts/enppang_logo_png.js library/brand/enppang     # PNG 내보내기

- 대표안(PRIMARY)은 폴더 바로 아래에 둔다: 밝은 바탕, 어두운 바탕, 금색 바탕, 한 줄 설명을 붙인 로고
  (한 줄 설명에는 TTF가 필요하다).
- 심볼 후보 여섯 가지(쪼개진 동전 A, N + 0 변형 1 ~ 5)를 같은 방식으로 '빵' 옆에 놓은 것은 candidates/ 아래에 둔다.
- 대표안을 바꾸려면 PRIMARY만 바꿔서 다시 돌린다.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enppang_logo import INK, GOLD, PAPER, PAD, PPANG_BOX, ncoin, ppang, svg, tagline  # noqa: E402
import enppang_logo_n0 as n0  # noqa: E402

X0 = 5.5                                   # 로고의 왼쪽 끝
PP_L, TOP, PP_R, BOTTOM = PPANG_BOX        # '빵'의 획이 놓이는 범위
PRIMARY = 'a'                              # 대표안으로 내보낼 심볼

NAMES = {'a': ('a-split-coin', '쪼개진 동전')}
NAMES.update({key[0]: (key, name) for key, name, _ in n0.VARIANTS})

# 둥근 심볼은 '빵'보다 위아래로 조금 크게 놓아야 같은 키로 보인다
OVER = {'a': 1.5, '2': 1.5, '5': 1.5}
# 심볼과 '빵' 사이. 둥근 가장자리는 조금 더 붙인다
GAP = {'a': 11.5, '1': 13.5, '2': 11.5, '3': 9.5, '4': 11.5, '5': 11.5}


def symbol(key, mode):
    """심볼 그림과 그 범위 (왼쪽, 위, 오른쪽, 아래).

    mode: 'light'(밝은 바탕) | 'dark'(어두운 바탕) | 'gold'(금색 바탕)
    """
    coin = PAPER if mode == 'gold' else GOLD          # 금색 바탕에서는 동전을 종이색으로 바꾼다
    if key == 'a':
        r = 100
        frag = ncoin(0, 0, r, GOLD, pieces=True) if mode == 'dark' else ncoin(0, 0, r, coin, INK)
        return frag, (-r, -r, r, r)
    fn, box = n0.DRAW[key], n0.BOX[key]
    if key == '1':                                     # 한 가지 색으로 그린다
        return fn(None, GOLD if mode == 'dark' else INK, None), box
    if key in ('2', '3'):                              # 0은 동전색, N은 글자색
        if mode == 'dark':
            return fn(INK, GOLD, PAPER), box
        return fn(None, INK if (mode == 'gold' and key == '2') else coin, INK), box
    if key == '4':                                     # 밝은 바탕에서는 색을 뒤집지 않고 N을 통째로 잉크색으로
        return (fn(INK, GOLD, PAPER) if mode == 'dark' else n0.v4_flat(coin, INK)), box
    if key == '5':
        return (fn(INK, GOLD, PAPER) if mode == 'dark' else fn(None, coin, None, back=INK)), box
    raise KeyError(key)


def nppang(key, mode):
    """'N빵' 로고. 반환: (svg 조각, 폭). 높이는 '빵'과 같은 TOP ~ BOTTOM이다."""
    frag, (x0, y0, x1, y1) = symbol(key, mode)
    over = OVER.get(key, 0)
    s = (BOTTOM - TOP + 2 * over) / (y1 - y0)
    w = (x1 - x0) * s
    tx, ty = X0 - x0 * s, TOP - over - y0 * s
    ink = PAPER if mode == 'dark' else INK
    ox = X0 + w + GAP[key] - PP_L
    body = f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{frag}</g>' + ppang(ox, ink)
    return body, w + GAP[key] + (PP_R - PP_L)


def viewbox(width, extra=0.0):
    return (X0 - PAD, TOP - PAD, width + 2 * PAD, BOTTOM - TOP + extra + 2 * PAD)


def main(out, font=None):
    os.makedirs(os.path.join(out, 'candidates'), exist_ok=True)

    def write(name, body, vb, label):
        text = svg(1200, round(1200 * vb[3] / vb[2]), body, vb, label=label)
        open(os.path.join(out, name), 'w', encoding='utf-8').write(text)

    # ---------- 심볼 후보마다 한 벌씩: candidates/ 아래
    for key, (slug, name) in NAMES.items():
        for suffix, mode in (('', 'light'), ('-on-dark', 'dark')):
            body, width = nppang(key, mode)
            write(f'candidates/nppang-{slug}{suffix}.svg', body, viewbox(width), f'N빵 (심볼: {name})')

    # ---------- 대표안: 바탕색별 로고
    for suffix, mode in (('', 'light'), ('-on-dark', 'dark'), ('-on-gold', 'gold')):
        body, width = nppang(PRIMARY, mode)
        write(f'nppang{suffix}.svg', body, viewbox(width), 'N빵')

    # ---------- 대표안: 한 줄 설명을 붙인 로고
    if font:
        for suffix, mode in (('', 'light'), ('-on-dark', 'dark')):
            body, width = nppang(PRIMARY, mode)
            tg, cap = tagline('내 돈 나눠 먹는 사람들', width, PAPER if mode == 'dark' else INK, font)
            gapy = 13
            body += f'<g transform="translate({X0} {BOTTOM + gapy + cap:.2f})">{tg}</g>'
            write(f'lockup-nppang{suffix}.svg', body, viewbox(width, gapy + cap + 4), 'N빵 | 내 돈 나눠 먹는 사람들')
    print('written to', out)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'out-nppang', sys.argv[2] if len(sys.argv) > 2 else None)
