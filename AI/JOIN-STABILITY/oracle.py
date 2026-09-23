"""Exact oracle for JOIN-STABILITY - no floating tolerance for decision."""
import numpy as np
from collections import defaultdict

def c_bip(blocks, T, n):
    """FIXED version - original returned 1 always."""
    m=len(blocks)
    lab={x:i for i,b in enumerate(blocks) for x in b}
    p=list(range(2*m))
    def find(x):
        while p[x]!=x:
            p[x]=p[p[x]]; x=p[x]
        return x
    def unite(a,b):
        pa,pb=find(a),find(b)
        if pa!=pb: p[pa]=pb
    for i,blk in enumerate(blocks):
        targets=set(lab[T[x]] for x in blk)
        for j in targets:
            unite(i, m+j)
    return len(set(find(v) for v in range(2*m)))

def P_matrix(blocks, n):
    P=np.zeros((n,n))
    for b in blocks:
        k=len(b)
        if k==0: continue
        for i in b:
            for j in b:
                P[i,j]=1.0/k
    return P

def rank_D(blocks, T, n):
    K=np.zeros((n,n))
    for i,ti in enumerate(T): K[i,ti]=1.0 # Koopman pullback
    P=P_matrix(blocks,n)
    D=(np.eye(n)-P)@K@P
    return int(np.linalg.matrix_rank(D, tol=1e-9)), D

def is_pullback_stable(T, E):
    n=len(T)
    for a in range(n):
        for b in range(n):
            if (a,b) in E:
                continue
            if (T[a],T[b]) in E:
                # need (a,b) in E to be stable, but it isn't
                # so actually check contrapositive: if (T(a),T(b)) in E then (a,b) must be in E
                # Here (T(a),T(b)) in E and (a,b) not in E => NOT stable
                pass
    # correct check:
    for a in range(n):
        for b in range(n):
            if (T[a],T[b]) in E and (a,b) not in E:
                return False
    return True

def join_equiv(E,F,n):
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for a,b in E|F:
        union(a,b)
    return {(a,b) for a in range(n) for b in range(n) if find(a)==find(b)}
