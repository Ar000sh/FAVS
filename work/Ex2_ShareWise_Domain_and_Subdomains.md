# ShareWise: Domain Knowledge, Features & Subdomains (Ex2 part 1)

**Purpose:** everything we know about ShareWise in one place, ending with the subdomain classification for Ex2 part 1 (DDD slide 27: "ShareWise Domains? Discuss in groups").

| Source | What it gives us |
|---|---|
| 01.Intro, slides 30–34 | Idea, 5 capabilities, Mallorca scenario, core concepts "Group, Member, Expense, …", roadmap |
| 02.DDD, slides 5–8, 27, 35, 36, 40, 44, 55, 64, 68, 69 | 10-step journey, open step-9 rules, language hints, User/Member/Participant/Debtor, Expense model |
| 03.TechStack | No ShareWise content. Only the stack (Spring Boot + Next.js) |
| Exercises 1 and 2 | Ex1b: "more complete example" incl. corrections, join/leave. Ex2: subdomains, BCs, context map, language |
| `work/Ex1b_ShareWise_User_Journeys.md` | Full journeys J1–J17, rules R1–R17, market research (source of most of §2–§5 here) |

**Conventions:**
- "(slide N)" = PDF page of the named deck.
- 🟢 **Decision** = our own design choice, not lecture content. It must be defensible in P1.
- "(note:)" = our own clarification.

---

## 1. ShareWise in a nutshell

ShareWise is "a collaborative application for managing expenses within groups". Tagline: "Shared expenses made simple" (Intro slide 31).

**It helps groups to** (Intro slide 31):
1. record shared expenses
2. distribute costs among participants
3. understand who owes whom
4. record settlement payments
5. close and archive completed groups

**10-step journey "Mallorca 2027"** (DDD slides 5–6):
1. register
2. create group
3. invite friends
4. invitees join
5. record expenses
6. correct/remove expenses
7. review balances
8. record settlement payments
9. **an authorized member closes the group for settlement**
10. archive

Step 9 is marked: "What are the business rules for this step?"

**Mallorca data** (Intro slide 32). Alice creates the group; Bob, Carol and David join.

| Expense | Paid by | Amount | Participants |
|---|---|---|---|
| Hotel | Alice | €900 | everyone |
| Dinner | Bob | €180 | everyone |
| Rental car | Carol | €420 | Alice, Carol, David |
| Museum | David | €75 | Bob, Carol, David |

(note:) The slide gives no split rule. Assuming equal splits, the balances are:
- Alice +490
- Bob −115
- Carol −15
- David −360

Sum = 0, verified by script.

**Other facts from the slides:**
- **Core concepts given:** Group, Member, Expense, "…" (Intro slide 33, left open on purpose).
- **Language candidates:** Expense, Share, Balance, Debt, Settlement (DDD slide 36).
- **Same person, four contexts** (DDD slide 40):
  - User (account, login)
  - Member (group, invitation, role)
  - Participant (in one expense)
  - Debtor/Creditor (balance)
- **Domain-language method names** (DDD slide 35): `closeGroupForSettlement()`, `recordSettlementPayment()`, `calculateFinalBalances()`, `archiveGroup()`. Not generic names like `updateStatus()`.
- **Roadmap** (Intro slide 34): understand domain → modular monolith → containerize → automate build/deploy → identify change drivers → extract services → events and messaging → distributed consistency → resilience and observability.
- **Stack:** Spring Boot backend, Next.js frontend.

---

## 2. User journeys

13 MVP journeys (J1–J13) and 4 Should/Could journeys (J14–J17). Full flows with alternatives are in `Ex1b_ShareWise_User_Journeys.md` §5.

**Actors:**
- Visitor (no account)
- User (account)
- Group Admin (the creator; can promote others)
- Member
- Payer (of one expense)
- Participant (shares one expense)
- Debtor/Creditor (negative/positive balance)
- System (timers, notifications)

| # | Journey | Actor | Slide step | Key rules | Domain events |
|---|---|---|---|---|---|
| J1 | Register and log in | Visitor | 1 | email unique | UserRegistered |
| J2 | Create group (name, currency, OPEN, creator = admin) | User | 2 | name required | GroupCreated, MemberJoined |
| J3 | Invite and join (link or email) | Admin, invitee | 3–4 | R9, R10 | MemberInvited, InvitationAccepted/Declined, MemberJoined |
| J4 | Record expense: equal / exact / percentage | Member | 5 | R1–R5 | ExpenseRecorded |
| J5 | Correct expense, old version kept | Recorder, payer, admin | 6 | R5–R7 | ExpenseCorrected |
| J6 | Remove expense (soft delete) | Recorder, payer, admin | 6 | R5, R6, R8 | ExpenseRemoved |
| J7 | Review balances + simplified plan | Member | 7 | R14, R15 | none (query) |
| J8 | Record settlement payment, creditor confirms | Debtor, creditor | 8 | R16, R17 | SettlementPaymentRecorded, …Confirmed/Rejected |
| J9 | Late joiner (only new expenses) | Invitee | 4 | R10 | MemberJoined |
| J10 | Leave group (only at balance 0) | Member | – | R11–R13 | MemberLeft |
| J11 | Remove member (only at balance 0) | Admin | – | R11 | MemberRemoved |
| J12 | Close for settlement / J12b reopen | Admin | 9 | §3.1 | GroupClosedForSettlement, GroupReopened |
| J13 | Archive (auto at all balances 0, or manual) | System, admin | 10 | §3.1 | AllBalancesSettled, GroupArchived |
| J14 | Payment reminder | Creditor | – | Should | PaymentReminderSent |
| J15 | Recurring expense | System | – | Could | RecurringExpenseScheduled |
| J16 | Activity feed (domain events rendered) | Member | – | Should | – |
| J17 | Placeholder member without account | Admin | – | Could | – |

### 2.1 Extended Mallorca example

Five members: Alice (admin), Bob, Carol, David, and Eve, who joins on day 3. Splits are equal unless stated.

| Day | Journey | Event | Payer | Amount | Participants → share |
|---|---|---|---|---|---|
| 1 | J4 | Hotel | Alice | €900 | A, B, C, D → 225 |
| 1–2 | J4, J5 | Dinner, entered as €180, corrected to €200 | Bob | €200 | A, B, C, D → 50 |
| 2 | J4 | Rental car | Carol | €420 | A, C, D → 140 |
| 2 | J4 | Museum | David | €75 | B, C, D → 25 |
| 3 | J9 | Eve joins (late joiner) | – | – | – |
| 3 | J4 | Boat trip | Eve | €300 | A, B, E → 100 |
| 4 | J4, J6 | Groceries; the duplicate entry is removed | Bob | €60 | A–E → 12 |
| 5 | J4b exact | Farewell dinner | Alice | €250 | A 50, B 50, C 40, D 60, E 50 |

**Balances after day 5** (verified by script, sum = 0):
- Alice +573
- Bob −202
- Carol −72
- David −437
- Eve +138

**What happens next:**
1. Bob tries to leave and is refused, because he owes €202.
2. Bob pays Alice €202, and Alice confirms.
3. Bob leaves.
4. Alice closes the group.
5. Carol's late taxi expense is refused, because the group is closed.
6. The settlements are paid per the plan.
7. The last confirmation triggers auto-archive.

**Simplified plan after Bob left:** three payments instead of up to six.
- David → Alice €371
- David → Eve €66
- Carol → Eve €72

---

## 3. Business rules and decisions

All rules are 🟢 our own decisions unless a slide is cited. The slides give only the 5 Expense invariants (DDD slide 69) and the open step-9 questions (DDD slide 7).

### 3.1 Group lifecycle

```
          closeGroupForSettlement()            all balances = 0 (auto)
  OPEN ───────────────────────────► CLOSED_FOR_SETTLEMENT ───────────────────► ARCHIVED
    ▲                                   │                    or archiveGroup() by admin
    └──────── reopenGroup() ────────────┘                    (only if balances = 0)
```

| Slide-7 question | 🟢 Decision |
|---|---|
| Who is authorized to close? | Group admins only. The creator is admin and can promote others. |
| Can expenses be added afterwards? | No. While the group is closed, only settlement payments are allowed. |
| Can expenses still be corrected? | No. An admin must reopen the group first. The reopen shows in the activity feed. |
| Must all balances be 0 before closing? | No. Closing freezes the expenses and fixes the plan. Balance 0 is needed to archive. |
| Is archiving automatic? | Yes, when the last balance reaches 0. An admin may also archive manually at balance 0. |
| Can closing be revoked? | Yes, an admin can reopen while the group is CLOSED. ARCHIVED is final and read-only. |

### 3.2 Expenses
- **R1** The amount is > 0. (slide 69)
- **R2** The payer is a member of the group when the expense is recorded. (slide 69)
- **R3** Every participant is a member, and there is at least 1 participant. The payer may or may not participate. (slide 69; ⚠ see §4.1)
- **R4** The shares add up exactly to the amount. With percentages, they add up to 100 %. Remainder cents go to the first participant(s). (slide 69 + 🟢 our rounding rule)
- **R5** Expenses can be recorded, corrected or removed only while the group is OPEN.
- **R6** The recorder, the payer or an admin may correct or remove an expense.
- **R7** A correction keeps the old version in the history (status CORRECTED) and notifies the participants. (slide 69: "a finalized expense may not be changed directly")
- **R8** Removal is a soft delete (status REMOVED). Removed expenses are ignored for balances.

### 3.3 Membership
- **R9** Members join only via a valid invitation. Invitations expire after 7 days.
- **R10** Late joiners share only in expenses recorded after they join, unless an expense is explicitly corrected to include them.
- **R11** A member can leave, or be removed, only at balance 0 (industry standard, Splitwise).
- **R12** The last admin must promote someone before leaving.
- **R13** Former members stay visible in old expenses ("Bob (left)").

### 3.4 Balances and settlement
- **R14** Balance = paid − owed shares (active expenses) ± confirmed settlements. The sum over all members is always 0.
- **R15** The settlement plan uses the minimum number of payments and never changes anyone's total balance.
- **R16** The debtor records a payment (PENDING) and the creditor confirms it (CONFIRMED). Only confirmed payments change balances.
- **R17** A payment can't be larger than the debtor's open debt.

---

## 4. Still to consider

4 slide conflicts and 10 domain questions are still open. Each needs a decision before P1 (20.10.26).

### 4.1 Conflicts on the slides
- [ ] **ExpenseShare vs ExpenseParticipant.**
  - DDD slide 68 calls the share a value object.
  - Slide 64 models an ExpenseParticipant entity (UserId + owedShare).
  - Pick one name and type, and put it in the glossary.
- [ ] **2..\* participants vs our R3 (≥ 1).**
  - Slide 64 requires at least 2 participants per expense.
  - Our R3 allows 1 (e.g. Alice pays for Bob only).
  - Either adopt 2..\* or justify the difference.
- [ ] **UserId vs MemberId.**
  - Slide 64 uses `UserId paidBy`.
  - Slide 40 says a payer is a Member/Participant, not a User.
  - Which identity does the Expense context store?
- [ ] **"Payer belongs to the group"** (slide 69) can't be checked inside Expense, which only holds a GroupId (aggregate rule 3, slide 67). Options:
  - the application service checks it before the command, or
  - a local membership copy, fed by events.

### 4.2 Open from slides and exercises
- [ ] Intro slide 33: complete the core concepts "Group, Member, Expense, …". Our glossary seeds cover it.
- [ ] Intro slide 31: "Example use cases?" J1–J17 answer it.
- [ ] Ex1a: our own NIST vs ISO write-up is still missing. The table exists in the P1 prep.
- [ ] Ex2 says "work in the teams". Team members, P1 format and P1 length are unknown. Check Moodle or ask on 20.10.

### 4.3 Domain questions not decided yet
- [ ] **Correction after a settlement.** Bob already paid €202, and then the hotel is corrected. The balances are recomputed. Does Bob get a new debt or credit, and is he notified again?
- [ ] **Who may invite?** J3 says "admin/member". Any member, or admins only?
- [ ] **Rejoining.** Can a former member be invited again, and do they keep their history?
- [ ] **Auto-archive scope.** Only from CLOSED_FOR_SETTLEMENT, or also an OPEN group whose balances happen to be 0?
- [ ] **Deleting a group.** Is that allowed for an OPEN group without expenses?
- [ ] **Account deletion (GDPR).** A user deletes their account but still appears in a group's history.
- [ ] **Placeholder members (J17) vs R9.** Placeholders join without an invitation. Make an exception or drop J17?
- [ ] **Rejected settlement.** After REJECTED, can the debtor edit and resubmit it, or must they record a new one?
- [ ] **Plan recalculation.** After partial payments or a reopen, is the simplified plan recomputed from scratch?

---

## 5. Ideas from other apps

Every competitor has the same core: groups, splitting, balances, simplify debts, settle up. **None has an explicit "close for settlement" phase. That is our differentiator.** Data: Ex1b market research.

| Feature | Splitwise | Tricount | Settle Up | Splid | Spliit (OSS) | ShareWise |
|---|---|---|---|---|---|---|
| Groups + invite link/email | yes | yes (≤ 50 people) | yes | yes, no signup | link = group | Must |
| Members without account | via email | names only | yes | yes | yes | Could |
| Split equal / exact / % / shares | all | yes | yes | yes | yes | Must (equal, exact, %) |
| Multiple payers per expense | yes | no | yes | yes | no | Won't |
| Edit / delete expense | yes, restore deleted | yes | yes | yes | yes | Must + history |
| Simplify debts | yes | yes | yes | yes | yes | Must |
| Record / mark as paid | yes | yes | yes | yes | yes | Must |
| Remove member only at balance 0 | yes | no open expenses | – | – | – | Must rule |
| Leave group | at balance 0 | keeps obligation | – | – | – | Must, at 0 |
| Archive group | yes | yes, restorable | yes | – | – | Must |
| Close for settlement | no | no | no | no | no | **Must, differentiator** |
| Multi-currency | 76 currencies | free, daily rates | yes | yes | yes | Won't (dropped 14.10) |
| Recurring expenses | yes | no | paid | no | beta | Could |
| Categories + statistics | yes | yes | paid | – | yes | Could |
| Receipt photo / OCR | Pro OCR | photo | – | – | AI scan | Won't |
| Activity feed + notifications | yes | yes | – | – | – | Should |
| Export CSV/PDF/Excel | CSV | – | Excel | PDF/Excel | – | Could |
| Payment integration | Venmo/PayPal (US) | bunq | – | – | – | Won't |

**What we adopt:**
- Splitwise's rule "no removal with an open balance" → R11.
- Splitwise's guarantee for simplify debts: "it never changes anyone's total balance; it only optimizes the payment paths" → R15, and a glossary sentence.
- Tricount lets a leaver keep their obligation. We chose the stricter Splitwise rule, so be ready to defend it.
- Identity and notifications are commodity in every app → generic candidates. Exchange rates and payment transfer are commodity too, but we leave them out entirely (§7.3).

Sources:
- [Splitwise: simplify debts](https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts)
- [Splitwise: removing a person](https://kb.splitwise.com/groups/how-do-i-remove-a-person-from-a-group)
- [Tricount help](https://help.tricount.com/articles/how-can-i-manage-my-tricounts-and-expenses)
- [Comparison 2026](https://tripprof.com/en/blog/best-apps-track-split-group-trip-expenses/)
- [Tricount vs Splid](https://spliit.pro/blog/tricount-vs-splid/)
- [Spliit](https://spliit.app/)

---

## 6. Features (MoSCoW)

(note:) The MVP is small but domain-rich. The interesting rules sit in splitting, correcting and closing, which is where the architecture work of P1–P3 pays off.

| Priority | Feature | Journey | Rules |
|---|---|---|---|
| Must | Register and log in | J1 | – |
| Must | Create group (name, currency) | J2 | – |
| Must | Invite by link/email, join, decline | J3, J9 | R9, R10 |
| Must | Record expense: equal, exact, percentage | J4 | R1–R5 |
| Must | Correct expense with history | J5 | R5–R7 |
| Must | Remove expense (soft delete) | J6 | R5, R6, R8 |
| Must | Balances + simplified settlement plan | J7 | R14, R15 |
| Must | Record settlement payment | J8 | R16, R17 |
| Must | Leave group / remove member at balance 0 | J10, J11 | R11–R13 |
| Must | Promote member to admin | J10 | R12 |
| Must | Close for settlement, reopen | J12 | §3.1 |
| Must | Archive (auto + manual) | J13 | §3.1 |
| Should | Creditor confirms payment (MVP may skip this) | J8 | R16 |
| Should | Activity feed | J16 | – |
| Should | Notifications (invite, expense changed, group closed) | several | – |
| Should | Payment reminders | J14 | – |
| Could | Placeholder members without account | J17 | conflicts with R9 |
| Could | Recurring expenses | J15 | – |
| Could | Categories + statistics | – | – |
| Could | Comments on expenses | – | – |
| Could | CSV/PDF export of an archived group | J13 | – |
| Could | Restore a removed expense | J6 | – |
| Won't | Multi-currency / exchange rates, real payment transfer, receipt OCR, multiple payers, offline mode | – | – |

---

## 7. Subdomains (Ex2 part 1, DDD slide 27)

ShareWise is **one business domain**: "shared expense management for groups", i.e. the service offered to customers (DDD slide 20). 🟢 It splits into **2 core, 2 supporting and 2 generic subdomains**. The classification is ours; the slides give none.

(note:) Slide 27's title says "Domains", but it sits at the end of the subdomain section. It is the first of four "ShareWise …?" prompts that match Ex2's four parts:
- slide 27 → subdomains
- slide 36 → language
- slide 44 → bounded contexts
- slide 55 → context map

**Method used** (DDD slides 21–26, 43):
1. Group the journey steps into fine-grained areas of business activity (slide 21). Ask: "Which department would own this?"
2. Place each area on the complexity × differentiation chart (slide 22).
3. Justify the type with the slide-26 criteria: USP, company-specific, complexity, rate of change, existing products, in-house, outsourcing.
4. Remember that subdomains are discovered, not designed (slide 43). Bounded contexts come next (slide 44).

**Subdomain map** (slide-22 style; read it like the Core Banking oval on slide 23):

```
 Complexity
   ▲
 high ┌─ GENERIC · buy ──────────┐ ┌─ CORE · build in-house, invest here ───────────┐
      │ ┌──────────────────────┐ │ │ ╔════════════════════╗  ╔════════════════════╗ │
      │ │ Identity and Access  │ │ │ ║  Expense Sharing   ║  ║     Settlement     ║ │
      │ └──────────────────────┘ │ │ ║ split, correct,    ║  ║ balances, simplify ║ │
      │ ┌──────────────────────┐ │ │ ║ remove, late joiner║  ║ payments, close    ║ │
      │ │ Notification Delivery│ │ │ ╚════════════════════╝  ╚════════════════════╝ │
      │ └──────────────────────┘ │ └────────────────────────────────────────────────┘
      │                          │ ┌─ SUPPORTING · frameworks or outsource ─────────┐
      │                          │ │ ┌────────────────────┐  ┌────────────────────┐ │
      │                          │ │ │ Group & Membership │  │History & Reporting │ │
      │                          │ │ │ invite, roles,     │  │ activity feed,     │ │
      │                          │ │ │ leave at balance 0 │  │ archive, export    │ │
  low │                          │ │ └────────────────────┘  └────────────────────┘ │
      └──────────────────────────┘ └────────────────────────────────────────────────┘
      └──────── low ─────────────────────── high ──────► Business model differentiation
```

### 7.1 Core

Core = high complexity + high differentiation. Build it in-house, invest most here, never outsource it (slide 23).

| Subdomain | Journeys | Why core (slide-26 criteria) |
|---|---|---|
| **Expense Sharing**: recording expenses, split strategies (equal/exact/%), rounding, corrections with history, removal, late-joiner rule | J4–J6, J9 | **USP:** yes, it's what users come for. **Complexity:** high (3 strategies, rounding, 5 invariants, versioned corrections). **Change rate:** high (share-based splits and recurring expenses come next). No component to buy. |
| **Settlement**: balance calculation, debt simplification, settlement payments with confirmation, close-for-settlement lifecycle | J7, J8, J12, J13 | **USP:** yes, "who owes whom" plus our close phase, which no competitor has. **Complexity:** high (minimum-payment plan, plan recalculation, pending/confirmed payments, lifecycle rules). **Company-specific:** our freeze/reopen/auto-archive rules. |

- **Possible objection:** "Splitwise already exists, so this is not core."
  - Slide 26 asks whether a solution or component can be bought and plugged in. A competitor's whole app is not a component.
  - (note:) Minimising the number of settlement payments is NP-hard in general, so it is not a trivial algorithm.
- **Alternative view:** one core subdomain "Expense Sharing and Settlement".
  - 🟢 We split it because the two change for different reasons: split rules vs payment and closing rules.
  - That makes them good separate module candidates later.

### 7.2 Supporting

Supporting = company-specific but low complexity. Mostly CRUD, stable. Build it with frameworks or outsource it (slide 24).

| Subdomain | Journeys | Why supporting |
|---|---|---|
| **Group and Membership**: create group, invitations with expiry, join/decline, roles (admin), leave/remove, former members | J2, J3, J9–J11 | Company-specific rules (leave only at balance 0, the last admin must promote someone), but each rule is a simple check. Low complexity, low change rate. No advantage over competitors. |
| **History and Reporting**: activity feed, archived read-only view, export, statistics | J13, J16 | Read models over existing data, typical CRUD/ETL. Needed for a complete product (slide 22), but nobody picks an app for its export. |

**Borderline case:** Group and Membership could look core, because R11 couples it to balances. It stays supporting because the rule only asks Settlement "is the balance 0?". The complex part lives in Settlement.

### 7.3 Generic

Generic = can be complex, but it's solved the same way everywhere. Buy it or use standard software (slide 25).

| Subdomain | Journeys | Why generic | Off-the-shelf option (note:) |
|---|---|---|---|
| **Identity and Access**: registration, login, password reset, email confirmation | J1 | Security is complex, but every app does it the same way. Slide 25's own example is Active Directory. | Keycloak, Auth0, Spring Security OAuth2 |
| **Notification Delivery**: sending email and push messages | J3, J5, J12, J14 | Delivery is commodity. *What* to notify is decided by the core contexts. | SMTP service, Firebase Cloud Messaging |
**🟢 Dropped (team decision 14.10): Currency Exchange Rates and Payment Transfer.**
- Each group has exactly **one currency**, and every expense and settlement payment is in it. There is no conversion.
- ShareWise only **records** settlement payments. The money moves outside the app (cash, bank).
- So neither is a subdomain of our product any more, and neither gets a context or a context-map edge.

**Out of scope for the software:**
- Following the slide-21 "departments" view, a real ShareWise company would also have marketing, customer support and subscription billing.
- Slide 22 says a missing subdomain makes the solution incomplete. So name these in P1 and scope them out.

### 7.4 Next step

These 6 subdomains are the problem space. Ex2 part 2 (slide 44) designs the bounded contexts, and they need not be 1:1 with the subdomains. Slide 40's User / Member / Participant / Debtor split already points to these context candidates:
- Identity
- Group and Membership
- Expense Sharing
- Settlement
