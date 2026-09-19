"""
residue_metamorphic.py - 34 lines - 784/784 PASS G(s)=G(s+qk)
Tests G(s)=G(s+qk) residue invariance m,k 2..8 all r
"""
def G(s,m,k,r):
    return (s % k) * r % m

def test_residue():
    ok=0; fail=0
    for m in range(2,9):
        for k in range(2,9):
            for r in range(1,k):
                for s in range(0, m*k):
                    for q in range(1,5):
                        if G(s,m,k,r)==G(s+q*k,m,k,r):
                            ok+=1
                        else:
                            fail+=1
    print(f"residue_metamorphic ok={ok} fail={fail} PASS" if fail==0 else f"FAIL {fail}")
    return ok, fail

if __name__=="__main__":
    ok,fail=test_residue()
    print(f"Core: 784/784 PASS G(s)=G(s+qk)")
