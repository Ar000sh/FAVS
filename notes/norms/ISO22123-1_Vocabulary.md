# ISO/IEC 22123-1:2023 — Cloud computing, Part 1: Vocabulary

> Source: `exercises/isoiec22123-1ed20en.pdf` (ISO/IEC 22123-1, 2nd edition, 2023-02, 23 pages).
> Context: **FAVS Exercise 1** — "Compare the cloud computing definitions of NIST and ISO/IEC 22123 (esp. the service models part). The NIST definitions are rather old and were updated in the ISO norm."
> Clause numbers below are written as **(3.x.y)**. Text in quotation blocks is verbatim from the standard. Anything marked **(NIST SP 800-145)** comes from the NIST document, not from the PDF.

---

## 1. Overview of the document

| Item | Content |
|---|---|
| Full title | *Information technology — Cloud computing — Part 1: Vocabulary* |
| Edition | **Second edition, 2023-02** (ISO/IEC 22123-1:2023(E)) |
| Author body | ISO/IEC **JTC 1/SC 38** "Cloud Computing and Distributed Platforms" |
| Replaces | **ISO/IEC 17788:2014** (the original joint ISO/ITU-T cloud vocabulary/overview) **and** ISO/IEC 22123-1:2021 (first edition) |
| Scope (Clause 1) | "This document defines terms used in the field of cloud computing." It is **only a vocabulary**. The concepts and the architecture are covered in other parts of the 22123 series (e.g. 22123-2 *Concepts*) and in ISO/IEC 22123-3 / 17789 (reference architecture). |
| Normative references | None |
| Length | 23 pages. All content is in Clause 3 "Terms and definitions", plus a bibliography and an index. |

### Structure of Clause 3 (14 subclauses)

| Subclause | Topic | Notable terms |
|---|---|---|
| 3.1 | Cloud computing foundation | cloud computing, cloud service, cloud solution |
| 3.2 | Cloud deployment models | community, hybrid, private, public, multi-cloud, federated, hybrid multi-cloud, inter-cloud |
| 3.3 | Roles and activities | party, CSC, CSP, CSU, CSN, auditor, broker, developer, role, sub-role, CSC/CSP/CSN role |
| 3.4 | Key cloud computing characteristics | measured service, tenant, multi-tenancy, on-demand self-service, resource pooling |
| 3.5 | Cloud capabilities types and cloud service categories | application/infrastructure/platform capabilities type; CaaS, CompaaS, DSaaS, IaaS, NaaS, PaaS, SaaS |
| 3.6 | Interoperability | transport, syntactic, semantic data, behavioural, policy interoperability |
| 3.7 | Cloud service agreements | SLA, cloud SLA, SLO, SQO, remedy, failure notification policy |
| 3.8 | Cloud portability | data portability and application portability (several facets of each) |
| 3.9 | Cloud data | CSC data, cloud service derived data, CSP data, account data, EUII, OPD, ... |
| 3.10 | Security and privacy | PII, secure multi-tenancy |
| 3.11 | Inter-cloud | inter-cloud computing, primary/secondary CSP |
| 3.12 | Virtualization | virtual, VM, hypervisor, container, container image |
| 3.13 | Miscellaneous | availability, reversibility, resilience, audit, auditability, cloud native application, device platform, ... |
| 3.14 | Multiplicity and organization of cloud services (**new in 2023**) | affinity, geo-dispersion, availability domain/zone, cloud region |

### Main changes in the 2023 edition (from the Foreword)
- The definition of **hybrid cloud** was changed.
- **CSC role, CSP role and CSN role** were added. CSC, CSP and CSN are now defined through these roles.
- The ISO/IEC 27000 definitions (confidentiality, integrity, information security) were removed.
- The definition of **inter-cloud computing** was changed.
- **Multi-cloud** terms were added.
- *Peer* cloud service / *peer* CSP were renamed **secondary cloud service / secondary CSP**.
- The new subclause **3.14** (multiplicity and organization of cloud services) was added.

---

## 2. Key term definitions

### 2.1 Foundation (3.1)

**cloud computing (3.1.1)**
> paradigm for enabling network access to a scalable and elastic pool of shareable physical or virtual resources with self-service provisioning and administration on-demand
>
> Note 1 to entry: Examples of resources include servers, operating systems, networks, software, applications, and storage equipment.
> Note 2 to entry: Self-service provisioning refers to the provisioning of resources provided to cloud services (3.1.2) performed by cloud service customers (3.3.2) through automated means.

**cloud service (3.1.2)**
> one or more capabilities offered via cloud computing (3.1.1) invoked using a defined interface

**cloud solution (3.1.3)**
> cloud services (3.1.2) combined and controlled to meet cloud service customer (3.3.2) requirements
>
> Note 1 to entry: A cloud solution can use any combination of cloud deployment models (3.2.1).

### 2.2 Key cloud computing characteristics (3.4)

**measured service (3.4.1)**
> metered delivery of cloud services (3.1.2) such that usage can be monitored, controlled, reported and billed

**tenant (3.4.2)**
> one or more cloud service users (3.3.4) sharing access to a set of physical and virtual resources

**multi-tenancy (3.4.3)**
> allocation of physical or virtual resources such that multiple tenants (3.4.2) and their computations and data are isolated from and inaccessible to one another

**on-demand self-service (3.4.4)**
> feature where a cloud service customer (3.3.2) can provision computing capabilities, as needed, automatically or with minimal interaction with the cloud service provider (3.3.3)

**resource pooling (3.4.5)**
> aggregation of a cloud service provider's (3.3.3) physical or virtual resources to serve one or more cloud service customers (3.3.2)

Related: **secure multi-tenancy (3.10.2)**
> type of multi-tenancy (3.5.3) that employs security controls to explicitly guard against data breaches and provides validation of these controls for proper governance
>
> Note 1 to entry: Secure multi-tenancy exists when the risk profile of an individual tenant (3.5.2) is no greater than it would be in a dedicated, single-tenant environment.

*(Erratum in the PDF: these cross-references should read multi-tenancy **3.4.3** and tenant **3.4.2**. The numbers 3.5.3/3.5.2 are left over from the old numbering.)*

> **Important for the comparison:** Subclause 3.4 of the 2023 vocabulary defines only **four characteristic terms plus "tenant"**. **Broad network access** and **rapid elasticity and scalability** are **not separate entries** here, although ISO/IEC 17788:2014 still listed them as two of its six key characteristics. In 22123-1 they are part of the core definition itself: "*network access* to a *scalable and elastic* pool". The full list of six key characteristics (broad network access, measured service, multi-tenancy, on-demand self-service, rapid elasticity and scalability, resource pooling) comes from ISO/IEC 17788:2014 §6.2. That list is now continued in ISO/IEC 22123-2 (*Concepts*), not in this vocabulary.

### 2.3 Cloud capabilities types (3.5.1–3.5.4)

A capabilities type is a classification **by the resources the customer can use**. There are **exactly three**.

**cloud capabilities type (3.5.1)**
> classification of the functionality provided by a cloud service (3.1.2) to the cloud service customer (3.3.2), based on resources used
>
> Note 1 to entry: The cloud capabilities types are application capabilities type (3.5.2), infrastructure capabilities type (3.5.3) and platform capabilities type (3.5.4).

**application capabilities type (3.5.2)**
> cloud capabilities type (3.5.1) in which the cloud service customer (3.3.2) can use the cloud service provider's (3.3.3) applications

**infrastructure capabilities type (3.5.3)**
> cloud capabilities type (3.5.1) in which the cloud service customer (3.3.2) can provision and use processing, storage or networking resources

**platform capabilities type (3.5.4)**
> cloud capabilities type (3.5.1) in which the cloud service customer (3.3.2) can deploy, manage and run customer-created or customer-acquired applications using one or more programming languages and one or more execution environments supported by the cloud service provider (3.3.3)

### 2.4 Cloud service categories (3.5.5–3.5.12)

A service category is a **group of cloud services with common qualities**, i.e. a market-oriented label. One category can draw on **one or more** capabilities types.

**cloud service category (3.5.5)**
> group of cloud services (3.1.2) that possess some common set of qualities
>
> Note 1 to entry: A cloud service category can include capabilities from one or more cloud capabilities types (3.5.1).

The standard lists **seven** categories (alphabetical, as in the document):

| Clause | Category | Verbatim definition (the part after "cloud service category in which...") | Capabilities type(s) |
|---|---|---|---|
| 3.5.6 | **Communications as a Service (CaaS)** | "the capability provided to the cloud service customer is real time interaction and collaboration" | Application **and** platform (Note 1) |
| 3.5.7 | **Compute as a Service (CompaaS)** | "the capabilities provided to the cloud service customer are the provision and use of processing resources needed to deploy and run software" | Not stated (essentially infrastructure). Note 1: "To run some software, capabilities other than processing resources are potentially needed." |
| 3.5.8 | **Data Storage as a Service (DSaaS)** | "the capability provided to the cloud service customer is the provision and use of data storage and related capabilities" | **Any** of the three (Note 1) |
| 3.5.9 | **Infrastructure as a Service (IaaS)** | "the cloud capabilities type provided to the cloud service customer is an infrastructure capabilities type" | Infrastructure (1:1) |
| 3.5.10 | **Network as a Service (NaaS)** | "the capability provided to the cloud service customer is transport connectivity and related network capabilities" | **Any** of the three (Note 1) |
| 3.5.11 | **Platform as a Service (PaaS)** | "the cloud capabilities type provided to the cloud service customer is a platform capabilities type" | Platform (1:1) |
| 3.5.12 | **Software as a Service (SaaS)** | "the cloud capabilities type provided to the cloud service customer is an application capabilities type" | Application (1:1) |

Full verbatim text for the three "classic" categories:

**infrastructure as a service, IaaS (3.5.9)**
> cloud service category (3.5.5) in which the cloud capabilities type (3.5.1) provided to the cloud service customer (3.3.2) is an infrastructure capabilities type (3.5.3)
>
> Note 1 to entry: The cloud service customer (3.3.2) does not manage or control the underlying physical and virtual resources, but does have control over operating systems, storage, and deployed applications that use the physical and virtual resources. The cloud service customer (3.3.2) can also have limited ability to control certain networking components (e.g., host firewalls).

**platform as a service, PaaS (3.5.11)**
> cloud service category (3.5.5) in which the cloud capabilities type (3.5.1) provided to the cloud service customer (3.3.2) is a platform capabilities type (3.5.4)

**software as a service, SaaS (3.5.12)**
> cloud service category (3.5.5) in which the cloud capabilities type (3.5.1) provided to the cloud service customer (3.3.2) is an application capabilities type (3.5.2)

**How it fits together:** the model has two levels. **Capabilities types** (3 types, *what kind of resource the customer gets*) are separate from **service categories** (7+ categories, *how offerings are grouped and marketed*). IaaS, PaaS and SaaS are the categories that map 1:1 to a capabilities type. CaaS, NaaS and DSaaS cut across the types. The list of categories is open (the wording is "group of cloud services..."), so new "X-aaS" offerings can be added without breaking the model.

### 2.5 Cloud deployment models (3.2)

**cloud deployment model (3.2.1)**
> way in which cloud computing (3.1.1) can be organized based on the control and sharing of physical or virtual resources
>
> Note 1 to entry: Examples of cloud deployment models include community cloud (3.2.1), hybrid cloud (3.2.3), private cloud (3.2.4) and public cloud (3.2.5).

*(Erratum: community cloud is 3.2.2, not 3.2.1.)* The word "**Examples**" matters: the list is **open**, not fixed at four.

**community cloud (3.2.2)**
> cloud deployment model (3.2.1) where cloud services (3.1.2) exclusively support and are shared by a specific collection of cloud service customers (3.3.2) who have shared requirements and a relationship with one another, and where resources are controlled by at least one member of this collection

**hybrid cloud (3.2.3)**, changed in 2023
> cloud deployment model (3.2.1) that uses a private cloud (3.2.4) and a public cloud (3.2.5)

**private cloud (3.2.4)**
> cloud deployment model (3.2.1) where cloud services (3.1.2) are used exclusively by a single cloud service customer (3.3.2) and resources are controlled by that cloud service customer (3.3.2)

**public cloud (3.2.5)**
> cloud deployment model (3.2.1) where cloud services (3.1.2) are potentially available to any cloud service customer (3.3.2) and resources are controlled by the cloud service provider (3.3.3)

**multi-cloud / multicloud (3.2.6)**, new
> cloud deployment model (3.2.1) in which a cloud service customer (3.3.2) uses public cloud services (3.1.2) provided by two or more cloud service providers (3.3.3)
>
> Note 1 to entry: The cloud service customer (3.3.2) is responsible for integration and management of these cloud services (3.1.2) to form a cloud solution (3.1.3).

**cloud service federation (3.2.7)**
> two or more cloud service providers (3.3.3) bound together by an agreed set of policies, processes and trust in order to provide cloud services (3.1.2)

**federated cloud (3.2.8)**
> cloud deployment model (3.2.1) in which the cloud services (3.1.2) are provided by members of a cloud service federation (3.2.7)

**hybrid multi-cloud (3.2.9)**
> cloud deployment model (3.2.1) in which a cloud service customer (3.3.2) uses cloud services (3.1.2) from a hybrid cloud (3.2.3) and a multi-cloud (3.2.6)

**inter-cloud / intercloud (3.2.10)**
> cloud deployment model (3.2.1) in which a cloud service provider (3.3.3) offers a cloud service (3.1.2) by using one or more cloud services (3.1.2) provide[d] by other cloud service providers (3.3.3)
>
> Note 1 to entry: The primary cloud service provider (3.11.2) provides the cloud service typically via intermediation, aggregation, or arbitrage of the cloud services provided by secondary cloud service providers (3.11.4).

**Who integrates?** In **multi-cloud**, the *customer* integrates several CSPs. In **inter-cloud**, a *provider* (the primary CSP) integrates the services of secondary CSPs. In a **federated cloud**, the *providers* cooperate as equals under shared policies.

Related inter-cloud terms (3.11): **inter-cloud computing (3.11.1)** "paradigm for enabling the interworking between a primary cloud service provider and one or more secondary cloud service providers"; **primary CSP (3.11.2)**; **secondary cloud service (3.11.3)**; **secondary CSP (3.11.4)**. Before 2023 these were called "peer" cloud service / "peer" CSP.

### 2.6 Roles, sub-roles and parties (3.3)

The model has three layers: **activity → role → party**. A *party* (a real organisation or person) takes on one or more *roles*. A role is a set of *activities*.

| Clause | Term | Verbatim definition |
|---|---|---|
| 3.3.1 | **party** | "natural person, legal person or a group of either, whether or not incorporated, that can assume one or more roles (3.3.10)" |
| 3.3.8 | **activity** | "specified pursuit or set of tasks" |
| 3.3.9 | functional component | "functional building block needed to engage in an activity (3.3.8), backed by an implementation" |
| 3.3.10 | **role** | "set of activities (3.3.8) that serves a common purpose" |
| 3.3.11 | **sub-role** | "subset of the activities (3.3.8) of a given role (3.3.10)" |
| 3.3.14 | **CSC role** (new) | "set of activities (3.3.8) for the purpose of using cloud services (3.1.2)" |
| 3.3.15 | **CSP role** (new) | "set of activities (3.3.8) that make cloud services (3.1.2) available" |
| 3.3.16 | **CSN role** (new) | "set of activities (3.3.8) that support, or are auxiliary to, either the cloud service provider role (3.3.15) or the cloud service customer role (3.3.14), or both" |
| 3.3.2 | **cloud service customer (CSC)** | "party (3.3.1) that is acting in a cloud service customer role (3.3.14)" |
| 3.3.3 | **cloud service provider (CSP)** | "party (3.3.1) that is acting in a cloud service provider role (3.3.15)" |
| 3.3.5 | **cloud service partner (CSN)** | "party (3.3.1) that is acting in a cloud service partner role (3.3.16)" |
| 3.3.4 | **cloud service user (CSU)** | "natural person, or entity acting on their behalf, associated with a cloud service customer (3.3.2) that uses cloud services (3.1.2)". Note 1: entities include devices and applications. |
| 3.3.6 | cloud auditor (a CSN) | "cloud service partner (3.3.5) with the responsibility to conduct an audit (3.13.10) of the provision and use of cloud services (3.1.2)" |
| 3.3.7 | cloud service broker (a CSN) | "cloud service partner (3.3.5) that negotiates relationships between cloud service customers (3.3.2) and cloud service providers (3.3.3)" |
| 3.3.13 | cloud service developer (a CSN) | "cloud service partner (3.3.5) with the responsibility for designing, developing, testing and maintaining the implementation of a cloud service (3.1.2)" |
| 3.3.12 | device platform cloud service | "cloud service (3.1.2) offered by the device platform provider (3.13.13) to support the device platform (3.13.5)" |

**Key point:** **auditor, broker and developer are *specialisations of the partner (CSN)***, not top-level actors. The **CSC vs. CSU** distinction is also important. The CSC is the party that holds the business relationship (for example a company). The CSUs are the people or devices that actually use the service.

### 2.7 Cross-cutting aspects and other terms

The vocabulary has no subclause called "cross-cutting aspects". Those are described in ISO/IEC 17789 / 22123-3 (reference architecture): auditability, availability, governance, interoperability, maintenance & versioning, performance, portability, protection of PII, regulatory, resiliency, reversibility, security, SLAs. However, it **defines many of the terms behind those aspects**:

| Aspect | Terms (clause) |
|---|---|
| Interoperability | interoperability (3.6.1) "ability of two or more systems or applications to exchange information and to mutually use the information that has been exchanged"; cloud interoperability (3.6.2); facets: **transport (3.6.3), syntactic (3.6.4), semantic data (3.6.5), behavioural (3.6.6), policy (3.6.7)** |
| Portability | cloud application portability (3.8.1); data portability (3.8.2) "ability to easily transfer data from one system to another without being required to re-enter data"; cloud data portability (3.8.3); data syntactic/semantic/policy portability (3.8.4–3.8.6); application portability (3.8.7) with syntactic, instruction, metadata, behaviour and policy facets (3.8.8–3.8.12) |
| Service agreements / SLAs | SLA (3.7.1), cloud service product (3.7.2), product catalogue (3.7.3), service catalogue (3.7.4), **cloud SQO (3.7.5)** (qualitative, nominal/ordinal scale), **cloud SLA (3.7.6)**, **cloud SLO (3.7.7)** (quantitative, interval/ratio scale), cloud service agreement (3.7.8), metric (3.7.9), failure notification policy (3.7.10), remedy (3.7.11) |
| Data | CSC data (3.9.1), cloud service derived data (3.9.2), CSP data (3.9.3), account data (3.9.4), EUII (3.9.5), mixed dataset (3.9.6), individual data (3.9.7), organizational data (3.9.8), OPD (3.9.9), public domain data (3.9.10), non-personal data (3.9.11), data principal (3.9.12), transparency (3.9.13) |
| Security and privacy | PII (3.10.1), secure multi-tenancy (3.10.2) |
| Availability / resilience / reversibility / audit | availability (3.13.7) "ability to be in a state to perform as required"; **reversibility (3.13.8)** (customer gets data back and the CSP deletes it); resilience (3.13.9) "ability of a cloud service to recover operational condition quickly after a fault occurs"; audit (3.13.10); auditability (3.13.11) |
| Virtualization | virtual (3.12.1), VM (3.12.2), hypervisor (3.12.3), **container (3.12.4)** "isolated execution environment for running software that uses a virtualized operating system kernel", container image (3.12.5) |
| Modern cloud | **cloud native application (3.13.12)** "application that is explicitly designed to run within and to take advantage of the capabilities and environment of cloud services"; device, device platform, application marketplace, device platform provider (3.13.3–3.13.6, 3.13.13) |
| Multiplicity and organization (new 3.14) | affinity (3.14.1), geo-dispersion (3.14.2), **availability domain or zone (3.14.3)** "logically and physically isolated location within a cloud region", **cloud region (3.14.4)** |

---

## 3. Comparison: NIST SP 800-145 (2011) vs. ISO/IEC 22123-1:2023

**NIST definition (NIST SP 800-145, Sept. 2011):**
> "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction. This cloud model is composed of five essential characteristics, three service models, and four deployment models."

**ISO definition (3.1.1):**
> "paradigm for enabling network access to a scalable and elastic pool of shareable physical or virtual resources with self-service provisioning and administration on-demand"

### 3.1 Definition of cloud computing

| Aspect | NIST SP 800-145 | ISO/IEC 22123-1:2023 | What changed and why it matters |
|---|---|---|---|
| Nature | "model" | "**paradigm**" | ISO treats cloud as a general paradigm rather than one fixed model. |
| Structure | Fixed formula: 5 + 3 + 4 | No fixed counts. Lists use "examples" and "group of" | ISO is **open and extensible**, so new models and categories can be added. |
| Resources | "shared pool of configurable computing resources" | "scalable and elastic pool of shareable **physical or virtual** resources" | Virtualization is explicit. Elasticity moves into the core definition. |
| Provisioning | "rapidly provisioned and released with minimal management effort or service provider interaction" | "**self-service provisioning and administration** on-demand" | ISO adds *administration*, so the customer also manages the resources, not only provisions them. |
| Network | "ubiquitous, convenient ... network access" | "network access" | ISO drops the marketing adjectives. |

### 3.2 Essential characteristics (NIST) vs. key characteristics (ISO)

| NIST SP 800-145 essential characteristic | ISO counterpart | Comment |
|---|---|---|
| **On-demand self-service** | **on-demand self-service (3.4.4)** | Almost the same wording. ISO uses CSC/CSP instead of "consumer/service provider". |
| **Broad network access** | No separate entry in 22123-1:2023. Contained in 3.1.1 ("network access"). Listed as a key characteristic in ISO/IEC 17788:2014 and 22123-2 | Kept in substance. |
| **Resource pooling** (NIST: multi-tenant model, location independence) | **resource pooling (3.4.5)** "aggregation of a CSP's physical or virtual resources to serve one or more CSCs" | NIST mixed pooling and multi-tenancy in one item. **ISO separates them.** |
| **Rapid elasticity** | No separate entry in 22123-1:2023. Contained in 3.1.1 ("scalable and elastic pool"). Called "rapid elasticity **and scalability**" in 17788 / 22123-2 | ISO adds *scalability* next to elasticity. |
| **Measured service** | **measured service (3.4.1)** "metered delivery ... monitored, controlled, reported and **billed**" | ISO explicitly adds billing. |
| — (only implied inside resource pooling) | **multi-tenancy (3.4.3)** + **tenant (3.4.2)** + **secure multi-tenancy (3.10.2)** | **NEW as its own characteristic.** Isolation of tenants' computations and data becomes a defining property. This matters for security, compliance and SLAs. |

So NIST has **5** characteristics and ISO has **6** (17788/22123-2: the five + multi-tenancy). The 22123-1:2023 vocabulary itself defines only 4 of them as separate terms and puts the other two into the core definition.

### 3.3 Service models (NIST) vs. capabilities types + service categories (ISO). This is the main point of the exercise.

| | NIST SP 800-145 | ISO/IEC 22123-1:2023 |
|---|---|---|
| Concept | **3 service models**: SaaS, PaaS, IaaS. Each is defined by *what the consumer can control* | **Two levels**: (a) **3 cloud capabilities types** (application, platform, infrastructure; 3.5.1–3.5.4) and (b) an **open set of cloud service categories** (3.5.5) |
| SaaS | "capability ... to use the provider's applications running on a cloud infrastructure ... consumer does not manage or control the underlying cloud infrastructure ... with the possible exception of limited user-specific application configuration settings" | Application capabilities type (3.5.2) "can use the CSP's applications" + SaaS category (3.5.12) = the category that provides the application capabilities type |
| PaaS | "deploy onto the cloud infrastructure consumer-created or acquired applications created using programming languages, libraries, services, and tools supported by the provider" | Platform capabilities type (3.5.4) "deploy, manage and run customer-created or customer-acquired applications using one or more programming languages and one or more execution environments supported by the CSP" + PaaS (3.5.11) |
| IaaS | "provision processing, storage, networks, and other fundamental computing resources ... control over operating systems, storage, and deployed applications; and possibly limited control of select networking components (e.g., host firewalls)" | Infrastructure capabilities type (3.5.3) "provision and use processing, storage or networking resources" + IaaS (3.5.9). **Note 1 keeps NIST's control wording almost verbatim** (OS, storage, apps, host firewalls). |
| Further models | None. Everything else (e.g. "Storage-aaS", "Network-aaS") does not fit cleanly | **CaaS (3.5.6), CompaaS (3.5.7), DSaaS (3.5.8), NaaS (3.5.10)**. These categories may combine several capabilities types (DSaaS and NaaS: any of the three; CaaS: application + platform) |
| Mapping | 1 model = 1 level of control | **Many-to-many**: one category → one or more capabilities types |

**Why this matters:**
1. NIST mixes two things in one term: the *technical kind of capability* and the *market label*. ISO **separates them**. Capabilities types are a fixed technical classification (3 types). Categories are an open grouping (7 listed, more possible).
2. Real offerings such as cloud storage (S3), managed networking/SD-WAN, Teams/Zoom, or serverless compute do not fit exactly one NIST box. ISO can describe them, e.g. DSaaS offered as an infrastructure-type *or* an application-type capability.
3. ISO still covers the familiar **IaaS / PaaS / SaaS** (backward compatible with NIST) by defining them as the categories that map 1:1 onto a capabilities type.

### 3.4 Deployment models

| NIST SP 800-145 (4) | ISO/IEC 22123-1:2023 | Change |
|---|---|---|
| **Private cloud**: "provisioned for exclusive use by a single organization comprising multiple consumers ... may be owned, managed, and operated by the organization, a third party, or some combination ... on or off premises" | **private cloud (3.2.4)**: used exclusively by a single CSC **and resources are controlled by that CSC** | ISO bases the definition on **control and sharing**, not ownership or location. |
| **Community cloud**: "exclusive use by a specific community of consumers from organizations that have shared concerns (e.g., mission, security requirements, policy, and compliance considerations)" | **community cloud (3.2.2)**: shared by a specific collection of CSCs with shared requirements and a relationship, **resources controlled by at least one member** | Kept, with control made explicit. |
| **Public cloud**: "open use by the general public ... exists on the premises of the cloud provider" | **public cloud (3.2.5)**: potentially available to any CSC, **resources controlled by the CSP** | Same idea. Defined by control instead of premises. |
| **Hybrid cloud**: "composition of two or more distinct cloud infrastructures (private, community, or public) ... bound together by standardized or proprietary technology that enables data and application portability (e.g., cloud bursting)" | **hybrid cloud (3.2.3)**: "uses a private cloud and a public cloud" (**changed in 2023**. 17788 had "at least two different cloud deployment models") | ISO **narrows** hybrid to private + public. Other combinations get their own names. |
| — | **multi-cloud (3.2.6)** | **NEW**: one CSC uses public services of ≥2 CSPs; the CSC integrates them |
| — | **hybrid multi-cloud (3.2.9)** | **NEW**: hybrid + multi-cloud |
| — | **federated cloud (3.2.8)** + cloud service federation (3.2.7) | **NEW**: providers bound by shared policies, processes and trust |
| — | **inter-cloud (3.2.10)** + primary/secondary CSP (3.11) | **NEW** as a deployment model: a CSP builds its service on other CSPs' services |
| Fixed: 4 models | "Examples ... include". **Open list** | Extensible |

**Why it matters:** in 2011 one organisation usually combined *one* private with *one* public cloud. Today, multi-vendor strategies (AWS + Azure + GCP), sovereign or federated clouds (e.g. Gaia-X) and provider-on-provider stacks (SaaS built on IaaS from a hyperscaler) are common. NIST has no vocabulary for these and ISO does.

### 3.5 Roles / actors

| NIST | ISO/IEC 22123-1:2023 | Change |
|---|---|---|
| **SP 800-145** defines **no roles**. It uses only "consumer" and "provider" informally inside the definitions | Formal model: **activity (3.3.8) → role (3.3.10) / sub-role (3.3.11) → party (3.3.1)** | ISO separates *what is done* (role) from *who does it* (party). One party can hold several roles, e.g. a CSP that is also a CSC of another CSP (inter-cloud). |
| (NIST SP 500-292 Reference Architecture, 2011: **5 actors** — Cloud Consumer, Cloud Provider, Cloud Carrier, Cloud Auditor, Cloud Broker) | **3 roles**: **CSC role (3.3.14), CSP role (3.3.15), CSN role (3.3.16)** → parties **CSC (3.3.2), CSP (3.3.3), CSN (3.3.5)** | NIST's auditor and broker become **sub-types of the partner**: **cloud auditor (3.3.6), cloud service broker (3.3.7)**, plus a new **cloud service developer (3.3.13)**. NIST's *carrier* has no own term in the vocabulary. In the ISO architecture (17789) the network provider is a CSP or CSN function. |
| "consumer" = the organisation **and** the end user | **CSC** (party with the business relationship) vs. **CSU (3.3.4)** (natural person / device / application that actually uses the service) | Clearer for contracts, data ownership and liability. |

### 3.6 What ISO adds that NIST 800-145 does not cover at all

- **Cloud service** (3.1.2) and **cloud solution** (3.1.3) as separate terms
- **Interoperability** (5 facets) and **portability** (data and application, several facets each), which help avoid vendor lock-in
- **Service agreement terms**: cloud SLA, SLO (quantitative) vs. SQO (qualitative), remedy, failure notification policy
- **Data classes**: CSC data vs. cloud service derived data vs. CSP data vs. account data, PII, OPD. These are relevant for GDPR and for who owns what
- **Reversibility**, resilience, availability, auditability
- **Virtualization including containers** and **cloud native applications**. NIST 2011 predates Docker (2013) and Kubernetes (2014)
- **Topology terms**: cloud region, availability zone, affinity, geo-dispersion

---

## 4. Exam summary: key differences

1. **Age and status:** NIST SP 800-145 (2011) is a US-government *definition*, 7 pages, never revised. ISO/IEC 22123-1:2023 is an international *vocabulary* that replaces ISO/IEC 17788:2014 and 22123-1:2021.
2. **Definition:** NIST "model ... 5 + 3 + 4". ISO "paradigm", physical **or virtual** resources, self-service provisioning **and administration**, no fixed counts.
3. **Characteristics:** ISO keeps NIST's five and adds **multi-tenancy** as a separate key characteristic (with tenant and secure multi-tenancy). "Rapid elasticity" becomes "rapid elasticity **and scalability**". In 22123-1:2023 broad network access and elasticity are folded into the core definition.
4. **Service models → two levels:** NIST has 3 service models. ISO has **3 cloud capabilities types** (application, platform, infrastructure) and an **open set of cloud service categories** (CaaS, CompaaS, DSaaS, IaaS, NaaS, PaaS, SaaS). Categories can combine several capabilities types.
5. **IaaS/PaaS/SaaS** still exist, defined as the categories that map 1:1 to a capabilities type. The IaaS note keeps NIST's control-boundary wording.
6. **Deployment models:** NIST has a fixed 4. ISO has an open list defined by **control and sharing**. Hybrid is narrowed to private + public. **Multi-cloud, hybrid multi-cloud, federated cloud and inter-cloud** are added.
7. **Roles:** NIST 800-145 has none (SP 500-292: 5 actors). ISO uses activity → role → party with **CSC / CSP / CSN**. Auditor, broker and developer are CSN sub-types. The **CSU** is separate from the CSC.
8. **New areas:** interoperability, portability, SLA/SLO/SQO, data categories, reversibility, containers, cloud native, regions and zones.
