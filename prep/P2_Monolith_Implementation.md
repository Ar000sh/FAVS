# Presentation 2: Monolith Implementation, Limitations & Change Drivers (17.11.26)

**Status:** 🟡 skeleton. The scripts for lectures 5–7 are not out yet. This file gets filled as they arrive.

## Exercises feeding into P2
| Due | Exercise | Script |
|---|---|---|
| 26.10 | Ex4 Implement modulith (backend, frontend), AI allowed | `03.TechStack` ✅ |
| 02.11 | Ex5 Implement modulith (cont.) | Lecture 5: cloud economy, cloud-native, virtualization ⏳ |
| 09.11 | Ex6 Create containers, run locally | Lecture 6: Container ⏳ |
| 16.11 | Ex7 Create pipelines (build) | Lecture 7: DevOps & CI/CD ⏳ |

## What's already known
- **Roadmap steps covered:** 2 *build a modular monolith* → 3 *containerize* → 4 *automate build & deployment* → 5 ***identify change drivers*** (Intro slide 34).
- The title names the change drivers explicitly: **"more users, more scaling, …"**.
- **Tech:** Spring Boot (starter-parent 4.0.6, Web MVC, JPA, H2, Lombok) + Next.js (App Router), REST/JSON. See [`notes/skripte/03_TechStack.md`](../notes/skripte/03_TechStack.md).
- **Learning goal behind it:** "evaluate reasons for and against service extraction" (Intro slide 5).
- The module cut from P1 should carry over: one bounded context = one module.

## To fill in later
- Relevant concepts from lectures 5–7
- Limitations of the monolith (scaling, deployment coupling, team coupling …)
- Change-driver analysis per module
- Checklist + discussion questions
