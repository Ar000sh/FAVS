# Subdomains vs Bounded Contexts: how they fit together (ShareWise)

**Visual:** `work/Ex2_Subdomains_vs_Bounded_Contexts.html` (open in a browser).
**Status:** the bounded contexts here are a 🟢 **first proposal** for the workshop (step 4 in `prep/P1_Team_Workshop_Plan.md`), not a final decision.

---

## 1. The difference in one table (DDD slides 21, 29, 41, 43)

| | Subdomain | Bounded context |
|---|---|---|
| Space | **Problem space**: the business as it is (slide 29) | **Solution space**: our software model (slide 29) |
| How you get it | **Discovered**: it exists whether we build software or not (slide 43) | **Designed**: we choose the boundary; a strategic decision (slide 43) |
| Question it answers | "What does the business do, and how important is each part?" | "Where does one model with one language stay consistent?" |
| Defined by | Area of business activity (slide 21) | A consistent model + ubiquitous language (slide 41) |
| Used for | **Priorities**: where to invest (core), what to buy (generic) | **Modules** of the monolith → later services → teams (Conway, slide 15) |
| Typed? | Yes: core / supporting / generic | No type; it *inherits* importance from the subdomain(s) it implements |

**Key sentence:** *Subdomains tell us what matters; bounded contexts tell us where the model boundaries go. A context implements one or more subdomains, and they need not be 1:1.*

(note:) The slide-21 retailer diagram shows them 1:1 ("each coloured area is a subdomain (bounded context)"). That is the ideal case, not a rule. Slide 43 separates the two terms explicitly.

---

## 2. ShareWise: subdomains → bounded contexts

```
 PROBLEM SPACE (discovered)                       SOLUTION SPACE (designed)
 ──────────────────────────                       ─────────────────────────
 CORE
  Expense Sharing ─────────── 1:1 ──────────────► Expense Context
  Settlement ──────────────── 1:n ──────────────► Settlement Context
              └───────── (close/archive status) ─► Group Context
 SUPPORTING
  Group & Membership ──────── 1:1 ──────────────► Group Context
  History & Reporting ─────── 1:1 ──────────────► Activity Context (read model)
 GENERIC
  Identity & Access ───────── bought ───────────► Identity Context (Keycloak / Spring Security)
  Notification Delivery ───── 1:1 ──────────────► Notification Context (adapter to SMTP / push)
```

| Subdomain | Type | Bounded context | Mapping | Why this cut (🟢) |
|---|---|---|---|---|
| Expense Sharing | Core | **Expense** | 1:1 | Own language (payer, participant, share, split strategy) and many invariants (slide 69) |
| Settlement | Core | **Settlement** + status in **Group** | 1:n | Balances, plan and payments live in Settlement. The *status* OPEN/CLOSED/ARCHIVED belongs to the Group aggregate, so the closing rules touch the Group context too |
| Group & Membership | Supporting | **Group** | 1:1 | Member, role, invitation: one consistent model |
| History & Reporting | Supporting | **Activity** | 1:1 | Pure read model built from events of the other contexts |
| Identity & Access | Generic | **Identity** | bought | Off-the-shelf (slide 25: "Active Directory"). We only integrate it |
| Notification Delivery | Generic | **Notification** | 1:1 | Thin adapter around an email/push service |

**What the table shows:**
- **1:1** is the normal case (Expense, Group, Activity, Notification).
- **1:n**: one subdomain spread over two contexts (Settlement + Group status). This is the decision to defend: *"the status is a property of the group, but the rules for changing it come from settlement."*

🟢 **Dropped (team decision 14.10):** Currency Exchange Rates and Payment Transfer are no longer subdomains, so they get no context and no edge in the map. One currency per group, and settlement payments are only recorded (the money moves outside the app).

---

## 3. Why the boundaries are where they are: one person, actual data (slide 40)

Alice from "Mallorca 2027" is the **same person**, but each context models Alice differently and stores different data about Alice:

| Context | Alice is a… | What this context knows (Mallorca data) | What it does **not** know |
|---|---|---|---|
| Identity | **User** | account, email, password, display name "Alice" | groups, expenses, money |
| Group | **Member** (role ADMIN) | member of "Mallorca 2027" since day 0, created the group; other members: Bob (FORMER_MEMBER after day 5), Carol, David, Eve (joined day 3) | what anyone paid |
| Expense | **Payer** / **Participant** | payer of Hotel €900 and Farewell dinner €250; participant in Hotel 225, Dinner 50, Rental car 140, Boat 100, Groceries 12, Farewell 50 = **€577 owed** | password, role |
| Settlement | **Creditor** | balance **+573** (paid 1150 − owed 577) → **+371** after Bob pays €202 → plan: David → Alice €371 | which expense was the hotel |
| Activity | **Actor** in the feed | "Alice recorded Hotel €900", "Alice closed the group for settlement" | – (read only) |
| Notification | **Recipient** | "Bob paid you €202, please confirm" | – |

Each row is a different model of the same person with its own language. **That is the reason to cut there** (slide 39: one global model fails, "Lead" example).
The contexts link the person only by **ID** (UserId / MemberId), never by sharing one big `User` class (aggregate rule 3, slide 67).

### Same word, different meaning
| Word | Meaning in context A | Meaning in context B |
|---|---|---|
| "Group" | Group: members, roles, invitations, status | Expense / Settlement: only a `GroupId` that scopes the expenses and balances |
| "Payment" | Settlement: a recorded settlement payment (PENDING → CONFIRMED) | Expense: the payer's original outlay ("Alice paid the hotel") |
| "Close" | Group: status change OPEN → CLOSED_FOR_SETTLEMENT | Expense: "no new or corrected expenses allowed" |

---

## 4. How the contexts depend on each other (preview for the context map, step 6)

| From → To | What flows | Example (Mallorca) |
|---|---|---|
| Identity → Group | who is logged in (UserId) | Alice opens the invite page |
| Group → Expense | members of the group (payer/participant check) | Eve can be a participant from day 3 on |
| Expense → Settlement | `ExpenseRecorded / Corrected / Removed` | Dinner corrected 180 → 200: Bob +15 (paid +20, share +5), Alice/Carol/David −5 each |
| Settlement → Group | `AllBalancesSettled`, "balance of member = 0?" | Bob may leave after paying €202; last confirmation → archive |
| all → Activity, Notification | domain events | "Carol's taxi was refused: group closed" |

The patterns (Partnership, ACL, Conformist, OHS, …) are chosen in the workshop (step 6).

---

## Open decisions for the workshop
- [ ] Group status in Group (this proposal) or in Settlement?
- [ ] Activity as its own context, or a read model inside Settlement?
- [ ] Does Expense store `UserId` (slide 64) or `MemberId` (slide 40 logic)?
