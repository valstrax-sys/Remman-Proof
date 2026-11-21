# 3. Conséquences : les formules qui deviennent des théorèmes

Des milliers de résultats ont été démontrés **« sous RH »** ou **« sous GRH »** depuis 1900. Avec les énoncés de [01](01-ce-qui-est-prouve.md), ceux qui ne dépendent que de $\zeta$ et des fonctions L de Dirichlet deviennent **inconditionnels**.

Trois mises en garde :

- **La preuve formelle couvre RH et GRH de Dirichlet, pas leurs conséquences.** Que « RH ⇒ X » soit vrai est un fait de la littérature, sauf quand il est lui aussi formalisé ; voir l'exemple Robin ci-dessous.
- **Pour chaque conséquence, il faut vérifier quelle version de RH elle utilise.** On distingue $\zeta$, Dirichlet, ou une fonction de Dedekind non abélienne, qui n'est pas couverte (ERH).
- **Les constantes explicites citées sont celles des articles d'origine.**

## 3.1 Nombres premiers : le terme d'erreur optimal

Notations : $\pi(x)$ est le nombre de premiers $\le x$, $\operatorname{li}(x) = \int_2^x dt/\log t$ et $\psi(x) = \sum_{n \le x}\Lambda(n)$.

| Énoncé, maintenant inconditionnel | Source | Utilise |
|---|---|---|
| $\pi(x) = \operatorname{li}(x) + O(\sqrt x \log x)$, et c'est **équivalent** à RH | von Koch (1901) | $\zeta$ |
| $\lvert\pi(x) - \operatorname{li}(x)\rvert < \dfrac{\sqrt x \log x}{8\pi}$ pour $x \ge 2657$ | Schoenfeld (1976) | $\zeta$ |
| $\lvert\psi(x) - x\rvert < \dfrac{\sqrt x \log^2 x}{8\pi}$ pour $x \ge 73{,}2$ | Schoenfeld (1976) | $\zeta$ |
| Écart entre premiers consécutifs : $p_{n+1} - p_n = O(\sqrt{p_n}\log p_n)$ | Cramér (1920) | $\zeta$ |
| Il y a un premier entre $x - c\sqrt x\log x$ et $x$ pour $x$ assez grand ; version explicite : un premier dans $\bigl(x - \tfrac{4}{\pi}\sqrt x \log x,\ x\bigr]$ pour $x \ge 2$ | Dudek (2015) | $\zeta$ |
| $M(x) = \sum_{n\le x}\mu(n) = O(x^{1/2+\varepsilon})$ pour tout $\varepsilon > 0$, et c'est **équivalent** à RH | Littlewood (1912) | $\zeta$ |
| Hypothèse de Lindelöf : $\zeta(\tfrac12 + it) = O(\lvert t\rvert^{\varepsilon})$ | conséquence classique de RH | $\zeta$ |

**Lecture intuitive.** Les premiers sont « aussi bien répartis que possible ». Jusqu'à $x$, l'écart à la prédiction $\operatorname{li}(x)$ ne dépasse pas l'ordre de $\sqrt x$, à des logarithmes près. C'est le même ordre que l'écart d'une marche aléatoire de $x$ pas.

## 3.2 Critères arithmétiques élémentaires équivalents à RH

Ces énoncés ne parlent que d'entiers. Ils sont **équivalents** à RH, donc maintenant prouvés.

- **Robin (1984).** Pour tout $n > 5040$ :
  $$\sigma(n) < e^{\gamma}\, n \log\log n,$$
  où $\sigma(n)$ est la somme des diviseurs de $n$ et $\gamma \approx 0{,}5772$ la constante d'Euler.
- **Lagarias (2002).** Pour tout $n \ge 1$, avec $H_n = 1 + \tfrac12 + \dots + \tfrac1n$ :
  $$\sigma(n) \le H_n + e^{H_n}\log H_n .$$
- **Nicolas (1983).** Pour tout primoriel $N_k = 2 \cdot 3 \cdot 5 \cdots p_k$, on a $\dfrac{N_k}{\varphi(N_k)} > e^\gamma \log\log N_k$.
- **Critère de Riesz, critère de Báez-Duarte, positivité de Li** ($\lambda_n \ge 0$ pour tout $n$) : mêmes remarques.

> **Exemple d'« utilisation de la preuve » déjà réalisé.** La page du MIT combine l'archive avec le projet Lean `kimihiro64/Robin1984` (commit `acab1a3`). Elle obtient ainsi des **théorèmes Lean** `robin_inequality` et `lagarias_inequality`, eux aussi vérifiés par des noyaux indépendants. C'est le modèle à suivre pour dériver des conséquences de façon certifiée (voir [05](05-utiliser-la-preuve-en-lean.md)).

## 3.3 Progressions arithmétiques (GRH de Dirichlet)

Notation : $\pi(x;q,a)$ est le nombre de premiers $p \le x$ avec $p \equiv a \pmod q$, pour $\gcd(a,q) = 1$.

| Énoncé, maintenant inconditionnel | Source |
|---|---|
| $\pi(x;q,a) = \dfrac{\operatorname{li}(x)}{\varphi(q)} + O\bigl(\sqrt x \log(qx)\bigr)$, uniformément en $q$ | classique, sous GRH |
| Le plus petit premier $\equiv a \pmod q$ est $< 2(q\log q)^2$ | Bach–Sorenson (1996) |
| Le plus petit non-résidu quadratique modulo $p$ est $< 2\log^2 p$ | Ankeny (1952), forme explicite de Bach (1990) |
| Pour tout sous-groupe propre $G \subsetneq (\mathbb{Z}/n\mathbb{Z})^\times$, il existe $x \notin G$ avec $x < 2\log^2 n$ | Bach (1990) |
| $L(1,\chi) \asymp$ entre $1/\log\log q$ et $\log\log q$, pour $\chi$ réel non principal | Littlewood (1928) |
| Racine primitive : le plus petit générateur de $(\mathbb{Z}/p)^\times$ est $O\bigl((\log p)^{6}\bigr)$ | Shoup (1992) |

## 3.4 Corps quadratiques et nombres de classes

Pour $K = \mathbb{Q}(\sqrt d)$, on a $\zeta_K(s) = \zeta(s)L(s,\chi_d)$. La GRH de Dedekind pour $K$ est donc **couverte**. De même pour tout corps abélien (cyclotomique, etc.).

- **Bach (1990).** Le groupe des classes de $K$ est engendré par les idéaux premiers de norme $\le 12\log^2|\Delta_K|$. La constante vaut $6$ pour un corps quadratique.

  Cela **certifie** le résultat des algorithmes de calcul du groupe des classes et du régulateur, comme celui de Buchmann sous-exponentiel ou celui de Hafner–McCurley, pour les **corps quadratiques et abéliens**. Jusqu'ici, leur sortie n'était garantie que « sous GRH ».
- **Bornes de Littlewood.** $h(-d) \ll \sqrt d \log\log d$ et $h(-d) \gg \sqrt d/\log\log d$.
- **Pas couvert :** corps de degré $\ge 3$ non abéliens, par exemple les corps cubiques non galoisiens. Pour eux, les résultats « sous GRH » le restent.

## 3.5 Ce qui **n'en découle pas**

- **Conjecture d'Artin sur les racines primitives** (Hooley, 1967) : elle demande GRH pour les corps de Kummer $\mathbb{Q}(\zeta_n, a^{1/n})$, qui ne sont pas abéliens. Elle n'est **pas couverte** par Dirichlet seul.
- **Chebotarev effectif** pour des extensions non abéliennes (Lagarias–Odlyzko sous GRH) : **pas couvert**.
- **Conjecture de Birch et Swinnerton-Dyer, rangs de courbes elliptiques** : elles concernent d'autres fonctions L, donc **pas couvert**.
- **Goldbach ternaire** : déjà démontré sans RH (Helfgott, 2013). **Goldbach binaire** : RH ne suffit pas, et le problème reste ouvert.
- **Cryptographie (RSA, courbes elliptiques)** : **aucune faiblesse nouvelle**. RH ne donne pas d'algorithme de factorisation. Elle *garantit* le comportement de certains algorithmes (voir [04](04-algorithmes.md)).

## 3.6 Résumé des formules clés

$$
\begin{aligned}
&\textbf{RH :} && \zeta(s)=0,\ 0<\operatorname{Re}s<1 \ \Rightarrow\ \operatorname{Re}s=\tfrac12\\
&\textbf{GRH (Dirichlet) :} && L(s,\chi)=0,\ 0<\operatorname{Re}s<1 \ \Rightarrow\ \operatorname{Re}s=\tfrac12\\
&\textbf{Premiers :} && |\pi(x)-\operatorname{li}x| < \tfrac{1}{8\pi}\sqrt x\log x \quad (x\ge 2657)\\
&\textbf{Progressions :} && \pi(x;q,a)=\tfrac{\operatorname{li}x}{\varphi(q)}+O(\sqrt x\log qx)\\
&\textbf{Robin :} && \sigma(n)<e^\gamma n\log\log n \quad (n>5040)\\
&\textbf{Bach :} && \exists\, x<2\log^2 n,\ x\notin G \quad (G\subsetneq(\mathbb Z/n)^\times)\\
&\textbf{Plus petit premier} \equiv a\ (q) : && p<2(q\log q)^2
\end{aligned}
$$
