# AI Critique — HW02
## Domain Testing on EShop

During this homework, I used AI mainly to generate domain testing ideas, boundary value test cases, bug hypotheses, and some Selenium test structures. However, the AI output was not always reliable, so I have to review many parts very carefully.

One problem was in Feature D for the mobile app. At first, the AI mixed many different mobile behaviors together, like login, coupon, checkout, and quantity input into only one feature. This makes the scope became too big and did not match with the assignment requirement, because Pool D still needs one feature.

Another issue is AI wrote some "Actual Result" and "Verdict" cells as if the mobile test cases were already executed. But in the reality, they were only inferred from source code. This is a hallucination because the AI presented guessed runtime behavior like a real evidence. Also, the AI missed some important edge case especially the difference between input 1.9 and 0.9, where `parseInt()` causes different behaviors around the boundary.

To solve this, I had to narrow the feature scope, separate analysis-only results from executed evidence, and add the missed boundary cases. Then, I ran real Selenium tests on the Expo web build to verify what can actually be observed.

In conclusion, I learned that AI is very useful for fast brainstorming and finding suspicious areas, but we should never trust it to replace real execution results or careful human review