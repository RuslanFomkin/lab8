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

TEXT = (
    "Информация — это сведения, которые уменьшают неопределённость. "
    "Чем реже происходит событие, тем больше информации несёт сообщение о нём. "
    "Клод Шеннон предложил измерять количество информации в битах и показал, "
    "что энтропия источника задаёт нижнюю границу средней длины кода. "
    "Код Хаффмана строит оптимальный префиксный код: частые символы получают "
    "короткие кодовые слова, а редкие — длинные. Для текста на русском языке "
    "самыми частыми символами обычно оказываются пробел и буквы «о», «е», «а», "
    "поэтому сжатие получается заметным, хотя и не бесконечным."
)


def task10():
    print("\n" + "=" * 60)
    print("ЗАДАЧА 10")
    print("=" * 60)

    text = TEXT.lower()
    N = len(text)
    freq = Counter(text)
    tree, codes = build_huffman(freq)
    H, L, eta, R = stats(freq, codes)

    print(f"Длина текста N = {N} символов, алфавит K = {len(freq)}")
    print("\nСимвол  n_i   p_i      код               l_i")
    for s, n in sorted(freq.items(), key=lambda x: (-x[1], x[0])):
        name = {" ": "пробел", "\n": "\\n"}.get(s, s)
        print(f"{name:<7} {n:<5} {n/N:<8.4f} {codes[s]:<17} {len(codes[s])}")

    print(f"\nH(X) = {H:.4f} бит/символ")
    print(f"L    = {L:.4f} бит/символ")
    print(f"eta  = {eta:.3f} %")
    print(f"R    = {R:.3f} %")
    print("H <= L < H+1:", H <= L < H + 1)
    print("Префиксность:", is_prefix_free(codes))

    bits = encode(text, codes)
    assert decode(bits, tree) == text
    print("Декодирование корректно: True")

    utf8_bytes = len(text.encode("utf-8"))
    huff_bits = len(bits)
    huff_bytes = math.ceil(huff_bits / 8)
    pad = huff_bytes * 8 - huff_bits
    print(f"\nUTF-8: {utf8_bytes} байт = {utf8_bytes*8} бит")
    print(f"Поток Хаффмана: {huff_bits} бит -> {huff_bytes} байт "
          f"(выравнивание: +{pad} бит)")

    header = 2 + 4
    table = sum(len(s.encode("utf-8")) + 1 for s in freq)
    overhead = header + table
    total = overhead + huff_bytes
    print(f"\nСлужебные данные: заголовок {header} Б + таблица {table} Б = {overhead} Б")
    print(f"Итого файл: {total} байт")
    print(f"Kс без служебных данных (UTF-8 / поток): {utf8_bytes/huff_bytes:.4f}")
    print(f"S  без служебных данных: {(1 - huff_bytes/utf8_bytes)*100:.2f} %")
    print(f"Kс с таблицей и выравниванием: {utf8_bytes/total:.4f}")
    print(f"S  с таблицей и выравниванием: {(1 - total/utf8_bytes)*100:.2f} %")
    print(f"Справка: L / 8 = {L/8:.4f}; идеально по энтропии: "
          f"{math.ceil(H*N/8)} байт")


if __name__ == "__main__":
    task10()