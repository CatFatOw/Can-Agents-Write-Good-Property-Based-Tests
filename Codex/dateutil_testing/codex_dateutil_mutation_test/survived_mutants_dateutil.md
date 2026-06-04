# Surived Mutants: Codex dateutil PBT Suite

 `mutmut browse` 

```text
codex_dateutil_mutation_test
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `dateutil/parser/_parser.py` | 336 | 0 |
| `dateutil/parser/isoparser.py` | 36 | 0 |


## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible parsing behavior that the tests should catch with a targeted example. |
| Medium | The mutation could matter, but not sure whether generated inputs ever reach the affected code.|
| Low | The mutation probably doesn't change anything observable. |

Overall confidence in the current Codex dateutil mutation quality: **Medium**.
The tests cover many normal `parse()` and `isoparse()` success paths, but the
survivors show weak pressure on parser edge cases: ambiguous numeric tokens,
HMS suffixes, separator validation, uncommon ISO dates, timezone aliases, and
default parser options.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `parser._parse_numeric_token` | 60 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Numeric date/time ambiguity is under-tested. |
| `parser._parse` | 45 | Medium | Main parse loop branches survive for less common token patterns. |
| `_ymd.resolve_ymd` | 43 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Year-month-day disambiguation is not strongly checked. |
| `_timelex.get_token` | 36 | Medium | Tokenizer edge cases survive, especially punctuation and letter/number boundaries. |
| `_ymd.append` | 25 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Month-name and labeled Y/M/D handling needs more targeted tests. |
| `parserinfo.__init__` | 24 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Defaults such as `dayfirst` and `yearfirst` can change without failing tests. |
| `parser._find_hms_idx` | 23 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | `12h`, `12 h`, `12m`, `12s` style inputs are under-tested. |
| `parserinfo.validate` | 13 | Medium | Timezone and AM/PM validation paths need edge cases. |
| `parser.parse` | 13 | Medium | Default datetime and fuzzy-token variants are only partially constrained. |
| `isoparser._parse_tzstr` | 11 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | UTC normalization and offset validation need sharper assertions. |
| `isoparser._parse_isotime` | 9 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Fractional-second truncation and boundary time forms need tests. |
| Other functions | 70 | Low-Medium | Smaller clusters across setup, conversion, timezone building, and skipped-token recombination. |

## Example Survived Mutants

### 1. Default `dayfirst` changed

**Mutant:** `dateutil.parser._parser.xǁparserinfoǁ__init____mutmut_1`

```diff
-def __init__(self, dayfirst=False, yearfirst=False):
+def __init__(self, dayfirst=True, yearfirst=False):
```

**Why it survived:** The wrapper tests do check explicit `dayfirst=True` and
`dayfirst=False`, but they do not check the default `parser.parse(...)`
behavior on an ambiguous numeric date without passing `dayfirst`.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.


### 2. Numeric-token YMD branch changed

**Mutant:** `dateutil.parser._parser.xǁparserǁ_parse_numeric_token__mutmut_10`

```diff
-if (len(ymd) == 3 and len_li in (2, 4) and
+if (len(ymd) == 4 and len_li in (2, 4) and
```

**Why it survived:** The generated tests cover some slash-separated ambiguous
dates, but not enough compact or mixed numeric formats where the parser must
decide whether a numeric token belongs to Y/M/D or to a time component.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.


### 3. YMD label resolution changed

**Mutant:** `dateutil.parser._parser.xǁ_ymdǁresolve_ymd__mutmut_8`

```diff
 strids = (('y', self.ystridx),
           ('m', self.mstridx),
-          ('d', self.dstridx))
+          ('XXdXX', self.dstridx))
```

**Why it survived:** The tests mostly assert final parsed dates for common
formats. They do not strongly exercise labeled or month-name Y/M/D resolution
where the internal day marker must be preserved.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add month-name and labeled examples such as
`"day 5 month Feb year 2001"` if accepted, or realistic equivalents like
`"Feb 5 2001"`, `"5 Feb 2001"`, and `"2001 Feb 5"` with exact component
assertions.

### 4. HMS suffix boundary changed

**Mutant:** `dateutil.parser._parser.xǁparserǁ_find_hms_idx__mutmut_4`

```diff
-if idx+1 < len_l and info.hms(tokens[idx+1]) is not None:
+if idx+2 < len_l and info.hms(tokens[idx+1]) is not None:
```

**Why it survived:** The current parse test uses colon-separated times, but
does not directly test suffix forms like `12h`, `12 h`, `30m`, or `45s`.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact hours/minutes/seconds for strings such as
`"2020-01-01 12h"`, `"2020-01-01 12h30m"`, and `"2020-01-01 45s"`.


## Overall Assessment

Main weakness is precision on
documented edge behavior. Example failed invariants include: 

1. Default ambiguous date behavior without explicit `dayfirst` or `yearfirst`.
2. HMS suffix formats (`12h`, `12h30m`, `30m`, `45s`).
3. More numeric date/time ambiguity cases in `parse()`.

