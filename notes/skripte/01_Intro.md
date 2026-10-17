# FAVS – 01 Intro (Lecture 1, 29.09.2026)

Source: `skripte/01.Intro.pdf` (34 slides). Slide references are given as "(slide N)".
Anything marked **(note:)** is my own clarification. It is not on the slides.

---

## 1. Module organisation

### Basics
- **FAVS = "Fortgeschrittene Aspekte verteilter Systeme"** (Advanced Aspects of Distributed Systems). Subtitle: **"Cloud-Native Computing"** (slide 1).
- **Lecturer:** Hans Grönniger (slide 1).
- **Institution:** Hochschule Hannover (University of Applied Sciences and Arts), **Fakultät IV – Wirtschaft und Informatik** (slide 1).
- **Moodle course** (all slides, documents, discussions and announcements): https://moodle.hs-hannover.de/course/view.php?id=32888 (slide 3)

### Format (slide 3)
- **Lectures:** cloud(-native) computing and software engineering for the cloud. "Some theory but otherwise very hands-on."
- The accompanying **project is mostly a programming exercise**.
- **Exercises:** students develop a **web application, first as a monolith and later as a cloud-native app** (this is ShareWise, see section 4).

### Exam / grading ("Modulprüfung") (slide 4)
| Component | Points |
|---|---|
| Written test (during the normal exam period at the end of the semester / start of the next) | **55** |
| Project tasks | **45** |
| **Total** | **100** |

- There are **3 presentation slots**. **Attendance is required** and **active discussion is required**.
- **Pass condition:** at least **50% in the written test AND 50% in the project tasks (overall)**. Both conditions must hold separately.
  - (note:) That works out to at least 27.5/55 in the test and 22.5/45 in the project.
- (note:) The slides say nothing about team size or team rules, exact submission deadlines beyond the schedule below, or which tools are mandatory. The schedule does mention Spring Boot, Next.js, Azure, eduDSCloud/Proxmox and RabbitMQ (slide 7). It also says "using AI possible" for the implementation of the modulith.

### The three presentation dates (slide 7, highlighted green in the table)
1. **20.10.26** – Presentations: **modular architecture of ShareWise**
2. **17.11.26** – Presentations: **monolith implementation, limitations and change drivers** (more users, more scaling, …)
3. **15.12.26** – Presentations: **microservices architecture and pattern implementation**

---

## 2. Learning goals and lecture plan

### Learning goals (slide 5)
On completing the module, students will be able to:
- model a domain with **DDD** (Domain-Driven Design),
- design and implement a **modular monolith**,
- **containerize** applications and **deploy them automatically**,
- **evaluate reasons for and against service extraction**,
- use **synchronous and asynchronous communication**,
- distinguish **eventual consistency** from **transactional consistency**,
- apply **Saga, Retry and other patterns** correctly,
- (examine a distributed system with **logs, metrics and traces**) – this one is in parentheses on the slide, so it is probably optional,
- reflect on the **technical, business and economic consequences of a microservice architecture**.

Slide 6 is an interactive question: "What are your expectations?" (discuss for 2–3 min with your neighbour).

### Content & Timing (preliminary) (slide 7)
The table pairs each lecture (Tuesdays) with an exercise. The exercise date sits in the same row and falls on the Monday after the lecture.
(note:) The exercise date is probably the deadline or session for that task.

| # | Lecture date | Lecture topic | Exercise date | Exercise task |
|---|---|---|---|---|
| 1 | 29.09.26 | Intro, Definition, Market, ShareWise user journey | 05.10.26 | a) Compare **NIST to ISO/IEC 22123** (esp. the service models part); b) Familiarize with **ShareWise User Journey**, work on a more complete example |
| 2 | 06.10.26 | DDD foundation | 12.10.26 | Elaborate on ShareWise: 1) **Subdomains**, 2) **Bounded Contexts**, 3) **Context Map**, 4) **Ubiquitous Language** |
| 3 | 13.10.26 | Spring Boot, Nextjs | 19.10.26 | Elaborate on ShareWise: 1) **Entities, Value Objects**, 2) **Aggregates**, 3) **Domain Events**, 4) **(Hexagonal) Architecture** |
| 4 | 20.10.26 | **Presentations: modular architecture of ShareWise** | 26.10.26 | Implementation Modulith (backend, frontend) – using AI possible |
| 5 | 27.10.26 | Cloud economy, Cloud-native computing, Virtualization | 02.11.26 | Implementation Modulith (backend, frontend) – using AI possible |
| 6 | 03.11.26 | Container | 09.11.26 | Create containers and execute locally |
| 7 | 10.11.26 | DevOps & CI/CD | 16.11.26 | Create pipelines (to build) |
| 8 | 17.11.26 | **Presentations: monolith implementation, limitations and change drivers (more users, more scaling, …)** | 23.11.26 | Deployment to **eduDSCloud / proxmox** (adapt pipeline) |
| 9 | 24.11.26 | IaaS (Azure) | 30.11.26 | Factor out services, communicate via messages |
| 10 | 01.12.26 | strangler fig, loose coupling, messaging, rabbitmq, outbox | 07.12.26 | Implement patterns |
| 11 | 08.12.26 | API-Gateway, Eventual Consistency, Saga, Resilience Pattern | 14.12.26 | Implement patterns |
| 12 | 15.12.26 | **Presentations: microservices architecture and pattern implementation** | 04.01.27 | Rework if needed |
| 13 | 05.01.27 | buffer | – | – |

---

## 3. Technical concepts

### 3.1 Opening quote (slide 9)
> "The interesting thing about cloud computing is that we've redefined cloud computing to include everything that we already do." – **Richard Stallman**

### 3.2 IT infrastructure (slide 10)
IT infrastructure is the **basis for all services and applications**. Its components are:
- **Network**, including the connection to external networks (Internet) and security such as **firewalls**
- **Hardware / machines**: all IT components such as servers, routers and PCs, but possibly also **data centre buildings with cooling, redundant power supply**, etc.
- **Software**: standard software, operating systems, etc.

### 3.3 Development of IT infrastructure (slide 11)
An arrow diagram shows how IT infrastructure developed over time, with circles that grow along the arrow:
**Mainframe → Client/Server → Virtualization → Containerization → Serverless**.
A red label **"Dedicated server"** points at both *Mainframe* and *Client/Server*. Both are eras of dedicated servers.

### 3.4 Deployment units are getting smaller (slide 12)
The diagram has four boxes. Green boxes stand for the **"compute load"** (applications A, B):
1. **Dedicated Server:** A and B run directly on **Bare Metal**.
2. **Virtualization:** Bare Metal → two **VMs** → A and B run inside a VM.
3. **Containerization:** Bare Metal → VMs → **Container Engine** → A and B run as containers.
4. **Serverless:** Bare Metal → VMs → Container Engine → **FaaS Runtime** → A, B and more small functions.

The message: each step adds an abstraction layer and makes the deployable unit smaller and finer-grained.

### 3.5 Traditional IT vs. IaaS (slide 13)
- **Traditional IT infrastructure:** own data centres (buildings), own hardware, own operating staff.
- **Intermediate step:** **Virtualization**.
- **Infrastructure-as-a-Service:** **rental model**, **public cloud**.
- The slide has photos of a data centre server aisle and of modular container-style data centre units.

### 3.6 NIST definition of cloud computing (slide 14)
Source: NIST SP 800-145 – https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf

> "Cloud computing is a model for enabling **ubiquitous, convenient, on-demand network access** to a **shared pool of configurable computing resources** (e.g., networks, servers, storage, applications, and services) that can be **rapidly provisioned and released with minimal management effort or service provider interaction**."

> "This cloud model is composed of **five essential characteristics, three service models, and four deployment models**."

Mnemonic: **5 – 3 – 4**.

### 3.7 Five essential characteristics (NIST) (slide 15)
1. **On-demand self-service:** A consumer can provision computing capabilities, such as server time and network storage, unilaterally. This happens automatically as needed, **without human interaction** with each service provider.
2. **Broad network access:** Capabilities are available over the network. They are accessed through **standard mechanisms** that support heterogeneous **thin or thick client** platforms (mobile phones, tablets, laptops, workstations).
3. **Resource pooling:** The provider pools its computing resources to serve multiple consumers using a **multi-tenant model**. Physical and virtual resources are dynamically assigned and reassigned according to demand.
   - There is a sense of **location independence**: the customer generally has no control or knowledge over the exact location. The customer may still be able to specify location at a higher level (country, state, data centre).
   - Example resources: storage, processing, memory, network bandwidth.
4. **Rapid elasticity:** Capabilities can be provisioned and released elastically, sometimes automatically, to **scale rapidly outward and inward** with demand. To the consumer they often **appear to be unlimited** and can be obtained in any quantity at any time.
5. **Measured service:** Cloud systems automatically control and optimise resource use through a **metering capability (e.g. pay-per-use)**. The metering works at an abstraction level that fits the service (storage, processing, bandwidth, active user accounts). Usage can be **monitored, controlled and reported**, which gives **transparency** to both provider and consumer.

### 3.8 Three service models (NIST) (slide 16)
1. **Software as a Service (SaaS):** The consumer uses the **provider's applications** running on cloud infrastructure.
   - The applications are accessible via a **thin client** (e.g. a web browser for web-based email) or a program interface.
   - The consumer does **not** manage the infrastructure (network, servers, OS, storage) and not even individual application capabilities. The possible exception is **limited user-specific application configuration settings**.
2. **Platform as a Service (PaaS):** The consumer **deploys consumer-created or acquired applications** onto the cloud infrastructure.
   - These applications use programming languages, libraries, services and tools **supported by the provider**.
   - The consumer does not manage network, servers, OS or storage. The consumer **does control the deployed applications** and possibly the **configuration settings of the application-hosting environment**.
3. **Infrastructure as a Service (IaaS):** The consumer can **provision processing, storage, networks and other fundamental computing resources** and **deploy and run arbitrary software, including operating systems** and applications.
   - The consumer does not manage the underlying cloud infrastructure.
   - The consumer **has control over the OS, storage and deployed applications**, and possibly **limited control of select networking components** (e.g. host firewalls).

### 3.9 Four deployment models (NIST) (slide 17)
1. **Private cloud:** The infrastructure is for **exclusive use by a single organisation** with multiple consumers (e.g. business units).
   - It may be owned, managed and operated by the organisation, a third party or a combination of them.
   - It may exist **on or off premises**.
2. **Community cloud:** The infrastructure is for exclusive use by a **specific community of consumers from organisations with shared concerns** (mission, security requirements, policy, compliance).
   - It may be owned, managed and operated by one or more of the community's organisations, a third party or a combination.
   - It may exist on or off premises.
3. **Public cloud:** The infrastructure is for **open use by the general public**.
   - It may be owned, managed and operated by a business, academic or government organisation, or a combination.
   - It **exists on the premises of the cloud provider**.
4. **Hybrid cloud:** A **composition of two or more distinct cloud infrastructures** (private, community or public) that **remain unique entities**.
   - They are bound together by standardised or proprietary technology that enables **data and application portability** (e.g. **cloud bursting** for load balancing between clouds).

### 3.10 Responsibility stack: On-Premises vs. IaaS / PaaS / SaaS (slide 18)
The table has nine layers per column, top to bottom: Applications, Data, Middleware, Runtime, O/S, Virtualization, Servers, Storage, Networking.
Grey means **self** (managed by you). Dark blue means **other** (managed by the provider).

| Model | Slogan | Managed by you (self) | Managed by provider (other) |
|---|---|---|---|
| On-Premises | **"own it"** | all 9 layers | – |
| IaaS | **"host on it"** | Applications, Data, Middleware, Runtime, O/S | Virtualization, Servers, Storage, Networking |
| PaaS | **"build on it"** | Applications, Data | Middleware, Runtime, O/S, Virtualization, Servers, Storage, Networking |
| SaaS | **"consume it"** | – | all 9 layers |

### 3.11 Pizza-as-a-Service analogy (slide 19)
Source: Nane Kratzke, *Cloud-native Computing*, 2022.
The layers, top to bottom, are: Dining table, Drinks, Oven, Topping, Tomato sauce, Pizza dough, Ingredients. Blue means **self**, grey means **other**.

| Model | Real-world equivalent | Self | Other |
|---|---|---|---|
| On-Premises | **Pizza di Mama** (homemade) | everything | – |
| IaaS | **Buy & Bake** | Dining table, Drinks, Oven, Topping | Tomato sauce, Pizza dough, Ingredients |
| PaaS | **Pizza Service** (delivery) | Dining table, Drinks | Oven, Topping, Tomato sauce, Pizza dough, Ingredients |
| SaaS | **Pizzeria** (eat out) | – | everything |

### 3.12 Cloud computing: chances (slide 21)
Slide 20 is a 2–3 min discussion with your neighbour about chances and risks. The chances are:
- **Cost:** no large capital investments in hardware or software are needed.
- **Scalability:** resources can be scaled easily as needed, **vertically and horizontally**.
- **Performance:** big providers run data centres worldwide, so resources can be provisioned quickly and efficiently.
- **Speed and agility:** new resources are provisioned or released with a few clicks. This speeds up innovation and gives a competitive advantage.
- **Security:** providers offer policies, technologies and controls that can improve overall security.
- **Recoverability and backup:** backup, disaster recovery and business continuity are easier than on-premises.
- **Automation:** routine tasks (backup, updates, monitoring) can be automated, so IT can focus on strategic goals.

### 3.13 Cloud computing: risks (slide 22)
- **Cost:** getting started is easy, but costs can be high in the long run if services aren't managed or optimised.
- **Vendor lock-in:** switching to another vendor is complex and expensive.
- **Data protection and compliance:** this matters especially in regions with strict laws (EU) when data sits in other jurisdictions.
- **Security risks:** data leaks, hacks and cyberattacks remain potential risks.
- **Performance:** it depends on the internet connection quality, and latency and bandwidth also play a role.
- **Data transfer costs:** moving large data volumes in and out of the cloud is time-consuming and potentially expensive.
- **Loss of control:** outsourcing to a third party means giving away a certain degree of control.

### 3.14 Market figures (slides 23–26, source: Statista / Gartner / Canalys)
- **Slide 23:** bar chart "Umsatz mit Cloud Computing weltweit 2010–2023, Prognose bis 2025" (worldwide public cloud services revenue, in billions USD; source: Gartner):
  - 2010: 42.8 · 2011: 49.78 · 2012: 57.52 · 2013: 69.49 · 2014: 85.05 · 2015: 104.96 · 2016: 122.11 · 2017: 145.3 · 2018: 196.7 · 2019: 242.7 · 2020: 270.03 · 2021: 412.63 · 2022: 478.32 · 2023: 561.1 · 2024*: 675.43 · 2025*: 824.76 (* = forecast)
- **Slide 24:** pie chart of market shares of the leading cloud computing companies, **Q4 2023** (source: Canalys): **AWS 31%**, **Microsoft Azure 26%**, **Google Cloud 10%**, **Others (Andere) 34%**.
  - The slide also lists the **"BIG-FIVE": Amazon, Microsoft, Google, Alibaba, IBM**.
- **Slide 25:** stacked bars of revenue by segment, 2010–2025* (worldwide, Gartner). The segments are SaaS (Cloud Application Services), IaaS (Cloud Infrastructure Services), PaaS (Cloud Application Infrastructure Services), DaaS (Desktop as a Service) and BPaaS (Cloud Business Process Services).
  - SaaS is the largest segment, and IaaS and PaaS grow strongly. DaaS is tiny.
  - The total reaches about 820 bn USD in 2025*.
- **Slide 26:** IaaS market shares 2016–2023 (Gartner):
  - **Amazon** drops from 53.7% (2016) to 49.4%, 47.9%, 44.6%, 40.8%, 38.1%, 39.8% and finally **39% (2023)**.
  - **Microsoft** rises from **8.7% (2016)** to 12.7%, 15.6%, 17.4%, 19.7%, 20.6%, 21.5% and finally **23% (2023)**.
  - Alibaba stays at about 5–9% (around 7.9% in 2023). Google rises to about 8.2% (2023). Huawei is about 4% in later years. Others ("Andere") fall from 29.6% to 17.5%.

### 3.15 Gartner Hype Cycle for Cloud Computing, 2025 (slide 27)
The curve runs through five phases: Innovation Trigger → Peak of Inflated Expectations → Trough of Disillusionment → Slope of Enlightenment → Plateau of Productivity. The chart is as of June 2025. Selected entries:
- **Innovation Trigger:** Generative AI-Augmented CloudOps, Isolated Cloud, AI Supercomputing, Geopatriation, Quantum Computing as a Service (>10 yrs), Cross-Cloud Integration, Embedded Cloud Services.
- **Peak:** Cloud HPC, Enhanced Private Cloud Computing, Cloud Resilience, FinOps, GPU as a Service, Sovereign Cloud, Business-Driven Cloud Strategy, Distributed Hybrid Infrastructure, Cloud and Generative AI, Infrastructure Platform Consumption Services, Industry Cloud Platforms.
- **Sliding into the Trough:** Multicloud, Revirtualization, SaaS Management Platforms, **Cloud-Native**, Intercloud Data Management, Cloud Sustainability, Cloud Portability, Distributed Cloud, Multicloud Management, Cloud-Optimized Hardware, SaaS Security, **Container Management**.
- **Trough:** **Cloud Repatriation**, marked "obsolete before plateau".
- **Slope of Enlightenment:** Cloud AI Services, Public Cloud Security, Hybrid Cloud Computing, Cloud Marketplaces, **Serverless Infrastructure**, Cloud Center of Excellence, Strategic Cloud Platform Services.
- **Plateau:** **Cloud Managed Services**.

### 3.16 Other types of computing (slide 28)
- **Supercomputer:** often thousands of processors working **in parallel**, connected by a high-speed network. Often uses **specialised HW + SW**.
- **Cluster computing:** multiple computers (**nodes**) connected over a network so that they work as a **single (distributed) system**. Unlike a supercomputer, a cluster is often made of **off-the-shelf** computers.
- **Grid computing:** a **virtual supercomputing infrastructure** built from interconnected nodes that can be **geographically dispersed**. It is **more decentralised** than cluster computing.
- **Web or service computing:** creating, using and managing **web services** in a distributed environment, i.e. delivering software as services over the Internet. Other applications or services can use these services to automate complex tasks and business processes.
- Today these "web" services often run on **cloud platforms or infrastructure** (as in the NIST definition).

### 3.17 Pets vs. Cattle – "Cloud Computing is a Mindset Change" (slide 29)
Source: Nane Kratzke, *Cloud-native Computing*, 2022. The image is attributed to Bill Baker, Microsoft (cloudscaling).
- **Pets:** a sick dog with an ice pack, captioned **bowzer.company.com (scale-up)**. Individually named, hand-cared-for servers.
- **Cattle:** a herd of cows, captioned **web001.company.com (scale-out)**. Caption: **"(Virtual) Servers \*are\* cattle."**
- German bullet points on the slide:
  - "Alte Informatiker-Weisheit: Ausschalten, Einschalten, geht wieder." (Old IT wisdom: switch it off, switch it on, it works again.)
  - "**Server sind Wegwerf-Artikel!**" (Servers are disposable.) "Wegschmeißen – neu machen. Ist schneller als Problem suchen, Problem beheben." (Throw it away and make a new one. That is faster than finding and fixing the problem.)
  - "**Mehr Power kommt durch mehr Server.**" (More power comes from more servers, i.e. scale-out.)

---

## 4. Case study: ShareWise (slides 30–34)

### 4.1 Idea (slide 31)
- **Tagline:** **"ShareWise: Shared expenses made simple"**
- **What it is:** "A **collaborative application for managing expenses within groups**."
- **ShareWise helps groups of people:**
  1. **record shared expenses**
  2. **distribute costs among participants**
  3. **understand who owes whom**
  4. **record settlement payments**
  5. **close and archive completed groups**
- The slide asks an open question: "Example use cases?"
- Logo: a green and purple hexagon with a white "S" and the word "ShareWise".
- (note:) This is similar to apps like Splitwise or Tricount. That comparison is not on the slides.

### 4.2 User journey scenario: "Mallorca 2027" (slide 32)
Four friends plan a trip together:
- **Alice creates the group.**
- **Bob, Carol and David join.**
- The group **records expenses during the trip**.
- **Each expense has a payer and a cost distribution.**
- Members can **record settlement payments**.
- **The group is closed after the trip.**

Expense table from the slide:

| Expense | Paid by | Amount | Participants |
|---|---|---|---|
| Hotel | Alice | €900 | Everyone |
| Dinner | Bob | €180 | Everyone |
| Rental car | Carol | €420 | Alice, Carol, David |
| Museum | David | €75 | Bob, Carol, David |

**Actors / roles that appear:** the group creator (Alice), joining members (Bob, Carol, David), the payer of an expense, and the participants of an expense.

(note:) Worked example of the balances, assuming each expense is split **equally** among its participants. The slides do not specify the split rule.
- Shares: Hotel €225 each (4 people) · Dinner €45 each (4) · Rental car €140 each (Alice, Carol, David) · Museum €25 each (Bob, Carol, David). Total spent: €1,575.
- Alice: paid 900, share 410 → **+490** (is owed)
- Bob: paid 180, share 295 → **−115**
- Carol: paid 420, share 435 → **−15**
- David: paid 75, share 435 → **−360**
- Sum = 0. One possible settlement: Bob → Alice €115, Carol → Alice €15, David → Alice €360.

### 4.3 Core concepts (slide 33)
"What are the core concepts?" The slide lists **Group**, **Member**, **Expense**, **…**. The list is left open on purpose, for students to complete.
(note:) Candidates implied by slides 31–32 are Payer, Participant / cost distribution (share), Settlement payment, Balance / debt ("who owes whom"), and Group status (open / closed / archived). These feed directly into the DDD exercises (subdomains, ubiquitous language, entities, value objects, aggregates).

### 4.4 Roadmap: "From modular monolith to cloud-native system" (slide 34)
The flow diagram has 9 coloured boxes connected by numbered arrows 1–8. This is the project path for the whole semester:

1. **Understand the domain** →(1)→
2. **Build a modular monolith** →(2)→
3. **Containerize the application** →(3)→
4. **Automate build and deployment** →(4)→
5. **Identify change drivers** →(5)→
6. **Extract selected services** →(6)→
7. **Introduce events and messaging** →(7)→
8. **Handle distributed consistency** →(8)→
9. **Add resilience and observability**

(note:) Mapped to the schedule on slide 7, the steps line up as follows:
- Steps 1–2 = DDD and modulith (weeks 2–5)
- Step 3 = containers (week 6)
- Step 4 = CI/CD and the eduDSCloud deployment (weeks 7–8)
- Step 5 = presentation 2 on 17.11
- Steps 6–7 = factor out services, RabbitMQ / outbox (weeks 9–10)
- Steps 8–9 = Saga, eventual consistency, resilience (week 11)

---

## 5. Likely relevant for exercises and presentations

- **Exercise 1 (due/session 05.10.26):**
  - a) **Compare NIST SP 800-145 with ISO/IEC 22123**, especially the **service models**. Know the NIST 5 characteristics, 3 service models and 4 deployment models exactly (slides 14–17).
    - (note:) ISO/IEC 22123 uses different terminology, e.g. "cloud capabilities types" and "cloud service categories". The slides do not cover this; you need to research it.
  - b) **ShareWise user journey**: work out a more complete example, extending the Mallorca 2027 scenario (slide 32).
- **Exercises 2–3:** ShareWise DDD work: subdomains, bounded contexts, context map, ubiquitous language, then entities, value objects, aggregates, domain events and hexagonal architecture. Start from the core concepts on slide 33 and the features on slide 31.
- **Presentation 1 (20.10.26):** modular architecture of ShareWise.
- **Presentation 2 (17.11.26):** monolith implementation, its limitations and change drivers (more users, more scaling, …). This connects to slide 34, step 5.
- **Presentation 3 (15.12.26):** microservices architecture and pattern implementation (Saga, Retry, outbox, API gateway, resilience).
- **Tech stack hinted:** Spring Boot (backend), Next.js (frontend), containers, CI/CD pipelines, eduDSCloud / Proxmox deployment, Azure (IaaS), RabbitMQ. AI use is explicitly allowed for implementing the modulith.
- **Exam-relevant definitions:**
  - NIST definition (5-3-4)
  - IaaS/PaaS/SaaS responsibility split ("own it / host on it / build on it / consume it") and the pizza analogy
  - deployment models (including hybrid and cloud bursting)
  - chances vs. risks
  - pets vs. cattle (scale-up vs. scale-out)
  - supercomputer, cluster, grid and web/service computing
  - how deployment units evolved (dedicated server → VM → container → serverless/FaaS)
- **Pass rule reminder:** you need ≥50% in **both** the written test (55 pts) and the project (45 pts). Attendance and active discussion in all 3 presentation slots are required.
