# Human Review

Review the candidate invariants below. Delete rejected invariants, revise weak ones, and leave only accepted invariants in this file. Then rerun the same command. The script will automatically continue from this review file.

1. **Property:** `dot` returns a scalar, not an array, when both inputs are scalars or when both inputs are 1-D arrays; if `out` is provided, that same output object is returned.
   - **Evidence from source:** The docstring states: “If `a` and `b` are both scalars or both 1-D arrays then a scalar is returned; otherwise an array is returned. If `out` is given, then it is returned.”
   - **User-facing interpretation:** For scalar×scalar and vector·vector cases, users should expect a scalar result. Supplying `out` changes where the result is written, not the computation’s meaning, and the function returns that `out`.
   - **Preconditions / input domain:** Inputs must be valid for `np.dot`; for the `out` part, `out` must satisfy NumPy’s stated requirements (correct dtype/shape, C-contiguous, exact expected kind).
   - **Important edge cases:** Python scalars; 0-D NumPy arrays; empty 1-D arrays of matching length; `out` provided for scalar-like results.
   - **Why it matters:** Result shape/type stability is a central API guarantee and easy to break in refactors that accidentally wrap scalar outputs into 0-D arrays or ignore `out`.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

2. **Property:** When either argument is 0-D, `dot(a, b)` is semantically equivalent to elementwise multiplication `a * b`.
   - **Evidence from source:** The docstring explicitly says: “If either `a` or `b` is 0-D (scalar), it is equivalent to `multiply`…”
   - **User-facing interpretation:** Scalar involvement does not trigger matrix or contraction behavior; it behaves like ordinary multiplication.
   - **Preconditions / input domain:** At least one of `a` or `b` is scalar / 0-D and the multiplication is otherwise valid under NumPy broadcasting/type rules.
   - **Important edge cases:** One operand Python scalar and the other high-dimensional array; both operands 0-D; complex scalars; boolean scalars.
   - **Why it matters:** This distinguishes `dot` from generalized tensor contraction in a way users rely on, especially in mixed scalar/array code.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

3. **Property:** For 1-D inputs, `dot(a, b)` computes the non-conjugating inner product, so for complex vectors it differs from `vdot(a, b)` exactly by the absence of conjugation of the first argument.
   - **Evidence from source:** The docstring says for 1-D arrays it is the inner product “without complex conjugation,” and gives the explicit example `np.dot([2j, 3j], [2j, 3j]) == (-13+0j)`. The `See Also` section contrasts `vdot` as “Complex-conjugating dot product.”
   - **User-facing interpretation:** `dot` is not the Hermitian inner product. Complex values are multiplied directly, not with conjugation on the first input.
   - **Preconditions / input domain:** Both inputs are 1-D and have equal length.
   - **Important edge cases:** Purely real vectors (where `dot` and `vdot` coincide); purely imaginary complex vectors (where the distinction is obvious); empty vectors.
   - **Why it matters:** This is a subtle but important semantic guarantee that commonly causes user confusion and implementation mistakes.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

4. **Property:** For higher-dimensional inputs, `dot` contracts the last axis of `a` with the second-to-last axis of `b` (for `b.ndim >= 2`), so the output shape is `a.shape[:-1] + b.shape[:-2] + b.shape[-1:]`.
   - **Evidence from source:** The docstring states: “If `a` is an N-D array and `b` is an M-D array (where `M>=2`), it is a sum product over the last axis of `a` and the second-to-last axis of `b`: `dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])`.”
   - **User-facing interpretation:** `dot` is neither full broadcasting multiplication nor generic contraction over arbitrary axes; it uses one specific pair of axes.
   - **Preconditions / input domain:** `a.ndim >= 1`, `b.ndim >= 2`, and `a.shape[-1] == b.shape[-2]`.
   - **Important edge cases:** `a` 1-D with `b` 2-D+; `a` N-D with `b` exactly 2-D; singleton contracted dimensions; large leading batch dimensions.
   - **Why it matters:** This is the core semantic rule of `dot` for arrays and strongly constrains both result shape and values.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

5. **Property:** `dot` raises `ValueError` when the contracted dimensions are incompatible: specifically, when `a.shape[-1] != b.shape[-2]` in the general array case.
   - **Evidence from source:** The docstring says: “Raises `ValueError` if the last dimension of `a` is not the same size as the second-to-last dimension of `b`.”
   - **User-facing interpretation:** Shape mismatch in the contraction axes is a hard error, not something resolved by broadcasting, flattening, or partial computation.
   - **Preconditions / input domain:** Inputs are in a non-scalar case where contraction axes are defined and comparable; excludes cases where scalar multiplication semantics apply.
   - **Important edge cases:** 1-D vs 1-D different lengths; N-D vs 1-D mismatched last dimension; N-D vs M-D (`M>=2`) mismatched contraction axes.
   - **Why it matters:** Error behavior is part of the API contract and catches accidental changes toward broadcasting or silent flattening.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending
