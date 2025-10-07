#!/usr/bin/env python3
"""
offencloudsive.py

Usage examples:
  python3 offencloudsive.py --scenario scenario1 --profile offencloudsive
  python3 offencloudsive.py --scenario scenario1 --profile offencloudsive --destroy
"""

import argparse, os, subprocess, sys, json
from pathlib import Path

#cmd start
def run(cmd, cwd=None):
    print(f"[+] Run: {' '.join(cmd)} (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)

def export_profile_env(profile_name: str, region: str):
    os.environ.pop("AWS_ACCESS_KEY_ID", None)
    os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
    os.environ.pop("AWS_SESSION_TOKEN", None)
    os.environ["AWS_PROFILE"] = profile_name
    os.environ["AWS_DEFAULT_REGION"] = region
    print(f"[+] Exported AWS_PROFILE={profile_name}, AWS_DEFAULT_REGION={region}")
    
def get_terraform_outputs(cwd: str):
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        outputs = json.loads(result.stdout)
        return outputs
    except subprocess.CalledProcessError:
        print("[!] Failed to get Terraform outputs.")
        return {}
    except json.JSONDecodeError:
        print("[!] Terraform output was not valid JSON.")
        return {}
    
def print_selected_outputs(outputs: dict):
    if not outputs:
        print("[!] No outputs found.")
        return

    print("\n🧩 [Terraform Outputs]")
    print("-" * 40)
    for key, data in outputs.items():
        val = data.get("value")
        print(f"{key}: {val}")

    print("-" * 40 + "\n")

p = argparse.ArgumentParser()
p.add_argument("--scenario", "-s", required=True, help="scenario folder name under ./scenarios or direct path")
p.add_argument("--profile", "-p", required=True, help="AWS CLI profile name (used as AWS_PROFILE)")
p.add_argument("--destroy", action="store_true", help="run terraform destroy instead of apply")
p.add_argument("--region", default="ap-northeast-2", help="AWS region (default: ap-northeast-2)")
args = p.parse_args()

sc_path = Path(args.scenario)
if not sc_path.is_absolute():
    sc_path = Path.cwd() / "scenarios" / args.scenario if (Path.cwd() / "scenarios" / args.scenario).exists() else Path.cwd() / args.scenario
    print(f"[+] Starting scenario: {args.scenario}")
if not sc_path.exists() or not sc_path.is_dir():
    print(f"[!] Scenario folder not found: {sc_path}")
    sys.exit(2)

export_profile_env(args.profile, args.region)

try:
    run(["terraform", "init", "-input=false"], cwd=str(sc_path))

    if args.destroy:
        run(["terraform", "destroy", "-auto-approve"], cwd=str(sc_path))
        print("[+] Destroy completed")
        sys.exit(0)

    plan_cmd = ["terraform", "plan", "-out=plan.tfplan", "-input=false"]

    run(plan_cmd, cwd=str(sc_path))

    run(["terraform", "apply", "-auto-approve", "plan.tfplan"], cwd=str(sc_path))
    
    print("[+] Apply completed")
    
    outputs = get_terraform_outputs(str(sc_path))
    print_selected_outputs(outputs)
    
except subprocess.CalledProcessError as e:
    print(f"[!] Terraform failed: {e}")
    sys.exit(4)
