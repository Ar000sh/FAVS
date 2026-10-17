# Presentation 3: Microservices Architecture & Pattern Implementation (15.12.26)

**Status:** 🟡 skeleton. The scripts for lectures 9–11 are not out yet.

## Exercises feeding into P3
| Due | Exercise | Script |
|---|---|---|
| 23.11 | Ex8 Deploy to eduDSCloud / Proxmox (adapt pipeline) | ⏳ |
| 30.11 | Ex9 Factor out services, communicate via messages | Lecture 9: IaaS (Azure) ⏳ |
| 07.12 | Ex10 Implement patterns | Lecture 10: strangler fig, loose coupling, messaging, RabbitMQ, outbox ⏳ |
| 14.12 | Ex11 Implement patterns | Lecture 11: API gateway, eventual consistency, Saga, resilience ⏳ |

## What's already known
- **Roadmap steps covered:** 6 *extract selected services* → 7 *events & messaging* → 8 *distributed consistency* → 9 *resilience & observability* (Intro slide 34).
- **Learning goals:**
  - sync vs async communication
  - eventual vs transactional consistency
  - Saga, Retry & other patterns
  - logs/metrics/traces
  - technical, business and economic consequences of microservices
- **DDD groundwork already taught (02.DDD):**
  - aggregate rule 4: update other aggregates via **eventual consistency**
  - domain events as the aggregate's public interface → messaging
  - context-map patterns become the integration contracts between services: OHS/Published Language → API, ACL → translation layer
  - CQRS / projections, sync vs async
- Conway's law: BCs → services → teams.

## To fill in later
- Concepts from lectures 9–11
- Which ShareWise services get extracted, and why (from P2's change drivers)
- Pattern implementation notes (outbox, Saga, retry/circuit breaker, gateway)
- Checklist + discussion questions
