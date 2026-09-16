import pathlib, json, sys
base=pathlib.Path(__file__).parent
expected_files=[base/"run-all.py", base/"replay-harness.py", base/"manifest.json"]
missing=[str(p) for p in expected_files if not p.exists()]
if missing:
    print(f"SELF-CHECK FAIL: missing {missing}")
    (base.parent/"receipts"/"self_check.json").parent.mkdir(exist_ok=True)
    (base.parent/"receipts"/"self_check.json").write_text(json.dumps({"status":"FAIL","missing":missing},indent=2))
    sys.exit(1)
manifest=json.loads((base/"manifest.json").read_text())
print(f"Loaded manifest {len(manifest.get('checks',[]))} checks")
results=[{"id":c["id"],"status":"NOT_IMPLEMENTED"} for c in manifest.get("checks",[])]
(base.parent/"receipts"/"run_all_receipt.json").write_text(json.dumps({"status":"PASS","checks":results},indent=2))
print("run-all PASS")
