# FAVS – Module Overview

**Fortgeschrittene Aspekte verteilter Systeme – Cloud-Native Computing**
Hans Grönniger · Hochschule Hannover, Fakultät IV · WS 26/27
Moodle: https://moodle.hs-hannover.de/course/view.php?id=32888

---

## What you need to pass

| Component | Points | Pass condition |
|---|---|---|
| Written test (exam period) | 55 | ≥ 50 % (27.5) |
| Project tasks (ShareWise, incl. 3 presentations) | 45 | ≥ 50 % (22.5) |

**Both conditions must hold separately.** Attendance and active discussion at all **3 presentation slots** are mandatory.

## The 3 presentations

| # | Date | Topic | Builds on | Prep file |
|---|---|---|---|---|
| **P1** | **20.10.26** | Modular architecture of ShareWise | Ex 1–3 (cloud defs, DDD strategic + tactical, hexagonal) | [`../prep/P1_Modular_Architecture.md`](../prep/P1_Modular_Architecture.md) |
| P2 | 17.11.26 | Monolith implementation, limitations & change drivers | Ex 4–7 (modulith, containers, pipelines) | [`../prep/P2_Monolith_Implementation.md`](../prep/P2_Monolith_Implementation.md) |
| P3 | 15.12.26 | Microservices architecture & pattern implementation | Ex 8–11 (deployment, service extraction, messaging, patterns) | [`../prep/P3_Microservices_Patterns.md`](../prep/P3_Microservices_Patterns.md) |

## Schedule (preliminary, slide 7 of 01.Intro)

Lectures are on Tuesdays. The exercise is in the same row and is due on the following Monday.

| # | Lecture | Topic | Script | Exercise due | Exercise |
|---|---|---|---|---|---|
| 1 | 29.09 | Intro, definition, market, ShareWise journey | ✅ `01.Intro` | 05.10 | **Ex1** a) NIST vs ISO/IEC 22123 (service models) b) ShareWise user journey, fuller example |
| 2 | 06.10 | DDD foundation | ✅ `02.DDD` | 12.10 | **Ex2** Subdomains, Bounded Contexts, Context Map, Ubiquitous Language |
| 3 | 13.10 | Spring Boot, Next.js | ✅ `03.TechStack` | 19.10 | **Ex3** Entities/VOs, Aggregates, Domain Events, (Hexagonal) Architecture |
| 4 | **20.10** | **🎤 P1: modular architecture** | – | 26.10 | Ex4 Implement modulith (backend + frontend), AI allowed |
| 5 | 27.10 | Cloud economy, cloud-native, virtualization | ⏳ | 02.11 | Ex5 Implement modulith (cont.) |
| 6 | 03.11 | Container | ⏳ | 09.11 | Ex6 Create containers, run locally |
| 7 | 10.11 | DevOps & CI/CD | ⏳ | 16.11 | Ex7 Create build pipelines |
| 8 | **17.11** | **🎤 P2: monolith impl., limits, change drivers** | – | 23.11 | Ex8 Deploy to eduDSCloud / Proxmox (adapt pipeline) |
| 9 | 24.11 | IaaS (Azure) | ⏳ | 30.11 | Ex9 Factor out services, communicate via messages |
| 10 | 01.12 | Strangler fig, loose coupling, messaging, RabbitMQ, outbox | ⏳ | 07.12 | Ex10 Implement patterns |
| 11 | 08.12 | API gateway, eventual consistency, Saga, resilience | ⏳ | 14.12 | Ex11 Implement patterns |
| 12 | **15.12** | **🎤 P3: microservices + patterns** | – | 04.01 | Rework if needed |
| 13 | 05.01.27 | Buffer | | | |

## ShareWise: the semester project in one glance

"Shared expenses made simple." A group expense app (similar to Splitwise or Tricount).
Roadmap (slide 34): **understand domain → modular monolith → containerize → automate build/deploy → identify change drivers → extract services → events & messaging → distributed consistency → resilience & observability.**
Stack: **Spring Boot** backend + **Next.js** frontend → Docker → CI/CD → eduDSCloud/Proxmox → Azure → RabbitMQ.

## Learning goals (= what the exam can ask)
- Model a domain with DDD.
- Design and implement a modular monolith.
- Containerize and auto-deploy.
- Evaluate reasons for and against extracting a service.
- Sync vs async communication.
- Eventual vs transactional consistency.
- Saga, Retry and other patterns.
- (Logs, metrics, traces.)
- Consequences of microservices: technical, business, economic.

---

## Notes index

| File | Source | Content |
|---|---|---|
| [`skripte/01_Intro.md`](skripte/01_Intro.md) | 01.Intro.pdf | Admin, NIST 5-3-4, responsibility stack, pizza analogy, chances/risks, market, pets vs cattle, **ShareWise basics + Mallorca scenario** |
| [`skripte/02_DDD.md`](skripte/02_DDD.md) | 02.DDD.pdf | Strategic DDD (subdomains, UL, BCs, context-map patterns), tactical DDD (VO, entity, aggregate, events, ES), architectures (layered, hexagonal, CQRS), **all ShareWise DDD hints**, Ex2 method guide |
| [`skripte/03_TechStack.md`](skripte/03_TechStack.md) | 03.TechStack.pdf | React, Next.js (App Router, SSR/CSR/SSG, API routes), Spring/Spring Boot, REST CRUD with JPA/H2, setup to-dos. ⚠ Text-only; screenshot slides not visually checked |
| [`norms/ISO22123-1_Vocabulary.md`](norms/ISO22123-1_Vocabulary.md) | ISO/IEC 22123-1:2023 | All definitions + NIST vs ISO comparison tables |
| [`norms/ISO22123-2_Concepts.md`](norms/ISO22123-2_Concepts.md) | ISO/IEC 22123-2:2023 | Key characteristics, capabilities types vs service categories (Table A.1), roles, cross-cutting aspects, NIST vs ISO service models |

**Convention in all notes:** "(slide N)" = PDF page. "(note:)" = added clarification, not from the source.

**When new scripts or exercises arrive:** drop them into `skripte/` or `exercises/`. Then a new note goes into `notes/skripte/`, and the matching `prep/P*.md` file gets updated.
