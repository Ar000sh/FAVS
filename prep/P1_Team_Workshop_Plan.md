# P1 Team Workshop Plan: from Domain to Modular Architecture

**Session:** Wed 14.10.26, with the team. **Goal:** finish Ex2 + Ex3 content so P1 (Tue 20.10.26) only needs slides + rehearsal.
**Source deck:** 02.DDD (slide numbers = PDF pages). Our prepared material: `work/Ex1b_ShareWise_User_Journeys.md`, `work/Ex2_ShareWise_Domain_and_Subdomains.md`.

Each step lists: **Goal → Input → What we do → Decisions → Outcome → How the next step uses it → Done when.**
Rule for the day: one person writes into the `.md` files live; every 🟢 decision gets a one-line reason (we must defend it in P1).

---

## Overview: the chain

```
STRATEGIC (Ex2)                                                     TACTICAL (Ex3)
1 Domain ─► 2 Subdomains ─► 3 Language seeds ─► 4 Bounded Contexts ─► 5 Glossary per BC ─► 6 Context Map (v1)
                                                       │
                                                       ▼
                         7 Entities + VOs ─► 8 Aggregates + invariants ─► 9 Domain Events ─► 6' Context Map (final)
                                                                                 │
                                                                                 ▼
                                                     10 Hexagonal architecture + module/package layout
                                                                                 │
                                       11 Ex1a (independent) ──────────────────► 12 Slides + rehearsal
```

| # | Step | Ex | Slides | Timebox | Prepared? |
|---|---|---|---|---|---|
| 1 | Business domain | 2.1 | 20 | 10 min | ✅ draft |
| 2 | Subdomains: split + classify | 2.1 | 21–27 | 30 min | ✅ draft, review only |
| 3 | Language seeds + open questions | 2.4 | 29–36, 7 | 30 min | 🟡 rules exist, questions open |
| 4 | Bounded contexts | 2.2 | 39–44 | 45 min | ⏳ |
| 5 | Glossary per bounded context | 2.4 | 31–36, 41 | 30 min | ⏳ |
| 6 | Context map | 2.3 | 45–55 | 45 min | ⏳ |
| 7 | Entities + value objects | 3.1 | 65, 66, 68 | 30 min | ⏳ |
| 8 | Aggregates + invariants | 3.2 | 67, 69, 64 | 45 min | ⏳ |
| 9 | Domain events | 3.3 | 71, 64 | 30 min | ⏳ |
| 10 | Hexagonal architecture + modules | 3.4 | 75–77 | 45 min | ⏳ |
| 11 | Ex1a NIST vs ISO | 1a | Intro + ISO notes | (alone, later) | 🟡 table exists |
| 12 | Slides + rehearsal | P1 | – | (Sat–Mon) | ⏳ |

Steps 1–6 ≈ 3 h, steps 7–10 ≈ 2.5 h. If the day is short: do 1–6 together, split 7–10 among the team.

---

## Step 1: Business domain (Ex2.1, slide 20)

- **Goal:** one sentence that names what ShareWise does for its customers.
- **Input:** Intro slide 31 (5 capabilities), our journeys.
- **What we do:** agree on the sentence. Slide-20 test: "area of activity / the service offered to customers".
- **Draft:** "Shared expense management for groups."
- **Outcome:** the domain name = the title of the subdomain map.
- **Next step uses it:** it is the "whole" that step 2 splits into parts ("all subdomains together make up the business domain", slide 21).
- **Done when:** everyone can say it in one sentence.

## Step 2: Subdomains, split + classify (Ex2.1, slides 21–27)

- **Goal:** the list of subdomains, each typed Core / Supporting / Generic with a reason.
- **Input:** step 1 + the 10 journey steps + J1–J17.
- **What we do:**
  1. Walk the journeys; group steps into **areas of business activity** (slide 21). Ask "which department would own this?"
  2. Place each on the **complexity × differentiation** chart (slide 22).
  3. Justify with the **slide-26 criteria**: USP, company-specific, complexity, rate of change, existing products, in-house, outsourcing.
- **Our draft (review, don't redo):** `work/Ex2_…` §7.
  - Core: Expense Sharing, Settlement
  - Supporting: Group and Membership, History and Reporting
  - Generic: Identity and Access, Notification Delivery
  - ✅ Dropped 14.10: Currency Exchange Rates, Payment Transfer (one currency per group; payments only recorded)
- **Decisions:**
  - [ ] Keep 2 core subdomains or merge into 1?
  - [ ] Is the close-for-settlement lifecycle part of Settlement (draft) or of Group?
  - [ ] Out-of-scope subdomains (marketing, support, billing): mention in P1, yes/no?
- **Outcome:** subdomain table + chart (= P1 slide 2).
- **Next step uses it:** core subdomains tell us where to spend modelling effort: rich language, rich model, hexagonal (steps 3–10). Generic ones become "buy / external" contexts in the map.
- **Done when:** every subdomain has a type and a reason the whole team agrees with.

## Step 3: Language seeds + make assumptions explicit (Ex2.4, slides 29–36, 7)

- **Goal:** collect the terms and settle the hidden rules before drawing boundaries.
- **Input:** slide 36 candidates (Expense, Share, Balance, Debt, Settlement), slide 33 (Group, Member, Expense, …), our glossary seeds (Ex1b §7), rules R1–R17.
- **What we do:**
  1. List all business terms from the journeys. **Business words only, no tech words** (slides 32, 34).
  2. Mark **ambiguous terms** (one word, two meanings) and **synonyms** (two words, maybe two concepts) (slide 33). Examples: "close" vs "archive", "payment" vs "settlement", "user" vs "member".
  3. **Make implicit assumptions explicit** (slide 31): confirm the step-9 decisions (slide 7) and decide the open questions in `work/Ex2_…` §4.3.
- **Decisions to make here** (they change the boundaries):
  - [ ] Who may invite (any member or admins only)?
  - [ ] Correction after a settlement: what happens to balances?
  - [ ] Auto-archive only from CLOSED, or also OPEN?
  - [ ] Rejoining, deleting a group, GDPR account deletion, placeholder members (J17)
- **Outcome:** a raw term list with ambiguous terms flagged + the confirmed rule list.
- **Next step uses it:** **words that change meaning are exactly where we draw context boundaries** (slide 39, "Lead" example; slide 40, User/Member/Participant/Debtor).
- **Done when:** every flagged term has a note "means X here, Y there".

## Step 4: Bounded contexts (Ex2.2, slides 39–44)

- **Goal:** the modules of ShareWise: named contexts, each with its own consistent model.
- **Input:** subdomains (step 2) + the ambiguous terms (step 3) + slide 40.
- **What we do:**
  1. Start from slide 40: the same person is a **User** (account), a **Member** (group, role), a **Participant** (one expense), a **Debtor/Creditor** (balance). Each meaning = a candidate context.
  2. For each candidate, write: name, purpose, key concepts, **data it owns**, subdomain(s) it implements.
  3. Check size (slide 42): too big = inconsistent model; too small = lots of integration. Merge or split.
  4. Remember: subdomains are discovered, **contexts are designed** (slide 43). They need not be 1:1.
- **Starting candidates:**

| Candidate context | Person is a… | Implements subdomain | Owns |
|---|---|---|---|
| Identity | User | Identity and Access (generic) | accounts, credentials |
| Group Management | Member, Admin | Group and Membership | groups, memberships, invitations, roles, lifecycle? |
| Expense | Payer, Participant | Expense Sharing (core) | expenses, shares, history |
| Settlement | Debtor, Creditor | Settlement (core) | balances, plan, settlement payments |
| Notification | Recipient | Notification Delivery | messages, preferences |
| (Activity / Reporting) | Reader | History and Reporting | read models |

- **Decisions:**
  - [ ] Where does the group status (OPEN/CLOSED/ARCHIVED) live: Group Management or Settlement?
  - [ ] **UserId vs MemberId** (slide 64 vs 40): which ID does the Expense context store?
  - [ ] Is Reporting its own context, or a read model inside Settlement/Expense?
- **Outcome:** context list + a drawing of blobs with the same person/term in several blobs (like slide 41).
- **Next step uses it:** each context gets its own glossary (step 5); the contexts are the boxes in the context map (step 6) and later the **top-level packages** of the monolith (step 10).
- **Done when:** every concept from step 3 belongs to exactly one context (or has a different meaning in each).

## Step 5: Glossary per bounded context (Ex2.4, slides 31–36, 41)

- **Goal:** the ubiquitous language: one meaning per term, per context.
- **Input:** term list (step 3) + contexts (step 4).
- **What we do:**
  1. For each context: table **Term | Meaning in this context | Example**.
  2. Write the **invariants as business sentences** (slide 69 style: "The amount is positive").
  3. Name the **operations in domain language** (slide 35): `recordExpense()`, `correctExpense()`, `closeGroupForSettlement()`, `recordSettlementPayment()`, not `updateStatus()`.
- **Outcome:** glossary + invariant list + operation names (= P1 slide 3).
- **Next step uses it:** the operation names become the methods of the aggregate roots (step 8); invariants become aggregate rules (step 8); terms that cross contexts show what must be translated in the context map (step 6).
- **Done when:** slide-36 terms (Expense, Share, Balance, Debt, Settlement) are all defined and no term has two meanings inside one context.

## Step 6: Context map (Ex2.3, slides 45–55)

- **Goal:** how the contexts relate, with a named pattern for each link.
- **Input:** contexts (step 4) + crossing terms (step 5).
- **What we do:** for every pair that talks:
  1. What flows between them (data, command, event)? Which language is used (slide 45)?
  2. Who is **upstream** (provides) and who is **downstream** (depends)?
  3. Pick the pattern:
     - same team, shared goals → **Partnership** or **Shared Kernel** (slides 46–48)
     - downstream accepts upstream model → **Conformist** (slide 50)
     - downstream protects itself, translates → **Anti-Corruption Layer** (slide 51), especially if downstream is core
     - upstream offers a stable public API → **Open-Host Service / Published Language** (slide 52)
     - no integration → **Separate Ways** (slide 53), never for core
  4. Write one line *why* per link.
- **Likely links to discuss:**
  - Identity → Group Management (who is this user?)
  - Group Management → Expense (is the payer a member?)
  - Expense → Settlement (expense recorded/corrected/removed → balances change)
  - Settlement → Group Management (all balances 0 → archive; balance 0 → may leave)
  - Everyone → Notification
- **Outcome v1:** a slide-54-style diagram with U/D and patterns (= P1 slide 5).
- **Next step uses it:** the links tell us where aggregates may only **reference by ID** (step 8) and where **domain events** cross boundaries (step 9). After step 9 we finalise the map (6').
- **Done when:** every arrow has a pattern + reason, and no core context is "Separate Ways".

---

## Step 7: Entities + value objects (Ex3.1, slides 65, 66, 68)

- **Goal:** classify every concept inside each core context.
- **Input:** glossary (step 5). Slide 68 hint: Entities Group, Expense, SettlementPayment; VOs Money, ExpenseShare, Percentage, GroupName.
- **What we do:** for each concept ask:
  - "Do two with the same values count as the same?" → **VO** (immutable, equality by value) (slide 65)
  - "Do we need to track *this one* over time?" → **Entity** (identity, lifecycle) (slide 66)
  - Use VOs instead of primitives (Money, not BigDecimal; GroupName, not String).
- **Decisions:**
  - [ ] **ExpenseShare (VO, slide 68) vs ExpenseParticipant (entity, slide 64).** Expect a question on this in P1.
  - [ ] **2..\* participants (slide 64) vs our R3 (≥ 1)**
- **Outcome:** per context: entity list + VO list, with one-line reasons.
- **Next step uses it:** entities and VOs are the parts we group into aggregates.
- **Done when:** the slide-68 list is covered and the ExpenseShare conflict is decided with a reason.

## Step 8: Aggregates + invariants (Ex3.2, slides 67, 69, 64)

- **Goal:** consistency boundaries: what must be correct in **one** transaction.
- **Input:** entities/VOs (step 7) + invariants (step 5) + context map (step 6).
- **What we do:**
  1. Start from the slide-69 Expense aggregate (ExpenseId, GroupId, PayerId, Money, ExpenseShares, ExpenseStatus) and the slide-64 UML.
  2. Find the other aggregates: Group? Membership? SettlementPayment? Invitation?
  3. Check each against the **4 rules** (slide 67):
     1. protect invariants via the root
     2. keep it **small**
     3. reference other aggregates **by ID only**
     4. update other aggregates with **eventual consistency** (events)
  4. Assign every invariant from step 5 to exactly one aggregate.
- **Decisions:**
  - [ ] **"Payer belongs to group"** (slide 69): Expense only has a GroupId. Checked by the application service, or by a local membership copy fed by events?
  - [ ] Balance: an aggregate, or a calculated read model?
- **Outcome:** aggregate table (root, contents, invariants, references) + Expense UML (= P1 slide 6).
- **Next step uses it:** each state change on a root produces a **domain event** (step 9); rule 4 tells us which changes must travel as events.
- **Done when:** every invariant has a home, and no aggregate holds an object reference to another aggregate.

## Step 9: Domain events (Ex3.3, slides 71, 64)

- **Goal:** what happens in the business, as past-tense facts, and who reacts.
- **Input:** aggregates (step 8) + journey events (Ex1b §5) + slide 64 (`correct()` → `ExpenseCorrected`, `remove()` → `ExpenseRemoved`).
- **What we do:** table **Event | Published by (aggregate/context) | Payload | Listened to by | Reaction**.
  - Examples: `ExpenseRecorded` → Settlement updates balances; `AllBalancesSettled` → Group archives; `MemberJoined` → Expense allows the new participant.
- **Outcome:** event table (= part of P1 slides 5/6) + **final context map (6')**: arrows now labelled with the events that flow.
- **Next step uses it:** events are what modules use to talk inside the monolith (step 10) and later via RabbitMQ (P3).
- **Done when:** every cross-context arrow in the map is backed by an event or an API call.

## Step 10: Hexagonal architecture + module layout (Ex3.4, slides 75–77)

- **Goal:** the code structure of the modular monolith (this is what makes P1 "modular architecture").
- **Input:** contexts (step 4), aggregates (step 8), events (step 9), subdomain types (step 2).
- **What we do:**
  1. Choose architecture per context by type (slides 59–79): **core → hexagonal + domain model**; **supporting → layered / CRUD**; **generic → external, behind an adapter**.
  2. Draw the hexagon for one core context (Expense): domain in the centre, application services, **ports** (interfaces owned by the core), **adapters**: REST controller (driving), JPA repository (driven), event publisher.
  3. Map to Spring Boot (03.TechStack): `@RestController` = driving adapter, `@Service` = application layer, `JpaRepository` behind a port = driven adapter.
  4. Write the package tree: one top-level package per context, e.g. `sharewise.expense.{domain,application,adapter.in.web,adapter.out.persistence}`.
  5. Rule: modules talk only via public APIs or events, never via each other's tables.
- **Outcome:** hexagon diagram + package tree (= P1 slide 7). It is also the blueprint for Ex4/5 (implement the modulith).
- **Done when:** every context has a package and an architecture style with a reason.

---

## Step 11: Ex1a NIST vs ISO (independent)

- One person, any time. Base: the table in `prep/P1_Modular_Architecture.md` §1 + `notes/norms/`.
- Outcome: `work/Ex1a_NIST_vs_ISO.md` + at most 1 P1 slide (where ShareWise will run: IaaS/PaaS later).

## Step 12: Slides + rehearsal (Sat 17 – Mon 19)

- Outline from `prep/P1_Modular_Architecture.md` §0:

| P1 slide | Content | From step |
|---|---|---|
| 1 | ShareWise + Mallorca journey | Ex1b |
| 2 | Subdomains + classification | 2 |
| 3 | Ubiquitous language: glossary + rules + close-group decisions | 3, 5 |
| 4 | Bounded contexts (User/Member/Participant/Debtor) | 4 |
| 5 | Context map with patterns + events | 6, 9 |
| 6 | Expense aggregate + invariants + events | 7, 8, 9 |
| 7 | Hexagonal + module/package layout | 10 |
| 8 | (optional) Cloud: NIST vs ISO | 11 |

- Rehearse the 11 "why" questions in `prep/P1_Modular_Architecture.md` §6. Every team member should be able to answer each one.

---

## Before tomorrow (everyone)
- [ ] Read `work/Ex2_ShareWise_Domain_and_Subdomains.md` §1–4 (15 min).
- [ ] Skim DDD slides 39–55 (bounded contexts + context mapping).
- [ ] Bring an opinion on the 4 slide conflicts (`work/Ex2_…` §4.1).
- [ ] Ask on Moodle/in class: P1 length, format, who presents.
