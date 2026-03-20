---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: py2many/static-python-skill
# corpus-url: https://github.com/py2many/static-python-skill/blob/d4dfb249c82c6b4448cce76478fd1259120aea8e/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Static Python

A subset of Python that transpiles to compiled languages.

## Rules

- Use fixed-width integers: `i32`, `u64`, etc.
- Use decorators and composition instead of inheritance
- Use `Result[T, E]` instead of exceptions
- Use `match` as an expression. Note that there is no `case` keyword.
  ```
  match x:
      1: ...
      2: ...
  ```
- match can be nested inside other matches to write succinct code
- Elide types when easily inferred
- Always specify return types on functions
- Use design by contract with `smt.pre` and `smt.post`

## Example

```python
def classify_triangle(a: int, b: int, c: int) -> TriangleType:
    if smt.pre:
        assert a > 0
        assert b > 0
        assert c > 0
        assert a < (b + c)
        assert b < (a + c)
        assert c < (a + b)

    if a == b == c:
        result = TriangleType.EQUILATERAL
    elif a == b or b == c or a == c:
        result = TriangleType.ISOSCELES
    else:
        result = TriangleType.SCALENE

    if smt_post:
        assert smt.post(result)

    return result
```

## Reference
[Unsupported features](reference/unsupported.md)
[Verification](reference/verification.md)
[Decorators](reference/decorators.md)