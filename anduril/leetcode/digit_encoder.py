from collections import defaultdict

def encode_numeric_code(s: str) -> str:
    freq = defaultdict(int)
    res = []

    for ch in reversed(s):
        freq[ch] += 1
        res.append(f"{freq[ch]}{ch}")

    return "".join(reversed(res))

    