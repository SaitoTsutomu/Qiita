title: collections.Counterを使おう
tags: Python leetcode Collections collections.Counter
url: https://qiita.com/SaitoTsutomu/items/8eb33adbcde79aaf519f
created_at: 2020-10-04 14:32:31+09:00
updated_at: 2020-10-20 17:48:29+09:00
body:

# `collections.Counter`を使おう

Pythonでは標準でMultiSet（同一要素を許す集合）はありませんが、代わりに`collections.Counter`が使えます。単なるMultiSetではなくカウントに便利なメソッドがあるのでいろいろな場面で使えます。

参考：https://docs.python.org/ja/3/library/collections.html#collections.Counter

[LeetCode](https://leetcode.com/)を例に紹介します。

## [169. Majority Element](https://leetcode.com/problems/majority-element/)

> `nums`の最頻値を求めます。

下記のように`most_common`を使えます。

```py
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return collections.Counter(nums).most_common(1)[0][0]
```

## [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/)

> 2つの文字列`s`と`t`が、アナグラムかどうかを求めます。

アナグラムであるということは、出現回数が同じということです。したがって、`collections.Counter`を`==`で比較するだけです。

```py
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return collections.Counter(s) == collections.Counter(t)
```

## [299. Bulls and Cows](https://leetcode.com/problems/bulls-and-cows/)

> 数当てゲームで「位置と数」が一致する個数と数のみ一致する個数を求めます。

「位置と数」は、zipで取り出して比較すれば良いです。
数のみ一致する個数は、「&」で積集合を求め、個数（`values`）を数えれば良いです。

```py
class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        co = collections.Counter
        a = sum(i == j for i, j in zip(secret, guess))
        b = sum((co(secret) & co(guess)).values()) - a
        return f"{a}A{b}B"
```

## [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

> 上位K個の高頻度の要素を求めます。

そのまま、`most_common`を使います。

```py
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return [i for i, _ in collections.Counter(nums).most_common(k)]
```

## [350. Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/)

> 2つのリストの共通部分をリストで求めます。

要素は`elements`で取得できます。

```py
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        c = collections.Counter(nums1) & collections.Counter(nums2)
        return list(c.elements())
```

## [383. Ransom Note](https://leetcode.com/problems/ransom-note/)

> ransomNoteの各文字がmagazineに含まれるかを求めます。
magazineの各文字は一度だけ使えます。

差集合を「`-`」で計算すれば良いです。

```py
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return not (collections.Counter(ransomNote) - collections.Counter(magazine))
```

## [387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/)

> 最初のユニーク文字のインデックスを求めます。

出現回数が1のものを返すだけです。

```py
class Solution:
    def firstUniqChar(self, s: str) -> int:
        for k, v in collections.Counter(s).items():
            if v == 1:
                return s.index(k)
        return -1
```

ちなみに、1つしか存在しない数を求める「[136. Single Number](https://leetcode.com/problems/single-number/)」は、XORで累積すれば良いでしょう。

```py
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for i in nums:
            res ^= i
        return res
```

## [389. Find the Difference](https://leetcode.com/problems/find-the-difference/)

> 文字列sに1文字追加し、シャッフルした文字列をtとします。追加した文字を求めます。

差集合で計算できます。

```py
class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        return list((collections.Counter(t) - collections.Counter(s)).keys())[0]
```

## [532. K-diff Pairs in an Array](https://leetcode.com/problems/k-diff-pairs-in-an-array/)

> 差がkとなる要素ペアの個数を求めます。

`collections.Counter`は、辞書と同じように`items()`が使えます。
要素は、値と個数です。

```py
class Solution:
    def findPairs(self, nums: List[int], k: int) -> int:
        c = collections.Counter(nums)
        return sum(k > 0 and n + k in c or k == 0 and f > 1 for n, f in c.items())
```

## [657. Robot Return to Origin](https://leetcode.com/problems/robot-return-to-origin/)

> 移動後のロボットの終点が原点かどうかを求めます。

`collections.Counter`は、辞書と同じように`get(キー)`が使えます。
原点に帰るのは、左移動数と右移動数が等しく、下移動数と上移動数が等しいときです。
`str.count`も使えますが、`collections.Counter`の方が良いでしょう。

```py
class Solution:
    def judgeCircle(self, moves: str) -> bool:
        c = collections.Counter(moves)
        return c.get("L", 0) == c.get("R", 0) and c.get("D", 0) == c.get("U", 0)
```

## [819. Most Common Word](https://leetcode.com/problems/most-common-word/)

> bannedに含まれない最頻単語を求めます（大文字は小文字とみなします）。

最頻単語ですから`most_common`が使えます。

```py
class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        c = collections.Counter(re.findall(r"\w+", paragraph.lower()))
        return next(s for s, _ in c.most_common() if s not in banned)
```

## [893. Groups of Special-Equivalent Strings](https://leetcode.com/problems/groups-of-special-equivalent-strings/)

> 偶数番目同士または奇数番目同士を交換し一致すれば同一グループとします。グループ数を求めます。

奇数番目を大文字に変えて`collections.Counter`を使います。
また、`set(tuple(sorted(c.items())))`とすることで、グループがわかります。

```py
class Solution:
    def numSpecialEquivGroups(self, A: List[str]) -> int:
        cc = [collections.Counter(i[::2].upper() + i[1::2]) for i in A]
        return len(set(tuple(sorted(c.items())) for c in cc))
```

## [1002. Find Common Characters](https://leetcode.com/problems/find-common-characters/)

> 各単語に共通する文字を（重複を許して）求めます。

各単語の`collections.Counter`の積集合の`elements`で求まります。

```py
class Solution:
    def commonChars(self, A: List[str]) -> List[str]:
        cc = map(collections.Counter, A)
        return list(functools.reduce(operator.and_, cc).elements())
```

## [1010. Pairs of Songs With Total Durations Divisible by 60](https://leetcode.com/problems/pairs-of-songs-with-total-durations-divisible-by-60/)

> 60の倍数となるtimeの2つの要素のペア数を求めます。

timeの60の剰余の`collections.Counter`を使います。剰余が30の倍数かどうかで場合分けします。

```py
class Solution:
    def numPairsDivisibleBy60(self, time: List[int]) -> int:
        c = collections.Counter([t % 60 for t in time])
        return (
            sum(n * (c.get(60 - t, 0) if t % 30 else n - 1) for t, n in c.items()) // 2
        )
```

## 余談

LeetCodeに合わせて、`more_itertools`は使ってませんが、[使うともっとシンプルになります](https://leetcode.com/discuss/feedback/867704/import-more_itertools)。

参考：[collections.Counterを使ったLeetCodeの回答例](https://github.com/SaitoTsutomu/leetcode/search?q=collections.Counter)

