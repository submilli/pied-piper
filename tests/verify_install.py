#!/usr/bin/env python3
"""Verify package installation and permission boundaries without provider calls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cli', required=True, type=Path)
parser.add_argument('--published', action='store_true')
parser.add_argument('--ref', default='v0.1.1')
args = parser.parse_args()
cli = args.cli.resolve()
root = Path(__file__).resolve().parents[1]
packages = [
    ('@submilli/pied-piper-billing', 'pied-piper.example/charges.list', 'submilli/pied-piper'),
    ('@submilli/acme-billing', 'acme.com/charges.list', 'submilli/acme'),
]
ids = {'pied_piper': 2, 'hooli': 1, 'cus_northwind': 2, 'cus_initech': 1}
checks = 0
with tempfile.TemporaryDirectory(prefix='pied-piper-package-check-') as temporary:
    directory = Path(temporary)
    env = dict(os.environ, SUBMILLI_HOME=str(directory / 'store'))

    def command(*arguments, cwd=root, success=True):
        result = subprocess.run([str(cli), *arguments], cwd=cwd, env=env,
                                text=True, capture_output=True)
        if success and result.returncode != 0:
            raise AssertionError(f'{arguments}: {result.stdout}\n{result.stderr}')
        return result

    if args.published:
        for package, capability, repository in packages:
            result = command('install', f'{repository}@{args.ref}', package)
            print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
    else:
        result = command('build', 'publish-local')
        print(result.stdout.strip())

    for package, capability, repository in packages:
        for supplied, count in ids.items():
            script = directory / 'program.ts'
            script.write_text(
                f'import {{ listCharges }} from {json.dumps(package)};\n'
                f'function main(): string {{\n'
                f'  const charges = listCharges({json.dumps(supplied)});\n'
                f'  assert(charges.length === {count}, "charge count");\n'
                f'  assert(charges[0].customerId === {json.dumps(supplied)}, "requested ID");\n'
                f'  return "allowed";\n}}\n')

            def run_bound(bound, granted):
                blueprint = directory / 'blueprint.yaml'
                blueprint.write_text(
                    'name: package-migration-check\n'
                    'variables:\n  customerId:\n    required: true\n'
                    f'packages: [{json.dumps(package)}]\n'
                    'default: deny\npermissions:\n  main:\n'
                    f'  - capability: {granted}\n'
                    '    filter: customerId == ${vars.customerId}\n'
                    '    action: allow\n'
                    f'  {json.dumps(package)}: []\n')
                return command('run', '--blueprint', str(blueprint), '--var',
                               f'customerId={bound}', str(script), success=False)

            allowed = run_bound(supplied, capability)
            assert allowed.returncode == 0 and allowed.stdout.strip() == 'allowed', (
                package, supplied, allowed.stdout, allowed.stderr)
            checks += 1

            # Include an equivalent historical/canonical identity: alias resolution
            # must not bypass a filter on the argument the caller actually supplied.
            other = {'pied_piper': 'cus_northwind', 'cus_northwind': 'pied_piper',
                     'hooli': 'cus_initech', 'cus_initech': 'hooli'}[supplied]
            denied = run_bound(other, capability)
            assert denied.returncode != 0 and 'PermissionDeniedError' in denied.stderr, (
                package, supplied, 'alias bypass', denied.stdout, denied.stderr)
            checks += 1

            cross_customer = 'hooli' if supplied in ('pied_piper', 'cus_northwind') else 'pied_piper'
            denied = run_bound(cross_customer, capability)
            assert denied.returncode != 0 and 'PermissionDeniedError' in denied.stderr, (
                package, supplied, 'customer bypass', denied.stdout, denied.stderr)
            checks += 1

            other_capability = next(cap for name, cap, repo in packages if name != package)
            denied = run_bound(supplied, other_capability)
            assert denied.returncode != 0 and 'PermissionDeniedError' in denied.stderr, (
                package, supplied, 'capability bypass', denied.stdout, denied.stderr)
            checks += 1
        print(f'PASS {package}: canonical and historical IDs; exact-ID, customer and capability boundaries')
    print(f'{checks} permission and data checks passed; no provider calls')
