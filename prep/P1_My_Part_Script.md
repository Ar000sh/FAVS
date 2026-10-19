# P1 (20.10): my part – Settlement context, Shared types, Account

Speaker 2, about 5 minutes (~650 words). Before me: Group + Expense.
Diagram: `work/ShareWise_Domain_Model.drawio`. *[Italics in brackets = where to point.]*
Slides: 02.DDD deck. Only cite a slide when the sentence really is on it.

---

## 1. Hand-over (≈ 20 s)

"Thanks. We've seen the Group and Expense contexts. I'll present the rest of the domain: the **Settlement context**, the **shared types** and the **Account context**.

That gives us three more aggregates: **GroupLedger**, **SettlementPayment** and **Account**. *[point at the three dashed boxes]*

And like before, the aggregates don't call each other. They talk through **domain events**, and screens get their data from **read models**."

## 2. GroupLedger (≈ 2 min) – the main part

"Let's start with the **GroupLedger**, the core of the settlement context. *[point at GroupLedger]*

We went with the more complex option here. Instead of storing one balance number per person, every group has a **ledger**, like an accounting journal. This idea is from the lecture: on the Event Sourcing slide, a ledger is the example of an *append-only log of transactions*, where the balance is always derived from the entries (slide 72). I know it might feel like overkill for such a small context, but we wanted to try it out and see how it looks.

The ledger consists of **LedgerEntries**. *[point at LedgerEntry]* One entry is one booking: **who**, **how much plus or minus**, **what type**, **which expense or payment caused it**, and **when**. Entries are **never changed or deleted, only added**.

How do bookings get in? Through **events**:

- **Expense recorded.** Say Alice pays the hotel, 900 euros, for four people. The Expense context publishes *ExpenseRecorded*. The ledger listens and books: Alice **plus 900**, and each of the four **minus 225**.
- **Expense corrected.** The dinner was 200 and not 180. We don't overwrite anything. The ledger **reverses** the old entries and books the new ones. So the history still shows what happened.
- **Expense removed.** Same idea: only a reversal.

A person's **balance is simply the sum of their entries**. And because every booking adds up to zero, **all balances together are always zero**. That's a nice built-in check."

## 3. SettlementPayment (≈ 1 min)

"The second aggregate is the **SettlementPayment**. *[point at SettlementPayment]* This is when someone actually pays back money, in cash or by bank transfer outside the app.

The **debtor records** it, for example Bob: 'I paid Alice 75 euros'. It's **PENDING**. Then the **creditor confirms** it, and it becomes **CONFIRMED**. Or the creditor rejects it. When recording, the payment checks that Bob doesn't pay more than he owes.

Only when the payment is confirmed is *SettlementPaymentConfirmed* published, and the ledger books it: Bob **plus 75**, Alice **minus 75**. Now Bob is at zero."

## 4. Read models + events back to Group (≈ 45 s)

"From the ledger we build two **read models**. *[point at the pink boxes]* These are read-only views for the screens, the CQRS idea from the lecture (slide 78):

- **MemberBalance**: each person's balance.
- **SettlementPlan**: who should pay whom, with as few payments as possible.

And the ledger also publishes events back to the **Group**. When Bob's balance reaches zero, it publishes *MemberBalanceStatusChanged*, and the Group marks Bob with *hasZeroBalance*. Only then can Bob leave the group. When everyone is at zero, *AllBalancesSettled* is published and the group can be archived."

## 5. Shared types (≈ 20 s)

"Down here are the **shared types**. *[point at the grey box]* Money, Currency, GroupId and UserId. Every context uses them. Aggregates **only store IDs** of other aggregates, for example the Expense stores a GroupId and not the whole Group (aggregate rule 3, slide 67)."

## 6. Account (≈ 40 s)

"Finally, the **Account context**. *[point at Account]* This is a **generic subdomain**: every app needs login, and it doesn't make ShareWise special. So the lecture's advice is **buy, don't build** (slide 25).

Our idea is to use an identity provider like **Supabase Auth** or Keycloak. It handles registration, login, passwords and email verification. Our Account only keeps what ShareWise needs: the **UserId**, which is the ID the provider creates, plus the email, the display name and a status. All other contexts only use this UserId.

The **UserProfile** read model gives the other contexts the display names, so they can show 'Alice' instead of an ID.

That's it from my side. Thanks!"

---

## If they ask (short answers)

| Question | Answer |
|---|---|
| Why a ledger and not just a balance field? | History of corrections is kept, every balance is explainable, sum is always 0. Slide 72: ledger = append-only, audit-safe. |
| Isn't it overkill? | For a small app, yes, a bit. We wanted to try the pattern. A simple balance field would also work. |
| LedgerEntry never changes, why an entity? | Each booking is its own fact with an ID; reversals refer to it. Slide 66: entities are *often* mutable, not always. |
| Doesn't the ledger grow forever? | One ledger per group, hundreds of entries, not millions. Balances come from the read model. |
| Why is the balance updated later and not right away? | Eventual consistency between aggregates, rule 4 on slide 67. |
| Why is SettlementPayment its own aggregate? | It has its own lifecycle (PENDING → CONFIRMED/REJECTED) and its own rules; keeps the ledger small (rule 2). |
| Why no events in Account? | Nobody reacts to them. Events are for subscribers (slide 71). |
| What is DebtWaived / waive()? | The creditor can forgive the debt. Honest: still open in our team, not in our requirements yet. |
| Why is the plan a list of DirectedDebt and not of SettlementPayments? | The plan is a **suggestion** (bill), the payment is a **fact** (bank transfer). See §B below. |
| Are read models necessary at all? | For the ledger yes, it only stores bookings (slide 78). The others are for decoupling. See §C. |
| Why not use the Account entity directly? | Other contexts must not depend on another context's aggregate. UserProfile is Account's read-only window. See §C. |
| Do you use event sourcing? | Partly: only the idea, in the ledger. See §D. |

---

## Background for questions

### A. Where the plan comes from
- `GroupLedger.projectSimplifiedPlan()` computes the plan. It works from the **balances** (sum of the ledger entries), not directly from the expenses. The balances already include expenses, corrections and confirmed payments.
- The result is the read model **SettlementPlan** = list of **DirectedDebt** (fromDebtor, toCreditor, amount).

### B. DirectedDebt vs SettlementPayment
| | DirectedDebt (in the plan) | SettlementPayment |
|---|---|---|
| Meaning | Suggestion: "David should pay Alice €371" | Fact: "David says he paid Alice €200" |
| Lifetime | Recomputed whenever something changes | Created only when someone actually pays |
| Identity / status | None (value object) | ID + PENDING → CONFIRMED / REJECTED |
| Amount | Full open debt | Can be partial |

Why not a list of SettlementPayments in the plan:
1. It would create payments that never happened, and every new expense would force deleting or changing them.
2. Partial payments don't fit (plan €371, paid €200).
3. A read model shouldn't contain other aggregates, only their IDs (rule 3, slide 67).

How they connect: "Settle up" next to a DirectedDebt prefills `SettlementPayment.record(...)` (J8). **The plan suggests, the payment records what really happened.**

> "The plan is like the bill, the settlement payment is the bank transfer. You can pay a bill in parts, and the bill changes when something new is added."

### C. Read models: why, alternatives, one by one
**Main reason (slide 78):** with an event-sourced / append-only store, the state "cannot be flexibly queried". CQRS answers with read models. Our ledger is exactly that: it only has bookings, not the answer to "what is Bob's balance". **Ledger = write side, read models = query side.**

> "Because our ledger only stores bookings, we need read models to answer questions like 'what is Bob's balance' or 'who pays whom'. The ledger writes, the read models answer. Technically a read model can simply be a query, not a separate database."

**Alternatives we could have used:**
| Alternative | Pro | Con |
|---|---|---|
| Balance field per member, no ledger | Very simple, no read models | Corrections overwrite history, balances can't be explained |
| Query method on the aggregate (`getBalances()`) | No extra concept | Mixes writing and reading, loads the whole ledger for every screen |
| Plain DB query (`SUM … GROUP BY userId`) | Very little code (likely how we implement it in Ex4) | Really just a read model without the name |
| Ask the other context directly instead of keeping a copy | Simple, always current | Tight coupling, breaks when we split into services (P3) |

Slide 79: start with a **synchronous projection**, add async only if needed. So in the monolith, MemberBalance can simply be a query.

**One by one:**
- **MemberBalance:** needed. Balance = sum of entries. Used by the balance screen (J7), SettlementPayment (open debt, R17) and Group (leave only at 0).
- **SettlementPlan:** needed. Pure calculation from all balances, never stored as a fact.
- **GroupMembershipView** (Expense context): *not* about computing, Group already has the data. Reason = **context boundary**. Expense must check group rules (R2/R3/R5/R6) but may only hold the groupId (rule 3). It keeps its own small copy, fed by Group's events (rule 4, eventual consistency).
  - Alternative: the application service asks Group directly ("is Bob a member?"). In a monolith that would be enough and always current.
  - Honest: the view is a choice for **decoupling**, so the contexts stay independent and can become services later. Downside: it can lag a moment.
- **UserProfile** (Account context): why not the Account entity directly?
  1. Account is another context's aggregate. Loading it would couple everyone to its internals (email, status, …).
  2. Aggregates are for changes, not for reading lists of names (`findProfiles(Set<UserId>)` gets 5 names at once).
  3. It's Account's public, read-only "published language" (OHS idea, slide 52).
  - Honest: technically just a query that Account offers. "Read model" here means read-only.

> "Other contexts only know the UserId. To show names they use UserProfile, a read-only view that Account offers. They never touch the Account aggregate, so Account can change internally, or be replaced by Supabase, without breaking them."

**If asked "isn't that overkill?":**
> "For this size, a bit. The simple alternative is one balance field per member, but then corrections overwrite the history and we can't explain a balance. We wanted to try the pattern."

**Weak spot:** Group has `hasZeroBalance` (copy via event) **and** a "reads" line to MemberBalance. Answer: "hasZeroBalance is what Group uses for its rule; the line only means the balance can be shown on the group screen."

### D. Event sourcing (slide 72)
**What the slide says:**
- Every change in state is **stored as a domain event**. The current state itself is not stored.
- The **event store** is the single source of truth.
- Current state = **replay** the events ("rehydrate").
- Adds the **dimension of time**: you can see the state at any point in the past.
- Example on the slide: the **financial ledger**, an append-only log of transactions; the balance is derived by replaying it. **Audit-safe.**
- Diagram: a sales lead as an event stream (Initialized → StateSet → Contacted → ContactDetailsUpdated → Contacted/Converted).

**Normal vs event sourcing (Expense example):**
| Normal storage | Event sourcing |
|---|---|
| Row: Dinner, €200, CORRECTED (old value overwritten) | Stream: ExpenseRecorded(€180) → ExpenseCorrected(€200); state = replay |

**When to use it:** core subdomain that needs history / audit, usually **with CQRS**, because a pile of events can't be queried directly (slide 78). That's our ledger + read models.

**What we actually do:**
- The **idea** only, in the **ledger**: append-only bookings, balance derived from them, like the slide's ledger example.
- **Not full event sourcing:** Group, Expense, SettlementPayment and Account store their current state normally. Ledger entries are bookings, not the stored events of an aggregate.

> "Partly. We use its idea in the ledger: append-only bookings, and the balance is derived from them, like the ledger example on slide 72. The other aggregates store their current state normally. Full event sourcing everywhere would be too much for this project."

---

⚠ **Before presenting, check with the team:**
- Which Account version goes on the slide: the team version (with password, tokens and Hasher) or our proposal with Supabase? Section 6 above describes the proposal. If the team version is shown, replace the middle paragraph with: "For now we modelled login ourselves, with a password hash and tokens for email verification and password reset. Later we could replace it with a provider like Keycloak, because the other contexts only know the UserId."
- The main diagram also has a "reads" line from Group to MemberBalance. If asked: hasZeroBalance is the mechanism; the line is only for showing balances.
