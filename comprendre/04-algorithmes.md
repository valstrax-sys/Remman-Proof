# 4. Algorithmes : ce que la preuve change en informatique

Beaucoup d'algorithmes de théorie des nombres avaient une **analyse conditionnelle**. Ils fonctionnaient bien en pratique, mais leur **correction** ou leur **temps d'exécution** n'était démontré que « sous GRH ». Pour ceux qui ne dépendent que des fonctions L de **Dirichlet** (ou de corps quadratiques et abéliens), la garantie est désormais inconditionnelle.

Le code est dans [`code/rh_algos.py`](code/rh_algos.py), en Python pur. `python rh_algos.py --test` lance les tests, et la sortie de la démonstration est conservée dans [`code/demo-output.txt`](code/demo-output.txt).

| Algorithme | Avant | Maintenant | Ingrédient |
|---|---|---|---|
| **Test de Miller** (Miller–Rabin avec toutes les bases $a \le 2\ln^2 n$) | déterministe et correct **sous GRH** | **correct, déterministe, $\tilde O(\log^4 n)$** | Bach (1990) : témoin $< 2\ln^2 n$ |
| AKS (2002) | déjà inconditionnel, $\tilde O(\log^6 n)$ | inchangé ; Miller est plus rapide | — |
| Racine carrée modulo $p$ (Tonelli–Shanks, Cipolla) | probabiliste (on tire un non-résidu au hasard) ou déterministe sous GRH | **déterministe, temps polynomial** | non-résidu $< 2\ln^2 p$ |
| Calcul de $\varphi(n)$, ou d'un multiple de l'ordre, **⇒ factorisation de $n$** | réduction déterministe sous GRH (Miller 1976) | **réduction déterministe** | idem |
| Plus petite racine primitive modulo $p$ | recherche en $O(\log^6 p)$ essais sous GRH | garantie (Shoup 1992) | caractères modulo $p$ |
| Plus petit premier $\equiv a \pmod q$ | $< 2(q\ln q)^2$ sous GRH | garanti | Bach–Sorenson (1996) |
| Groupe des classes et régulateur des **corps quadratiques** (Buchmann, Hafner–McCurley) | sortie **certifiée seulement sous GRH** | **certifiée** | idéaux de norme $\le 6\ln^2\lvert\Delta\rvert$ |
| Même calcul pour des corps de degré $\ge 3$ non abéliens | sous GRH | **toujours sous GRH** (non couvert) | demanderait ERH |
| Tests et bornes « explicites » sur $\pi(x)$ (Schoenfeld, Büthe…) | constantes conditionnelles | inconditionnelles | RH pour $\zeta$ |

## Résultats de la démonstration (`code/demo-output.txt`)

- **Miller.** $2^{127}-1$ est déclaré premier après au plus 15 498 bases, sans aucun hasard. Le nombre de Carmichael $561$ est déclaré composé.
- **Schoenfeld.** Pour $x = 10^4, \dots, 10^7$, on observe $\lvert\pi(x) - \operatorname{li}(x)\rvert = 17, 38, 130, 339$. Les bornes théoriques valent $37, 145, 550, 2028$ : elles sont respectées, avec une marge de l'ordre d'un facteur 2 à 6.
- **Robin**, jusqu'à $2\cdot10^5$. Le pire cas est $n = 10080$, avec $\sigma(n)/(n\ln\ln n) = 1{,}7558 < e^\gamma = 1{,}7811$. Pour Lagarias, aucun contre-exemple.
- **Progressions arithmétiques.** Le plus petit premier dans chaque classe modulo $q = 9973$ est au plus $925\,949$. La borne vaut $1{,}7 \cdot 10^{10}$ : elle est très large, comme toujours avec les bornes explicites.

> **Ce que ces contrôles valent.** Ils **illustrent** les formules, mais ne **prouvent** rien : un contrôle numérique fini ne démontre jamais un énoncé pour tout $n$. Ce qui est nouveau, c'est que les bornes sont désormais des théorèmes. Le code les utilise comme **garanties de terminaison et de correction**.

## Impact pratique honnête

- **Cryptographie.** Aucune clé n'est affaiblie, puisque RH ne donne aucun algorithme de factorisation rapide. L'effet est **positif** : la génération de premiers, par exemple pour RSA, peut utiliser un test **déterministe prouvé**. En pratique, on garde Miller–Rabin aléatoire avec quelques bases, beaucoup plus rapide. La version prouvée sert surtout à la **certification**.
- **Logiciels de calcul formel** (PARI/GP, Magma, Sage). Plusieurs fonctions affichent des résultats « sous GRH », par exemple `bnfinit` dans PARI, sauf certification. Pour les corps quadratiques et abéliens, ces résultats deviennent certifiés sans calcul supplémentaire. Il resterait à le documenter dans ces logiciels.
- **Complexité théorique.** Plusieurs réductions de problèmes de théorie des nombres deviennent inconditionnelles : factorisation ↔ $\varphi(n)$, extraction de racines, etc.
