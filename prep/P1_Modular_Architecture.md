# Presentation 1: Modular Architecture of ShareWise (20.10.26)

**Status:** prep sheet. It lists what you need from the scripts in order to *solve* Ex 1–3 and present them.
**Sources:** `02.DDD` (main), `01.Intro` (ShareWise + cloud defs), ISO/IEC 22123-1/-2. Each section links to the full note.
**Not given anywhere:** the format and length of the presentation, and team size. ➜ Check Moodle or ask in class.
⚠ **The only official spec is one line on Intro slide 7: "Presentations: modular architecture of ShareWise".** The content below is *inferred* from the timing (right after Ex1–3) and DDD slides 3–4 ("Up next: modular monolith").

> Core idea of P1: you show **how you cut ShareWise into modules, and why**. In DDD terms: *problem space* (subdomains) → *solution space* (bounded contexts + context map) → *inside one context* (aggregates, entities, VOs, events) → *architecture* (hexagonal). Ubiquitous language runs through all of it. These modules become the packages of the **modular monolith** you build next (Ex4/5), and later the candidates for **service extraction**.

---

## 0. The storyline the slides themselves use

The overview diagram on DDD slides 14/19/28/38/57/74 is a ready-made outline for the talk:

```
 STRATEGIC DESIGN ─────────────────────────────►  TACTICAL DESIGN ──────────────────►
 Problem space        Solution space                Architecture           Code
 Domain → Subdomains → Bounded Contexts (+Map)  →   Hexagon (App+Adapters) → Aggregates…
 ◄──────────────────────── Ubiquitous Language (spans everything) ──────────────────►
```

**Suggested presentation outline** (my proposal, not from the slides):
1. ShareWise in one slide: idea + Mallorca journey (10 steps)
2. Subdomains + classification (Core/Supporting/Generic)
3. Ubiquitous language: glossary + invariants + the open "close group" rules
4. Bounded contexts: the User/Member/Participant/Debtor example as the reason for each cut
5. Context map with patterns + justification
6. Inside the core context: Expense aggregate (entities, VOs, invariants, domain events)
7. Architecture: hexagonal for core, layered for supporting → module/package structure of the monolith
8. (Optional, 1 slide) Cloud context: NIST vs ISO, which service model we will use where

---

## 1. Ex1 (05.10): background, probably 1 slide at most in P1

**a) NIST SP 800-145 vs ISO/IEC 22123.** Details: [`norms/ISO22123-1_Vocabulary.md`](../notes/norms/ISO22123-1_Vocabulary.md), [`norms/ISO22123-2_Concepts.md`](../notes/norms/ISO22123-2_Concepts.md)

| | NIST (2011) | ISO/IEC 22123-1/-2 (2023) |
|---|---|---|
| Nature | "a model": fixed 5-3-4 | "a paradigm": open lists |
| Characteristics | 5: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service | **6**: adds **multi-tenancy** as its own characteristic. "Rapid elasticity **and scalability**" (horizontal + vertical) |
| Service models | 3 closed models: IaaS, PaaS, SaaS | **Two axes:** 3 **cloud capabilities types** (application / platform / infrastructure), separated by separation of concerns, plus an **open set of cloud service categories** (CaaS, CompaaS, DSaaS, IaaS, NaaS, PaaS, SaaS, + 11 more in Annex A). A category may combine several types (e.g. NaaS, DSaaS = all three) |
| Deployment | private, community, public, hybrid ("2 or more") | Same 4, defined by **control & sharing** of resources. Hybrid = private + public. **Multi-cloud**, federated, inter-cloud added |
| Roles | none (SP 500-292 has 5 actors) | Parties CSC / CSP / CSN, roles, sub-roles, activities. Cloud service user ≠ customer |
| Extra | – | 13 cross-cutting aspects (security, portability, reversibility, SLAs …), data classes, containers/serverless, regions/AZs |

**Key sentence:** *ISO keeps IaaS/PaaS/SaaS but splits "which layer do I get" (capabilities type, exactly 3) from "what is it for" (service category, open-ended). NIST's closed list cannot classify the XaaS flood or offerings that span layers.*

**b) ShareWise user journey.** Covered below (§2.1). The fuller example (corrections, joining/leaving) feeds directly into the ubiquitous language and invariants.

---

## 2. Domain facts you must have at hand (from the slides)

### 2.1 ShareWise
- Helps groups **record shared expenses, distribute costs, understand who owes whom, record settlement payments, close & archive groups** (Intro slide 31).
- **Journey (DDD slide 5):**
  1. register
  2. create group "Mallorca 2027"
  3. invite friends
  4. invitees join
  5. record expenses
  6. correct/remove expenses
  7. review balances
  8. record settlement payments
  9. **authorized member closes group for settlement**
  10. archive
- **Open rules for step 9 (DDD slide 7). The slides expect *you* to decide these:**
  - Who is authorized?
  - Can expenses be added afterwards?
  - Can they still be corrected?
  - Must all balances be 0 before closing?
  - Is archiving automatic?
  - Can closing be revoked?
- **Ex1b asks additionally:** how are **corrections** handled? What happens when someone **joins or leaves** the group (late joiner, leaving with an open balance)?
- **Mallorca data:** Hotel €900 paid by Alice (everyone), Dinner €180 paid by Bob (everyone), Rental car €420 paid by Carol (Alice, Carol, David), Museum €75 paid by David (Bob, Carol, David).
  - Equal split gives the balances Alice **+490**, Bob −115, Carol −15, David −360 (verified, sum = 0).
- **Core concepts given:** Group, Member, Expense, "…" (Intro slide 33, left open on purpose).

### 2.2 Hints the slides already give for ShareWise (use them!)
| Slide (DDD) | Hint |
|---|---|
| 36 | Language candidates: **Expense, Share, Balance, Debt, Settlement** + "Business rules (invariants)" + **Glossary** |
| 35 | Method names in domain language: `closeGroupForSettlement()`, `recordSettlementPayment()`, `calculateFinalBalances()`, `archiveGroup()`. **Not** `updateStatus()`, `processData()` |
| **40** | **The same person is a User (account/login), a Member (group, invitation, role), a Participant (in one expense) and a Debtor/Creditor (balance).** ➜ the main hint for bounded contexts |
| 68 | Entities: Group, Expense, SettlementPayment. VOs: Money, ExpenseShare, Percentage, GroupName |
| 69 | Expense aggregate (ExpenseId, GroupId, PayerId, Money, ExpenseShares, ExpenseStatus) + 5 invariants |
| 64 | UML: Expense «AggregateRoot», SplitStrategy VO (EQUAL/EXACT/PERCENTAGE), ExpenseStatus VO (ACTIVE/CORRECTED/REMOVED), ExpenseParticipant «Entity» (2..*), Money VO (BigDecimal + Currency), GroupId by reference. `correct()` → `ExpenseCorrected`, `remove()` → `ExpenseRemoved` |
| 27 / 44 / 55 | "ShareWise Domains? / Bounded Contexts? / Context Mapping?" ➜ **no solutions given, this is your job** |

⚠ **Inconsistency on the slides:** slide 68 treats ExpenseShare as a *value object*, while slide 64 models the split as an ExpenseParticipant *entity*. Pick one, justify it, and put it in the glossary. Expect a question on this.

---

## 3. Ex2: strategic design (what to know to solve it)
Full method guide: [`skripte/02_DDD.md` §8](../notes/skripte/02_DDD.md)

### 3.1 Subdomains (discovered, not designed — slide 43)
- **Definition:** a subdomain is a fine-grained area of business activity. All subdomains together make up the business domain (slide 21).
- **Classification chart (slide 22):**
  - X axis = business differentiation, Y axis = complexity.
  - **Core** = high/high.
  - **Supporting** = low complexity.
  - **Generic** = low differentiation, can be complex.
- **Criteria table (slide 26).** Use it as your justification table:

| | Core | Supporting | Generic |
|---|---|---|---|
| USP / business-critical | Yes | No | No |
| Company-specific | Yes | Yes | No |
| Complexity | High | Low | High |
| Rate of change | High | Low | Low |
| Existing products | No | Partly | Yes |
| Build in-house | Yes | Yes | No |
| Outsource | No | Yes | No |

- **Implementation consequence:**
  - Core: build it yourself and invest there (slide 23).
  - Supporting: CRUD/ETL, frameworks, can be outsourced (slide 24).
  - Generic: buy it, e.g. identity à la Active Directory (slide 25).
- **Deliverable:** a list or table of subdomains with type + one-line reason, ideally placed on the slide-22 chart.

### 3.2 Ubiquitous language (slides 29–36)
- **One language** shared by experts, devs and code. **Business terms only.** **One meaning per term per context.**
- **Ambiguous terms:** split them, as in policy → regulatory provision / insurance contract.
- **Synonyms:** usually mean different concepts, as in visitor vs account.
- Unclear terms reveal hidden concepts, so **make implicit assumptions explicit**. This is exactly the step-9 questions.
- **Deliverable:** a **glossary** (scoped per bounded context) + **invariants written as business sentences** + domain-named operations.

### 3.3 Bounded contexts (designed — slides 39–43)
- **Why they exist:** one global model fails. Example: "Lead" means an *event* in Marketing and a *long-running process* in Sales. Solution: **several smaller languages**, each consistent inside its boundary (slide 41).
- **Size (slide 42):** no "right" size. The model must be clear and have a purpose. Bigger boundaries are harder to keep consistent; smaller ones bring more integration overhead.
- **Subdomain ≠ bounded context.** Subdomains are *identified* in the problem space. BCs are *designed* in the solution space, and choosing them is a strategic decision.
- Conway's law: BCs → services → teams (slides 11, 15).
- **Deliverable:** named BCs, each with its key concepts and owned data, and the subdomain(s) it implements. Drawn as blobs, with the same term appearing in several blobs carrying different meanings.

### 3.4 Context map (slides 45–54)
| Category | Pattern | When | Notation |
|---|---|---|---|
| Cooperation (same team / dependent goals) | **Partnership** | ad hoc coordination, both adapt, nobody dictates | line labelled "Partners" |
| | **Shared Kernel** | small shared compiled contract lib, high sync needed. Breaks "one team owns one BC" | overlapping ovals |
| Customer-Supplier (U/D, power imbalance) | **Conformist** | downstream accepts upstream model (e.g. industry standard) | arrow "Conforms", U/D |
| | **Anti-Corruption Layer** | downstream translates. Use if downstream is **core**, upstream is legacy, changes often or is huge | "ACL" box on downstream side |
| | **Open-Host Service** (+ Published Language) | upstream offers stable integration protocol (e.g. OpenAPI) decoupled from its internal model | "OHS" box on upstream side |
| **Separate Ways** | – | no integration, duplicate instead. **Never for core** | no line |

- Reading the map (slide 54): high-level design, team communication, org smells (everyone needs an ACL against one team).
- ⚠ Not on these slides: Big Ball of Mud, Event Storming, "Customer/Supplier" as its own pattern. Don't attribute them to the lecture.
- **Deliverable:** one diagram of all ShareWise BCs in slide-54 style, every edge labelled with its pattern, plus a one-line *why* per edge.

---

## 4. Ex3 (due 19.10): tactical design + architecture, also part of P1
Slides 58–79. Full detail: [`skripte/02_DDD.md` §7](../notes/skripte/02_DDD.md)

### 4.1 Building blocks
| Concept | Definition (slides) | Test question to ask yourself |
|---|---|---|
| **Value Object** (65) | immutable conceptual whole, **no identity**, equality by attributes, describes/measures an entity | "Do two with the same values count as the same?" → VO (Money, Percentage, GroupName) |
| **Entity** (66) | individual thing with **unique identity**, often mutable, lives inside an aggregate. "Use VOs instead of primitives" | "Do I need to track *this one* over time?" |
| **Aggregate** (67) | cluster of entities + VOs owned by a **root**. **Transactional consistency boundary** | "What must be consistent in *one* transaction?" |
| **Domain Event** (71) | message describing a significant business event. Part of the aggregate's **public interface** | past tense: `ExpenseRecorded`, `MemberJoined`, `GroupClosedForSettlement` |

**The 4 aggregate rules (slide 67). Learn them by heart:**
1. Protect invariants inside the boundary, via the root's interface.
2. Design **small** aggregates.
3. Reference other aggregates **by identity only** (Expense holds `GroupId`, not `Group`).
4. Update other aggregates with **eventual consistency** (→ domain events).

**Expense invariants given (slide 69):**
- The amount is positive.
- The sum of the shares equals the total.
- The payer belongs to the group.
- All participants belong to the group.
- A finalized expense can't be changed directly.

➜ *Rules 3 and 4 explain why "payer belongs to group" is tricky: Expense only knows GroupId. Think about how you check it (e.g. an application service checks it before the command, or a membership snapshot is used). That makes a good discussion point.*

### 4.2 Pattern by subdomain type (slides 59–79)
| Subdomain | Business logic | Architecture |
|---|---|---|
| Supporting | Transaction Script / Active Record | **Layered** (presentation → business → data access) |
| Core | **Domain Model** (aggregates) | **Ports & Adapters / Hexagonal** |
| Core + time/audit | Event Sourcing | CQRS (+ ES) |

### 4.3 Hexagonal architecture (slide 77)
- Business logic sits in the **centre** and has **no dependency on infrastructure** (dependency inversion).
- The **application layer** is a facade that orchestrates use cases.
- **Ports** are interfaces owned by the core. **Adapters** (REST controller, JPA repo, message queue) implement or call them.
- Fits **core** BCs. The slides say so explicitly.
- **Link to the tech stack (03.TechStack):**
  - Spring Boot backend: `@RestController` = driving adapter, Spring Data `JpaRepository` = driven adapter behind a port interface, `@Service` = application layer.
  - Next.js frontend: talks to the backend via REST.
  - See [`skripte/03_TechStack.md`](../notes/skripte/03_TechStack.md).

### 4.4 "Modular" = what P1 is literally about
(note:) The slides don't define "modular monolith" yet (that's lecture 5+). The obvious mapping:
- **one bounded context = one module** (top-level package)
- the core module(s) are hexagonal inside, the supporting ones layered
- modules talk via their public interfaces / domain events, never via each other's tables

Showing this mapping is what makes the presentation about "modular *architecture*" and not just about DDD.

---

## 5. Checklist before 20.10

**Ex1**
- [ ] Ex1a NIST vs ISO table (1 slide)
- [ ] Ex1b extended journey: corrections, join/leave, closing rules decided

**Ex2**
- [ ] Ex2.1 subdomain list + Core/Supporting/Generic justification (slide-26 criteria)
- [ ] Ex2.2 bounded contexts with their concepts. Use the User/Member/Participant/Debtor split
- [ ] Ex2.3 context map diagram, every edge with pattern + reason
- [ ] Ex2.4 glossary per context + invariants in business language

**Ex3**
- [ ] Ex3.1 entities vs VOs per context (resolve the ExpenseShare vs ExpenseParticipant conflict)
- [ ] Ex3.2 aggregates + invariants (Expense, Group, Settlement …), small, referenced by ID
- [ ] Ex3.3 domain events list (who publishes, who reacts)
- [ ] Ex3.4 hexagonal diagram for the core context + module/package layout of the monolith

**Presentation**
- [ ] Rehearse the "why" questions below

## 6. Questions you should be able to answer in the discussion
1. Why is X your core subdomain and not Y? What would you buy or outsource?
2. Subdomain vs bounded context: what is the difference? Why aren't they 1:1 in your design (or why are they)?
3. Why does "Member" exist in one context and "Participant" in another? Why not one `User` class?
4. Why did you choose an ACL/Conformist/Partnership here? What happens if the upstream model changes?
5. Why is ExpenseShare a VO (or an entity)?
6. Why doesn't Expense hold a reference to Group? How do you enforce "payer belongs to group"?
7. What happens to the balances when an expense is corrected? Which events fire, and who listens?
8. Who may close a group? Must balances be zero? Can it be reopened?
9. Why hexagonal for the core and layered for the rest?
10. Which of your modules would you extract as a service first later, and why? (This points ahead to P2/P3.)
11. Cloud: ISO capabilities type vs service category. Which category is a managed DB? (DSaaS, which spans all 3 types.)

---

## 7. My prepared answers (own notes, not from the slides)

**"LedgerEntry never changes. Why is it an entity and not a value object?"** 🟢 Decision: entity (team, 17.10)

*Short answer for the presentation:*
> "A ledger entry is a booking, and every booking has its own identity, like a line in an accounting journal. It is immutable, but an entity doesn't have to be mutable: the slides say entities are *often* mutable, not always (slide 66). What matters is that we need to tell individual bookings apart and refer to them."

*The arguments behind it:*
1. **Identity matters more than the values.** An entry is a fact: "on this date, this booking happened for Bob because of this expense". Two bookings can look alike and still be two separate facts. For example: an expense is recorded, removed (reversal), then recorded again. With value-object equality, bookings with equal values would count as the same thing, and the balance would be wrong.
2. **Traceability / audit.** A balance must be explainable: "which bookings make up Bob's −202?" (J7 step 4: drill down into the expenses behind a balance). For that, every booking needs a stable id the read models and the UI can point to.
3. **Reversals refer to what they reverse.** "Entry Y reverses entry X" is natural with ids. Accounting ledgers always number their entries for that reason.
4. **Immutable ≠ value object.** Slide 66 describes entities as "often mutable", so immutability alone doesn't make something a value object. The question from slides 65/66 is whether we care *which one* it is. For bookings we do.
5. (secondary, technical) An append-only table needs a key anyway. That is not a domain reason, so mention it last or not at all.

*If they push back ("but it never changes, so it should be a value object"):*
> "By the strict slide test it could be one, since an entry is fully described by its values. We chose an entity because we need to refer to single bookings (audit, reversals) and because two equal-looking bookings are still two facts. It's a deliberate trade-off."

**"Doesn't GroupLedger grow forever?"** (aggregate rule 2, slide 67: design small aggregates)
- There is one ledger per group, and a group is small: a trip has dozens or hundreds of expenses, not millions.
- Balances are not recomputed from all entries on every request. The read model MemberBalance holds them (projection, CQRS, slide 78).
- (note:) If it ever gets large, the usual event-sourcing technique is a snapshot of the balances (slide 72 introduces event sourcing; snapshots are background knowledge, not on the slides).
