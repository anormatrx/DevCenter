import json, re

with open('C:\\Users\\anorm\\.config\\opencode\\opencode.json', 'r', encoding='utf-8') as f:
    data = f.read()

lines = []
lines.append("=== Checking for garbled Arabic ===")
names = re.findall(r'"name":\s*"([^"]*)"', data)
for n in names:
    has_high = any(ord(c) > 127 for c in n)
    if has_high:
        lines.append(f'  Name: {repr(n)}')
        lines.append(f'  Hex: {n.encode("utf-8").hex()}')

lines.append("")
lines.append("=== Full file ===")
lines.append(data)

with open('D:\\DevCenter\\config_check.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Written to D:\\DevCenter\\config_check.txt")
