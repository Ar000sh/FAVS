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

⚠ **Before presenting, check with the team:**
- Which Account version goes on the slide: the team version (with password, tokens and Hasher) or our proposal with Supabase? Section 6 above describes the proposal. If the team version is shown, replace the middle paragraph with: "For now we modelled login ourselves, with a password hash and tokens for email verification and password reset. Later we could replace it with a provider like Keycloak, because the other contexts only know the UserId."
- The main diagram also has a "reads" line from Group to MemberBalance. If asked: hasZeroBalance is the mechanism; the line is only for showing balances.
