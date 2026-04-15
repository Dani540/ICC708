import heapq

from cv2 import merge
from pyparsing import nums

class CustomMinHeap:
    def __init__(self, iterable=None):
        if iterable is not None:
            self.heap = list(iterable)
            heapq.heapify(self.heap)
        else:
            self.heap = []

    def heapify(self, iterable):
        self.heap = list(iterable)
        heapq.heapify(self.heap)

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0
    
    def clear(self):
        self.heap.clear()
    
    def push_pop(self, item):
        return heapq.heappushpop(self.heap, item)
        
    def replace(self, item):
        if self.heap:
            return heapq.heapreplace(self.heap, item)
        else:
            heapq.heappush(self.heap, item)
            return None

    def k_smallest(self, k):
        return heapq.nsmallest(k, self.heap)
    
    def k_smallest_manual(self, k):
        temp_heap = self.heap.copy() 
        return [heapq.heappop(temp_heap) for _ in range(k)]

    def k_frecuency(self, k):
        from collections import Counter
        count = Counter(self.heap)
        return count.most_common(k)
    
    def k_frecuency_manual(self, k, heap=None):
        heap = self.heap if heap is None else heap
        frecs = {}
        for value in heap:
            frecs[value] = frecs.get(value, 0) + 1
        max_heap = [(-freq, value) for value, freq in frecs.items()]
        heapq.heapify(max_heap)
        return [heapq.heappop(max_heap)[1] for _ in range(k)]

    def merge_sorted_lists(self, listeilors:list):
        min_heap = []
        result = []
        for i, lst in enumerate(listeilors):
            if lst:
                heapq.heappush(min_heap, (lst[0], i, 0))  # (value, list_index, element_index)
        while min_heap:
            value, idx_list, idx_element = heapq.heappop(min_heap)
            result.append(value)
            next_idx_element = idx_element + 1
            if next_idx_element < len(listeilors[idx_list]):
                next_value = listeilors[idx_list][next_idx_element]
                heapq.heappush(min_heap, (next_value, idx_list, next_idx_element))
        return result

    def top_k_recommender(self, productos:list, k):
        min_heap = []
        producto: tuple
        for name, ptje in productos:
            heapq.heappush(min_heap, (ptje, name))
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        result = [nombre for puntaje, nombre in min_heap]
        return result[::-1]
        

    def __len__(self):
        return len(self.heap)
    
# El truco para el max heap está en invertir el signo de los valores que entran y luego volver a invertirlos cuando los queramos sacar.
class CustomMaxHeap(CustomMinHeap):
    def __init__(self, iterable=None):
        if iterable is not None:
            inverted_iterable = [-x for x in iterable]
            super().__init__(inverted_iterable)
        else:
            super().__init__()

    def push(self, item):
        super().push(-item)

    def pop(self):
        return -super().pop()

    def peek(self):
        val = super().peek()
        return -val if val is not None else None
        
    def push_pop(self, item):
        return -super().push_pop(-item)
        
    def replace(self, item):
        val = super().replace(-item)
        return -val if val is not None else None
    
    def k_max(self, k):
        temp_heap = self.heap.copy() 
        return [-heapq.heappop(temp_heap) for _ in range(k)]
    
    # Cómo están negativos, los más pequeños son los más grandes al invertir el signo
    def k_max_alt(self, k):
        return [-x for x in heapq.nsmallest(k, self.heap)]

if __name__ == "__main__":
    # Ejercicio 1: Dado un arreglo, encontrar el k-ésimo número más grande.
    # Entrada: nums = [3,2,1,5,6,4], k=2
    # Salida: 5
    customMaxHeap = CustomMaxHeap([3,2,1,5,6,4])
    print(customMaxHeap.k_max(2)) 
    print(customMaxHeap.k_max_alt(2)) 
    # Ejercicio 2.2: Mezclar k listas ordenadas.
    # Entrada: [[1,4,5],[1,3,4],[2,6]]
    # Salida: [1,1,2,3,4,4,5,6]
    customMinHeap = CustomMinHeap()
    print(customMinHeap.merge_sorted_lists([[1,4,5],[1,3,4],[2,6]])) 
    # Ejercicio 2.3: Dado un conjunto de productos con puntajes, devolver los Top-K productos más relevantes.
    #
    # Ejemplo:
    # productos = [("Laptop", 95), ("Mouse", 80), ("Teclado", 85)]
    # k = 2
    # Salida esperada: ['Laptop', 'Teclado']
    customMinHeap = CustomMinHeap()
    print(customMinHeap.top_k_recommender([("Laptop", 95), ("Mouse", 80), ("Teclado", 85)], 2)) 
