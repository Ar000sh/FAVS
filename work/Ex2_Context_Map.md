# ShareWise Context Map (Ex2 part 3, DDD slides 45–55)

**Status:** 🟢 first proposal for workshop step 6 (`prep/P1_Team_Workshop_Plan.md`). Builds on the 6 contexts in `work/Ex2_Subdomains_vs_Bounded_Contexts.md`.
Slide 55: "ShareWise Context Mapping? Part of the exercises." The slides give no solution.

---

## 1. What a context map is

- Bounded contexts are modelled **independently**, but they are **not isolated**: the system only works if they interact (slide 45).
- Where they touch, there is a **contract**. The two contexts speak **different languages**, so the key question is: **"which language is used for integration?"** (slide 45).
- A **context map** is the **top-level picture of all bounded contexts and the relationships between them** (slide 54). Every line carries a **pattern** that answers the language question.
- It gives insight on three levels (slide 54):
  - high-level design
  - communication patterns (who works with whom)
  - organisational problems ("all consumers of one team need an ACL against it")

## 2. Why the slides keep talking about "teams"

- **Conway's law** (slides 11, 15): a system's structure mirrors the communication structure of the organisation. Handwritten on slide 15: "From this, ultimately **services are defined and teams are formed**."
- DDD assumes **one team owns one bounded context**. Slide 48 calls this a "core principle".
- So a relationship between two contexts is really a relationship between **the teams that own them**. The pattern depends on:
  - **how well the teams communicate**
  - **who has the power** to dictate the contract (upstream or downstream)
- The 3 categories follow from that:

| Category | Team situation | Patterns |
|---|---|---|
| **Cooperation** (slide 46) | Well-established communication: same team, or dependent goals ("one succeeds only if the other does") | Partnership, Shared Kernel |
| **Customer-Supplier** (slide 49) | Both teams can succeed independently → **power imbalance**. Upstream (U) = supplier, downstream (D) = consumer | Conformist, Anti-Corruption Layer, Open-Host Service |
| **Separate Ways** (slide 53) | Teams won't or can't work together | none; duplicate instead |

**What this means for us (note:):**
- We are **one student team**, so strictly every internal link would be "cooperation".
- But the project's path is modular monolith → **microservices (P3)**, where each context *could* get its own team. So we map as if each context had its own owner.
- **External systems are real "other teams"** we have no power over: Keycloak and the email provider. That is where Conformist and ACL apply for real.
- Say this explicitly in P1. It shows we understand that the patterns are organisational, not just technical.

## 3. The patterns: when and why

| Pattern | Notation | Who has the power | Use it when | Don't use it when |
|---|---|---|---|---|
| **Partnership** (47) | line labelled "Partners" | nobody dictates; both adapt immediately | same or closely coordinated team, dependent goals | geographically dispersed teams |
| **Shared Kernel** (48) | overlapping ovals | shared, no imbalance | a **small** compiled library holds the contract; same team as a discipline | the kernel grows; teams can't synchronise (a change breaks the other build) |
| **Conformist** (50) | arrow "Conforms" from D to U | upstream: "take it or leave it" | upstream model is an **industry standard** or good enough for D | D is core and the upstream model would distort it |
| **Anti-Corruption Layer** (51) | "ACL" box on the **downstream** edge | upstream, but D refuses to adapt | D is **core**; U is legacy, changes often, or is huge and only part is needed | the translation costs more than it protects |
| **Open-Host Service** (52) | "OHS" box on the **upstream** edge | **consumers**; U wants to serve them well | U has several consumers; U publishes a stable **published language** (e.g. OpenAPI) separate from its internal model | only one consumer, same team, changes together |
| **Separate Ways** (53) | no line | – | communication problems; generic library (e.g. **logging**); models too different | **never for core** subdomains |

## 4. Applied to ShareWise

### 4.1 The relationships

| # | Upstream (U) → Downstream (D) | What flows | Pattern | Why (🟢) |
|---|---|---|---|---|
| 1 | **Identity** → **Group** | logged-in user: `UserId`, display name (from the OIDC token) | **Conformist** | Keycloak/OIDC is an **industry standard** (slide 50). We only need the user ID and name, so adopting its model costs nothing. Group is supporting, so there's no core model to protect. |
| 2 | **Group** → **Expense** | members of a group and since when; group status OPEN/CLOSED | **OHS** on Group + **ACL** on Expense | **OHS:** Group has several consumers (Expense, Settlement), so it publishes one stable membership interface/events (published language). **ACL:** Expense is **core** (slide 51). It translates "Member" into its own concept "Participant" and doesn't let Group's model (roles, invitations) leak in. |
| 3 | **Group** → **Settlement** | members; `GroupClosedForSettlement`, `GroupReopened` | **OHS** on Group + **ACL** on Settlement | Same reasons as #2. Settlement is core and translates Member into Debtor/Creditor. |
| 4 | **Expense** ↔ **Settlement** | `ExpenseRecorded / Corrected / Removed` → balances recalculated | **Partnership** | Both core, **dependent goals** (slide 46): balances are meaningless without expenses, and closing for settlement must block expenses. Both change together (e.g. a new split type changes both), so we coordinate ad hoc. |
| 4b | Expense ∩ Settlement | `Money`, `GroupId`, `MemberId` | **Shared Kernel** (small) | Both need exactly the same money arithmetic (cents, rounding) and IDs. Keep it **tiny**, only the integration contract (slide 48). Anything bigger stays in each context. |
| 5 | **Settlement** → **Group** | "is this member's balance 0?" (leave/remove rule R11); `AllBalancesSettled` → archive | **Conformist** (Group conforms) | Group is supporting. It just accepts Settlement's answer and event as they are and doesn't need its own model of balances. |
| 6 | **all contexts** → **Activity** | published domain events | **Conformist** | Activity is a read model (supporting). It shows the events as they are; translation would add nothing. |
| 7 | **all contexts** → **Notification** | domain events → messages | **Conformist** | Same as #6: it reacts to the published events. |
| 8 | **Notification** → **email/push provider** (external) | send message | **Conformist** | Provider API/SMTP is a standard; Notification is a thin generic adapter. |
| 9 | Logging, validation helpers | – | **Separate Ways** | Slide 53, reason 2: a generic library is cheaper to use locally in each context than as a shared service. |

🟢 Exchange rates and payment transfer were dropped on 14.10, so the former ECB → Expense ACL edge is gone.

### 4.2 The map

```
                         ┌──────────────────────┐
                         │ Identity (Keycloak)  │ generic · external
                         └──────────┬───────────┘
                                   U│
                                    │ Conforms                      (1)
                                   D▼
  Settlement ─U── Conforms ──D─►┌──────────────────────┐
  (balance 0? / all settled)(5) │        Group         │ supporting
                                └──[OHS]────────[OHS]──┘
                                   U│            U│
                               (2)  │            │  (3)
                                   D▼            ▼D
                          ┌──[ACL]──────┐   ┌──[ACL]────────┐
                          │   Expense   │═══│  Settlement   │ core + core
                          │             │(4)│               │ Partners
                          └─────────────┘   └───────────────┘
                                    ◖ Shared Kernel: Money, GroupId, MemberId ◗ (4b)

  All contexts ─U── published domain events ── Conforms ──D─► Activity, Notification   (6)(7)
  Notification ─D── Conforms ──U─ email/push provider                                    (8)
  Logging: Separate Ways (each context uses the library locally)                         (9)
```

### 4.3 What the map tells us (slide 54 reading)
- **Group is the main upstream** (2 OHS). That's why it should publish a stable interface: changes there hit two core contexts.
- **Both core contexts protect themselves** with ACLs against the supporting Group model. That's slide 51's main rule, and a good P1 sentence.
- **The only cooperation is between the two cores.** They are the most tightly coupled pair, so they're the last candidates to split into separate services later (P3), or they would be extracted together.
- **Group ↔ Settlement goes in both directions** (#3 and #5). Inside the monolith we break the cycle with **events**: Settlement publishes `AllBalancesSettled`, Group subscribes. Expect this as a discussion question.

## 5. Questions to expect in P1
1. Why ACL on Expense but Conformist on Activity? → Core vs supporting (slide 51).
2. Why OHS on Group? → several consumers, stable published language (slide 52).
3. You are one team. Why not Partnership everywhere? → Section 2: we design for the later team/service split; external systems are real other teams.
4. Doesn't Shared Kernel break "one team per context"? → Yes (slide 48). That's why it's kept tiny and only between the two cores.
5. Where would you use Separate Ways? → Logging (slide 53). Never between core contexts.

## Open decisions for the workshop
- [ ] Expense–Settlement: Partnership only, or Partnership + Shared Kernel (Money, IDs)?
- [ ] OHS + ACL on #2/#3, or simpler Partnership (we are one team)? Recommendation: keep OHS + ACL, because it's the more defensible answer.
- [ ] Identity → Expense/Settlement directly, or only through Group (MemberId)? Depends on the UserId vs MemberId decision.
