"""엔빵 심볼 'N + 0' 변형 다섯 가지를 SVG로 내보낸다.

N(엔)과 0(빵)을 한 그림으로 합치는 다섯 가지 방법이다. 모두 도형으로 직접 그린다.
둥근 모양인 2번과 5번은 워드마크의 ㅇ 자리에 넣은 모습도 함께 내보낸다.

사용법:
    python3 scripts/enppang_logo_n0.py library/brand/enppang/svg/n0
    node scripts/enppang_logo_png.js library/brand/enppang     # PNG 내보내기
"""
import math, os, sys

INK = '#17130E'
GOLD = '#FFC62B'
PAPER = '#FFF7E3'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out-n0'
os.makedirs(OUT, exist_ok=True)

C = 400  # 800×800 판의 가운데


def svg(body, bg, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" '
            f'role="img" aria-label="{label}"><rect width="800" height="800" fill="{bg}"/>'
            f'<g transform="translate({C} {C})">{body}</g></svg>\n')


def rrect(w, h, r):
    """가운데가 원점인 둥근 사각형의 path 조각."""
    x, y = -w / 2, -h / 2
    return (f'M{x + r:.2f},{y:.2f} H{x + w - r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + w:.2f},{y + r:.2f} '
            f'V{y + h - r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + w - r:.2f},{y + h:.2f} '
            f'H{x + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x:.2f},{y + h - r:.2f} '
            f'V{y + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + r:.2f},{y:.2f} Z')


def ellipse(rx, ry):
    return f'M{-rx:.2f},0 A{rx:.2f},{ry:.2f} 0 1 0 {rx:.2f},0 A{rx:.2f},{ry:.2f} 0 1 0 {-rx:.2f},0 Z'


def n_parts(w, h, t):
    """가운데가 원점인 N. 반환: (왼쪽 세로획, 오른쪽 세로획, 대각선) 꼭짓점 목록."""
    x, y = w / 2, h / 2
    left = [(-x, -y), (-x + t, -y), (-x + t, y), (-x, y)]
    right = [(x - t, -y), (x, -y), (x, y), (x - t, y)]
    diag = [(-x, -y), (-x + t, -y), (x, y), (x - t, y)]
    return left, right, diag


def poly(points):
    return 'M' + ' L'.join(f'{px:.2f},{py:.2f}' for px, py in points) + ' Z'


def arc(p, q, R):
    """원 위의 점 p에서 q까지 짧은 쪽 호."""
    sweep = 1 if p[0] * q[1] - p[1] * q[0] > 0 else 0
    return f'A{R:.2f},{R:.2f} 0 0 {sweep} {q[0]:.2f},{q[1]:.2f}'


def line_circle(p, q, R):
    """p→q 직선이 반지름 R인 원과 만나는 두 점 (p 쪽부터)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    a = dx * dx + dy * dy
    b = 2 * (p[0] * dx + p[1] * dy)
    c = p[0] ** 2 + p[1] ** 2 - R * R
    s = math.sqrt(b * b - 4 * a * c)
    t1, t2 = (-b - s) / (2 * a), (-b + s) / (2 * a)
    return (p[0] + t1 * dx, p[1] + t1 * dy), (p[0] + t2 * dx, p[1] + t2 * dy)


def band_in_circle(e1, e2, R):
    """평행한 두 변 e1, e2 사이의 띠가 원 안에 들어가는 부분."""
    a1, a2 = line_circle(e1[0], e1[1], R)
    b1, b2 = line_circle(e2[0], e2[1], R)
    return (f'M{a1[0]:.2f},{a1[1]:.2f} L{a2[0]:.2f},{a2[1]:.2f} {arc(a2, b2, R)} '
            f'L{b1[0]:.2f},{b1[1]:.2f} {arc(b1, a1, R)} Z')


def save(name, text):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(text)


# ------------------------------------------------------------------ 1. 빗금 친 0
def v1(bg, main, sub):
    """0의 양옆이 N의 세로획이 되고, 빗금이 N의 대각선이 된다."""
    w, h, t, r = 390, 520, 70, 122
    ring = rrect(w, h, r) + ' ' + rrect(w - 2 * t, h - 2 * t, r - t)
    xi, yi = w / 2 - t, h / 2 - t          # 안쪽 사각형의 반폭, 반높이
    c = r - t                               # 안쪽 모서리의 둥근 반지름. 빗금이 딱 여기서 벽과 만난다
    e = 24                                  # 고리 안으로 밀어 넣어 이음매를 없애는 여유
    diag = [(-xi - e, -yi - e), (-xi + c, -yi - e), (-xi + c, -yi), (xi, yi - c), (xi + e, yi - c),
            (xi + e, yi + e), (xi - c, yi + e), (xi - c, yi), (-xi, -yi + c), (-xi - e, -yi + c)]
    return f'<path fill="{main}" fill-rule="evenodd" d="{ring}"/><path fill="{main}" d="{poly(diag)}"/>'


# ------------------------------------------------------------------ 2. 0 속의 N
def v2(bg, main, sub):
    """세로로 긴 0 안에 N이 떠 있다."""
    rx, ry, t = 232, 292, 64
    ring = ellipse(rx, ry) + ' ' + ellipse(rx - t, ry - t)
    left, right, diag = n_parts(176, 270, 58)
    n = ' '.join(poly(p) for p in (left, right, diag))
    return f'<path fill="{main}" fill-rule="evenodd" d="{ring}"/><path fill="{sub}" d="{n}"/>'


# ------------------------------------------------------------------ 3. N 어깨 위의 0
def v3(bg, main, sub):
    """굵은 N의 오른쪽 어깨에 작은 0(동전)이 붙어 있다. 지수처럼 읽힌다."""
    w, h, t = 350, 430, 102
    ox, oy = -22, 28                         # N을 왼쪽 아래로 살짝 옮긴다
    left, right, diag = n_parts(w, h, t)
    n = ' '.join(poly([(px + ox, py + oy) for px, py in part]) for part in (left, right, diag))
    cx, cy, R, tr, halo = 164, -184, 96, 38, 24   # 테두리 여백이 세로획의 모서리까지 덮는 자리
    ring = ellipse(R, R) + ' ' + ellipse(R - tr, R - tr)
    return (f'<path fill="{sub}" d="{n}"/>'
            f'<g transform="translate({cx} {cy})"><circle r="{R + halo}" fill="{bg}"/>'
            f'<path fill="{main}" fill-rule="evenodd" d="{ring}"/></g>')


# ------------------------------------------------------------------ 4. 0을 뚫고 나온 N
def v4(bg, main, sub):
    """동전(0)보다 큰 N이 동전을 뚫고 지나간다. 동전 안쪽에서는 N이 바탕색으로 뒤집힌다."""
    R = 216
    w, h, t = 300, 548, 88
    left, right, diag = n_parts(w, h, t)
    n = ' '.join(poly(p) for p in (left, right, diag))
    x = w / 2
    ya, yb = math.sqrt(R * R - x * x), math.sqrt(R * R - (x - t) ** 2)
    # 세로획이 동전과 겹치는 부분
    lin = (f'M{-x:.2f},{-ya:.2f} {arc((-x, -ya), (-x + t, -yb), R)} V{yb:.2f} '
           f'{arc((-x + t, yb), (-x, ya), R)} Z')
    rin = (f'M{x - t:.2f},{-yb:.2f} {arc((x - t, -yb), (x, -ya), R)} V{ya:.2f} '
           f'{arc((x, ya), (x - t, yb), R)} Z')
    din = band_in_circle((diag[1], diag[2]), (diag[0], diag[3]), R)
    return (f'<path fill="{sub}" d="{n}"/><circle r="{R}" fill="{main}"/>'
            f'<path fill="{bg}" d="{lin} {rin} {din}"/>')


# ------------------------------------------------------------------ 5. N이 쪼갠 0
def v5(bg, main, sub, back=None):
    """N 모양으로 쪼개진 동전의 두 반쪽이 대각선을 따라 엇갈려 미끄러진다.

    back을 주면 두 반쪽 밑에 그 색을 깔아 N 자리를 채운다. 밝은 바탕에서 N이 보이게 할 때 쓴다.
    """
    R, stem, xoff = 270, 0.24, 0.42
    hw = stem * R / 2
    a_, b_ = xoff * R + hw, xoff * R - hw
    ya, yb = math.sqrt(R * R - a_ * a_), math.sqrt(R * R - b_ * b_)
    m = 2 * yb / (a_ + b_)
    y_r = -yb + m * 2 * b_
    y_l = -yb + m * 2 * hw
    A = f'A{R:.2f},{R:.2f} 0 0'
    # 대각선 방향 단위 벡터 (왼쪽 위 → 오른쪽 아래)
    n_ = math.hypot(a_ + b_, 2 * yb)
    ux, uy = (a_ + b_) / n_, 2 * yb / n_
    s_ = 46                                   # 미끄러진 거리
    lower = (ux * s_, uy * s_)                # 왼쪽 반쪽은 오른쪽 아래로
    upper = (-ux * s_, -uy * s_)              # 오른쪽 반쪽은 왼쪽 위로
    pieces = [
        (f'M{-a_:.2f},{-ya:.2f} {A} 0 {-a_:.2f},{ya:.2f} Z', lower),                           # 왼쪽 조각
        (f'M{-b_:.2f},{y_l:.2f} L{b_:.2f},{yb:.2f} {A} 1 {-b_:.2f},{yb:.2f} Z', lower),        # 가운데 아래 조각
        (f'M{a_:.2f},{-ya:.2f} {A} 1 {a_:.2f},{ya:.2f} Z', upper),                             # 오른쪽 조각
        (f'M{-b_:.2f},{-yb:.2f} {A} 1 {b_:.2f},{-yb:.2f} V{y_r:.2f} Z', upper),                # 가운데 위 조각
    ]
    under = ''
    if back:
        # 두 반쪽 밑에, 대각선 띠까지 품은 원 조각을 깐다. 띠는 두 조각이 겹쳐서 채운다
        rb = R - 3                                # 조각 가장자리 밖으로 번지지 않게 살짝 줄인다
        up = line_circle((-b_, -yb), (b_, y_r), rb)    # 대각선 띠의 위쪽 변
        lo = line_circle((-b_, y_l), (b_, yb), rb)     # 대각선 띠의 아래쪽 변
        for (p, q), (dx, dy), sweep in ((up, lower, 0), (lo, upper, 1)):
            under += (f'<path fill="{back}" transform="translate({dx:.2f} {dy:.2f})" '
                      f'd="M{p[0]:.2f},{p[1]:.2f} A{rb:.2f},{rb:.2f} 0 1 {sweep} {q[0]:.2f},{q[1]:.2f} Z"/>')
    return under + ''.join(f'<path fill="{main}" transform="translate({dx:.2f} {dy:.2f})" d="{d}"/>'
                           for d, (dx, dy) in pieces)


VARIANTS = [
    ('1-slashed-zero', '빗금 친 0', v1),
    ('2-n-inside-zero', '0 속의 N', v2),
    ('3-zero-on-shoulder', 'N 어깨 위의 0', v3),
    ('4-n-through-zero', '0을 뚫고 나온 N', v4),
    ('5-split-zero', 'N이 쪼갠 0', v5),
]

for key, name, fn in VARIANTS:
    save(f'n0-{key}.svg', svg(fn(INK, GOLD, PAPER), INK, f'엔빵 심볼 변형: {name}'))
    save(f'n0-{key}-on-gold.svg', svg(fn(GOLD, INK, PAPER), GOLD, f'엔빵 심볼 변형: {name} (금색 바탕)'))

# ------------------------------------------------------------------ 워드마크의 ㅇ 자리에 넣어 보기
# 둥근 모양인 2번과 5번만 '엔'의 ㅇ 자리에 들어간다. 1번은 ㅁ으로 읽히고, 3·4번은 ㅇ 모양이 아니다.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enppang_logo import letters, wordmark_viewbox, svg as wordmark_svg, O_SLOT  # noqa: E402


def in_slot(fragment, scale):
    cx, cy, _ = O_SLOT
    return f'<g transform="translate({cx} {cy}) scale({scale:.5f})">{fragment}</g>'


vb = wordmark_viewbox()
hgt = round(1200 * vb[3] / vb[2])
TRIALS = (
    # (번호, ㅇ 자리에 맞추는 배율, 밝은 바탕용 그림, 어두운 바탕용 그림)
    ('2', 50 / 584, v2(PAPER, GOLD, INK), v2(INK, GOLD, PAPER)),
    ('5', 25 / 316, v5(PAPER, GOLD, INK, back=INK), v5(INK, GOLD, PAPER)),
)
for key, scale, light, dark in TRIALS:
    save(f'wordmark-with-{key}.svg', wordmark_svg(1200, hgt, letters(o_glyph=in_slot(light, scale)), vb))
    save(f'wordmark-with-{key}-on-dark.svg',
         wordmark_svg(1200, hgt, letters(ink=PAPER, o_glyph=in_slot(dark, scale)), vb))
print('written to', OUT)
