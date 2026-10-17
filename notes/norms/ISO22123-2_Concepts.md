# ISO/IEC 22123-2:2023 — Cloud computing — Part 2: Concepts

> Source: `exercises/isoiec22123-2ed10en.pdf` (ISO/IEC 22123-2, 1st edition 2023-09, 42 PDF pages / 35 numbered pages).
> Prepared by ISO/IEC JTC 1/SC 38 ("Cloud computing and distributed platforms").
> Relevant for **Exercise 1**: *Compare the cloud computing definitions of NIST and ISO/IEC 22123 (esp. the service models part).*
> Citations in the form "§5.3" are clauses of ISO/IEC 22123-2. Statements about NIST are marked **(NIST SP 800-145)**.

---

## 0. TL;DR (exam card)

- 22123 is a **series**: Part 1 = Vocabulary (definitions), **Part 2 = Concepts** (this doc), Part 3 = Reference architecture (roles/sub-roles/activities in detail).
- Parts 1 + 2 together **replace ISO/IEC 17788:2014** (Foreword). (17788 was itself the ISO/ITU-T counterpart of NIST SP 800-145.)
- **6 key characteristics** (§5.2): broad network access, measured service, **multi-tenancy**, on-demand self-service, rapid elasticity **and scalability**, resource pooling. NIST has 5 "essential characteristics" — no multi-tenancy.
- **Two-level model for "service models"** (§5.3/§5.4):
  - **Cloud capabilities types** = exactly **3** functional classes: *application*, *platform*, *infrastructure* — non-overlapping ("separation of concerns").
  - **Cloud service categories** = open-ended, market-driven groups ("X as a service"): SaaS, PaaS, IaaS, NaaS, CaaS, CompaaS, DSaaS (+ 11 more in Annex A). A category may offer **one, two or all three** capability types.
- **4 deployment models** (§5.5): private, public, community, hybrid (+ multi-cloud mentioned in §10.2.2). Defined via **control and sharing** of resources, not location.
- **Parties vs roles** (§6): CSC, CSP, CSN (cloud service *partner*). A party can play multiple roles. Roles = sets of activities; sub-roles in 22123-3.
- **13 cross-cutting aspects** (§7): auditability, availability, governance, interoperability, maintenance & versioning, performance, portability, protection of PII, regulatory, resiliency, reversibility, security, SLAs.
- New compared to 17788: data (§8), virtualization incl. containers & **serverless** (§9), multiple CSPs (multi-cloud/inter-cloud, §10), logical/physical organization (instances, regions, availability zones, edge, §11).

---

## 1. Overview: scope and structure

### Scope (§1)
> "This document specifies concepts used in the field of cloud computing. These concepts expand upon the cloud computing vocabulary defined in ISO/IEC 22123-1 and provide a foundation for other documents that are associated with cloud computing."

The only normative reference is **ISO/IEC 22123-1 (Vocabulary)** — the actual *definition* of "cloud computing" lives there, not in Part 2 (§5.1: "ISO/IEC 22123-1 defines cloud computing and notes that examples of resources include servers, operating systems, networks, software, applications, and storage equipment."). For reference, 22123-1 defines cloud computing as a *paradigm for enabling network access to a scalable and elastic pool of shareable physical or virtual resources with self-service provisioning and administration on-demand* (wording from 22123-1/17788, not quoted in Part 2).

### History (Foreword)
> "This first edition of ISO/IEC 22123-2, together with ISO/IEC 22123-1 cancels and replaces ISO/IEC 17788:2014, which has been technically revised."

Main changes listed in the Foreword:
- terminology moved to 22123-1;
- key characteristics descriptions expanded;
- **"the number and descriptions of the cloud service categories have been expanded"**;
- deployment model descriptions "expanded and corrected";
- **"added differentiation between cloud computing parties and role"**;
- cross-cutting aspects expanded;
- new Clauses 8 (data), 9 (virtualization), 10 (multiple CSPs), 11 (logical/physical organization);
- Annex A expanded with additional service categories.

### Structure by clause

| Clause | Content |
|---|---|
| 1–3 | Scope, normative refs (22123-1), terms (only PII principal / PII controller / PII processor, from ISO/IEC 29100) |
| 4 | Abbreviations (CSC, CSP, CSN, CSU, CSA, SLA, SLO, SQO, SaaS/PaaS/IaaS/NaaS/CaaS/CompaaS/DSaaS/FaaS, ...) |
| 5 | **Foundational concepts**: 5.2 key characteristics, 5.3 cloud capabilities types, 5.4 cloud service categories, 5.5 deployment models |
| 6 | **Parties and roles** (CSC, CSP, CSN) |
| 7 | **Cross-cutting aspects** (7.2–7.14) |
| 8 | Data and cloud services (processing, flow, multi-source, data sharing/DSA) |
| 9 | Virtualization (VMs, hypervisors, containers, serverless, virtual networking, virtualized DSaaS) |
| 10 | Cloud computing involving multiple CSPs (multi-cloud, inter-cloud) |
| 11 | Organization: logical (cloud service instances) and physical (regions, availability zones, edge, affinity, geo-dispersion) |
| Annex A (informative) | Table A.1 service categories x capabilities types; Table A.2 descriptions of extra categories |

Naming convention (§5.1):
> "a name such as cloud service customer (CSC) or cloud service provider (CSP) represents a cloud computing party while CSC role or CSP role indicates a cloud computing role."

---

## 2. Detailed concepts

### 2.1 Key characteristics of cloud computing (§5.2)

> "The concept of key characteristics refers to the fundamental properties of cloud computing that differentiate it from other Information Technology paradigms." (§5.2.1)

| # | Characteristic | Key sentence (verbatim) | Notes |
|---|---|---|---|
| 5.2.2 | **Broad network access** | "a characteristic in which the CSP's physical and virtual resources are available over a network and accessed through standard mechanisms that promote use [by] the CSC." | Network may be public internet, exchange provider's net or CSP's own network. Covers user access, application access, **peer cloud service interaction (intra-/inter-cloud)** and **management/control via APIs**. |
| 5.2.3 | **Measured service** | "a characteristic in which the metered delivery of cloud services is such that usage can be monitored, controlled, reported, and billed." | "the customer only pays for the resources that they use"; metering algorithm can be fixed in the SLA (ISO/IEC 19086). |
| 5.2.4 | **Multi-tenancy** | "a characteristic in which physical or virtual resources are allocated in such a way that multiple tenants and their computations and data are isolated from and inaccessible to one another." | A **tenant** = group of CSUs, usually belonging to the same CSC; one CSC can have many tenancies (departments, subsidiaries) — for security/confidentiality or regulatory reasons. **Not a separate characteristic in NIST.** |
| 5.2.5 | **On-demand self-service** | "a characteristic in which a CSC can provision cloud services, as needed, automatically or with minimal interaction with the CSP." | e.g. changing RAM/disk without human intervention. |
| 5.2.6 | **Rapid elasticity and scalability** | "Cloud services can be rapidly and elastically adjusted, in some cases automatically, to quickly increase or decrease capacity." | Explicitly distinguishes **horizontal scaling** (more instances) and **vertical scaling** (bigger instance; can incur delay). Resources "often appear to be unlimited". CSP must describe scalability limits/latency; CSC checks them. See ISO/IEC TS 23167. |
| 5.2.7 | **Resource pooling** | "a characteristic in which a CSP's physical or virtual resources can be aggregated to serve one or more CSCs." | Abstraction masks complexity; CSC generally has no control/knowledge over location, but can specify location "at an abstract level". Only resources of a similar type can be pooled. CSC can stipulate that resources are not shared. |

### 2.2 Cloud capabilities types (§5.3)

> "A cloud capabilities type is a classification of the functionality provided by a cloud service to the CSC, based on the resources used. Cloud capabilities types follow the principle of separation of concerns, i.e. they have minimal functionality overlap between each other."

The three (and only three) types:
- **Application capabilities type**: "A cloud capabilities type in which the CSC can use the CSP's applications";
- **Infrastructure capabilities type**: "A cloud capabilities type in which the CSC can provision and use processing, storage or networking resources";
- **Platform capabilities type**: "A cloud capabilities type in which the CSC can deploy, manage and run customer-created or customer-acquired applications using one or more programming languages and one or more execution environments supported by the CSP."

> NOTE: "In this context 'applications' includes scripts, containers, complete programs, partial programs, code and function libraries, microservices, AI training data, and other forms of compliable or executable software. **There are only three cloud capabilities types defined in this document. These cloud capabilities types should not be confused with other categorizations of cloud services.**"

Intuition: capabilities types answer *"what kind of functionality does the CSC get / at which level of the stack does it interact?"* — use an app / run own code on a managed environment / get raw resources.

### 2.3 Cloud service categories (§5.4) and their mapping to capabilities types

> "A cloud service category is a group of cloud services that possess some common set of qualities. **A cloud service category can include capabilities from one or more cloud capabilities types.**" (§5.4.1)

> "The primary determining factors for categorizing a cloud service are:
> — the cloud computing capabilities types that are provisioned (application, platform or infrastructure);
> — its intended use."

> "Cloud service categories are typically referred to using something 'as a service.'"

> "The three best known cloud service categories are: SaaS, which offers application capabilities types; PaaS, which offers platform capabilities types; IaaS, which offers infrastructure capabilities types. **However, there are many other examples of cloud service categories.**"

> "Some cloud service categories can offer two or all three of the cloud capabilities types. For example, communications as a service (CaaS) can offer both platform and application capabilities types."

So: **capabilities type = closed, orthogonal axis (3 values); service category = open, market-oriented label (many values)**, defined by *which capabilities types are offered* **plus** *intended use* (e.g. networking, communication, storage). The relationship is many-to-many.

#### Table A.1 — Cloud service categories and cloud capabilities types (Annex A, reproduced)

"An 'X' at the intersection of a row and column depicts that the cloud service category ... is of the indicated cloud capabilities type". Categories in **bold** are described in §5.4; the rest in Table A.2.

| Cloud service category | Infrastructure | Platform | Application |
|---|:-:|:-:|:-:|
| **Compute as a Service (CompaaS)** | X | X | |
| **Communications as a Service (CaaS)** | | X | X |
| **Data Storage as a Service (DSaaS)** | X | X | X |
| **Infrastructure as a Service (IaaS)** | X | | |
| **Network as a Service (NaaS)** | X | X | X |
| **Platform as a Service (PaaS)** | | X | |
| **Software as a Service (SaaS)** | | | X |
| Database as a Service | | X | X |
| Desktop as a Service | X | X | X |
| Email as a Service | | X | X |
| Identity as a Service | | X | X |
| Management as a Service | | X | X |
| Security as a Service | | X | X |
| Serverless Computing | | X | |
| Function as a Service | | X | |
| Container as a Service | X | | |
| AI as a Service | | X | |
| Blockchain as a Service | | X | |

Observations:
- Only the "classic trio" maps **1:1** (IaaS→I, PaaS→P, SaaS→A). They are effectively the "pure" categories, one per capabilities type.
- NaaS, DSaaS, Desktop aaS cover **all three** types; many others two.
- Annex A rules of thumb: VMs/containers/basic storage/basic networking → "Infrastructure"; running customer code "(such as any combination of runtimes, SQL queries, serverless computing, quantum computing, or other code execution)" → "Platform"; use of a CSP application "(usually including a user interface of some kind)" → "Application".
- > "Note that a newly defined cloud service category can offer any combination of the three cloud capabilities types." / "The commercial cloud computing market is very dynamic and new cloud services continue to materialize into new informal cloud service categories." (Annex A)

#### Each service category described in §5.4

**SaaS (§5.4.2)** — "a cloud service category in which the cloud capabilities type provided to the CSC is an application capabilities type."
- "The cloud service provisioned for the CSC uses the CSP's software application running on CSP resources."
- Access via thin client (web browser, e.g. web-based email) **or an API**.
- "The customer does not manage or control the underlying resources including network, servers, operating systems, storage, or even individual application capabilities, with the possible exception of limited user-specific application configuration settings."
- CSP responsible for deploying, configuring, maintaining, updating; the entity offering the service "can be different from the SaaS application developer".
- Extensible SaaS (customer scripting) is still SaaS: "the execution of such code is not central to the service being offered."

**PaaS (§5.4.3)** — "a cloud service category in which the cloud capabilities type provided to the CSC is a platform capabilities type."
- "The capability provided to the CSC is to develop or deploy onto the CSP resources customer-created or acquired applications created using programming languages, libraries, services, and tools supported by the CSP." (Does "not necessarily preclude" tools from other sources.)
- "PaaS is distinguished from an extensible SaaS or web application by its primary customers: **developers and operations staff versus end users.**"
- CSC does not control network/servers/OS/storage, "but has control over the deployed applications and possibly configuration settings for the application-hosting environment."

**IaaS (§5.4.4)** — "a cloud service category in which the cloud capabilities type provided to the CSC is an infrastructure capabilities type."
- "The capability provided to the CSC is to provision physical or virtual processing, storage, networks, and other fundamental computing resources where the customer is able to deploy and run arbitrary software, which can include operating systems and applications."
- CSC controls OS, storage, deployed apps; "possibly limited control of select networking components (e.g. host firewalls)."
- Example: hosting CSC-defined VM images on a CSP hypervisor — more freedom, but CSC must maintain all its software.
- "arbitrary software" = any software, subject only to environment limitations; CSP is typically unaware of it.

**NaaS (§5.4.5)** — "a cloud service category in which the capability provided to the CSC is transport connectivity and related network capabilities. NaaS can provide the application, platform and infrastructure cloud capabilities types."
- CSC can create/manage/remove connections between endpoints of its choice; doesn't control physical network.
- Can include switches, routers, CDNs, caches, proxies, firewalls, satellite links; also **non-IP** (TDM, optical, satellite, PSTN). "transport" ≠ TCP/IP transport layer.
- Infrastructure = raw connectivity; Platform = execute customer code for dynamic routing, call queuing, CDN/caching/firewall behaviour; Application = CSP-built network management apps. Example: TV broadcaster's contribution link.

**CaaS — Communications as a Service (§5.4.6)** — "a cloud service category in which the capability provided to the CSC is real-time interaction and collaboration."
- "real-time" = no perceivable delay for an average human user; communications between humans or human-like software (bots).
- Text chat, screen sharing, voice, video, file transfer, presence, shared editing; conferencing; recording; PSTN interfacing (possibly via NaaS); PBX/Centrex features.
- (Note: CaaS here ≠ "Container as a Service", which Annex A lists separately.)

**CompaaS — Compute as a Service (§5.4.7)** — "a cloud service category in which the capability provided to the CSC is the provision and use of processing resources needed to deploy and run arbitrary software."
- Storage typically obtained separately (e.g. from DSaaS). "A VM-based cloud service where all storage is external to the cloud service can qualif[y] as CompaaS."
- "If the service includes data storage functions or anything more than basic connectivity in addition to processing, it is usually better categorised as an IaaS."
- Stakeholders: ICT operators/developers.

**DSaaS — Data Storage as a Service (§5.4.8)** — "a cloud service category in which the capability provided to the CSC is the provision and use of data storage and related capabilities."
- Ranges from file/block storage over relational databases to big-data platforms; backup, DR, geo-redundancy.
- "For a basic file storage service, the DSaaS exhibits only infrastructure capabilities type functions. For a more sophisticated storage service such as a relational database, the DSaaS can support execution of scripts and software with exposed APIs, thus also exhibiting platform capabilities type functions." UI for DB admins → application capabilities.
- **Best illustration of the ISO idea**: one category, capability types depend on the concrete service.

**Additional categories (Table A.2)**: Database aaS, Desktop aaS, Email aaS, Identity aaS (IAM, SSO), Management aaS, Security aaS, Container aaS, AI aaS (incl. ML aaS), Blockchain aaS, Function aaS. Serverless computing is defined in §9.4 as "a cloud service category in which the CSC can use different cloud capabilities types without the CSC having to provision, deploy and manage either hardware or software resources, other than providing CSC application code or providing CSC data." FaaS = execution of CSC code as functions "each triggered by a CSC specified event"; serverless database = CSP-operated DB via API.

### 2.4 Cloud deployment models (§5.5)

> "A cloud deployment model represents the way in which cloud computing can be organized based on the **control and sharing** of physical or virtual resources." ... "Cloud deployment models do not specify implementation details or how resources are configured." (§5.5.1)

| Model | Definition (verbatim) | Key points |
|---|---|---|
| **Private** (§5.5.2) | "a cloud deployment model in which the cloud services are used exclusively by a single CSC and the underlying resources are controlled by that CSC." | Can be owned/managed/operated by the CSC or a third party; **on or off premises** ("off premises private cloud" = **"dedicated cloud"**). Can still be multi-tenant (tenants = groups of CSUs of the same CSC). CSC decides reserve capacity for elasticity. Combining on-prem + off-prem private cloud has challenges similar to hybrid. Figures 1/2: on-prem private cloud at CSC premises; off-prem private cloud at CSP premises connected via a "cloud access network". |
| **Public** (§5.5.3) | "a cloud deployment model in which cloud services (and resources) are potentially available to (almost) any CSC and in which the resources are potentially made available to any CSC, typically over a public network." | Owned by business, academic, government org or combination. Very broad boundaries; CSC has "no control over which other CSCs and their CSUs are also users of the same cloud service". |
| **Community** (§5.5.4) | "a cloud deployment model in which the cloud services exclusively support and are shared by a specific collection of CSCs who have shared requirements and a relationship with one another, and where resources are controlled by at least one member of this collection." | Shared concerns: mission, security requirements, policy, compliance. On or off premises (Figures 4/5). Community verifies membership; CSP verifies only authorized CSUs have access; a cloud auditor can verify exclusivity. |
| **Hybrid** (§5.5.5) | "a cloud deployment model which uses a private cloud and a public cloud." | "The individual clouds involved remain unique entities but are bound together by appropriate technology that enables interoperability, data portability and application portability." CSPs may not even be aware of the CSC's hybrid cloud. |

Plus (§10.2.2): "**Multi-cloud** is a cloud deployment model that can be used to deliver application, platform or infrastructure capabilities types."

Difference to NIST: NIST defines hybrid as a composition of "two or more distinct cloud infrastructures (private, community, or public)" **(NIST SP 800-145)**; ISO narrows it to private + public, emphasizes **control** of resources (private: "controlled by that CSC"; community: "controlled by at least one member") rather than who owns/where located, and makes on/off-premises explicit.

### 2.5 Parties, roles, sub-roles, activities (§6)

**Parties (§6.1)**: "Parties are entities that play roles. A party can play more than one role at any given point in time and can only engage in a specific subset of activities of that role."
- **Cloud service customer (CSC)**: "A party which is in a business relationship with cloud service provider(s) for the purpose of using cloud services." Can also have business relationships with CSNs.
- **Cloud service partner (CSN)**: "A party which is engaged in support of, or auxiliary to, activities of either the cloud service provider or the cloud service customer, or both."
- **Cloud service provider (CSP)**: "A party which is in a business relationship for the purpose of providing cloud services. The business relationship is with a cloud service customer or a cloud service partner."
- Also used: **cloud service user (CSU)** — natural person / entity acting for the CSC that uses the service (e.g. Figures 1–3); a **tenant** is a group of CSUs (§5.2.4).

**Roles (§6.2)**: CSC role, CSN role, CSP role.
> "These roles can be further organized into sub-roles (see ISO/IEC 22123-3). Roles and sub-roles, in turn, are sets of activities ... All cloud computing activities can be categorized into three main groups: **activities that use cloud services, activities that provide cloud services and activities that support cloud services.**" (§6.2.1)

- Party ≠ role: an organization operating an internal private cloud and also using cloud services is both CSP and CSC; one organization with independent divisions can act as multiple CSCs; a CSC can centralize administration while distributing users, so "not all CSC sub-roles are implemented in each CSC role".
- **CSC role (§6.2.2)**: "includes activities for the purpose of using cloud services" — smooth operation, acquisition and use, integration with existing ICT systems.
- **CSP role (§6.2.3)**: "a set of activities that make cloud services available" — providing services, deploying and monitoring, managing business plans, providing audit data, maintenance; **example sub-roles: business manager, service manager, network provider, security and risk manager**.
- **CSN role (§6.2.4)**: "a set of activities that support, or are auxiliary to, either the CSP role or the CSC role, or both." Varies by partner type (ISO/IEC TR 23187).

Sub-roles in detail are delegated to ISO/IEC 22123-3 (the former 17789). For orientation (from 17789/22123-3, **not stated in Part 2**): CSC sub-roles = cloud service user, CSC business manager, CSC cloud service administrator, CSC cloud service integrator; CSP sub-roles = CSP cloud service operations manager, cloud service deployment manager, cloud service manager, CSP cloud service business manager, customer support & care representative, inter-cloud provider, cloud service security & risk manager, network provider; CSN sub-roles = cloud service developer, cloud auditor, cloud service broker. (No roles figure exists in Part 2.)

Compared with NIST: NIST SP 500-292 (Reference Architecture) uses five actors — consumer, provider, carrier, auditor, broker; SP 800-145 itself defines no roles. ISO folds carrier into the CSP sub-role "network provider" and auditor/broker into CSN sub-roles.

### 2.6 Cross-cutting aspects (§7)

> "Cross-cutting aspects are behaviours or capabilities which are coordinated across roles and implemented consistently in a cloud computing system. Such aspects can impact multiple roles, activities, and functional components ... in such a way that it is not possible to clearly assign them to individual roles or functional components" (§7.1). "cross cutting aspects like security, protection of PII, and governance have been identified as major concerns and in some cases an impediment to the adoption of cloud computing."

| Clause | Aspect | Core definition / key points |
|---|---|---|
| 7.2 | **Auditability** | "the capability of collecting and making available necessary evidential information related to the operation and use of a cloud service, for the purpose of conducting an audit." Evidence = records/logs from CSC and CSP, kept securely. Audits of CSC use or CSP provision (e.g. certifications; compliance with CSA/SLA). ISO/IEC TR 3445. |
| 7.3 | **Availability** | "the ability to be in a state to perform as required, depends upon the combined characteristics of the reliability, recoverability, and maintainability." Typical SLO: "the amount or percentage of time in a given period that the cloud service is accessible and usable." Also a security property (27017). |
| 7.4 | **Governance** | "the system by which the provision and use of cloud services are directed and controlled by the decision-makers of the organisation (CSP or CSC)." **Internal** cloud governance = design-/run-time policies; **external** = CSA between CSC and CSP. No cloud-specific standard; ISO/IEC 38500 applies. |
| 7.5 | **Interoperability** | "the ability of a CSC's system to interact with a cloud service, or the ability for one cloud service to interact with other cloud services, by exchanging information according to a prescribed method to obtain predictable results." Multiple interfaces: service, administration, business. |
| 7.6 | **Maintenance and versioning** | Maintenance = modifying after delivery (21827); versioning = unique names/numbers for states (24765). CSP vs CSC maintenance split "depends on the cloud service capabilities type". DevOps → frequent updates → need for versioning, esp. **API forward compatibility**; breaking changes only with warnings. |
| 7.7 | **Performance** | Response time, transaction rate, latency, throughput, concurrency, storage capacity, threads, RAM, elasticity limits — covered by SLA (19086-1). |
| 7.8 | **Portability** | Cloud **application** portability ("ability to migrate an application from one cloud service to another cloud service or between a CSC's system and a cloud service") and cloud **data** portability. "Portability in cloud computing is rarely confined to a binary decision of possible or impossible. More often, portability is possible subject to **switching costs**" (19941). |
| 7.9 | **Protection of PII** | Usually **CSC = PII controller, CSP = PII processor**; CSP can be controller (e.g. direct-to-consumer services). PIMS (27701), 27018 (public cloud PII processors), 29100 principles, 19086-4 SLOs/SQOs, data use statements (19944-1), notices/consent (29184). |
| 7.10 | **Regulatory** | Jurisdiction-dependent; cloud-specific vs general (security, privacy) vs domain-specific (health, finance); lawful interception, digital evidence (27037), e-discovery (27050), tax. "The core mechanism ... is the cloud service agreement (CSA) and its related SLA." Policy guidance: TR 22678. |
| 7.11 | **Resiliency** | "the ability of a system to provide and maintain an acceptable level of service in the face of faults (unintentional, intentional, or naturally caused) affecting normal operation." Determined by the least resilient component → risk management. |
| 7.12 | **Reversibility** | "the process for the CSC to retrieve their CSC data and application artefacts and for the CSP to delete all CSC data as well as contractually specified cloud service derived data after an agreed upon period." Exit process; backups kept until exit completes; also applies to peer services. Covered by CSA/SLA (19086), portability (19941). |
| 7.13 | **Security** | "Information security is the preservation of confidentiality, integrity and availability of information" (+ authenticity, accountability, non-repudiation, reliability). **Shared responsibility** depending on capabilities type: "it is likely that the majority of responsibilities lie with the CSP for cloud services of application capabilities type. By contrast, for cloud services of infrastructure capabilities type, much more responsibility is likely to lie with the CSC." CSA must describe the split (27017); certifications 27001+27017; incident and vulnerability handling (29147, 30111). |
| 7.14 | **Service levels and SLA** | "Service level agreements are important components of cloud computing governance and represent measurable elements needed to assure an agreed upon quality of service between a CSC and a CSP." Cloud SLA = part of CSA containing **SLOs** (quantitative) and **SQOs** (qualitative) (19086). Details vary by service category, capabilities type, key characteristics, cross-cutting aspects and deployment model. |

### 2.7 Other key concepts

**Data (§8)**: data processing transparency via data taxonomy & data use statements (19944-1, 22624); data flow (19941, edge 23188); processing of multi-source data with trust elements (provenance, chain of custody, immutable proof of compliance; 23186); **data sharing agreement (DSA)** (23751).

**Virtualization (§9)**:
- **VM** (§9.2.2): "an isolated execution environment for running software that uses virtualized physical resources" — full stack incl. own OS.
- **Hypervisor** (§9.2.3): "software that virtualizes physical resources and allows for running virtual machines".
- **Container** (§9.3): "an isolated execution environment for running software that uses a virtualized operating system kernel (termed the host operating system)" — containers share the host kernel.
- **Serverless** (§9.4), FaaS, serverless DB (see 2.3).
- Virtualized networking (VPN, §9.5), virtualized DSaaS (sharding, replication, §9.6).

**Multiple CSPs (§10)**:
- **Multi-cloud** (§10.2.2): CSC uses public cloud services of two or more CSPs and integrates them; combination for own use = a **cloud solution**.
- **Inter-cloud** (§10.2.3): "A CSP that uses one or more cloud services provided by other CSPs is said to be in an inter-cloud relationship." Primary vs secondary CSP; can be invisible to the CSC.
- Considerations (§10.3): identity and access management, policy (different jurisdictions), management (access, billing, resources), operations. Details in ISO/IEC 5140.

**Logical organization (§11.1)**:
- **Cloud service instance** (§11.1.1): "an entity providing the capabilities of the cloud service. Each cloud service instance has its own resources, isolated from the resources of other cloud service instances." Example: each VM in a CompaaS service is an instance.
- Multiple services/instances (§11.1.2): e.g. web app = FaaS UI instance + container business logic + database instance (Figure 9); multiple instances for scalability (horizontal), fault tolerance, latency; microservices.

**Physical organization (§11.2)**: CSP = highest level; **cloud region** = "a geographical area containing a set of physical resources that are independent and isolated from the physical resources contained in other cloud regions"; **availability domain/zone** = "a logically and physically isolated location within a cloud region" with independent power, cooling, network (min. three per region advisable); an instance lives in exactly one AZ/region; **edge computing** (23188); **affinity** (place resources close → low latency) vs **geo-dispersion** (keep apart → fault tolerance).

---

## 3. Service models: NIST vs ISO

### 3.1 What NIST says (NIST SP 800-145, Sept 2011)

- Definition **(NIST SP 800-145)**: "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction. This cloud model is composed of five essential characteristics, three service models, and four deployment models."
- **Three service models (NIST SP 800-145)**, each defined by "the capability provided to the consumer":
  - **SaaS**: "to use the provider's applications running on a cloud infrastructure" — consumer controls at most limited user-specific settings.
  - **PaaS**: "to deploy onto the cloud infrastructure consumer-created or acquired applications created using programming languages, libraries, services, and tools supported by the provider" — consumer controls deployed apps and hosting environment config.
  - **IaaS**: "to provision processing, storage, networks, and other fundamental computing resources where the consumer is able to deploy and run arbitrary software, which can include operating systems and applications."
- The list is **closed**: exactly three models, and the service model *is* the classification — a service is either SaaS, PaaS or IaaS. NIST adds the notion of "cloud infrastructure" (hardware + abstraction layer) underlying all three.

Note how ISO §5.4.2–5.4.4 deliberately reuse NIST's wording almost verbatim for the descriptions of SaaS/PaaS/IaaS — the change is not in *what* these three mean, but in the **model around them**.

### 3.2 What ISO/IEC 22123-2 does differently

ISO splits NIST's single concept "service model" into **two orthogonal concepts**:

| | **Cloud capabilities type** (§5.3) | **Cloud service category** (§5.4) |
|---|---|---|
| What it classifies | *the kind of functionality* the CSC gets, "based on the resources used" | *groups of real cloud services* with "some common set of qualities" |
| Values | exactly 3: application, platform, infrastructure — "There are only three" | open-ended: SaaS, PaaS, IaaS, NaaS, CaaS, CompaaS, DSaaS + 11 in Annex A, "many more ... can continue to emerge" |
| Overlap | "separation of concerns ... minimal functionality overlap" | categories can overlap; a category "can include capabilities from one or more cloud capabilities types" |
| Determined by | resources/functionality | capabilities types provisioned **+ intended use** |
| Stability | stable, abstract, technology-neutral | market-driven, "informal", evolving |

The classic trio becomes the special case where a category corresponds to exactly one capabilities type (SaaS ↔ application, PaaS ↔ platform, IaaS ↔ infrastructure).

### 3.3 Why the separation — what it fixes in NIST

1. **"XaaS" explosion / closed list.** In practice the market invented NaaS, DBaaS, DaaS, FaaS, CaaS, AIaaS, BlockchainaaS, ... NIST's 3-model taxonomy cannot place these without forcing ("is DBaaS PaaS or SaaS?"). ISO lets new categories be defined freely while still anchoring them to the stable 3-value axis: "a newly defined cloud service category can offer any combination of the three cloud capabilities types" (Annex A).
2. **Hybrid services that span layers.** Many real services offer several capability types at once — NaaS (raw connectivity = infrastructure, custom routing code = platform, management apps = application), DSaaS (block storage = infra, SQL/scripts = platform, admin UI = application), CaaS (platform + application). Under NIST, a service must be exactly one of SaaS/PaaS/IaaS; under ISO the category simply has several "X" in Table A.1.
3. **Separating "what layer" from "what purpose".** NIST mixes both into one label. ISO categorizes by *capabilities types* **and** *intended use* (§5.4.1) — e.g. CaaS = real-time communication, NaaS = transport connectivity, DSaaS = storage — independently of the abstraction level.
4. **Precise reasoning about responsibilities.** Cross-cutting aspects are tied to the capabilities type, not the marketing label: security shared-responsibility split ("majority of responsibilities lie with the CSP for ... application capabilities type ... for ... infrastructure capabilities type, much more responsibility is likely to lie with the CSC", §7.13), maintenance split ("depends on the cloud service capabilities type", §7.6), SLA details vary by both category and capabilities type (§7.14). This works even for a mixed category like DSaaS.
5. **Finer granularity below IaaS.** ISO adds CompaaS (compute only) and DSaaS (storage only) alongside IaaS; §5.4.7 even states the boundary: with storage or more than basic connectivity it "is usually better categorised as an IaaS". NIST has only one infrastructure model.
6. **Newer technologies.** Containers, serverless/FaaS, serverless databases (§9), edge (§11.2.6), multi-/inter-cloud (§10) did not exist in mainstream form in 2011; ISO places them in its framework (e.g. Serverless Computing and FaaS → platform type; Container aaS → infrastructure type; multi-cloud "can be used to deliver application, platform or infrastructure capabilities types").
7. **Wording updates.** ISO SaaS explicitly allows access via **API** as well as thin client; PaaS is distinguished from extensible SaaS by its users ("developers and operations staff versus end users"); IaaS explicitly includes **physical** (not just virtual) resources and mentions hypervisor-hosted VM images.

### 3.4 Other NIST vs ISO differences (beyond service models)

| Aspect | NIST SP 800-145 (2011) | ISO/IEC 22123-1/-2 (2023) |
|---|---|---|
| Characteristics | 5 essential: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service **(NIST SP 800-145)** | 6 key: + **multi-tenancy** as its own characteristic; "rapid elasticity **and scalability**" (horizontal/vertical) |
| Service models | 3, closed | 3 capabilities types + open set of service categories (7 described, 18 in Table A.1) |
| Deployment models | private, community, public, hybrid ("two or more distinct cloud infrastructures") **(NIST SP 800-145)** | private, public, community, hybrid (private + public); defined via **control and sharing**; on/off premises explicit; "dedicated cloud"; multi-cloud mentioned |
| Actors/roles | not in 800-145; SP 500-292 has consumer, provider, carrier, auditor, broker | parties vs roles; CSC, CSP, CSN; sub-roles and activities (22123-3) |
| Cross-cutting aspects | none | 13 (security, PII, governance, SLAs, reversibility, ...) |
| Terminology | "consumer", "provider" | CSC, CSP, CSN, CSU, tenant, cloud service instance |
| Scope extras | none | data, virtualization, multi-CSP, regions/availability zones/edge |
