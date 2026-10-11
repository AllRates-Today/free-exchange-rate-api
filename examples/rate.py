"""python examples/rate.py USD EUR [bank]"""
import sys, json, urllib.request

source, target, bank = (sys.argv[1:] + ["USD", "EUR", "ecb"])[:3]
url = f"https://allratestoday.com/api/open/central-bank/{bank}?source={source}&target={target}"
with urllib.request.urlopen(url, timeout=20) as resp:
    r = json.load(resp)
if "error" in r:
    raise SystemExit(r["error"])
flag = ", derived" if r.get("derived") else ""
print(f"1 {r['source']} = {r['rate']} {r['target']} ({r['bank'].upper()}, {r['rate_date']}{flag})")
