#!/usr/bin/env python3
"""Generate a Lean axiom-audit file for a task (packet or module ID).

Written by the rh-verif agent. It lives outside the archive and never modifies it.

The generated file imports every module of the task and walks the dependency graph
(the same constant fields as Lean core's CollectAxioms) from *every* declaration
of those modules, one traversal for the whole task. It reports the union of axioms
reached. Only when that union holds a non-standard axiom does it repeat the walk per
module, to say which module causes it. It also lists, per module, the declarations
that are axioms, @[extern] or @[implemented_by].
"""
import sys, gzip, json
idx = '/work/repo/tracker/modules.jsonl.gz'
target, out = sys.argv[1], sys.argv[2]
mods = []
with gzip.open(idx, 'rt') as f:
    for line in f:
        r = json.loads(line)
        if target in (r['id'], r['packet'], r['module']):
            mods.append(r['module'])
if target.startswith('MODS:'):
    mods = target[5:].split(',')
if not mods:
    sys.exit('unknown target ' + target)
L = ['import Lean'] + ['import ' + m for m in mods] + ['']
L.append('open Lean Elab Command')
L.append('')
L.append('def auditTargets : Array Name := #[' + ', '.join('`' + m for m in mods) + ']')
L.append(r'''
def stdAxioms : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]

def deps (ci : ConstantInfo) : Array Name :=
  match ci with
  | .axiomInfo v => v.type.getUsedConstants
  | .defnInfo v => v.type.getUsedConstants ++ v.value.getUsedConstants
  | .thmInfo v => v.type.getUsedConstants ++ v.value.getUsedConstants
  | .opaqueInfo v => v.type.getUsedConstants ++ v.value.getUsedConstants
  | .quotInfo v => v.type.getUsedConstants
  | .ctorInfo v => v.type.getUsedConstants
  | .recInfo v => v.type.getUsedConstants
  | .inductInfo v => v.type.getUsedConstants ++ v.ctors.toArray

def isAx (env : Environment) (n : Name) : Bool :=
  match env.find? n with
  | some (.axiomInfo _) => true
  | _ => false

/-- Axioms reachable from `roots`, number of constants visited, number of missing constants. -/
def reach (env : Environment) (roots : Array Name) : NameSet × Nat × Nat := Id.run do
  let mut visited : NameHashSet := {}
  let mut axs : NameSet := {}
  let mut stack := roots
  let mut missing := 0
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if visited.contains n then continue
    visited := visited.insert n
    match env.find? n with
    | some ci =>
      if let .axiomInfo _ := ci then axs := axs.insert n
      for d in deps ci do
        if !visited.contains d then stack := stack.push d
    | none => missing := missing + 1
  return (axs, visited.size, missing)

run_cmd do
  let env ← getEnv
  let names := env.header.moduleNames
  let datas := env.header.moduleData
  let mut perModule : Array (Name × Array Name) := #[]
  let mut notLoaded := 0
  for target in auditTargets do
    match names.findIdx? (· == target) with
    | some i => perModule := perModule.push (target, datas[i]!.constNames)
    | none =>
      notLoaded := notLoaded + 1
      logInfo m!"AXIOM_AUDIT module={target} verdict=NOT_LOADED"
  let mut flaggedStatic := 0
  let mut allRoots : Array Name := #[]
  for (target, decls) in perModule do
    allRoots := allRoots ++ decls
    let thms := decls.filter fun n => match env.find? n with
      | some (.thmInfo _) => true
      | _ => false
    let declAx := decls.filter (isAx env)
    let ext := decls.filter (isExtern env)
    let impl := decls.filter fun n => (Compiler.getImplementedBy? env n).isSome
    let ok := declAx.isEmpty && ext.isEmpty && impl.isEmpty
    if !ok then flaggedStatic := flaggedStatic + 1
    logInfo m!"AXIOM_AUDIT module={target} decls={decls.size} theorems={thms.size} declared_axioms={declAx.toList} extern={ext.toList} implemented_by={impl.toList} static_verdict={if ok then "OK" else "FLAG"}"
  let (axs, visited, missing) := reach env allRoots
  let nonStd := axs.toList.filter fun a => !stdAxioms.contains a
  logInfo m!"AXIOM_AUDIT_UNION roots={allRoots.size} reachable={visited} missing={missing} axioms={axs.toList} nonstandard={nonStd}"
  if !nonStd.isEmpty then
    for (target, decls) in perModule do
      let (a, _, _) := reach env decls
      let bad := a.toList.filter fun x => !stdAxioms.contains x
      if !bad.isEmpty then
        for d in decls do
          let (ad, _, _) := reach env #[d]
          let b := ad.toList.filter fun x => !stdAxioms.contains x
          if !b.isEmpty then logInfo m!"AXIOM_AUDIT_DECL module={target} decl={d} nonstandard={b}"
  let verdict := if nonStd.isEmpty && flaggedStatic == 0 && notLoaded == 0 && missing == 0 then "OK" else "FLAG"
  logInfo m!"AXIOM_AUDIT_SUMMARY targets={auditTargets.size} loaded={perModule.size} static_flagged={flaggedStatic} nonstandard={nonStd} verdict={verdict}"
''')
open(out, 'w').write('\n'.join(L) + '\n')
print(out, len(mods), 'modules')
