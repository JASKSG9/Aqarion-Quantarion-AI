WU1 — MELLIN RESIDUE LEDGER
STATUS: FROZEN · EXACT ALGEBRA · NO PROMOTION

Let

    L = log(1/delta)
    A = L + 1 + gamma

------------------------------------------------------------
B0
------------------------------------------------------------

Mellin integrand:

    Gamma(s) zeta(s) zeta(s-1)

Surviving poles:

    s = 2
    s = 1
    s = 0

Expansion:

    B0 =
        (pi^2/6) delta^(-2)
        - (1/2) delta^(-1)
        + 1/24
        + R0

Target contour:

    Re(s) = -3

Formal remainder:

    R0 = O(delta^3)

Contour constant:

    OPEN


------------------------------------------------------------
B1
------------------------------------------------------------

Mellin integrand:

    Gamma(s) zeta(s-1)^2

Surviving poles:

    s = 2      double
    s = 0
    s = -2
    s = -4
    ...

Expansion:

    B1 =
        A delta^(-2)
        + 1/144
        + delta^2/28800
        + R1

Residue at s = -2:

    Res =
        (1/2) zeta(-3)^2
        = 1/28800

Target contour after extracting s=-2:

    Re(s) = -3

Formal remainder:

    R1 = O(delta^3)

Contour constant:

    OPEN


------------------------------------------------------------
B2
------------------------------------------------------------

Mellin integrand:

    Gamma(s) zeta(s-2) zeta(s-1)

Surviving poles:

    s = 3
    s = 2

Expansion:

    B2 =
        (pi^2/3) delta^(-3)
        - (1/2) delta^(-2)
        + R2

Target contour:

    Re(s) = -2

Formal remainder:

    R2 = O(delta^2)

Contour constant:

    OPEN


------------------------------------------------------------
DETERMINANT
------------------------------------------------------------

D(delta):

    delta^5 (B0 B2 - B1^2)


Constant:

    pi^4/18


delta term:

    -A^2 - pi^2/4


delta^2:

    C5 = 1/4 + pi^2/72


delta^3:

    -(A/72 + 1/48)


Therefore:

    C6 = -1/72

    C7 = -(1 + gamma)/72 - 1/48


delta^4:

    NO CONTRIBUTION FROM THE DISPLAYED POLE LEDGER


delta^5 log coefficient:

    C8 = -1/14400


Formal expansion:

    D(delta)
      = pi^4/18
      + delta[-A^2 - pi^2/4]
      + delta^2[1/4 + pi^2/72]
      - delta^3[A/72 + 1/48]
      - delta^5[A/14400]
      + remainder


STATUS:

    C5 = [V + formal residue support]
    C6 = [R]
    C7 = [R]
    C8 = [R]

    contour estimates = OPEN
    final remainder theorem = OPEN

NO PROMOTION.
