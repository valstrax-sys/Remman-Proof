"""Algorithmes dont la correction ou la complexité reposait sur RH / GRH (Dirichlet),
et vérifications numériques des formules de comprendre/03-consequences-et-formules.md.

Python 3 pur, sans dépendance.
- Lancer : python rh_algos.py         (démonstration et contrôles numériques)
- Tests  : python rh_algos.py --test

Rappel : la preuve formelle (archive Lean d'Alpöge) établit RH et GRH pour les fonctions L
de Dirichlet. Les théorèmes « GRH ⇒ borne » utilisés ici (Bach 1990, Bach–Sorenson 1996,
Schoenfeld 1976, Robin 1984) proviennent de la littérature : ils ne sont pas formalisés dans
l'archive, sauf Robin et Lagarias (via kimihiro64/Robin1984, voir la page MIT).
"""
import math
import sys

EULER_GAMMA = 0.57721566490153286


# ---------------------------------------------------------------- Miller (Bach 1990)
def miller_bound(n: int) -> int:
    """Bach (1990) : sous GRH, si n est composé, il existe un témoin de Miller-Rabin a < 2 ln^2 n."""
    return min(n - 1, math.floor(2 * math.log(n) ** 2))


def _is_strong_probable_prime(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def is_prime_miller(n: int) -> bool:
    """Test de primalité DÉTERMINISTE en O(log^4 n) opérations binaires.

    Correct pour tout n dès que GRH (Dirichlet) est vraie (Miller 1976 ; borne explicite
    de Bach 1990). Seuls les caractères de Dirichlet modulo n interviennent : c'est la GRH
    prouvée par l'archive. Avant, ce test n'était qu'« un test correct sous GRH ».
    """
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    for a in range(2, miller_bound(n) + 1):
        if not _is_strong_probable_prime(n, a):
            return False
    return True


# ------------------------------------------------- non-résidus, racines carrées modulaires
def legendre(a: int, p: int) -> int:
    r = pow(a, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def least_nonresidue(p: int) -> int:
    """Plus petit non-résidu quadratique mod p (p premier impair).
    Sous GRH : < 2 ln^2 p (Ankeny 1952 ; Bach 1990), donc recherche en temps polynomial."""
    a = 2
    while legendre(a, p) != -1:
        a += 1
    return a


def sqrt_mod(a: int, p: int) -> int:
    """Racine carrée modulo p premier, DÉTERMINISTE (Tonelli–Shanks). Le non-résidu nécessaire
    est trouvé par recherche bornée par 2 ln^2 p : temps polynomial garanti par GRH."""
    a %= p
    if a == 0:
        return 0
    if p == 2:
        return a
    if legendre(a, p) != 1:
        raise ValueError("a n'est pas un carré modulo p")
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = least_nonresidue(p)
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def least_primitive_root(p: int) -> int:
    """Plus petit générateur de (Z/p)^*. Sous GRH : O(log^6 p) (Shoup 1992)."""
    phi, f, x = p - 1, [], p - 1
    d = 2
    while d * d <= x:
        if x % d == 0:
            f.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        f.append(x)
    g = 2
    while any(pow(g, phi // q, p) == 1 for q in f):
        g += 1
    return g


# ------------------------------------------------------------ crible et formules de comptage
def sieve(n: int) -> bytearray:
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i :: i] = bytearray(len(range(i * i, n + 1, i)))
    return s


def li(x: float) -> float:
    """Logarithme intégral li(x) = ∫_0^x dt/ln t (valeur principale), série de Ramanujan."""
    if x == 2:
        return 1.045163780117492784844588889194613136522615578151
    L = math.log(x)
    total, fact, term_sum, k = 0.0, 1.0, 0.0, 0
    for n in range(1, 200):
        fact *= n
        while k <= (n - 1) // 2:
            term_sum += 1.0 / (2 * k + 1)
            k += 1
        t = ((-1) ** (n - 1)) * L ** n / (fact * 2 ** (n - 1)) * term_sum
        total += t
        if abs(t) < 1e-17 * abs(total):
            break
    return EULER_GAMMA + math.log(L) + math.sqrt(x) * total


def schoenfeld_check(xs, s):
    """|π(x) − li(x)| < √x ln x / (8π) pour x ≥ 2657 (Schoenfeld 1976, sous RH ⇒ théorème)."""
    out, cnt, last = [], 0, 0
    for x in sorted(xs):
        cnt += sum(s[last + 1 : x + 1])
        last = x
        err = abs(cnt - li(x))
        bound = math.sqrt(x) * math.log(x) / (8 * math.pi)
        out.append((x, cnt, li(x), err, bound, err < bound))
    return out


def sigma_table(n: int):
    sig = [0] * (n + 1)
    for d in range(1, n + 1):
        for m in range(d, n + 1, d):
            sig[m] += d
    return sig


def robin_check(n_max: int):
    """Robin (1984) : RH ⇔ σ(n) < e^γ n ln ln n pour tout n > 5040. Renvoie le pire rapport."""
    sig = sigma_table(n_max)
    worst = max(range(5041, n_max + 1), key=lambda n: sig[n] / (n * math.log(math.log(n))))
    ratio = sig[worst] / (worst * math.log(math.log(worst)))
    return worst, ratio, math.exp(EULER_GAMMA), ratio < math.exp(EULER_GAMMA)


def lagarias_check(n_max: int):
    """Lagarias (2002) : RH ⇔ σ(n) ≤ H_n + exp(H_n) ln(H_n) pour tout n ≥ 1."""
    sig = sigma_table(n_max)
    H = 0.0
    for n in range(1, n_max + 1):
        H += 1.0 / n
        if sig[n] > H + math.exp(H) * math.log(H) + 1e-9:
            return n
    return None


def least_prime_in_ap(a: int, q: int, s) -> int:
    """Plus petit premier p ≡ a (mod q). Sous GRH : p < 2 (q ln q)^2 (Bach–Sorenson 1996)."""
    p = a if a > 1 else a + q
    while not s[p]:
        p += q
    return p


# ------------------------------------------------------------------------------ démonstration
def demo():
    print("== Primalité déterministe (Miller, borne de Bach 2 ln² n) ==")
    for n in (561, 2_147_483_647, 1_000_000_007 * 998_244_353, 2**89 - 1, 2**127 - 1):
        print(f"  n = {n}  bases ≤ {miller_bound(n)}  premier ? {is_prime_miller(n)}")

    print("\n== Racine carrée modulaire déterministe ==")
    p = 10**9 + 7
    r = sqrt_mod(2, p)
    print(f"  sqrt(2) mod {p} = {r}  (vérif : {r * r % p})  non-résidu utilisé : {least_nonresidue(p)}"
          f" (borne 2 ln² p = {2 * math.log(p) ** 2:.1f})")

    N = 10**7
    s = sieve(N)
    print("\n== Écart π(x) − li(x) et borne de Schoenfeld ==")
    for x, c, l, e, b, ok in schoenfeld_check([10**4, 10**5, 10**6, 10**7], s):
        print(f"  x = {x:>9}  π = {c:>7}  li = {l:12.1f}  |écart| = {e:8.1f}  borne = {b:9.1f}  {'OK' if ok else 'VIOLÉE'}")

    print("\n== Robin : σ(n) < e^γ n ln ln n (n > 5040) ==")
    w, ratio, eg, ok = robin_check(200_000)
    print(f"  jusqu'à 2·10^5 : pire n = {w}, σ(n)/(n ln ln n) = {ratio:.5f} < e^γ = {eg:.5f} : {ok}")
    print(f"  Lagarias jusqu'à 2·10^5 : premier contre-exemple = {lagarias_check(200_000)}")

    print("\n== Plus petit premier en progression arithmétique (borne 2(q ln q)²) ==")
    for q in (101, 1009, 9973):
        worst = max(least_prime_in_ap(a, q, s) for a in range(1, q) if math.gcd(a, q) == 1)
        print(f"  q = {q:>5}  max_a p_min(a, q) = {worst:>8}  borne = {2 * (q * math.log(q)) ** 2:12.0f}")


def tests():
    s = sieve(200_000)
    for n in range(2, 200_000):
        assert is_prime_miller(n) == bool(s[n]), n
    for n in (3215031751, 2152302898747, 3474749660383, 341550071728321):  # pseudo-premiers forts
        assert not is_prime_miller(n)
    for p in (3, 7, 13, 10007, 999983):
        assert least_nonresidue(p) < 2 * math.log(p) ** 2 or p < 10
        for a in range(1, 60):
            if legendre(a, p) == 1:
                r = sqrt_mod(a, p)
                assert r * r % p == a % p
    assert least_primitive_root(10**9 + 7) == 5
    assert all(ok for *_, ok in schoenfeld_check([2657, 10**4, 10**5], s))
    assert robin_check(50_000)[3]
    assert lagarias_check(50_000) is None
    assert abs(li(10**6) - 78627.5491594622) < 1e-6
    print("tous les tests passent")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tests() if "--test" in sys.argv else demo()
