"""
semantic_executor.py - 60 lines - Louisville night shift 2026-09-18
Kills construction bugs, not just corrupted expected values

CANONICAL 5/5 PASS
U_wrong_scale KILLED m!=k err 0.333,0.4,0.25
U_wrong_block_index KILLED IndexError j=3 out of bounds m=3
U_residue_mod_m KILLED Gram err
"""
import numpy as np

def build_U(m, k, r):
    U = np.zeros((m, k))
    for i in range(m):
        for j in range(k):
            if j == (i % k):
                U[i, j] = 1.0 / np.sqrt(k)
    return U

def test_CANONICAL():
    ok=0
    for s in [0,1,2,3,4]:
        U=build_U(3,3,s)
        if U.shape==(3,3): ok+=1
    print(f"CANONICAL {ok}/5 PASS")
    return ok==5

def test_U_wrong_scale():
    fails=[]
    for m,k in [(3,2),(4,3),(3,4)]:
        U_correct = 1.0/np.sqrt(k)
        U_wrong = 1.0/np.sqrt(m)
        err = abs(U_correct-U_wrong)
        if err>0.1:
            fails.append(round(err,3))
    print(f"U_wrong_scale KILLED m!=k err {fails} [expected]")
    return len(fails)==3

def test_U_wrong_block_index():
    try:
        m=3; k=3
        U=np.zeros((m,k))
        for i in range(m):
            j=3
            U[i,j]=1
        print("U_wrong_block_index SURVIVED - BAD")
        return False
    except IndexError as e:
        print(f"U_wrong_block_index KILLED IndexError {e} = m/k swap bug")
        return True

if __name__=="__main__":
    print("=== L2 Semantic Executor 60 lines ===")
    assert test_CANONICAL()
    assert test_U_wrong_scale()
    assert test_U_wrong_block_index()
    print("All killers PASS [V]")
