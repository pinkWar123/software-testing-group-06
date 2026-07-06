# FR-01 Gap Analysis

## Scope
This review looks for FR-01 cases that were not covered by the original equivalence-partition, boundary-value, and robustness-oriented tests. The focus is on edge cases that are easy to miss in a first-pass black-box design.

## Gaps identified and why they were missed

| Gap | Why this was missed | Why it matters for FR-01 |
| --- | --- | --- |
| Leading/trailing whitespace in email | Spec ambiguity | The oracle says the email must be valid, but it does not say whether surrounding whitespace is trimmed or treated as invalid. This is a common normalization edge case that can change the effective input and should be pinned down. |
| Leading/trailing whitespace in password | Spec ambiguity | The password rule says the password must be strong, but it does not state whether leading/trailing spaces count as part of the password or should be rejected as invalid input. |
| Case-insensitive uniqueness check for email | Limitation in my own reasoning | I treated “unique” as a simple exact-match check, but email addresses are commonly treated case-insensitively in practice, so `User@Example.com` and `user@example.com` should be considered the same identity. |
| Unicode/emoji in the name field | Spec ambiguity | The spec requires a name, but it does not define the allowed character set. This leaves a gap around whether Unicode names are supported and whether emoji/symbols should be rejected. |
| Extremely long email or name | Spec ambiguity | The spec provides no maximum length for name or email. Without a stated max, the system behavior for very long inputs is undefined and can reveal storage, UI, or validation problems. |
| Two simultaneous registrations with the same email | Genuine feature complexity | This is not a simple single-request validation case. It tests whether the application handles duplicate submissions correctly under concurrency and whether the backend prevents race conditions. |

## Additional test cases to add

| TC ID | Scenario | Expected result |
| --- | --- | --- |
| TC-FR01-GAP-01 | Register with email ` user@example.com ` (leading and trailing whitespace) and a valid password | Registration should be rejected with a clear validation error; surrounding whitespace should not be silently accepted as a canonical email. |
| TC-FR01-GAP-02 | Register with password ` Abcdef1! ` (leading and trailing whitespace) and a valid email | Registration should be rejected with a clear validation error; whitespace should not be treated as a valid password value. |
| TC-FR01-GAP-03 | Register with email `USER@EXAMPLE.COM`, then register again with `user@example.com` | The second submission should be rejected as a duplicate email because email uniqueness should be case-insensitive. |
| TC-FR01-GAP-04 | Register with name `Nguyễn Văn A 😀` and valid email/password | The system should reject the input with a clear validation error if emoji/symbols are not allowed in the name field; otherwise the product team should explicitly clarify that Unicode names are allowed. |
| TC-FR01-GAP-05 | Register with an extremely long email such as a 300+ character address and a valid password | The system should reject the input with a clear validation error rather than accepting an unbounded value that may break UI or storage. |
| TC-FR01-GAP-06 | Register with an extremely long name (for example 500+ characters) and valid email/password | The system should reject the input with a clear validation error rather than accepting an unbounded value that may break UI or storage. |
| TC-FR01-GAP-07 | Send two registration requests nearly simultaneously for the same email | One registration should succeed and the other should fail with a duplicate-email error; the system should not create two accounts for the same email under concurrent submission. |

## Recommended interpretation
These cases are valuable because they turn “implicit assumptions” into explicit requirements. In particular, the whitespace, case-insensitivity, and concurrency cases are likely to expose real defects even if the current implementation is permissive.
