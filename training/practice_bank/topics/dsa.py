"""DSA practice topic bank."""
DSA_TOPICS = [
    {
        "question": "Implement two-pointer technique to find two numbers with a given sum in a sorted array.",
        "ideal_topics": "two pointers, sorted array, O(n)",
        "solution_code": '''def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None''',
        "solution_explanation": "Sorted order lets us move the window in O(n) without extra space.",
        "hints": "Compare sum with target; move the pointer that moves sum toward target.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Solve longest substring without repeating characters (sliding window).",
        "ideal_topics": "sliding window, hash map, O(n)",
        "solution_code": '''def length_of_longest_substring(s: str) -> int:
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best''',
        "solution_explanation": "Expand right, shrink left when duplicate found. Track max window size.",
        "hints": "Use a set or dict mapping char → last index.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Binary search on a rotated sorted array.",
        "ideal_topics": "binary search, rotated array",
        "solution_code": '''def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1''',
        "solution_explanation": "Identify which half is sorted, then binary search within that half.",
        "hints": "Compare mid with lo to detect sorted half.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Implement a stack using two queues for push/pop.",
        "ideal_topics": "stack, queue, amortized analysis",
        "solution_code": '''from collections import deque

class StackWithQueues:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x: int) -> None:
        self.q2.append(x)
        while self.q1:
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1

    def pop(self) -> int:
        return self.q1.popleft()''',
        "solution_explanation": "Push reverses order into second queue, making pop O(1) amortized.",
        "hints": "Alternatively use one queue and rotate on push.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Reverse a linked list in-place (iterative).",
        "ideal_topics": "linked list, pointers, O(n) O(1)",
        "solution_code": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev''',
        "solution_explanation": "Three-pointer walk: detach next, point to prev, advance.",
        "hints": "Draw pointers before coding.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Detect cycle in linked list (Floyd's algorithm).",
        "ideal_topics": "fast slow pointers, cycle detection",
        "solution_code": '''def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False''',
        "solution_explanation": "Fast pointer catches slow inside cycle if one exists.",
        "hints": "To find cycle start, reset one pointer to head after detection.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Generate all permutations via backtracking.",
        "ideal_topics": "backtracking, recursion, permutations",
        "solution_code": '''def permutations(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start: int):
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result''',
        "solution_explanation": "Swap-based backtracking generates permutations without extra path list.",
        "hints": "Track used elements with a path list for alternative approach.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "DFS traversal of a binary tree (preorder, inorder, postorder).",
        "ideal_topics": "DFS, tree traversal, recursion",
        "solution_code": '''def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)''',
        "solution_explanation": "Recursive DFS mirrors definition. Inorder gives sorted order for BST.",
        "hints": "Implement iterative versions with explicit stack.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "BFS level-order traversal of a binary tree.",
        "ideal_topics": "BFS, queue, level order",
        "solution_code": '''from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    levels = []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(level)
    return levels''',
        "solution_explanation": "Process queue size per level to separate layers.",
        "hints": "Use deque for O(1) pops from front.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Validate a binary search tree.",
        "ideal_topics": "BST, bounds, recursion",
        "solution_code": '''def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return (
        is_valid_bst(root.left, low, root.val)
        and is_valid_bst(root.right, root.val, high)
    )''',
        "solution_explanation": "Pass valid (min, max) range down the tree for each node.",
        "hints": "Inorder traversal should be strictly increasing.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Find kth largest element using a min-heap of size k.",
        "ideal_topics": "heap, top-k, priority queue",
        "solution_code": '''import heapq

def kth_largest(nums: list[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)
    for n in nums[k:]:
        if n > heap[0]:
            heapq.heapreplace(heap, n)
    return heap[0]''',
        "solution_explanation": "Min-heap of size k tracks k largest; root is kth largest.",
        "hints": "heapq.nlargest(k, nums) for library shortcut.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Graph BFS shortest path in unweighted graph.",
        "ideal_topics": "graph, BFS, adjacency list",
        "solution_code": '''from collections import deque

def shortest_path(graph: dict, start, end):
    q = deque([(start, 0)])
    seen = {start}
    while q:
        node, dist = q.popleft()
        if node == end:
            return dist
        for nei in graph.get(node, []):
            if nei not in seen:
                seen.add(nei)
                q.append((nei, dist + 1))
    return -1''',
        "solution_explanation": "BFS explores layers; first hit of target is shortest distance.",
        "hints": "Store parent map to reconstruct path.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Topological sort using Kahn's algorithm.",
        "ideal_topics": "topological sort, DAG, indegree",
        "solution_code": '''from collections import deque, defaultdict

def topo_sort(n, edges):
    indeg = [0] * n
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []  # empty if cycle''',
        "solution_explanation": "Peel nodes with zero indegree; cycle prevents full ordering.",
        "hints": "DFS postorder is alternative topo sort.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Union-Find (Disjoint Set Union) with path compression.",
        "ideal_topics": "union find, connectivity, amortized",
        "solution_code": '''class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True''',
        "solution_explanation": "Path compression + rank heuristic yields near O(1) operations.",
        "hints": "Use for dynamic connectivity and Kruskal's MST.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "0/1 knapsack with DP tabulation.",
        "ideal_topics": "dynamic programming, knapsack",
        "solution_code": '''def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]''',
        "solution_explanation": "Iterate capacity backwards to avoid reusing same item.",
        "hints": "2D table dp[i][c] is easier to reason about first.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Longest increasing subsequence (O(n log n)).",
        "ideal_topics": "LIS, patience sorting, binary search",
        "solution_code": '''import bisect

def length_of_lis(nums: list[int]) -> int:
    tails = []
    for n in nums:
        pos = bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)
        else:
            tails[pos] = n
    return len(tails)''',
        "solution_explanation": "tails[i] is smallest tail of increasing subsequence length i+1.",
        "hints": "bisect_left finds insertion position.",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Coin change — minimum coins to make amount.",
        "ideal_topics": "DP, unbounded knapsack variant",
        "solution_code": '''def coin_change(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1''',
        "solution_explanation": "Bottom-up DP: min coins for amount a from smaller amounts.",
        "hints": "Forward loop over coins then amounts for unbounded use.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Merge intervals after sorting by start.",
        "ideal_topics": "intervals, sorting, greedy",
        "solution_code": '''def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged''',
        "solution_explanation": "Sort then merge overlapping/adjacent intervals greedily.",
        "hints": "Compare current start with last merged end.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Subarray sum equals k (prefix sum + hash map).",
        "ideal_topics": "prefix sum, hash map, subarray",
        "solution_code": '''def subarray_sum(nums: list[int], k: int) -> int:
    count = 0
    prefix = 0
    freq = {0: 1}
    for n in nums:
        prefix += n
        count += freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
    return count''',
        "solution_explanation": "If prefix[j] - prefix[i] = k, subarray (i,j] sums to k.",
        "hints": "Initialize freq[0]=1 for subarrays starting at index 0.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Implement Trie (prefix tree) for autocomplete.",
        "ideal_topics": "trie, prefix tree, strings",
        "solution_code": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.end

    def _walk(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node''',
        "solution_explanation": "Each node maps character → child; end marks complete word.",
        "hints": "starts_with shares _walk logic checking end=False.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Find median from data stream using two heaps.",
        "ideal_topics": "heap, median, streaming",
        "solution_code": '''import heapq

class MedianFinder:
    def __init__(self):
        self.low = []   # max-heap via negation
        self.high = []  # min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.low) < len(self.high):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2''',
        "solution_explanation": "Keep heaps balanced so max of low and min of high define median.",
        "hints": "low stores negatives for max-heap behavior.",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Word break — can string be segmented into dictionary words?",
        "ideal_topics": "DP, string segmentation",
        "solution_code": '''def word_break(s: str, word_set: set[str]) -> bool:
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]''',
        "solution_explanation": "dp[i] true if prefix s[:i] can be segmented.",
        "hints": "BFS on indices is alternative approach.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Number of islands in a 2D grid (DFS).",
        "ideal_topics": "grid DFS, flood fill",
        "solution_code": '''def count_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count''',
        "solution_explanation": "Mark visited cells by mutating grid; each DFS marks one island.",
        "hints": "BFS with queue works equally well.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Analyze time and space complexity of your solution verbally and in code comments.",
        "ideal_topics": "Big-O, complexity analysis",
        "solution_code": '''# Example: nested loop with halving inner range
# Outer: n iterations
# Inner: n/2 + n/4 + ... ≈ n → O(n) total (not O(n²))
def work(n: int) -> int:
    total = 0
    i = n
    while i > 0:
        for j in range(i):
            total += 1
        i //= 2
    return total  # O(n) time, O(1) space''',
        "solution_explanation": "Aggregate inner loops; watch for hidden costs in dict/list operations.",
        "hints": "State worst case, average, and space including recursion stack.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Implement monotonic decreasing stack for daily temperatures.",
        "ideal_topics": "monotonic stack, next greater element",
        "solution_code": '''def daily_temperatures(temps: list[int]) -> list[int]:
    result = [0] * len(temps)
    stack = []  # indices
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)
    return result''',
        "solution_explanation": "Stack holds indices waiting for a warmer day; pop when current is warmer.",
        "hints": "Pattern solves next greater/smaller element family.",
        "time_estimate_minutes": 22,
    },
]
