# Chaldean mapping (no letters map to 9)
CHAR_MAP = {
    1: list("AIJQY"),
    2: list("BKR"),
    3: list("CGLS"),
    4: list("DMT"),
    5: list("EHNX"),
    6: list("UVW"),
    7: list("OZ"),
    8: list("FP"),
}
LETTER_TO_VAL = {ch: val for val, letters in CHAR_MAP.items() for ch in letters}

def clean_name(name: str) -> str:
    return "".join(ch for ch in name.upper() if ch.isalpha())

def letter_value(ch: str) -> int:
    return LETTER_TO_VAL.get(ch, 0)

def sum_name(name: str) -> tuple[int, list[int]]:
    cleaned = clean_name(name)
    vals = [letter_value(c) for c in cleaned]
    return sum(vals), vals

def reduce_number(n: int, preserve: set[int] = {11, 22, 33}) -> int:
    # keep master/compound; allow 9 as final single digit
    if n in preserve:
        return n
    while n > 9 and n not in preserve:
        n = sum(int(d) for d in str(n))
    return n

def analyze_name(name: str) -> dict:
    total, vals = sum_name(name)
    reduced = reduce_number(total)
    ruling_planet = ruling_planet_for(reduced)
    return {
        "input": name,
        "cleaned": clean_name(name),
        "letter_values": vals,
        "total": total,
        "number": reduced,
        "ruling_planet": ruling_planet,
    }

def ruling_planet_for(n: int) -> str:
    # Chaldean style associations (simplified)
    mapping = {
        1: "Sun",
        2: "Moon",
        3: "Jupiter",
        4: "Rahu",
        5: "Mercury",
        6: "Venus",
        7: "Ketu",
        8: "Saturn",
        9: "Mars",
        11: "Master (Sun/Moon blend)",
        22: "Master (Jupiter/Saturn blend)",
        33: "Master (Jupiter/Venus blend)",
    }
    return mapping.get(n, "Unknown")
