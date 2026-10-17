# FAVS – 02 Domain-Driven Design (Lecture 2, 06.10.2026)

Source: `skripte/02.DDD.pdf` (80 slides, Hans Grönniger). The deck says it is "adapted from Nane Kratzke, *Cloud-native Computing*, 2024" (slide 9). Most diagrams come from **Vladik Khononov, *What Is Domain-Driven Design?*, O'Reilly 2019** ("Bildquelle").

**Slide numbering:** "(slide N)" means the **PDF page number**. The printed footer number matches it up to slide 44. From slide 45 on, the footer is **one higher** (PDF p45 shows "46", PDF p80 shows "81"). Slides 9/10 print "99"/"1010".
Anything marked **(note:)** is my own clarification. It is not on the slides.

---

## 0. Where this lecture sits in the ShareWise project

### "Where do we stand in the ShareWise project?" (slide 3)
| | |
|---|---|
| **So far** | Defined cloud computing · got to know ShareWise as a case study · gone through the Mallorca user journey |
| **Today, we learn how to** | **Specify the language of the domain** · **Make business processes visible** · **Identify business boundaries** · **Discover rules and invariants** |
| **Up next** | Implement ShareWise as a **modular monolith** |

### Project roadmap: "ShareWise: From modular monolith to cloud-native system" (slide 4)
The diagram is a chain of 8 numbered steps, drawn as coloured boxes:
**Understand the domain** →1→ **Build a modular monolith** →2→ **Containerize the application** →3→ **Automate build and deployment** →4→ **Identify change drivers** →5→ **Extract selected services** →6→ **Introduce events and messaging** →7→ **Handle distributed consistency** →8→ **Add resilience and observability**.
This lecture is the first box: "Understand the domain".

### Opening quote (slide 2)
> "There should be some learning when a domain model is discussed." – **Eric Evans**

---

## 1. ShareWise: everything in this deck

### 1.1 User journey (slides 5, 6)
Slides 5 and 6 show the ShareWise logo (green/purple hexagon with "S") next to the 10-step "Mallorca 2027" journey:
1. A user registers
2. The user creates the group "Mallorca 2027"
3. Friends are invited
4. The invited users join the group
5. Members record shared expenses
6. Expenses are corrected or removed when necessary
7. Members review their current balances
8. Members record settlement payments
9. **An authorized member closes the group for settlement**
10. The group is archived

On slide 6, step 9 is **bold** and has a red annotation: **"What are the business rules for this step?"**

### 1.2 Business rules of step 9 (slide 7)
"An authorized member closes the group for settlement". **What are the rules for this step?**
- Who is authorized?
- Can expenses be added afterwards?
- Can expenses still be corrected?
- Need all balances be 0 before closing?
- Does archiving happen automatically afterwards?
- Can closing be revoked?

(note:) The slides only ask these questions and leave them open. They show the kind of question you have to answer explicitly when you define the ubiquitous language and the invariants ("make implicit assumptions explicit", slide 31).

### 1.3 Why a common business model is needed (slide 8)
**"Same words, different concepts, different understanding."**
Possible consequences:
- contradictory requirements
- unclear business rules
- incorrect data models
- unclear responsibilities
- special cases in the application code
- unstable module boundaries
- inappropriate service limits

> "Before we technically divide into modules, we need a common business model. And agree on the meaning of words. Work on a common 'mental model'."

### 1.4 "ShareWise Domains?" (slide 27)
- "Discuss in groups." (The slides give no solution.)

### 1.5 "ShareWise Language?" (slide 36)
Candidate terms for the ubiquitous language:
- **Expense**
- **Share**
- **Balance**
- **Debt**
- **Settlement**

Then two more bullets:
- **Business rules (invariants)**
- **Glossary** (in red, i.e. the expected artefact)

### 1.6 Ubiquitous language in ShareWise code (slide 35)
| Like so (domain language) | But not like (technical/generic) |
|---|---|
| `closeGroupForSettlement()` | `updateStatus()` |
| `recordSettlementPayment()` | `processData()` |
| `calculateFinalBalances()` | `handlePayment()` |
| `archieveGroup()` *(sic)* | `calculate()` |

### 1.7 "ShareWise Example": same person, different contexts (slide 40)
"The very same person using the app can be modelled differently in different context":
- **User** (with an account, login)
- **Member** (of a group, with invitation, a role in the group)
- **Participant** (in one concrete expense)
- **Debtor, creditor** (with a balance)

(note:) This is the ShareWise version of the "Lead" example on slide 39 (marketing vs. sales). It is the main hint the slides give for drawing ShareWise bounded contexts.

### 1.8 "ShareWise Bounded Contexts?" (slide 44)
- The slide is empty apart from the title and logo. It is a discussion/exercise prompt.

### 1.9 "ShareWise Context Mapping?" (slide 55)
- "**Part of the exercises.**"

### 1.10 Tactical building blocks for ShareWise (slide 68)
- **Entity:** Group, Expense, SettlementPayment, …
- **Value Object:** Money, ExpenseShare, Percentage, GroupName

### 1.11 Expense aggregate and invariants (slide 69)
**Expense Aggregate** (tree):
- ExpenseId
- GroupId
- PayerId
- Money
- ExpenseShares
- ExpenseStatus

**Possible invariants:**
- The amount is positive.
- The sum of the shares corresponds to the total amount.
- The payer belongs to the group.
- All those involved belong to the group.
- A finalized issue *(sic, meaning: expense)* may not be changed directly.

### 1.12 Expense domain model as a UML class diagram (slide 64)
The diagram on the "Core Subdomains: Domain Model" slide is a ShareWise model:
- **«Aggregate Root» Expense**
  - Attributes: `+ExpenseId id`, `+GroupId groupId`, `+UserId paidBy`, `+Money amount`, `+SplitStrategy splitStrategy`, `+ExpenseStatus status`
  - Operations: `+correct(newAmount) : ExpenseCorrected`, `+remove() : ExpenseRemoved`. These return **domain events**.
- **«Value Object» SplitStrategy**: `EQUAL`, `EXACT`, `PERCENTAGE` (composition 1–1)
- **«Value Object» ExpenseStatus**: `ACTIVE`, `CORRECTED`, `REMOVED` (composition 1–1)
- **GroupId**: dashed "references" arrow. Another aggregate is referenced **by identity only** (cf. aggregate rule 3).
- **«Entity» ExpenseParticipant**: `+UserId userId`, `+Money owedShare`. Expense "splits into" **2..\*** participants (composition).
- **«Value Object» Money**: `+BigDecimal amount`, `+Currency currency`. Used for the Expense's "total amount" (1) and the participant's "owed share" (1).

(note:) Slide 68 lists "ExpenseShare" as a value object, while slide 64 models the split as an "ExpenseParticipant" entity. The slides do not reconcile the two. Pick one name and put it in your glossary.

---

## 2. DDD: what it is

### Agenda (slides 9, 10, 18, 37, 56, 73)
- **Domain Driven Design:** What is it? · Effective Software Design · Strategic Design · Tactical Design
- **Strategic Design:** Subdomains · Ubiquitous Language · Bounded Context · Context Mapping. (On slides 9/10 the order is "Subdomains · Bounded Context + Ubiquitous Language · Context Mapping".)
- **Tactical Design:** Business Logic Pattern · Architectural Pattern

The recurring sketch next to the agenda (slides 18, 37, 56, 73) is Vernon-style. It shows dashed **context boundaries** around a **Shipping Subdomain** (Packaging, Delivery), a **Pricing Subdomain** (Discounts), a **Sales Subdomain** (Purchasing, Bundles, Claiming) and a **Legacy Context** (Inventory, ERP). Labels "Domain Model", "Model in Context" and "Context Boundary" point into it.

### Well-known principles for cloud-native design (slide 11)
"On the quest for a good design methodology for cloud-native systems":
- Decomposition (into services)
- Loose coupling (standard formats, e.g. JSON/XML, messaging)
- High cohesion (in modules) (single responsibility principle)
- Independent deployability
- Conway's Law
- You build it, you run it
- …

### Definition (slide 12)
- **DDD is a methodology for modeling complex software.**
- Its major concern is to **understand the business logic**.
- For the design to be effective, it has to be **built around a model of the application domain, the domain model**.
- DDD is oriented towards agile development but does not require it.
- However, **iterative software development and close collaboration between developers and domain experts is required.**

### Effective design (slide 13)
- Strive **not for a perfect but an effective design**.
- Fulfil requirements up to a point so that the software **creates business value** (e.g., be better than the competitor in the core aspects).
- Push organizations to think about what makes the software create that business value.
- **Efforts are focused on the core domain** of requirements.
- **Other areas should be covered with standard software or external services.**
- Quote (Steve Jobs, sketch portrait): *"Most people make the mistake of thinking design is what it looks like. … Design is how it works."*

### Overview diagram (slides 14, 19, 28, 38, 57, 74, 80)
Two chevrons across the top: **Strategic Design → Tactical Design**.
- Left part, **Problem space**: a grey blob, the **Domain**, splits (dashed arrow) into a blob with three red circles (the subdomains).
- Middle, **Solution Space**: a blob with connected red nodes, labelled **Bounded Context**.
- Right: a hexagon, **Architecture**, with **Application** in the centre and **Adapters** on its sides. It connects to a **User**, a **Web service** (cloud) and a **Database**. A dashed arrow leads to **Code** (a red tree of boxes).
- A big red arrow along the bottom: **Ubiquitous Language** spans all of it.
- A red arrow marks the current topic on each copy of the slide: slide 19 = strategic/problem space, slide 28 = solution space/bounded context, slide 38 = bounded context, slide 57 = tactical/code, slide 74 = architecture.

### Strategic design: "How to find out what's important?" (slide 15)
- What is important to reach our business goals?
- How do we divide the work based on priorities?
- Where do we consolidate?

**Approach:**
- Involve **domain matter experts** using a common language (**Ubiquitous Language**)
- **Divide complex domain models into subdomains and bounded contexts**
- **Clarify the integrations between subdomains using context mappings**
- Handwritten note: *"From this, ultimately services are defined and teams are formed according to Conway's law."*
- Sketch: "STRATEGY = TAKE THE RIVER; TACTICS = USE A BOAT" (a river through mountains and desert).

### Tactical design: "How to break down what's important" (slide 16)
- "Tactical design is like using a **thin brush to paint the fine details** of your domain model." (Vaughn Vernon)
- Transition from problem to solution space.
- Work out the details of a bounded context.

**Approach:**
- Working **inside** a bounded context
- **Combining entities and value objects into aggregates**
- **Model and implement service interactions across bounded contexts using domain events**

### DDD everywhere? (slide 17)
> "There is a life beyond DDD. Not every good design needs to be Domain-Driven (though I can accept it should always be driven by the domain, just not necessarily in the DDD sense). **You can design good systems even if you're not a DDD expert.**" – Stefan Tilkov (INNOQ), blog post. See also GOTO 2019 "Good Enough Architectures".

---

## 3. Strategic design: business domain and subdomains

### Business domain (slide 20)
- "A **business domain** defines the **area of activity of an organization or company**. In general, it is the service offered to customers."
- A company can operate in **multiple business domains**. Example: **Amazon** offers both retail and cloud computing services.
- Companies may **change their business areas over time**. Example: **Nokia** has been active in woodworking, rubber manufacturing, telecommunications and mobile devices.
- Logos on the slide, with the question "**Main business domain?**": **DHL Group, Starbucks, Galeria Karstadt Kaufhof**.

### Subdomain (slide 21)
- To achieve the goals of its business domain, a company must operate in **multiple subdomains**.
- "**A subdomain is a fine-grained area of business activity.**"
- **All subdomains together make up the company's business domain.**
- Often, **subdomains correlate with the company's departments** or other organizational units.
- Example: an **online retail store** might include catalog management, advertising, accounting, support, customer relations, supplier relationships, and others.
- **Diagram "Retailer Domain Model":** a UML-like entity model with coloured areas. The legend says "**Each coloured area is a subdomain (bounded context)**". Solid lines are relationships, **dashed lines are cross-context references**.
  - *Catalog Management:* Category (1–0..\*) Product (id, sku, name, description, status); Product (1–1..\*) ProductVariant (sku, attributes, price, status); ProductImage (url, altText); InventoryItem (quantityOnHand, reorderPoint)
  - *Advertising:* Campaign (name, objective, budget, startDate, endDate) 1–1..\* Ad (title, content, mediaUrl, status); Channel (name, type); AdPlacement (placementDate, cost, impressions, clicks)
  - *Customer Relations* (centre): Customer (name, email, phone, status, joinedAt), CustomerSegment, Address, LoyaltyAccount (pointsBalance, tier)
  - *Supplier Relationships:* Supplier, SupplierContact, PurchaseOrder, PurchaseOrderItem, SupplierProduct (supplierSku, leadTimeDays)
  - *Support:* Ticket (subject, description, status, priority, createdAt), TicketMessage, TicketAssignment, Agent
  - *Accounting:* Order → OrderItem → Payment → Invoice → Refund
  - Customer Relations has dashed cross-context links to Catalog, Advertising, Supplier Relationships, Support and Accounting.

### The term "domain" and the three subdomain types (slide 22)
- "A **domain** is generally understood to be a **specific area of business activity or knowledge**."
- The term is very broad and abstract. To make it more concrete and tangible, it makes sense to **divide it into smaller parts called subdomains**.
- **Subdomains come in 3 types:** Core Domain, Supporting Subdomain, Generic Subdomain.
- **Diagram:** a 2-axis chart. Y = **Complexity of business model** (low/high), X = **Business model differentiation** (low/high).
  - **Core** is a circle at **high complexity + high differentiation** (top right).
  - **Generic** is a vertical strip at **low differentiation**, extending up to **high complexity** (left column).
  - **Supporting** is a horizontal strip at **low complexity** (bottom row).
- "**All subdomains, regardless of category, are important for overall solutions.** If a domain is missing, the solution will be incomplete. However, the domains require **different effort** and can also have **different requirements for quality and completeness**."

### Core subdomain (slide 23)
- **Differentiates companies from competitors** through new products or process optimizations.
- **Easy-to-implement core subdomains are not sustainable**, so they are usually **complex with high barriers to entry**.
- **Investments** in system and software development should **primarily go into the core domain**.
- Core subdomains **must be implemented internally** and **cannot be purchased or adopted**.
- **Outsourcing** the implementation of a core subdomain **isn't a good idea**.
- **Diagram (Core Banking example):** an oval "Core Banking" divided by two curves into **Generic** (Security, Communications, Marketing, Accounts, Customers), **Support** (Offers, Benefits, Investment, Mortgage, Cards, Money management) and a middle core area (On-boarding, Products, Payments). (note:) The bubble placement is approximate, read from the image. The same diagram is reused on slide 25.

### Supporting subdomain (slide 24)
- **Does not provide a competitive advantage**. It merely supports the company's core business.
  - **Does not have complex business logic.**
  - Often based on **simple ETL or CRUD** interfaces.
  - **Does not change very often**, is stable.
- Example, an **online advertising company**:
  - *Core domain:* tailoring ads to visitors; ad effectiveness optimization; minimization of advertising costs.
  - *Supporting domain:* **managing creative materials** (does not affect profits).
- **Implementation?**
  - Try to **avoid implementing it yourself**, because it gives no competitive advantage.
  - Often there are no ready-made solutions. Then use **comprehensive application development frameworks**.
  - The simplicity of the business logic makes supporting subdomains an **obvious candidate for outsourcing**.

### Generic subdomain (slide 25)
- Generic subdomains **also show complexity**.
- They **do not provide a competitive advantage**, because there are already **proven and widely used implementations ("commodity")**.
- They are business activities that **all companies carry out in the same way**.
- Therefore attempts are usually made to cover them with **standard software** and systems.
- Examples: **identity management with Microsoft's Active Directory**, **Oracle's database products**, **SAP R/3 or S/4 HANA**.

### Domain types: summary table (slide 26)
(note:) The plain-text extraction of this table is shifted by one row. The values below are read from the rendered slide.

| Criterion | Core | Supporting | Generic |
|---|---|---|---|
| Unique Selling Point / Business Critical | Yes | No | No |
| Company-specific | Yes | Yes | No |
| Technical complexity (barrier to entry) | High | Low | High |
| Technical Rate of Change | High | Low | Low |
| Exist Solutions / Products / Services | No | Partly | Yes |
| In-house development makes sense | Yes | Yes | No |
| Outsourcing of development makes sense | No | Yes | No |
| Do COTS products / managed services exist? | No | Partly | Yes |

---

## 4. Strategic design: ubiquitous language

### Problem space vs. solution space (slide 29)
- A domain is sometimes called a **"problem space"** because it defines the business problems that software is supposed to solve.
- The **problem space** focuses on **business problems**. The **solution space** focuses on **technical solutions**.
- **The subdomains belong in the problem space.**
- The relationship between the problem space and the solution space **is difficult to maintain**.
- Handwritten: common software development methodologies are usually implicitly based on these **translations**: domain knowledge → analysis models → requirements → system design → source code. "**Translation errors can occur at any of these transitions.**"
- Sketch: a "Problem Space" cloud (stakeholders, shared vision, "decompose", "understand the reality of the business") next to a "Solution Space" cloud (collaborate, describe a model using ubiquitous language, validate, experiments, code, bounded contexts).

### Codification of domain knowledge (slide 30)
- Software modeling often translates domain knowledge into an **"engineer-friendly" form**.
- Such artefacts (e.g. UML class diagrams) are called **analysis models**. They describe the requirements for the system.
- Analysis models are **less about understanding the business domain** and more about structuring the solution.
- This translation is **dangerous**: **domain knowledge is lost** on the way to software engineers.
- Yellow box: since the software crisis of the 1960s, studies of failed projects show that **communication is essential**. Most models pass knowledge on through **intermediary roles** (system/business analysts, product owners, project managers). That does not automatically mean effective, understanding-based communication. "**DDD attempts to bring the knowledge of domain experts to software engineers by means of a ubiquitous – and jointly developed – language, the so-called Ubiquitous Language.**"

### Concepts in the problem space: ubiquitous language (slide 31)
- **A common language is key to common understanding.**
- It is a complex but necessary step: **clarification of technical terms**.
- **The clarity of the common language indicates how deeply the problem space is understood.**
- **Unclear terms indicate deeper and hidden (possibly misunderstood) concepts.**
- **Implicit assumptions must be made explicit** so that each term has a clear meaning within the ubiquitous language.
- Red box, **"Ubiquitous":**
  - **Everyone in the project speaks and understands the same language.**
  - **All relevant concepts are described in the language.**
  - The language is **developed evolutionarily** and is **present in all phases of development (also in the code!)**.
  - **One of the most important concepts in DDD**: the basis for common understanding, the basis for end-to-end understanding, and an indicator of domain penetration and descriptive stability.
- Cartoon: people around a table, thought bubble "What are they talking about?"

### Non-DDD vs. DDD (slide 32)
- **Non-DDD diagram:** a red arrow cascading downwards: Domain knowledge → Analysis model → Requirements → System Design → Source code. This is a chain of translations.
- **DDD diagram:** a circle. **Ubiquitous Language** is in the centre, connected to **Domain Knowledge, Analysis model, Requirements, System Design, Source code** around it.
- "Instead of constantly translating domain knowledge, DDD calls for **cultivating a single language to describe the business domain**: the ubiquitous language."
- "Through the consistent use of ubiquitous language, a common understanding can be cultivated between all project stakeholders. **The ubiquitous language should only consist of terms that relate to the business domain.**"

### Ambiguous and synonymous terms (slide 33)
- **Ambiguous terms:** "**Policy**" can mean "legal regulation" or "insurance contract". In an insurance company, *policy* is ambiguous. **Ubiquitous language requires us to define a single meaning for each term.** Solution: use "**regulatory provision**" and "**insurance contract**" (but not *policy*).
- **Synonymous terms:** two terms cannot be used interchangeably. Many systems use "user", "visitor", "administrator", "account", etc. interchangeably. **Synonymous terms usually refer to different detailed concepts.** For example, "visitor" and "account" may technically mean **unregistered** and **registered** users. Understanding the differences allows **simpler and clearer models** and implementations of the domain entities.

### Domain language vs. technical language: marketing example (slide 34)
| Like so (language of marketing domain experts) | But not like (purely technical) |
|---|---|
| An advertising campaign can display various creative formats (videos, banners, animations). | The ad iFrame displays an HTML file that embeds content linked by a URL. |
| A campaign can only be published if at least one of its formats is active. | A campaign can only be published if it has at least one associated record in the active-placements table. |
| Sales commissions are charged for approved transactions. | Sales commissions are based on correlated records from the transactions and approved sales tables. |

Slide 35 gives the ShareWise code example (see §1.6), slide 36 the ShareWise term list (see §1.5).

---

## 5. Strategic design: bounded contexts

### Mastering conceptual complexities: the "Lead" example (slide 39)
- "It is common for **mental models of domain experts to be consistent only in a specific context**."
- **Example: telemarketing company.** The diagram is a flow: Online Advertisement → **Lead** → Call → Sale. Marketing generates leads through online ads. Sales gets potential customers to buy. Both departments understand "lead" differently:
  - **Marketing Department:** a lead represents an **event** that someone is interested in one of the products. Receiving the potential customer's contact details is called a lead.
  - **Sales Department:** a lead represents the **entire lifecycle of a sales process**. It is not just an event, it is a long-lasting process.
- Handwritten: "Enterprise architecture management approaches often claim to develop a **global 'ubiquitous language'** (without calling it that) for an entire company. However, **these approaches often fail.**"

### What is a bounded context? (slide 41)
- "The solution to dealing with such problems is simple. **The goal is not to develop a single, all-encompassing ubiquitous language, but several smaller ones!**"
- **Diagram:** two separate blobs, **Marketing Context** and **Sales Context**. Each contains its own "**Lead**". In Marketing, Lead is annotated as an "**Event**". In Sales, it is a "**Complex Entity**".
- (note:) The deck has no one-line definition of "bounded context". By slides 41–43 it is the **boundary within which one ubiquitous language/model is consistent**, and its boundaries are **designed**.

### Scope of a bounded context (slide 42)
- **The size of a bounded context does not matter too much.**
- Models should never be large or small per se. **Models must be clear and have a purpose.**
- **The broader the boundary of a ubiquitous language, the more difficult it is to keep it consistent.**
- **How large a bounded context is depends on the specific problem domain.**
- Grey box:
  - It can be beneficial to **split a large ubiquitous language into smaller, more manageable problem domains**.
  - However, **striving for small bounded contexts will also create more integration overhead**.
- **Diagram (Khononov):** green blobs show different cut granularities: {Creatives, Acquisition, Ad Campaigns}, {Publishing, Optimization, Reporting}, {CRM, Telephony, Billing}, {Authorization}, {Accounting, Commissions}.

### Bounded contexts vs. subdomains (slide 43)
| Subdomains (microscope icon) | Bounded Contexts (architect-with-blueprint icon) |
|---|---|
| The analysis phase **identifies** the different types of subdomains (Core, Supporting, Generic). | Bounded contexts, on the other hand, are **designed**. |
| "Identification" means the subdomains are **already there**. They are part of the business. Through analysis we **discover** subdomains that already exist. **We don't design them!** | **Choosing the boundaries of models is a strategic design decision.** We decide how to divide the business domain into smaller, manageable problem domains. |
| Subdomains help us **set priorities** and use limited resources primarily in the **core subdomains**. | |

Slide 44 then asks: **"ShareWise Bounded Contexts?"**

---

## 6. Strategic design: context mapping

### Relations between bounded contexts (slide 45)
- Models in different bounded contexts can be developed and implemented **independently** of each other.
- But bounded contexts are **not isolated**. A system cannot be built from independent components. The components must interact to achieve the overarching system goals.
- So there will always be **touchpoints, known as contracts**.
- Two bounded contexts use different ubiquitous languages. **Which language should be used for integration?**
- DDD has patterns for relationships and integrations between bounded contexts, in **three categories**:
  1. **Cooperation**
  2. **Customer-Supplier**
  3. **Separate Ways**

### 6.1 Cooperation patterns (slide 46)
- Cooperation patterns apply to bounded contexts implemented by **teams with well-established communication**.
- E.g., bounded contexts implemented by **the same team**, or teams with **dependent goals**, where the success of one team depends on the other and vice versa.
- Two patterns: **Partnership** and **Shared Kernel**.

#### Partnership (slides 46, 47)
- **Notation:** two ovals "Bounded Context 1" — "Bounded Context 2", joined by a plain line labelled **"Partners"**.
- Integration between the bounded contexts is **coordinated on an ad hoc basis**.
- One team can notify the other of an API change, and the second team will cooperate and adjust **immediately (both ways)**.
- **No team dictates the language.** The teams choose the most appropriate integration solution together.
- **Neither team is interested in blocking the other.**
- Requires **well-established collaboration practices, high engagement and frequent synchronization** between teams.
- **Usually not suitable for geographically dispersed teams** (synchronization and communication issues).

#### Shared Kernel (slides 46, 48)
- **Notation:** two **overlapping** ovals. The red lens-shaped intersection is labelled **"Shared Kernel"**.
- A **more formal way of defining a contract** between bounded contexts **without a power imbalance**.
- The contract is **explicitly defined in a compiled library: the common kernel**.
- Shared kernels **contradict a core principle** of bounded contexts: **only one team should own a bounded context**.
- Key: **keep the shared kernel small** and **limit it to the integration contract only**.
- **Changing the contract can break the other team's build**, so the pattern requires a **high level of synchronization**.
- Shared kernels can be a **disciplining prerequisite** for integrating bounded contexts **owned by the same team**.

### 6.2 Customer-Supplier patterns (slide 49)
- **Notation:** two ovals joined by a line. The left end is marked **U = Upstream (Supplier)**, the right end **D = Downstream (Consumer)**.
- Unlike cooperation, **both teams (upstream and downstream) can succeed independently**.
- So there is often an **imbalance of power**: either the upstream or the downstream team can **dictate the integration contract**.
- DDD has **three patterns** for these power inequalities:
  1. **Conformist**
  2. **Anti-Corruption Layer**
  3. **Open-Host Service**

#### Conformist (slide 50)
- **Notation:** BC1 (U) ← arrow labelled **"Conforms"** ← (D) BC2. The downstream points to the upstream it conforms to.
- **Power is with the upstream team**, which is **not motivated to support its customers' needs**.
- It only provides the integration contract, defined according to **its own model: take it or leave it**.
- Such power imbalances often exist with **external service providers**, but can also come from **internal organizational policies**.
- If the downstream team can accept the upstream model, the relationship is called **conformist**.
- "**The downstream team conforms to the model of the upstream team.**" Giving up some autonomy can make perfect sense, e.g. when the upstream contract is an **industry-standard, well-established model**.

#### Anti-Corruption Layer (ACL) (slide 51)
- **Notation:** BC1 ← arrow ← a small box **"ACL"** at the edge of BC2. The ACL sits on the **downstream** side.
- **The consumer is not willing to accept the supplier's model unconditionally.**
- Power is **still with the upstream** service, but the downstream bounded context is **not ready to adapt**.
- Instead, the upstream model is **translated via an anti-corruption layer** into a model tailored to the needs of the downstream context.
- Use it when fully conforming is **not desirable or not worth the effort**:
  - The downstream bounded context contains a **core subdomain**. Adhering to the supplier's model could hinder modeling its own problem domain.
  - The upstream model is a **legacy model** (e.g., poor or unsuitable).
  - The supplier's contract **changes frequently**.
  - The supplier's model is **very large** and only **parts of it are needed**.

#### Open-Host Service (OHS) + Published Language (slide 52)
- **Notation:** a box **"OHS"** at the edge of the **upstream** BC1. Arrow from BC2 → OHS. OpenAPI Initiative logo on the slide.
- **Power is with the consuming services.**
- The supplier wants to **protect consumers (from changes)** and provide the **best possible service**.
- The upstream supplier **decouples its implementation from the public interface**. So it can evolve its **implementation model and public model at different speeds**.
- The provider's public interface does **not** follow its own ubiquitous language. It gives consumers a **convenient protocol in an integration-oriented language**. This public protocol is called a **"published language"**.

### 6.3 Separate Ways (slide 53)
- The last option is **not to collaborate at all**. Teams are **not willing or able** to work together.
- **Should never be used on bounded contexts belonging to a core subdomain.**
- Reasons:
  1. **Problems with communication:** communication difficulties caused by the size of the organization or internal politics. Then it may be more cost-effective to **duplicate functionality** in several bounded contexts.
  2. **Generic subdomains (libraries):** if the generic solution is easy to integrate, it may be cheaper to integrate it locally in each bounded context. Example: a **logging framework**. It would make little sense to offer it as a service. Duplicating it is efficient.
  3. **Model differences:** the models are so different that a conformist relationship is impossible, and an ACL would cost more than duplicating functionality.

### 6.4 Context maps (slide 54)
- "**Context maps are a top-level visual representation of all bounded contexts of a system.**"
- This simple notation gives strategic insights on several levels:
  - **High-level design:** an overview of the system's components and models.
  - **Communication patterns:** shows which teams work together.
  - **Organizational issues:** "What does it mean when downstream consumers of a particular upstream team all rely on anti-corruption layers, or when all separate ways are focused on the same team?"
- **Example context map (Khononov)**, in words:
  - **Marketing** and **CRM** are **Partners** (plain line).
  - **Billing** (U) ← "Conforms" ← (D) **Marketing**. Marketing conforms to Billing.
  - **Identity and Access** (U) ← "Conforms" ← (D) **Marketing**. A second "Conforms" arrow also goes from **CRM** to Identity and Access.
  - **CRM** has two **ACLs**: one facing **Ads Publisher** (arrow CRM → Ads Publisher, ACL on CRM's side) and one facing **Legacy System** (ACL on CRM's side).
  - **Legacy System** and a second **Billing** oval overlap in a red lens: a **Shared Kernel**.
  - **SQS** offers an **OHS**. CRM → OHS of SQS.
- Notation summary: oval = bounded context. Plain line + "Partners" = partnership. Overlap with red lens = shared kernel. U/D labels = upstream/downstream. Arrow labelled "Conforms" = conformist. "ACL" box on the downstream edge = anti-corruption layer. "OHS" box on the upstream edge = open-host service. (note:) Separate ways is drawn as no connection at all.

Slide 55: **"ShareWise Context Mapping? Part of the exercises."**

(note:) **Not on these slides**, so don't quote them as from this lecture: "Big Ball of Mud" (no slide), "Published Language" as its own context-map pattern (only mentioned inside OHS, slide 52), and "Customer/Supplier" as a separate pattern (here it is only the category name). **Event Storming, Repositories, Factories and Domain/Application Services are not covered in this deck.**

---

## 7. Tactical design

### Intro (slide 58)
- So far: strategic design decisions.
- **Tactical design is about implementing components (bounded contexts), not the entire system architecture.**
- Design patterns for tactical design are discussed **on an overview level**, to explain the differences and where each pattern fits.
- Shown: the book cover of *Patterns of Enterprise Application Architecture* (Martin Fowler et al., 2002) and the river sketch with "TACTICS = USE A BOAT" circled.

### Business logic implementation patterns (slides 59, 61, 63, 70)
- **Not all subdomains are created equal.** Different subdomains have different strategic importance and complexity. **Each pattern suits a different level of complexity** in the business domain.

| Supporting Subdomains | Core Subdomains |
|---|---|
| **Transaction Script** | **Domain Model** (Aggregates) |
| **Active Record** | **Event Sourcing** (Domain Events) |

#### Transaction Script (supporting) (slide 60)
- **Extract – Transform – Load.** Works for the **simplest** problem domains, where business logic resembles ETL: extract data from a source, transform it, load it into the target store. Diagram: Source →Extract→ (gear) Transform →Load→ Destination.
- Business logic is based on **simple procedures**. **Each procedure is implemented as a script.**
- A thin abstraction layer for integration with storage ("memory mechanisms") is optional. **Direct database access is allowed.**
- **The only requirement is transactional behaviour:** operations must succeed or fail. If the system fails, it stays consistent. Hence the name *Transaction Script*.

#### Active Record (supporting) (slide 62)
- Also for simple business logic, but **on more complex data structures** (object trees and hierarchies instead of flat datasets).
- For complex data structures, transaction scripts lead to a lot of **repetitive code**.
- **Active records represent a data structure and implement the required CRUD operations.**
- But the objects **depend on ORM frameworks** or other data-access frameworks.
- Access goes **via Active Records**, not directly to the DB. The name comes from each record being "active", i.e. it implements its own data-access logic.
- Example diagram: Advertiser 1–\* Ad Campaign 1–\* Placement; Placement — Website — Zone; Placement \*–\* Creative.
- Code example: a `CreateUser.Execute(userDetails)` with `DB.StartTransaction()`, `new User()`, setting Name/Email, `user.Save()`, `DB.Commit()`, and `DB.Rollback()` on exception.

#### Domain Model (core) (slide 64)
- Martin Fowler: "a domain model is an **object model of a domain that contains both behavior and state (data)**."
- DDD's tactical building blocks include **Value Object** and **Aggregate**.
- The domain model pattern lets the code **"speak" the ubiquitous language** and follow the mental models of the domain experts.
- Diagram: the ShareWise Expense UML (see §1.12).

#### Value Object (slide 65)
- A Value Object (or simply a Value) **models an immutable conceptual whole**.
- It **does not have a unique identity**.
- **Equality is determined by comparing the attributes** encapsulated by the value type.
- It is **not a thing**, but is often used to **describe, quantify, or measure an Entity**.
- Code: immutable `Color` class (`readonly byte Red/Green/Blue`). `MixWith(other)` **returns a new Color** with component-wise `Math.Min(sum, 255)`.

#### Entity (slide 66)
- An Entity **models an individual thing**.
- Each Entity has a **unique identity** that distinguishes it from all other Entities of the same or a different type.
- Many times an Entity is **mutable**: its state changes over time.
- **Implemented in the context of an Aggregate.**
- Code: `class Person { PersonId _id; Name _name; PhoneNumber _landline; PhoneNumber _mobile; EmailAddress _email; Height _height; CountryCode _country; }`. Annotation: "**Use Value Objects instead of primitive types.**"

#### Aggregate (slide 67)
- Each Aggregate consists of **one or more Entities**. One of them is the **Aggregate Root**.
- Aggregates may also contain Value Objects.
- **The Root Entity owns all the other elements clustered inside it.**
- **The Root Entity's name is the Aggregate's conceptual name.**
- **Each Aggregate forms a transactional consistency boundary.**
- **Rules:**
  1. **Protect functional invariants within aggregate boundaries by means of interfaces.**
  2. **Design small aggregates.**
  3. **Reference other aggregates only by their identity.**
  4. **Update other aggregates using eventual consistency.**
- Diagram: an orange blob ("**Strongly Consistent Data**") contains Order —1..\*— Transaction, Customer, Offer. Outside it, with dashed arrows ("**Eventually Consistent Data**"), are Product, Source Campaign and Promotion.

ShareWise application: slides 68, 69 (see §1.10, §1.11).

#### Domain Events (core) (slide 71)
- "**A domain event is a message that describes a significant event that occurred in the business domain.**"
- Examples: order paid, stock replenished, advertising campaign published.
- **Domain events are part of an aggregate's public interface.** An aggregate **publishes its domain events through its public interface**.
- Diagrams: (a) an Aggregate fans out to three "Domain event" envelopes, each going to a **Subscriber**. (b) The Order/Customer/Offer/Transaction aggregate. **Customer is the Aggregate Root**, connected to a "**Public Interface**" that pushes "**Domain Events**" up into a red **Messaging** bar.

#### Event Sourcing (core) (slide 72)
- Uses domain events to **introduce the dimension of time** into the domain model.
- **Every change in system state is expressed and recorded as a domain event.**
- **The database that stores the domain events is the only highly consistent store: the system's "single source of truth".**
- Stored events are used to **recreate the state of an aggregate (rehydrate)**.
- Example: the **financial industry**. A **ledger is an append-only log of transactions**. The current state (e.g. account balance) can always be derived by replaying the ledger. (**Audit-safe.**)
- Diagram: **Event Store** —Rehydrate (events)→ **Aggregate** —Commit (events)→ Event Store. Below is an event stream for a lead: Initialized (name William Davis, phone, email, state Converted…) → StateSet (New Lead) → Contacted (Followup Set) → ContactDetailsUpdated (new phone) → Contacted (Converted).

### Architectural patterns (slide 75)
- **Which architectural pattern to use is an important tactical design decision.**
- The right pattern supports the functional and non-functional requirements.
- Three common patterns: **1. Layered Architecture, 2. Ports & Adapters, 3. CQRS**.

#### Layered Architecture (slide 76)
- Presentation Layer (presents and defines the UI) → Business Logic Layer (implements business logic) → Data Access Layer (access to persistence: DBs and other infrastructure).
- "A classic! Maybe even THE classic!" Maslow quote: "If the only tool you have is a hammer, you tend to see every problem as a nail."
- The dependency between business logic and data access makes it a **good fit for business logic implemented with Active Record**.
- "**Often found in bounded contexts for supporting domains!**"

#### Ports & Adapters / Hexagonal Architecture (slide 77)
- Aims to **decompose the code base according to technological aspects**.
- "**Infrastructure**" means UI, data access and other infrastructural concerns.
- **Business logic sits at the centre and should not depend directly on infrastructure (dependency inversion).**
- **Application layer:** public interface facade that orchestrates business logic.
- **Decouples business logic from all technological concerns.**
- Diagram: nested hexagons, Infrastructure ⊃ Application ⊃ Business Logic. **Ports** sit on the business logic. **Adapters** sit outside and connect to DBs, a cloud and message queues.
- "**Often found in bounded contexts for core domains!**" (See also Alistair Cockburn.)

#### CQRS (slides 78, 79)
- A **single model** performs the operations that **change state (write)**: the **Command Execution Model**, the only model with highly consistent data (**single source of truth**).
- The system can generate **any number of read models via projections**. These are **read-only**. No operation can change read-model data directly.
- **Supports polyglot modeling well.**
- With event sourcing, an aggregate's state must be hydrated and **cannot be flexibly queried**. CQRS solves this with read models.
- "**Often found in bounded contexts with event sourcing of core subdomains!**"
- Diagram: user → Execute Commands → Command Execution Model → Publish Changes → Projection Engine → Project → Read Models ← Query ← user.
- **Projections (slide 79):** **Synchronous:** the projection engine pulls committed changes ("Get changes since last checkpoint") and projects them into read models. **Asynchronous:** the command model publishes changesets, and several projection engines subscribe and generate read models.
- **Tip:** "Use a **synchronous projection as a basis** and only add an asynchronous projection if necessary. **Why?**" (note:) The slide leaves the answer open. A likely reason is that async projections bring eventual consistency/staleness and more operational complexity.

### Mapping summary (from slides 59–79)
| Subdomain type | Business logic pattern | Typical architecture |
|---|---|---|
| Supporting (simple) | Transaction Script / Active Record | Layered Architecture |
| Core (complex) | Domain Model (Aggregates) | Ports & Adapters (Hexagonal) |
| Core (complex, needs time/audit) | Event Sourcing (Domain Events) | CQRS (often with Event Sourcing) |
| Generic | (buy/standard software, slide 25) | – |

---

## 8. How to apply this to Exercise 2

**Exercise 2 (due 12.10.26):** "Elaborate on ShareWise: 1) Subdomains, 2) Bounded Contexts, 3) Context Map, 4) Ubiquitous Language." It feeds into Presentation 1 (20.10.26, modular architecture of ShareWise).

### 8.1 Subdomains (problem space, discovered, not designed)
**Method from the slides**
- Start from the **business domain** ("the service offered to customers", slide 20). Then split it into **fine-grained areas of business activity** (slide 21). These often correlate with **departments/organizational units**.
- Walk the **user journey** (slides 5–7) and group its steps into areas of activity.
- **Classify** each subdomain as **Core / Supporting / Generic** with:
  - the **complexity × differentiation chart** (slide 22)
  - the **summary table criteria** (slide 26): USP/business critical? company-specific? technical complexity? rate of change? existing solutions? in-house vs. outsource? COTS/managed services?
- Remember (slide 43): subdomains are **identified/discovered, not designed**. Their purpose is to **set priorities** and put limited resources into the core.
- Remember (slide 22): **all** subdomains are needed. They differ in effort and quality requirements.

**Heuristics**
- Core = the differentiator, complex, high barrier to entry, built in-house, never outsourced (slide 23).
- Supporting = simple CRUD/ETL, stable, no competitive advantage. Outsource or use frameworks (slide 24).
- Generic = complex but commodity, done the same way by every company. Buy standard software (e.g. identity management à la Active Directory) (slide 25).

**Expected deliverable form**
- A list of subdomains, each with a type and a one-line justification. Ideally a **table using the slide-26 criteria** and/or the **slide-22 quadrant chart** with each subdomain placed on it.
- (note:) For ShareWise, likely candidates from the journey are expense recording/splitting, balance calculation/settlement, group & membership management, user registration/identity, archiving. Identity is an obvious "Generic" candidate per slide 25. **The slides do not give this classification. Slide 27 says "Discuss in groups".**

### 8.2 Bounded contexts (solution space, designed)
**Method from the slides**
- Look for terms whose **meaning changes with context** (the "Lead" example, slides 39/41). For ShareWise, slide 40 shows that the same person is a **User** (account, login), a **Member** (group, invitation, role), a **Participant** (in one expense), or a **Debtor/Creditor** (balance). Each meaning points to a separate model/context.
- **Don't build one global language.** Build several smaller ones (slide 41). Global enterprise-wide languages "often fail" (slide 39).
- Choosing boundaries is a **strategic design decision** (slide 43). Subdomains are discovered, bounded contexts are designed. A bounded context may or may not line up 1:1 with a subdomain (in the slide-21 retailer diagram it does: "each coloured area is a subdomain (bounded context)").
- **Sizing (slide 42):** size "does not matter too much". Models must be **clear and have a purpose**. Broader boundaries are harder to keep consistent. Smaller ones mean **more integration overhead**.
- Keep Conway's law in mind (slides 11, 15): bounded contexts → services → teams.

**Expected deliverable form**
- Named bounded contexts, each with its **own ubiquitous language/model**: its key concepts, what it owns, and which subdomain(s) it implements.
- Visual form: **blobs/ovals per context** (like slides 21, 41, 42). Draw the same term inside several blobs with different meanings, e.g. "Lead" as "Event" vs. "Complex Entity" on slide 41.
- Optionally an entity diagram with coloured areas per context and **dashed lines for cross-context references** (retailer model legend, slide 21).

### 8.3 Context map
**Method from the slides**
- For every pair of interacting contexts, identify the **contract/touchpoint** and **which language is used for integration** (slide 45).
- Decide the **category**, then the pattern:
  - **Cooperation** (same team / dependent goals, good communication): **Partnership** (ad hoc, both-way adaptation, no team dictates) or **Shared Kernel** (small, compiled shared contract library, needs high synchronization) (slides 46–48).
  - **Customer-Supplier** (teams can succeed independently, power imbalance), mark **U/D**:
    - **Conformist:** downstream accepts the upstream model (e.g. an industry standard) (slide 50).
    - **ACL:** downstream translates the upstream model. Use it if the downstream is core, the upstream is legacy, or the upstream changes often or is huge (slide 51).
    - **OHS / Published Language:** upstream offers a stable, integration-oriented public protocol (e.g. OpenAPI) decoupled from its internal model (slide 52).
  - **Separate Ways:** no integration, duplicate instead. Use it for communication problems, generic libraries (e.g. logging) or very different models. **Never for core subdomains** (slide 53).
- Afterwards, **read the map** for insights (slide 54): high-level design, team communication, organizational smells (everyone needs an ACL against one team, or all separate ways point at one team).

**Notation to use (slides 46–54)**
- Oval = bounded context.
- Line + "Partners" = partnership.
- Overlapping ovals with a red intersection = shared kernel.
- "U"/"D" at the line ends = upstream/downstream.
- Arrow with "Conforms" = conformist.
- "ACL" box at the downstream edge = anticorruption layer.
- "OHS" box at the upstream edge = open-host service.

**Expected deliverable form**
- One **top-level diagram of all ShareWise bounded contexts** in the style of slide 54, with every relationship labelled by pattern. Add a short justification per relationship (why that pattern, given team setup and core/supporting/generic).
- (note:) For a student project (one team), the slides suggest cooperation patterns are natural (slide 46: "bounded contexts implemented by the same team"). External services such as an identity provider fit **Conformist/ACL** (slides 50/51). This is my inference, not on the slides.

### 8.4 Ubiquitous language
**Method from the slides**
- Build **jointly with domain experts**. Keep it evolving, and use it **everywhere, including code** (slides 30–32).
- **Only business-domain terms**, no technical jargon (slides 32, 34).
- **One meaning per term.** Resolve **ambiguous terms** (policy → regulatory provision / insurance contract). Distinguish **synonyms**, which usually mean different concepts (visitor vs. account = unregistered vs. registered) (slide 33).
- **Make implicit assumptions explicit.** Unclear terms reveal hidden concepts (slide 31). Example: answer the step-9 questions (who is authorized, can closing be revoked, must balances be 0, …) (slide 7).
- **The language is per bounded context** (slide 41). The same word may legitimately mean different things in different contexts (User/Member/Participant/Debtor, slide 40). Scope every glossary entry to its context.
- Phrase rules as **domain statements**, not technical ones (slide 34). Name operations in domain language: `closeGroupForSettlement()`, not `updateStatus()` (slide 35).

**Expected deliverable form (slide 36)**
- A **glossary**, at least covering **Expense, Share, Balance, Debt, Settlement**. (note:) Also add Group, Member, User, Participant, SettlementPayment, Money, etc. from slides 40, 68 and 69.
- A list of **business rules (invariants)** in domain language. Model them on slide 69: "The amount is positive", "The sum of the shares corresponds to the total amount", "The payer belongs to the group", "All those involved belong to the group", "A finalized expense may not be changed directly". Add rules for closing/settlement/archiving (slide 7 questions).
- Optionally, **domain-language method names** for key operations (slide 35 style).

### 8.5 Preview: what Exercise 3 needs from the same slides
Entities and value objects (slides 65, 66, 68), aggregates with the 4 rules and invariants (slides 67, 69), domain events (slide 71, e.g. `ExpenseCorrected`, `ExpenseRemoved` on slide 64), and hexagonal architecture (slide 77).
