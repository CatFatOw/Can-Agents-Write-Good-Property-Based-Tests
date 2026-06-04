# Survived Mutants: Gemini dateutil PBT Suite

`mutmut results`

```text
gemini_dateutil_mutation_test
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `dateutil/parser/_parser.py` | 429 | 0 |
| `dateutil/parser/isoparser.py` | 53 | 0 |

Current `mutmut results` also reported 7 timeout mutants. The recorded aggregate
metrics in [`mutation_testing_results.py`](../../../mutation_testing_results.py)
may differ slightly if they came from an earlier mutation run.

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible parsing behavior that the tests should catch with a targeted example. |
| Medium | The mutation could matter, but not sure whether generated inputs ever reach the affected code. |
| Low | The mutation probably does not change anything observable. |

Overall confidence in the current Gemini dateutil mutation quality: **Medium-Low**.

The Gemini tests cover common successful `parse()` and `isoparse()` shapes, but
the survivor count is high and concentrated in parser ambiguity code. The suite
mostly generates structurally clean dates and times, so it misses ambiguous
numeric tokens, labeled HMS suffixes, timezone-name paths, parser defaults,
tokenizer punctuation, and ISO timezone boundary validation.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `parser._parse_numeric_token` | 100 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Numeric date/time ambiguity is the largest weakness. |
| `_timelex.get_token` | 52 | Medium | Tokenizer edge cases survive, especially punctuation, dots, spaces, and letter/number boundaries. |
| `_ymd.resolve_ymd` | 44 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Year-month-day disambiguation and month-name ordering are not strongly checked. |
| `isoparser._parse_tzstr` | 38 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Offset sign, UTC normalization, and timezone-range validation need sharper assertions. |
| `parser._parse` | 33 | Medium | Main parse-loop branches survive for less common token patterns. |
| `parser._find_hms_idx` | 31 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | `12h`, `12 h`, `12m`, and `12s` style inputs are under-tested. |
| `parserinfo.__init__` | 24 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Defaults such as `dayfirst` and `yearfirst` can change without failing tests. |
| `_ymd.append` | 23 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Month-name and labeled Y/M/D handling needs targeted examples. |
| `parserinfo.validate` | 22 | Medium | Timezone, AM/PM, and parsed-result validation branches are weakly constrained. |
| `parser.parse` | 18 | Medium | Default datetime, fuzzy-token, and ignored-token behavior are only partially checked. |
| `parser._could_be_tzname` | 12 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Timezone-name detection needs examples with named zones and ambiguous uppercase tokens. |
| `parser._build_naive` | 10 | Medium | Default-field replacement and month-end fallback behavior need edge cases. |
| `isoparser._parse_isotime` | 10 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Separator consistency, fractional seconds, and boundary time forms need tests. |
| Other functions | 65 | Low-Medium | Smaller clusters across parser setup, conversion, timezone construction, skipped-token recombination, and helper routines. |

## Example Survived Mutants

### 1. Default `dayfirst` changed

**Mutant:** `dateutil.parser._parser.xǁparserinfoǁ__init____mutmut_1`

```diff
-def __init__(self, dayfirst=False, yearfirst=False):
+def __init__(self, dayfirst=True, yearfirst=False):
```

**Why it survived:** The Gemini parse wrapper generates mostly unambiguous ISO-like
dates. It does not assert the default behavior of `parser.parse(...)` on an
ambiguous numeric date such as `"01/02/2003"` without explicitly passing
`dayfirst`.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert default, `dayfirst=True`, and `yearfirst=True`
results on ambiguous strings such as `"01/02/2003"` and `"01/02/03"`.

### 2. Numeric-token YMD branch changed

**Mutant:** `dateutil.parser._parser.xǁparserǁ_parse_numeric_token__mutmut_10`

```diff
-    if (len(ymd) == 3 and len_li in (2, 4) and
+    if (len(ymd) == 4 and len_li in (2, 4) and
```

**Why it survived:** The largest survivor cluster is in numeric-token parsing.
The tests generate clean `YYYY-MM-DD HH:MM:SS` strings and a small partial
`YYYY-MM` fallback case, but they do not stress compact dates, slash-separated
ambiguous dates, or mixed date/time numeric tokens.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add exact component assertions for `"20010102"`,
`"01/02/2003"`, `"2003/01/02"`, `"01-02-03"`, and date strings followed by
standalone numeric time tokens.

### 3. YMD label resolution changed

**Mutant:** `dateutil.parser._parser.xǁ_ymdǁresolve_ymd__mutmut_8`

```diff
 strids = (('y', self.ystridx),
           ('m', self.mstridx),
-          ('d', self.dstridx))
+          ('XXdXX', self.dstridx))
```

**Why it survived:** The tests mainly assert regular numeric date components.
They do not strongly exercise month-name ordering or labeled Y/M/D resolution,
where the parser must preserve which token represents the day.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact components for `"Feb 5 2001"`,
`"5 Feb 2001"`, `"2001 Feb 5"`, and fuzzy variants that include surrounding
text.

### 4. HMS suffix boundary changed

**Mutant:** `dateutil.parser._parser.xǁparserǁ_find_hms_idx__mutmut_4`

```diff
-    if idx+1 < len_l and info.hms(tokens[idx+1]) is not None:
+    if idx+2 < len_l and info.hms(tokens[idx+1]) is not None:
```

**Why it survived:** The parse wrapper checks colon-separated times, but does
not directly test dateutil's HMS suffix forms such as `12h`, `12 h`, `30m`, or
`45s`.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact hours/minutes/seconds for strings such as
`"2020-01-01 12h"`, `"2020-01-01 12h30m"`, and `"2020-01-01 45s"`.

### 5. ISO timezone sign handling changed

**Mutant:** `dateutil.parser.isoparser.xǁisoparserǁ_parse_tzstr__mutmut_14`

```diff
-    if tzstr[0:1] == b'-':
+    if tzstr[0:2] == b'-':
```

**Why it survived:** The isoparse wrapper generates timezone offsets, but it
mostly checks the class of the returned `tzinfo`, not the exact sign and offset
seconds. A negative offset can be accepted while still producing a `tzoffset`
object.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact offsets for `"2020-01-01T12:00:00-05:30"`
and `"2020-01-01T12:00:00+05:30"` using
`dt.tzinfo.utcoffset(dt).total_seconds()`.

### 6. ISO time separator state changed

**Mutant:** `dateutil.parser.isoparser.xǁisoparserǁ_parse_isotime__mutmut_14`

```diff
-    has_sep = False
+    has_sep = None
```

**Why it survived:** Separator consistency is an important ISO parsing rule.
The wrapper generates valid basic and extended time forms, but does not assert
that malformed mixed-separator strings are rejected.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert that mixed forms such as
`"2020-01-01T12:3045"` and `"20200101T12:3045"` raise `ValueError`, while
consistent basic and extended forms parse successfully.

### 7. Timezone-name detection broadened

**Mutant:** `dateutil.parser._parser.xǁparserǁ_could_be_tzname__mutmut_1`

```diff
-            len(token) <= 5 and
-            (all(x in string.ascii_uppercase for x in token)
+            len(token) <= 5 or (all(x in string.ascii_uppercase for x in token)
```

**Why it survived:** The parse wrapper draws an `ignoretz` flag, but its
generated date strings do not include named timezones. That leaves timezone-name
detection and `ignoretz=False` behavior mostly untested.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add examples with `UTC`, `GMT`, and explicit `tzinfos`,
and assert both `ignoretz=True` and `ignoretz=False` behavior.

## Overall Assessment

The main weakness is precision on documented parser edge behavior. Gemini's
tests validate many clean success paths, but the mutation survivors show that
the suite does not apply enough pressure to ambiguous or malformed inputs.
Highest-priority gaps:

1. Ambiguous numeric date behavior with default, `dayfirst`, and `yearfirst`
   options.
2. Compact and mixed numeric date/time strings in `parse()`.
3. HMS suffix formats (`12h`, `12h30m`, `30m`, `45s`).
4. Exact ISO timezone offsets, including negative signs and zero-offset UTC
   normalization.
5. Malformed ISO time strings that should raise rather than parse.
6. Named timezone handling and `ignoretz` behavior.

