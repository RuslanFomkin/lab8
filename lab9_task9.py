import heapq
import math
from itertools import count
from collections import Counter


def build_huffman(freq):
    """Построение дерева Хаффмана через heapq. Возвращает (tree, codes)."""
    if not freq:
        raise ValueError("Пустой алфавит")
    order = count()
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    heapq.heapify(heap)
    if not heap:
        raise ValueError("Все частоты нулевые")
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))
    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


def stats(freq, codes):
    """H(X), средняя длина L, эффективность eta и избыточность R."""
    total = sum(freq.values())
    p = {s: w / total for s, w in freq.items() if w > 0}
    H = -sum(pi * math.log2(pi) for pi in p.values())
    L = sum(p[s] * len(codes[s]) for s in p)
    eta = H / L * 100 if L > 0 else 100.0
    return H, L, eta, 100 - eta


def encode(text, codes):
    return "".join(codes[s] for s in text)


def decode(bits, tree):
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)
    result, node = [], tree
    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree
    if node is not tree:
        raise ValueError("Неполное кодовое слово")
    return "".join(result)


def is_prefix_free(codes):
    ws = sorted(codes.values())
    return all(not ws[i + 1].startswith(ws[i]) for i in range(len(ws) - 1))

def task9():
    print("=" * 60)
    print("ЗАДАЧА 9")
    print("=" * 60)
    text = "ABCADE"
    freq = Counter(text)
    tree, codes = build_huffman(freq)
    bits = encode(text, codes)
    H, L, eta, R = stats(freq, codes)
    print("Частоты:", dict(freq))
    for s in sorted(codes):
        print(f"  {s}: {codes[s]}  (l={len(codes[s])})")
    print("Префиксность:", is_prefix_free(codes))
    print("Биты:", bits, f"({len(bits)} бит)")
    print("Декодирование:", decode(bits, tree))
    print(f"H = {H:.4f}, L = {L:.4f}, eta = {eta:.2f}%, R = {R:.2f}%")
    assert decode(bits, tree) == text
    print("decode(encode(text)) == text  ->  True")

    t1 = "AAAAA"
    tr1, c1 = build_huffman(Counter(t1))
    b1 = encode(t1, c1)
    print("\nОдин символ:", c1, "биты:", b1, "->", decode(b1, tr1))
    assert decode(b1, tr1) == t1


if __name__ == "__main__":
    task9()