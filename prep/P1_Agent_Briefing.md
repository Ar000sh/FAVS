# Briefing for the coaching agent: my part in P1 (20.10.26)

You are helping me (a master's student) prepare and rehearse **my part of a team presentation today**. Read this file fully. Then go through my part with me, quiz me, and keep me up to date on what I still need to know. Keep explanations **simple and short**. English, but keep German terms where they come up.

Attached with this file:
- `ShareWise_Domain_Model.png`: the team's class diagram (main version, the team edits it in draw.io).
- `ShareWise_Domain_Model_Account_External_IdP.png`: my **proposal** for the Account context (Supabase/Keycloak instead of our own login). The other contexts are identical to the main version.
- `P1_My_Part_Script.md`: my ~5-minute speaking script + Q&A table + background sections A–D. **This is the main material. Coach me on it.**

---

## 1. The course and the project
- Module **FAVS** ("Fortgeschrittene Aspekte verteilter Systeme – Cloud-Native Computing"), Hochschule Hannover, master, WS 26/27, lecturer Hans Grönniger.
- Semester project **ShareWise**: "shared expenses made simple" (like Splitwise/Tricount). Groups record shared expenses, split them, see who owes whom, record settlement payments, close and archive groups.
- Path over the semester: DDD model → modular monolith (Spring Boot + Next.js) → containers → CI/CD → cloud → microservices with RabbitMQ, outbox, Saga.
- **Presentation P1 today: "modular architecture of ShareWise"**, based on exercises 1–3: subdomains, bounded contexts, ubiquitous language, entities/value objects, aggregates, domain events, (hexagonal) architecture. Attendance and active discussion are graded.
- Main lecture source: the **02.DDD slide deck**. Slide numbers below refer to it. **Never present something as lecture content if it is not on the slides.**

## 2. Who presents what
- Speaker 1 (before me): **Group context** and **Expense context**.
- **Me (speaker 2), about 5 minutes: Settlement context, Shared types, Account context.**

## 3. The model in short (what the diagram shows)
Five aggregates, each a dashed box: **Group, Expense, GroupLedger, SettlementPayment, Account.** Aggregates reference each other **by ID only** and talk through **domain events** (publish/subscribe). Screens and other contexts read **read models** (CQRS).

### Group context (speaker 1, only for orientation)
- Group (root) with Membership and Invitation. Lifecycle OPEN → CLOSED_FOR_SETTLEMENT → ARCHIVED.
- `Membership.hasZeroBalance` = local copy, set by the event `MemberBalanceStatusChanged` from the ledger. A member can only leave at balance 0.
- Read model **GroupMembershipView** (groupId, isOpen, activeMembers, admins): Expense's own copy of the group, fed by Group's events.

### Expense context (speaker 1, only for orientation)
- Expense (root): paidBy, recordedBy, title, totalAmount: Money, splitStrategy EQUAL/EXACT/PERCENTAGE, status ACTIVE/CORRECTED/REMOVED. ExpenseShare = value object (participantId, owedShare).
- Publishes ExpenseRecorded, ExpenseCorrected, ExpenseRemoved.

### Settlement context (MY PART)
**Aggregate GroupLedger**: one per group, an accounting journal.
- `groupId`, list of **LedgerEntry** (entity): id, userId, deltaAmount: Money, type, referenceId, occurredAt.
- LedgerEntryType: EXPENSE_PAID, EXPENSE_OWED, EXPENSE_REVERSAL, PAYMENT_SENT, PAYMENT_RECEIVED, DEBT_WAIVED.
- Entries are **append-only**: never changed, never deleted. A correction = reversal of the old entries + new entries.
- Subscribes to ExpenseRecorded/Corrected/Removed and SettlementPaymentConfirmed/DebtWaived, with one `append…()` method per event.
- Publishes **MemberBalanceStatusChanged** (a member's balance reached 0 or left it) and **AllBalancesSettled**. Group subscribes to both.
- `projectBalances()` → read model **MemberBalance** (userId, netBalance). `projectSimplifiedPlan()` → read model **SettlementPlan** = list of **DirectedDebt** (fromDebtor, toCreditor, amount), with the minimum number of payments.
- Balance of a person = sum of their entries. Sum over all members is always 0.
- The idea comes from **slide 72 (Event Sourcing)**: "a ledger is an append-only log of transactions", balance derived from it, audit-safe.

**Aggregate SettlementPayment**: a real payback outside the app (cash/bank).
- id, groupId, fromDebtor, toCreditor, amount, status PENDING → CONFIRMED / REJECTED / WAIVED.
- `record(groupId, fromDebtor, toCreditor, amount, openDebt)`: debtor records it; can't pay more than the open debt. `confirm()` / `reject()` by the creditor. `waive()` = creditor forgives (⚠ still open in the team, not in our requirements).
- Only a CONFIRMED payment reaches the ledger.

**Worked example (verified with a script):**
1. Hotel €900 paid by Alice for A, B, C, D → Alice +900, each −225 → Alice +675, Bob/Carol/David −225.
2. Dinner €180 paid by Bob for all four → Alice +630, Bob −90, Carol −270, David −270.
3. Dinner corrected to €200 → reverse old (Bob −180, each +45), book new (Bob +200, each −50) → Alice +625, Bob −75, Carol −275, David −275.
4. Bob pays Alice €75, Alice confirms → Bob 0, Alice +550 → ledger publishes MemberBalanceStatusChanged(Bob) → Group sets hasZeroBalance → Bob may leave.

### Shared types (MY PART)
Money (amount: BigDecimal, currency: Currency), Currency, GroupId, UserId. Used by all contexts. Aggregates store only IDs of other aggregates (rule 3, slide 67). Only Expense draws its "references by ID" lines as the example; all other ID attributes work the same way.

### Account context (MY PART)
- Generic subdomain → "buy, don't build" (slide 25).
- **Team version (main diagram):** own login with PasswordHash, RawPassword, Hasher, AccountToken (email verification / password reset), EmailSender and many events.
- **My proposal (second picture):** Supabase Auth / Keycloak does registration, login, passwords, email verification. Account keeps only `id: UserId` (= the user id the provider creates), email, displayName, status (ACTIVE/DEACTIVATED), registeredAt. Methods: `registerFromIdentityProvider(UserId, Email, DisplayName)` on the first login, `changeDisplayName()`, `deactivate()`. **No domain events**, because no other context reacts to them. The frontend calls Supabase directly; the backend only checks the token (JWT) and reads the UserId.
- Read model **UserProfile** (userId, displayName, isActive) with `findProfiles(Set<UserId>)`: other contexts get names from it, never from the Account aggregate.
- ⚠ **Open: which Account version is shown today.** The script describes the proposal and has a replacement paragraph for the team version.

## 4. Key concepts I must be able to explain
- **Aggregate** + the 4 rules (slide 67): invariants via the root, small aggregates, reference by ID, eventual consistency between aggregates. Dashed box = one transaction / consistency boundary.
- **Entity vs value object** (slides 65/66). LedgerEntry is an entity although immutable: each booking is its own fact, and reversals refer to it. Slide 66 says entities are *often* mutable, not always.
- **Domain events** (slide 71): past tense, part of the aggregate's public interface, publisher doesn't know its subscribers.
- **Read models / CQRS** (slides 78/79): write side vs query side. Projections can be synchronous (slide 79: start sync).
- **Event sourcing** (slide 72): only events are stored, state = replay. We use the idea **only in the ledger**, not full event sourcing.
- Why ledger + read models belong together (slide 78: an append-only store can't be queried flexibly).
- GroupMembershipView and UserProfile are not for computing; they exist for **decoupling** between contexts.
- DirectedDebt (suggestion, recomputed) vs SettlementPayment (fact with lifecycle): "bill vs bank transfer".

## 5. Known weak spots (be ready)
- Group has `hasZeroBalance` (copy via event) **and** a "reads" line to MemberBalance → answer: hasZeroBalance is the rule mechanism; the line is only for showing balances.
- `waive()` / DebtWaived isn't in our requirements yet.
- Ledger "overkill" for a small app → honest: yes a bit, we wanted to try the pattern from slide 72.
- ExpenseRevision is mentioned but not drawn (speaker 1's area).
- The ledger attribute is named `groupLedger: List<LedgerEntry>`; just call it "the entries".

## 6. How to coach me
1. Let me read or tell my script part by part; give short feedback (clarity, timing ~5 min, correct terms).
2. Then quiz me with likely examiner questions, one at a time: start with the Q&A table in the script, then "why" questions on the ledger, read models, event sourcing, the aggregate rules and Account. Wait for my answer, then correct it briefly.
3. Keep a short running list of my weak spots and repeat those at the end.
4. Keep everything simple. If I'm unsure, give me one sentence I can say in the presentation.
5. Don't invent lecture content; if something isn't on the slides, say so.
