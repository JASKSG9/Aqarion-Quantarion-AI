"""
CLAIMLOCK policy kernel — Aqarions-Quantarion-AI hub
Policy evaluator: does NOT decide truth, only whether promotion allowed.
"""
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class Scope(Enum):
    NUMERIC=1
    EXACT=2
    FORMAL=3
    INDEPENDENT=4
    @classmethod
    def from_str(cls,s:str): return cls[s.upper()]

class Outcome(Enum):
    ALLOW="ALLOW"
    CL_SCOPE_INSUFFICIENT="CL_SCOPE_INSUFFICIENT"
    CL_MISSING_EVIDENCE="CL_MISSING_EVIDENCE"
    CL_EXACT_COMPUTATION_MISSING="CL_EXACT_COMPUTATION_MISSING"
    CL_FORMALIZATION_MISSING="CL_FORMALIZATION_MISSING"
    CL_INDEPENDENT_CHECK_MISSING="CL_INDEPENDENT_CHECK_MISSING"

@dataclass
class Evidence:
    id:str; scope:Scope; exact:bool=False; formal:bool=False; independent:bool=False

@dataclass
class Claim:
    id:str; evidence:List[Evidence]

@dataclass
class Policy:
    min_scope:Scope; requires_exact:bool=False; requires_formal:bool=False; requires_independent:bool=False

def evaluate(claim:Claim, policy:Policy)->Dict:
    strongest=max((e.scope for e in claim.evidence), default=Scope.NUMERIC, key=lambda s:s.value)
    if strongest.value < policy.min_scope.value:
        return {"outcome":Outcome.CL_SCOPE_INSUFFICIENT.value,"strongest":strongest.name,"required":policy.min_scope.name}
    if policy.requires_exact and not any(e.exact for e in claim.evidence):
        return {"outcome":Outcome.CL_EXACT_COMPUTATION_MISSING.value}
    if policy.requires_formal and not any(e.formal for e in claim.evidence):
        return {"outcome":Outcome.CL_FORMALIZATION_MISSING.value}
    if policy.requires_independent and not any(e.independent for e in claim.evidence):
        return {"outcome":Outcome.CL_INDEPENDENT_CHECK_MISSING.value}
    return {"outcome":Outcome.ALLOW.value,"strongest":strongest.name}

if __name__=="__main__":
    claim=Claim(id="SV-001-V2", evidence=[Evidence(id="sv001_exact", scope=Scope.EXACT, exact=True, independent=True)])
    policy=Policy(min_scope=Scope.EXACT, requires_exact=True, requires_independent=True)
    print(evaluate(claim,policy)) # ALLOW
