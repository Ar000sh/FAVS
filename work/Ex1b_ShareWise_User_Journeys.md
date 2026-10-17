# ShareWise: User Journeys (Ex1b) + Feature Scope

**Purpose:** a complete picture of ShareWise functionality as the base for Ex2 (subdomains, bounded contexts, context map, ubiquitous language) and Ex3 (aggregates, events).
**Starting point from the lecture:**
- The 10-step Mallorca journey (DDD slide 5)
- The open "close group" questions (DDD slide 7)
- Ex1b: "how are corrections handled, what happens if somebody joins or leaves the group"

Everything marked **🟢 Decision** is *our* design choice. The slides leave it open. Be ready to defend these in the presentation.

---

## 1. Market research: what similar apps do

| Feature | Splitwise | Tricount | Settle Up | Splid | Spliit (OSS) | → ShareWise |
|---|---|---|---|---|---|---|
| Groups + invite (link/email) | ✅ | ✅ (≤50 people) | ✅ | ✅ (no signup) | ✅ link = group | **MVP** |
| Members without account (placeholder) | ✅ (via email) | ✅ (just names) | ✅ | ✅ | ✅ | Could |
| Split equally | ✅ | ✅ | ✅ | ✅ | ✅ | **MVP** |
| Split by exact amounts / % / shares | ✅ all | ✅ | ✅ | ✅ | ✅ | **MVP** (exact, %) |
| Multiple payers per expense | ✅ | – | ✅ | ✅ | – | Won't (MVP) |
| Edit / delete expense | ✅ (restore deleted) | ✅ | ✅ | ✅ | ✅ | **MVP** (+ history) |
| Comments on expense | ✅ | – | – | – | – | Could |
| Balances "who owes whom" | ✅ | ✅ | ✅ | ✅ | ✅ | **MVP** |
| **Simplify debts** (min. # payments) | ✅ | ✅ | ✅ | ✅ | ✅ | **MVP** |
| Record settlement / mark as paid | ✅ | ✅ | ✅ | ✅ | ✅ | **MVP** |
| Payment reminders / requests | ✅ | ✅ | ✅ (paid) | – | – | Should |
| Remove member only if balance = 0 | ✅ (must clear balance first) | ✅ (no open expenses) | | | | **MVP rule** |
| Leave group | ✅ (balance 0) | ✅ (keeps settlement obligation) | | | | **MVP** |
| Archive group | ✅ | ✅ (restore possible) | ✅ | | | **MVP** |
| Explicit "close for settlement" | – | – | – | – | – | **MVP**, our differentiator |
| Multi-currency (exchange rates) | ✅ 76 currencies, Pro conversion | ✅ free, daily rates | ✅ | ✅ | ✅ | Won't (dropped 14.10) |
| Recurring expenses | ✅ (weekly…yearly) | ❌ | ✅ (paid) | ❌ | ✅ beta | Could |
| Categories + statistics | ✅ | ✅ | ✅ (paid) | | ✅ | Could |
| Receipt photo / OCR itemisation | ✅ Pro OCR | ✅ photo | | | ✅ AI scan | Won't |
| Activity feed + notifications | ✅ | ✅ | | | | Should |
| Export (CSV/PDF/Excel) | ✅ CSV | | ✅ Excel | ✅ PDF/Excel | | Could |
| Offline entry | | ✅ | | ✅ | PWA | Won't |
| Payments integration (Venmo/PayPal/bank) | ✅ (US) | ✅ (bunq) | | | | Won't (generic / external) |

**Takeaways for ShareWise**
1. Every competitor has *the same core*: groups, expense splitting, balances, debt simplification, settlement. That is the **core domain** candidate.
2. **No competitor has an explicit "close for settlement" lifecycle.** Groups are only archived. The lecture's step 9 gives ShareWise a clear differentiator: a freeze phase in which only settlements are allowed.
3. Splitwise's rule "a member with an open balance can't be removed" is the industry standard. We adopt it as an invariant.
4. Splitwise's simplify-debts guarantee: **"it never changes anyone's total balance; it only optimizes the payment paths"**. This is a perfect sentence for the glossary.
5. Identity and notifications are commodity → **generic** candidates. Currency rates and payment transfer are commodity too; 🟢 we dropped both on 14.10 (one currency per group, payments only recorded).

---

## 2. Feature scope (MoSCoW)

| Priority | Features |
|---|---|
| **Must (MVP)** | Register/login · create group · invite + join · record expense (equal / exact / percentage) · correct expense · remove expense · balances + simplified settlement plan · record settlement payment · leave group / remove member (balance = 0) · close group for settlement · reopen · archive |
| **Should** | Activity feed · notifications (invite, expense added/corrected, reminder) · payment reminders · confirm received payment |
| **Could** | Placeholder members without account · recurring expenses · categories + statistics · comments · CSV/PDF export |
| **Won't (this semester)** | Multi-currency / exchange rates · real payment transfer · receipt OCR · multiple payers per expense · offline mode |

(note:) The semester is short and the focus is architecture, not features. Keep the MVP small but *domain-rich*: the interesting rules sit in splitting, correction and closing.

---

## 3. Actors & roles

| Actor | Description |
|---|---|
| **Visitor** | Not registered. Can open an invite link and is asked to register. |
| **User** | Registered account (email, display name, password). Can create groups. |
| **Group Admin** | The member who created the group (Alice). Can promote other members to admin. |
| **Member** | A user who joined a group. |
| **Payer** | The member who paid one specific expense. |
| **Participant** | A member who shares the cost of one specific expense. |
| **Debtor / Creditor** | A member with a negative / positive balance in a group. |
| **System** | Timers (invite expiry, auto-archive), notifications. |

(note:) These are exactly the "same person, different contexts" roles from DDD slide 40. Keep this table: it is your argument for the bounded contexts in Ex2.

---

## 4. Business rules (decided)

### 4.1 Group lifecycle (answers DDD slide 7)
```
          closeGroupForSettlement()            all balances = 0 (auto)
  OPEN ───────────────────────────► CLOSED_FOR_SETTLEMENT ───────────────────► ARCHIVED
    ▲                                   │                    or archiveGroup() by admin
    └──────── reopenGroup() ────────────┘                    (only if balances = 0)
```
| Slide 7 question | 🟢 Decision |
|---|---|
| Who is authorized to close? | **Group admins only** (creator is admin by default; admins can promote members). |
| Can expenses be added afterwards? | **No.** When CLOSED, only settlement payments are allowed. |
| Can expenses still be corrected? | **No.** Admin must **reopen** first. The reopen is visible in the activity feed. |
| Must all balances be 0 before closing? | **No.** Closing *freezes* the expenses and fixes the final settlement plan. Balances must be 0 to **archive**. |
| Does archiving happen automatically? | **Yes**, as soon as the last balance reaches 0. An admin can also archive manually, but only at balance 0. |
| Can closing be revoked? | **Yes**, an admin can reopen while CLOSED. **ARCHIVED is final** (read-only). |

### 4.2 Expenses
- **R1** The amount is > 0.
- **R2** The payer is a member of the group (at the time of the expense).
- **R3** Every participant is a member of the group. There must be at least 1 participant (the payer may or may not be one).
- **R4** The shares add up exactly to the amount.
  - With percentages, they sum to 100 %.
  - Rounding: remainder cents go to the first participant(s). 🟢 Decision.
- **R5** Expenses can only be recorded, corrected or removed while the group is OPEN.
- **R6** May correct or remove: the person who recorded the expense, the payer, or an admin. 🟢 Decision.
- **R7** A correction does **not overwrite silently**. The old version stays in the history, status becomes CORRECTED, and participants are notified.
- **R8** Removal is a **soft delete** (status REMOVED, visible in history, ignored for balances).

### 4.3 Membership
- **R9** Join only via a valid invitation (link or email). Invitations expire after 7 days. 🟢 Decision.
- **R10** **Late joiners** only share in expenses recorded *after* they join. Nothing is retroactive, unless an existing expense is explicitly corrected to include them.
- **R11** A member can **leave only with balance = 0**. The same applies when an admin **removes** a member (industry standard, Splitwise).
- **R12** The last admin can't leave while other members remain. They must promote someone first.
- **R13** Former members stay visible in historical expenses ("Bob (left)").

### 4.4 Balances & settlement
- **R14** Balance = total paid − total owed shares (over active expenses) ± settlements. **The sum over all members is always 0.**
- **R15** The settlement plan is **simplified** (minimum number of payments). It **never changes anyone's total balance**, only who pays whom.
- **R16** A settlement payment is recorded by the debtor (status PENDING) and **confirmed by the creditor** (CONFIRMED). Only confirmed payments change balances. 🟢 Decision (Should; MVP may skip confirmation).
- **R17** A settlement can't be larger than the debtor's open debt. 🟢 Decision.

---

## 5. User journeys

Format per journey: actor · trigger · preconditions · main flow · alternatives/errors · rules · **domain events** (useful for Ex3).

### J1: Register & log in
- **Actor:** Visitor
- **Trigger:** wants to use ShareWise or opened an invite link
- **Flow:**
  1. Enter email, display name, password.
  2. Confirm email.
  3. Log in.
  4. Land on "My groups" (empty).
- **Alternatives:**
  - Email already registered → offer login.
  - Coming from an invite link → after login, continue straight to J3.
- **Events:** `UserRegistered`
- *(note: identity = generic subdomain candidate, could be Keycloak / OAuth instead of self-built)*

### J2: Create a group
- **Actor:** User (Alice)
- **Flow:**
  1. "New group".
  2. Name "Mallorca 2027", currency EUR (one per group, fixed), optional description and dates.
  3. The group is created in status OPEN.
  4. Alice becomes member + admin.
- **Errors:** empty name.
- **Events:** `GroupCreated`, `MemberJoined(Alice, ADMIN)`

### J3: Invite friends & join
- **Actors:** Admin/Member (Alice) → Invitee (Bob, Carol, David)
- **Flow:**
  1. Alice opens the group and chooses "Invite".
  2. Either shares an invite **link** or enters **emails**.
  3. Bob opens the link and logs in (or registers, J1).
  4. Bob sees the group preview and taps "Join".
  5. Bob becomes a Member, and everyone sees "Bob joined".
- **Alternatives:**
  - Invite expired → "Ask for a new invite".
  - Already a member → open the group.
  - Group CLOSED or ARCHIVED → joining not possible.
  - Invitee declines → invitation status DECLINED.
- **Rules:** R9, R10
- **Events:** `MemberInvited`, `InvitationAccepted` / `InvitationDeclined`, `MemberJoined`

### J4: Record an expense
- **Actor:** Member
- **Preconditions:** group OPEN
- **Flow:**
  1. "Add expense".
  2. Enter title, amount, date, payer (default: me) and participants (default: all).
  3. Choose the split: **equal / exact amounts / percentage**.
  4. The system previews each person's share.
  5. Save. Balances update and participants are notified.
- **Variants:**
  - **4a Equal:** €180 / 4 = €45 each.
  - **4b Exact:** amounts per person. They must add up to the total (R4).
  - **4c Percentage:** they must add up to 100 %. Rounding by R4.
- **Errors:**
  - amount ≤ 0
  - shares ≠ total
  - payer or participant not a member
  - group not OPEN
- **Rules:** R1–R5
- **Events:** `ExpenseRecorded`

### J5: Correct an expense
- **Actor:** recorder, payer, or admin (R6)
- **Trigger:** wrong amount, wrong payer, someone forgotten in the split
- **Flow:**
  1. Open the expense and choose "Correct".
  2. Change the amount, payer, participants or split.
  3. Optionally give a reason.
  4. Save. The old version goes to the history and the status becomes CORRECTED.
  5. Balances are recalculated and affected participants are notified.
- **Alternatives:**
  - Group CLOSED → "Ask an admin to reopen the group" (→ J12b).
  - Not authorized → error.
- **Rules:** R5–R7
- **Events:** `ExpenseCorrected(old, new)`
- *Example:* the dinner was actually €200, not €180, so each share goes from €45 to €50.

### J6: Remove an expense
- **Actor:** recorder, payer, or admin
- **Flow:**
  1. Open the expense and choose "Remove".
  2. Confirm.
  3. Status becomes REMOVED. The expense is ignored for balances but stays visible in the history.
- **Alternative:** restore a removed expense (Could).
- **Rules:** R5, R6, R8
- **Events:** `ExpenseRemoved`
- *Example:* groceries were entered twice by mistake, so the duplicate is removed.

### J7: Review balances ("who owes whom")
- **Actor:** Member
- **Flow:**
  1. Open the "Balances" tab.
  2. See each member's balance (+ is owed / − owes).
  3. See the **simplified settlement plan**, e.g. "David → Alice €371".
  4. Optionally drill down into the expenses behind a balance.
- **Rules:** R14, R15
- **Events:** none (read model / query)
- *(note: a natural read model, CQRS candidate later)*

### J8: Record a settlement payment
- **Actors:** Debtor (David) → Creditor (Alice)
- **Flow:**
  1. David taps "Settle up" next to "David → Alice €371".
  2. The amount is prefilled. He records it as paid (cash/bank outside the app).
  3. The payment is PENDING and Alice is notified.
  4. Alice confirms receipt. Status becomes CONFIRMED and balances update.
- **Alternatives:**
  - Partial payment (e.g. €200 of €371).
  - Alice disputes it → REJECTED, and David is notified.
  - Amount > open debt → error (R17).
- **Rules:** R16, R17
- **Events:** `SettlementPaymentRecorded`, `SettlementPaymentConfirmed` / `…Rejected`

### J9: Late joiner
- **Actor:** Eve (invited on day 3)
- **Flow:** same as J3. From then on Eve can be payer or participant in *new* expenses.
- **Rule:** R10. The hotel (day 1) is not split with Eve unless someone explicitly corrects it (J5).
- **Events:** `MemberJoined`

### J10: Leave a group
- **Actor:** Member (Bob)
- **Flow:**
  1. "Leave group".
  2. The system checks the balance.
  3. If it is 0, Bob leaves. The status becomes FORMER_MEMBER and he stays visible in old expenses.
- **Alternative:** balance ≠ 0 → "You still owe Alice €202. Settle first." (link to J8).
- **Errors:** last admin with other members present → "Promote another admin first" (R12).
- **Rules:** R11–R13
- **Events:** `MemberLeft`

### J11: Remove a member (admin)
- **Actor:** Admin
- **Flow:**
  1. Open the member list and choose "Remove Bob".
  2. Balance check (R11).
  3. Bob is removed and notified.
- **Alternative:** balance ≠ 0 → the admin is shown the settlement options.
- **Events:** `MemberRemoved`

### J12: Close the group for settlement
- **Actor:** Admin (Alice)
- **Preconditions:** group OPEN
- **Flow:**
  1. "Close group for settlement".
  2. The system shows a summary: total spent, final balances, simplified plan.
  3. Alice confirms. Status becomes CLOSED_FOR_SETTLEMENT.
  4. Adding or correcting expenses is now blocked.
  5. All members are notified with "your final amount".
- **J12b Reopen:**
  1. Admin chooses "Reopen". Status becomes OPEN.
  2. Corrections are possible again.
  3. Members are notified.
- **Rules:** §4.1
- **Events:** `GroupClosedForSettlement`, `GroupReopened`

### J13: Archive the group
- **Trigger:** the last settlement is confirmed, so all balances are 0 (automatic), or the admin archives manually.
- **Flow:**
  1. Status becomes ARCHIVED.
  2. The group is read-only and moves to "Archived groups".
  3. Optional: export.
- **Errors:** manual archive with balances ≠ 0 → refused.
- **Events:** `AllBalancesSettled`, `GroupArchived`

### Should/Could journeys (short)
- **J14 Payment reminder:** a creditor sends a reminder to a debtor (`PaymentReminderSent`).
- **J15 Recurring expense:** a monthly expense (e.g. rent in a shared flat) is generated by the system (`RecurringExpenseScheduled`).
- **J16 Activity feed:** a chronological list of all group events. These are just the domain events, rendered as a feed.
- **J17 Placeholder member:** an admin adds "Grandpa" without an account. He can claim the placeholder later when he registers.

---

## 6. End-to-end example: "Mallorca 2027", extended

Members: Alice (admin), Bob, Carol, David. **Eve joins on day 3.** All splits are equal unless stated otherwise.

| # | Day | Journey | What happens | Payer | Amount | Participants → share |
|---|---|---|---|---|---|---|
| 1 | 0 | J1–J3 | Alice registers, creates the group, invites. B, C, D join | | | |
| 2 | 1 | J4a | **Hotel** | Alice | 900 | A, B, C, D → 225 |
| 3 | 1 | J4a | **Dinner** (entered as €180) | Bob | 180 | A, B, C, D → 45 |
| 4 | 2 | J5 | Dinner **corrected** to €200 (receipt was wrong) | Bob | 200 | A, B, C, D → 50 |
| 5 | 2 | J4a | **Rental car** | Carol | 420 | A, C, D → 140 |
| 6 | 2 | J4a | **Museum** | David | 75 | B, C, D → 25 |
| 7 | 3 | J9 | **Eve joins** (late joiner) | | | |
| 8 | 3 | J4a | **Boat trip** | Eve | 300 | A, B, E → 100 |
| 9 | 4 | J4a | **Groceries** | Bob | 60 | A, B, C, D, E → 12 |
| 10 | 4 | J6 | Groceries accidentally entered **twice**, duplicate **removed** | | | |
| 11 | 5 | J4b | **Farewell dinner, exact split** | Alice | 250 | A 50, B 50, C 40, D 60, E 50 |

### Balances after step 11 (J7)
| Member | Paid | Owed share | **Balance** |
|---|---|---|---|
| Alice | 900 + 250 = **1150** | 225 + 50 + 140 + 100 + 12 + 50 = **577** | **+573** |
| Bob | 200 + 60 = **260** | 225 + 50 + 25 + 100 + 12 + 50 = **462** | **−202** |
| Carol | **420** | 225 + 50 + 140 + 25 + 12 + 40 = **492** | **−72** |
| David | **75** | 225 + 50 + 140 + 25 + 12 + 60 = **512** | **−437** |
| Eve | **300** | 100 + 12 + 50 = **162** | **+138** |
| **Σ** | **2205** | **2205** | **0** ✓ |

### Continuation
| # | Day | Journey | What happens |
|---|---|---|---|
| 12 | 5 | J10 (fails) | Bob flies home early and tries to **leave** → refused: "You owe €202". |
| 13 | 5 | J8 | Bob pays Alice **€202**, Alice confirms. Bob = 0, Alice = +371. |
| 14 | 5 | J10 | Bob **leaves**. He shows as "Bob (left)" in old expenses. |
| 15 | 6 | J12 | Alice **closes the group for settlement**. The final balances + simplified plan are shown (below). |
| 16 | 6 | J4 (fails) | Carol tries to add a forgotten taxi → refused: "Group is closed for settlement." The group agrees it's not worth reopening. *(Otherwise J12b: Alice reopens, Carol adds the taxi, Alice closes again, and the plan is recalculated.)* |
| 17 | 7–10 | J8 | Settlements per the plan, each confirmed by the creditor. |
| 18 | 10 | J13 | Last confirmation → all balances 0 → **auto-archive**. |

**Simplified settlement plan after Bob left** (Alice +371, Eve +138, Carol −72, David −437):
- David → Alice **€371**
- David → Eve **€66**
- Carol → Eve **€72**

Check: David pays 437 ✓, Eve receives 138 ✓, Alice receives 371 ✓. That is **3 payments** instead of up to 6 pairwise debts.

---

## 7. Bridge to Ex2: what the journeys reveal (first draft, discuss)

| Journeys | Area of activity | Subdomain type (first guess) | Why |
|---|---|---|---|
| J4–J6 | Expense recording & splitting | **Core** | Split strategies, corrections, invariants. Complex and the heart of the product |
| J7, J8, J12, J13 | Balance calculation & settlement (incl. close lifecycle) | **Core** | Debt simplification + close-for-settlement lifecycle = our differentiator |
| J2, J3, J9–J11 | Group & membership management | **Supporting** | Company-specific rules (leave only at 0), but mostly CRUD |
| J1 | Identity & access | **Generic** | Commodity: buy/use Keycloak/OAuth |
| J14, J16 | Notifications / activity feed | **Generic / Supporting** | Standard messaging/email services |

The **same person** appears as User (J1), Member (J2/J3/J10), Payer/Participant (J4) and Debtor/Creditor (J7/J8). These are the context boundaries that DDD slide 40 hints at.

### Glossary seeds (for the ubiquitous language)
Group · Member · Admin · Invitation · Expense · Payer · Participant · Share · Split strategy (equal/exact/percentage) · Correction · Balance · Debt · Creditor/Debtor · Settlement plan · Settlement payment · Close for settlement · Reopen · Archive · Late joiner · Former member

---

### Sources (market research)
- [Splitwise: App Store](https://apps.apple.com/us/app/splitwise/id458023433), [What is Simplify Debts?](https://kb.splitwise.com/balances-and-expenses/what-is-simplify-debts), [Removing a person from a group](https://kb.splitwise.com/groups/how-do-i-remove-a-person-from-a-group)
- [Tricount Help: manage tricounts & expenses](https://help.tricount.com/articles/how-can-i-manage-my-tricounts-and-expenses)
- [Splitwise vs Tricount vs Settle Up 2026](https://tripprof.com/en/blog/best-apps-track-split-group-trip-expenses/), [Tricount vs Splid](https://spliit.pro/blog/tricount-vs-splid/), [Best bill splitting apps 2026](https://www.splitmyexpenses.com/articles/best-bill-splitting-apps)
- [Spliit (open source)](https://spliit.app/), [GitHub spliit-app/spliit](https://github.com/spliit-app/spliit)
