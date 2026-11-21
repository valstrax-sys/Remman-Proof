#!/usr/bin/env bash
# Negative control for the axiom audit: Init.Core declares sorryAx / ofReduceBool etc.
export PATH="$HOME/.elan/bin:$PATH" ELAN_HOME=/work/vol/elan XDG_CACHE_HOME=/work/vol/cache
cd /work/vol/lean; TC=$ELAN_HOME/toolchains/leanprover--lean4---v4.33.1/bin
LP="$(elan run leanprover/lean4:v4.33.1 lake env printenv LEAN_PATH)"
mkdir -p /work/audit
python3 /exchange/in/gen_audit.py "MODS:Init.Core,Lean.Elab.Tactic.ElabTerm" /work/audit/control.lean
env LEAN_PATH="$LP" "$TC/lean" /work/audit/control.lean 2>&1 | grep -E "AXIOM_AUDIT" | cut -c1-700 | head -8
