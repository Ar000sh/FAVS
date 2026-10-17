# 03 – Tech Stack: Next.js + Spring Boot

**Module:** FAVS – Fortgeschrittene Aspekte verteilter Systeme (Hochschule Hannover, Hans Grönniger), WS 26/27
**Source:** `skripte/03.TechStack.pdf` (66 slides)

> (note:) These notes come from the PDF's text extraction. The page images could not be rendered (no PDF renderer was available), so the content of pure screenshot/diagram slides (2, 24, 29, 35, 40, 45, 51, 62, 64, 66) is described only as far as their text shows. Check those slides in the PDF yourself.
> (note:) Slide numbers follow PDF page order. They match the "Seite N" footers that appear on slides 13, 16, 19, 26, 27 and 39–66.

---

## 0. Big picture / what this lecture covers

The deck has three parts, one for each layer of the course tech stack:

| Part | Slides | Topic |
|---|---|---|
| 1 | 1–10 | Why React / why Next.js (client-side architecture, SPA, Virtual DOM) |
| 2 | 11–21 | React basics (components, JSX, props, state, hooks, MVC classification) |
| 3 | 22–37 | Next.js (setup, project structure, Tailwind, routing, API routes, SSR/CSR/SSG) |
| 4 | 38–66 | Spring Framework + Spring Boot (modules, beans/DI, Maven, Spring MVC + Mustache, REST + JPA + H2) |

**Stack named on the title slide (slide 1): "Next.js + Spring Boot".**
(note:) This suggests a frontend in Next.js/React talking over REST/JSON to a backend in Spring Boot, i.e. the client-side architecture from slide 2.

**Not in this deck:** ShareWise, Docker/containers, Kubernetes, cloud services, message brokers, CI/CD, project milestones or deliverables. The words "microservices" and "messaging" come up only in passing (slides 42, 43, 47). See section 6.

---

## 1. Client-side architecture and SPAs

### Reminder: Client-Side Architecture (slide 2)
- The **web server** holds web pages with static HTML code and JavaScript code.
- The **web client** (browser) builds the complete HTML page:
  - it runs the JavaScript and loads data (usually **JSON**) from the backend (usually **REST**)
  - it inserts the business data into the HTML page using JavaScript.
- The **application server** offers a **REST interface** for the web client.
- (note:) The slide likely has a diagram (browser ↔ web server, browser ↔ application server/REST) that the extraction does not capture.

### Single-page applications (slide 3)
- **Traditional web:** a set of linked web pages. Navigating loads pages one at a time from the web server.
  - Problems: pages can take a long time to load, users wait, and **state must be preserved** when another page is loaded.
- **SPA:**
  - the web server delivers **only one web page**
  - the app shows **different views** on that page
  - **data is stored in the browser**, and needed resources are **reloaded asynchronously**.

---

## 2. React: motivation and concepts

### Motivation for React (slide 4)
- In 2010–2012, complex web apps were hard to build with **jQuery/DOM manipulation**. Maintenance and performance suffered.
- **Facebook** hit the limits of dynamic pages (e.g. the constantly updating News Feed). A change in one place often broke code elsewhere.
- **Goal:** keep UI complexity manageable by splitting the app into **many small, independent components**.
- Components should encourage **reusability** and **reduce side effects**.

### Problem: manual DOM manipulation (slide 5)
- **Imperative updates:** the view had to be updated by hand, e.g. `document.getElementById(...).innerText = ...`.
- With several pieces of data, this code becomes error-prone and hard to maintain. Developers must keep UI and data consistent themselves.
- Example: jQuery code that updates the DOM after an event gets hard to follow as the app grows.
- **MVC problem:** controller logic that manipulates the DOM directly breaks the separation of presentation and logic, which leads to "spaghetti code".

### React's solution: declarative UI and Virtual DOM (slides 6–7)
- **Declarative rendering:** you describe **what** the UI should look like for a given state, not **how** to update the DOM. React updates the view when data changes.
- **Virtual DOM:** a lightweight **in-memory representation of the DOM**. When state changes, React recalculates a virtual DOM tree and it replaces the previous one.
- An efficient **diff algorithm** applies only the **minimum necessary real DOM changes**. This gives smoother updates, better performance and less direct DOM manipulation.
- **Components:** the UI is built from reusable components. Each one encapsulates the presentation and update logic for part of the UI.
- **One-way data flow:** data flows top-down, which makes changes easier to track than complex **two-way binding**. (note:) Two-way binding is the Angular approach.

### React ecosystem: tools and libraries (slide 8)
- React itself is only the **basic UI library**. A full app also needs a build system, routing, state management, etc.
- **Bundlers/compilers:** Webpack, Vite. **Transpiler:** Babel (JSX/ES6 → ES5).
- **Create React App (CRA):** long the standard way to set up a React SPA. It configures the build and dev server but targets **purely client-side SPAs**.
- Other libraries:
  - **React Router** for routing
  - **Redux** or the **Context API** for complex state
  - **Jest / React Testing Library** for testing.
- **Downside of not using a framework:** you decide many things yourself (folder structure, code splitting, SEO, SSR), which overwhelms beginners. This is where **Next.js** comes in.

### Components in React (slides 12–13)
- Components are the **building blocks** of every React app. Each one encapsulates part of the UI and its logic.
- A component is a **function or a class**. Today it is mostly **function components with hooks**. It receives **inputs (props)** and **returns a rendering (JSX elements)**.
- Components split the UI into **independent, reusable parts** that can be developed in isolation, which helps maintainability.

**First component: person data (static for now, "to be fetched from a web service later") (slide 13)**
```jsx
const persons = [
  {
    "id": 1,
    "firstName": "Max",
    "lastName": "Muster",
    "position": "CTO"
  },
  ...
];

function List() {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        {persons.map((person) => (
          <tr key={person.id}>
            <td>{person.id}</td>
            <td>{person.firstName}</td>
            <td>{person.lastName}</td>
            <td>{person.position}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
export default List;
```
(note:) The header says "Email", but the cell shows `position`. That mismatch is on the slide. Slide 16 fixes the header to "Position". `key={person.id}` is needed for list items so the diff algorithm can match them.

### JSX: JavaScript XML (slide 14)
- A syntax extension for JS that looks like HTML/XML, e.g. `<Welcome name="Sara" />`.
- **Purpose:** define the UI structure declaratively inside JS instead of using strings or DOM APIs. This is easier to read and keeps markup and logic close together.
- **Under the hood:** the build (**Babel**) transpiles JSX into plain JS, e.g. `React.createElement` calls.
- Curly braces `{ }` embed JS expressions:
```jsx
const myElement = <h1>React is {5 + 5} times better with JSX</h1>;
```

### Props (properties) (slide 15)
- Information flows **from parent to child**.
- Props are the component's **input parameters**, passed by the parent like function arguments.
- Props are **read-only**. A component must not modify its props.
- Examples: text, numbers, callback functions, complex objects. In `<Button label="Save" onClick={...} />`, `label` and `onClick` are props.
- **Callback functions passed as props** let information flow **from child to parent**.

### Props: example (slide 16)
```jsx
// PersonsList.js
import PersonListItem from "./PersonListItem";

export default function PersonsList({ persons }) {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Position</th>
        </tr>
      </thead>
      <tbody>
        {persons.map((person) => (
          <PersonListItem key={person.id} person={person} />
        ))}
      </tbody>
    </table>
  );
}
```
```jsx
// PersonListItem.js
export default function PersonListItem({ person }) {
  return (
    <tr>
      <td>{person.id}</td>
      <td>{person.firstName}</td>
      <td>{person.lastName}</td>
      <td>{person.position}</td>
    </tr>
  );
}
```

### Client-side state (slides 17–18)
- **State** is a component's internal, **mutable** data. Props come from outside; state is managed inside the component.
- A state change triggers a **re-render** of the component and its children, so the UI always shows the current state.
- In function components, state is managed with **hooks**:
  `const [count, setCount] = useState(0);` creates a state value `count` with initial value `0` and an update function.
- A component can hold **several state values** (several `useState` calls or a complex state object). Keep state **minimal**: only what rendering and interaction need.
- **Lifecycle:** like Angular's lifecycle hooks (`ngOnInit`, etc.), React lets you react to state and prop changes, e.g. with the **`useEffect`** hook.

### State: example – fetching persons from an API (slide 19)
```jsx
import { useEffect, useState } from "react";
import PersonsList from "./components/PersonsList";

export default function Home() {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPersons = async () => {
      try {
        const response = await fetch("/api/persons");
        if (!response.ok) {
          throw new Error("Failed to load persons.");
        }
        const data = await response.json();
        setPersons(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPersons();
  }, []);

  return (
    <main>
      <h1>People</h1>
      {loading && <p>Loading people...</p>}
      {error && !loading && (
        <p> {error} </p>
      )}
      {!loading && !error && (
        <div>
          <PersonsList persons={persons} />
        </div>
      )}
    </main>
  );
}
```
(note:) The empty dependency array `[]` makes the effect run once after the first render. This page uses state and hooks, so in the Next.js App Router it needs `"use client"` (see slide 35). `/api/persons` is a Next.js API route (slides 10, 31).

### React and MVC (slides 20–21)
- React is **not a classic MVC framework**. It mainly provides the **view layer**. There is no prescribed controller or model. People call it "**the V in MVC**".
- A component tree can still form an MVC-like pattern:
  - model data from external sources (API, state)
  - the component renders it (view)
  - event handlers handle user events (controller logic).
- **Component-based paradigm (slide 21):** one component manages its state (Model), renders the UI (View) and sometimes handles events (Controller) as a single unit. This gives **high cohesion**.
- **Large apps:** structuring patterns such as **Flux/Redux** add a unidirectional data flow:
  - the state is a central store (model)
  - actions are the controller logic
  - React components are the view.
- React does **not enforce a pattern**. It can sit inside MVC-like layers or custom architectures.
- **Conclusion:** React is lean and flexible, deliberately "just" the view library. The developer sets the architecture principles.

---

## 3. Next.js

### Next.js overview (slide 9)
- A **React-based framework** developed by **Vercel** that provides many necessary features out of the box.
- **Purpose:** simplify building production web apps with React, including **routing, server-side rendering, API endpoints and build optimizations**.
- **Philosophy: "Zero-Config".** Proven defaults make code splitting, hot module replacement and routing work without extra configuration.
- **Compared with Angular:** React alone is "just a library". Next.js + React is closer to a full framework like Angular, with structure similar to Angular's CLI + modules, but **more flexible and less prescriptive**.

### Key features (slide 10)
- **File-based router:** pages are defined by files and directories (slide example: `app/index.tsx` for the home page). No manual route setup.
  (note:) In the current App Router the home page file is `app/page.js`/`page.tsx`, as slides 24 and 28 say.
- **SSR and SSG:** pages can be rendered on the server (for SEO and performance). You choose **per page** between precompiling at build time and rendering on request.
- **API routes:** backend logic under `app/api/*`. This makes Next.js a **full-stack framework**: simple REST endpoints without a separate server, often used in the **BFF (Backend-for-Frontend) pattern**.
- **Dev tools:** built-in dev server (`next dev`), hot reloading, built-in **TypeScript** support.

### Setting up a new Next.js project (slide 23)
```bash
npx create-next-app@latest my-react-app --js
```
(note:) The extraction shows the flag as "�js". It is most likely `--js` (JavaScript template).
- This uses the defaults. You can also run it **without flags**, and the CLI wizard asks for the details.
- **CLI prompts:**
  - project name
  - **TypeScript = Yes**
  - **ESLint = Yes**
  - CSS framework (e.g. **Tailwind**), optional
  - **use `src/` directory = Yes**
  - **App Router (recommended) = Yes**

  The options can vary slightly between Next.js versions.
- The CLI creates all files and installs dependencies (React, Next, Webpack, etc.).
- Start it:
```bash
cd my-react-app
npm run dev
```
- The terminal shows the local URL (default **http://localhost:3000**).
- **First test:** open `localhost:3000`. The default Next.js welcome page confirms the setup worked.

### Project structure (slide 24)
(Slide shows a VS Code Explorer screenshot.)
- `app/` (or `pages/` for the legacy router): page components, e.g.
  - `app/page.js`: home page component
  - `layout.js`: root layout, **must contain the `<html>` tag**
  - `globals.css`: global CSS styles
- `public/`: static files (e.g. `favicon.ico`, possibly an images directory).
- `package.json`: dependencies (React, react-dom, next) and scripts (`dev`, `build`, `start`, ...).
- Other config the CLI predefines: `jsconfig.json` (JS settings), `.eslintrc.json` (lint rules), etc.
- Unlike Angular, there is **no module structure**. Next.js is organized mainly **by pages**, and you can arrange component folders however you like.

### Display Person Data – demo (slide 25)
- A live demo of the components already shown: `PersonsList`, `PersonListItem`, `Home` (slides 13–19).

### Styling with Tailwind (slides 26–27)
- **Tailwind** is a CSS framework for consistent styling. You style components with **predefined utility classes written directly in the markup**.
```jsx
<main className="mx-auto flex w-full max-w-4xl flex-1 flex-col p-6 md:p-10">
```
| Class | Meaning (from slide) |
|---|---|
| `mx-auto` | centers the page container horizontally |
| `flex` | makes `main` a flex container |
| `w-full` | uses the full available width |
| `max-w-4xl` | limits the width so content doesn't get too wide |
| `flex-1` | lets the area expand to fill the remaining vertical space in the parent layout |
| `flex-col` | stacks child elements vertically |
| `p-6` | base padding on all sides |
| `md:p-10` | more padding on medium and larger screens |

- This **contradicts many traditional best practices** (it resembles inline styles).
- Possible advantages:
  - **speed:** no class names or selectors to define yourself
  - the **impact of changes stays local**
  - it supports a **component-based approach**
  - the **CSS does not keep growing**
- More info: https://tailwindcss.com/
- Tailwind is **not required**. Other CSS frameworks or fully custom styles also work.

### Routing: file-system-based (slide 28)
- Next.js has **built-in routing (App Router)** based on the file system. Each directory in the root folder becomes a route (URL). No extra router library is needed.
- `/page.js` → home page `/`; `aboutus/page.js` → `/aboutus`.
- It is convention-based: create or name folders to define pages and routes.
- **"Folder name = URL."**

### Static routes (slide 29)
- To add a fixed-name page, create a folder and a file inside `app`. The page is then available at that URL automatically.
- Example: `impressum/page.js` → `/impressum`.

### Navigation between pages (slide 30)
- Use the `<Link>` component from `'next/link'`. It loads the new page in the background and switches to it seamlessly, for a smoother UX.
- A plain `<a href>` also works but **reloads the whole page**.
```jsx
<p>
  <Link href="/">
    Back to the home page (without reloading)
  </Link>
</p>
<p>
  <a href="/">
    Back to the home page (with reload)
  </a>
</p>
```
(note:) You need `import Link from "next/link";`.

### Dynamic routes / API route handler (slide 31)
- Dynamic routes are pages or endpoints with **variable URL parameters**, written with **square brackets** in the path.
- `/api/persons/[id]/route.js` defines a dynamic route. A **GET** to `/api/persons/3` runs the matching function in `route.js`. The bracket name (`id`) is passed to the function as a parameter.
```js
export async function GET(_request, { params }) {
  try {
    const { id: rawId } = await params;
    const id = Number(rawId);

    if (!Number.isInteger(id)) {
      return Response.json({ error: "Invalid id." },
                           { status: 400 });
    }

    const persons = await loadPersons();
    const person = persons.find(
        (person) => Number(person.id) === id);

    if (!person) {
      return Response.json(
          { error: "Person not found." }, { status: 404 });
    }
    return Response.json(person);
  } catch {
    return Response.json(
        { error: "Could not read data." }, { status: 500 });
  }
}
```
(note:)
- Status codes used: **400** for an invalid id, **404** when not found, **500** for a read error.
- `params` is awaited because it is a Promise in recent Next.js versions.
- `loadPersons()` is a helper whose definition is not shown, presumably reading a JSON file.

### Pre-rendering (slide 32)
- Unlike classic client-only SPAs, Next.js pages can arrive as **fully rendered HTML** ("cf. PHP"). There are two strategies:
  - **SSR:** the **page** (not the whole site) is rendered on the server **on every request**.
  - **SSG:** the **page** is generated **once in advance** (e.g. at build time) as static HTML and reused for later requests.
- Both are supported, and a **hybrid** too. You choose **per page**.
- This combines the strengths of classic multi-page server apps with React's.
- In a classic React SPA the browser first sees a **blank page** and then builds the UI in JS. Pre-rendered HTML gives **faster loading and better SEO**.

### Server-Side Rendering (SSR) (slide 33)
- The server builds the full HTML anew for each request (possibly after DB/API queries) and sends it.
- The browser shows ready-made HTML right away, while React **"hydrates"** in the background, i.e. makes the server-delivered page interactive.
- Result: fast initial load with **current data**, and search engines see the complete content.
- Best for **highly dynamic or personalized** content that must be current on every request.
- Downside: the server handles every request, so **time-to-first-byte (TTFB)** goes up slightly.

### SSR in Next.js (slide 34)
- SSR needs no explicit enabling. **Every page and component is SSR by default** (rendered on the server).
- Person data can also be loaded via SSR. The **API call is replaced by a local function call on the server**.
```jsx
import { loadNormalizedPersons } from "../lib/persons-store";
import PersonsList from "./components/PersonsList";

export default async function SsrPersonsPage() {
  let persons = [];
  try {
    persons = await loadNormalizedPersons();
  } catch {
    error = "Could not load persons data.";
  }
  return (
    <main>
      <h1>Persons</h1>
      <div>
        <PersonsList persons={persons} />
      </div>
    </main>
  );
}
```
(note:)
- `error` is never declared in this snippet as shown. A `let error = "";` is presumably left out.
- The page component is `async`. That is possible because it is a **React Server Component**.

### CSR in Next.js (slide 35)
- To render a page or component **explicitly on the client**, add the directive **`"use client"`** (at the top of the file).
- Some components cannot render on the server, e.g. those that keep **React state** on the client side.
- The slide shows the **error message you get when `"use client"` is missing** (screenshot).
- A CSR component is still **SSR-rendered first**, then **"hydrated" on the client**.

### Outlook: Static Site Generation (SSG) (slide 36)
- Pages are generated as static HTML **at build time** and stored on the server or a **CDN**. They are served immediately without server-side rendering.
  - This gives very fast delivery and low server load.
- Ideal for content that **rarely changes** or changes only on deployment (blog, docs, marketing pages).
- **Excellent SEO** and optimal load times. Files can be **cached worldwide via a CDN**.
- **Downside:** when content changes, the site must be **rebuilt or redeployed**, otherwise users see stale content. So SSG suits fairly static content, not frequently updated data.

### SSR vs. SSG vs. CSR quick comparison (note: own summary of slides 32–36)
| | When is HTML produced | Good for | Downside |
|---|---|---|---|
| SSR | per request on server | dynamic/personalized, SEO | higher TTFB, server load |
| SSG | once at build | rarely changing content, CDN | stale until rebuild |
| CSR (`"use client"`) | prerendered + hydrated, then client JS | interactive state (useState/useEffect) | data loads after hydration |

### Summary (slide 37)
- React is the **component-based UI library** that grew out of the need to handle complex UIs better.
- Next.js extends React with key features (**routing, SSR, ...**) so you can build working projects quickly.

---

## 4. Spring Framework and Spring Boot

### What is the Spring Framework? (slide 39)
- An **application framework for the Java platform**, developed by **VMware and Pivotal Software Inc.**
- Commonly used as a supplement to or **replacement for Enterprise Java Beans (EJB)**.
- Open source:
  - Spring Framework: https://github.com/spring-projects/spring-framework
  - other Spring projects: https://github.com/spring-projects
- **Main goals:** simplify Java Enterprise development and promote good programming practices.

### Core architecture / modules of Spring (slides 40–44)
(Slide 40 is a module diagram, not visible in the text.)

| Group | Module | What it does (slides) |
|---|---|---|
| Core Container | **Spring Core + Spring Beans** | basic functionality: **Inversion of Control (IoC)** and **Dependency Injection (DI)**; **BeanFactory** implements the **Factory pattern** (41) |
| | **Spring Context** | builds on spring-core/spring-beans; "framework-style" object access (similar to a **JNDI registry**); supports Java EE features like **EJB, JMX** (41) |
| | **Spring SpEL** | expression language for querying/manipulating object graphs at runtime (41) |
| AOP etc. | **Spring AOP** | enables **interceptors** ("An interceptor extends a framework or middleware without modifying it itself.") (42) |
| | **Spring Aspects** | integration with **AspectJ** (42) |
| | **Spring Instrument** | instruments Java classes (modifies **bytecode at runtime**); ClassLoader implementations for app servers (e.g. `spring-instrument-tomcat`) (42) |
| | **Spring Messaging** | support for **STOMP** (Simple Text Oriented Messaging Protocol) (42) |
| Data Access/Integration | **Spring JDBC** | JDBC abstraction layer (43) |
| | **Spring ORM** | integration layers for ORM APIs: **JPA, JDO, Hibernate, iBatis** (43) |
| | **Spring OXM** | object-to-XML mapping abstraction: **JAXB, Castor, XMLBeans, JiBX, XStream** (43) |
| | **Spring JMS** | Java Messaging Service: sending and receiving messages (43) |
| | **Spring Transactions** | programmatic and declarative **transaction management** for classes implementing specific interfaces (43) |
| Web | **Spring Web** | basic functionality for web apps (44) |
| | **Spring Web MVC (Servlet)** | **MVC pattern** implementation and **REST web services** (44) |
| | **Spring WebSocket** | WebSocket-based **bidirectional** client–server communication (44) |
| | **Spring Portlet** | MVC implementation for portlet environments, mirrors Web Servlet (44) |
| Test | **Spring Test** | component and integration testing of Spring modules with **JUnit or TestNG** (44) |

### Spring projects (slide 45)
- Many Spring projects exist for specific problems. See https://spring.io/projects (slide shows an overview graphic).

### Spring Boot (slides 46–47)
- Quote: "...makes it easy to create **stand-alone, production-grade** Spring-based applications that you can **'just run'**. We take a strong stance of the Spring platform and third-party libraries so you can get started with minimal hassle. Most Spring Boot applications require **minimal Spring configuration**."
- Open source: https://github.com/spring-projects/spring-boot. **Phil Webb** is a contributor (https://github.com/philwebb).
- Offers a **"convention-over-configuration"** approach for production-ready standalone Spring apps.
- A **popular choice for microservices**.
- Advantages:
  - Spring apps that are easy to understand and develop
  - higher productivity
  - shorter development time.

### Build systems (slide 48)
- Spring Boot uses build systems to **automate as many build steps as possible**: compiling, testing, packaging and distributing the software.
- Examples: **Apache Maven**, **Gradle**.

### Spring MVC (slide 49)
- A part of the Spring Framework for building web apps, following **MVC**:
  - **Model:** data models (Java objects)
  - **View:** a template that generates the HTML page
  - **Controller:** responds to HTTP requests from the browser.

### Spring-managed beans container (slide 50)
(Source cited on slide: *Spring Boot 3 and Spring Framework 6*, Christian Ullenboom, 2023)
- When a Spring app starts, a **container for beans** is initialized. **Beans ≈ components.**
- The container:
  - **manages beans** (add, query, delete)
  - **configures dependencies (references) between beans automatically**.
- Beans are added **declaratively (annotations)** or **registered manually**.
- Beans reference each other through **injection**.
- Stereotype annotations:
  - `@Component`: any component
  - `@Repository`: data storage
  - `@Service`: application logic
  - `@Controller`: requests from the front end

### Spring Boot project setup (slides 51–53)
- Use **Spring Initializr**, either **in the IDE (IntelliJ)** or on the web at **https://start.spring.io**.
- Choose the initial dependencies (web, databases, etc.).
- **Add the Lombok annotation framework.**
- The generated project is **ready to run immediately**.
- The Maven target **`package`** builds a **JAR file**. (note:) e.g. `mvn package` / `./mvnw package`.
- With a dependency on **Spring Web**, an **embedded web server starts automatically**.
- **Directory structure / files (slide 53):**
  - `pom.xml`:
    - the Project Object Model (Maven configuration)
    - dependency definitions
    - there is also a **parent POM**
  - `application.properties`:
    - the Spring application configuration
    - strictly speaking, for the **default profile**
    - lives in the `resources` folder, which holds other non-source artifacts
  - Java packages with the source code for the app and the tests
  - `HELP.md`: documentation links that depend on the configured dependencies

### pom.xml excerpt (slide 54) – note the versions
```xml
<?xml version="1.0" encoding="UTF-8"?>
<modelVersion>4.0.0</modelVersion>
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>4.0.6</version>
  <relativePath/> <!-- Look up parent from repository -->
</parent>
...
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mustache</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
  </dependency>
  <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <scope>annotationProcessor</scope>
  </dependency>
</dependencies>
...
```
- **Spring Boot version: 4.0.6** (parent `spring-boot-starter-parent`).
- Starters: **`spring-boot-starter-mustache`** (template engine), **`spring-boot-starter-webmvc`** (Spring MVC), **Lombok**.
- (note:) In Spring Boot 4 the web starter is named `spring-boot-starter-webmvc`; in Boot 3 it was `spring-boot-starter-web`.

### Spring MVC example: Controller (slide 55)
```java
@Controller
public class GreetingController {

    @GetMapping("/greeting")          // URL for the request
    public String greeting(Model model) {
        model.addAttribute("name", "World");   // extend the model
        return "greeting_template";           // template name used to generate the HTML page
    }
}
```

### Spring MVC example: View with Mustache (slide 56)
`greeting_template.html`:
```html
<html>
  <body>
    <p>Hello, {{name}}</p>
  </body>
</html>
```
- Templates contain **placeholders named after model attributes**. When the HTML is generated, they are replaced with the attribute values (here `name`).
- Mustache uses the **`.mustache`** extension by default. To use `.html`, configure:

`application.properties`
```properties
spring.mustache.suffix:.html
```
`application.yaml`
```yaml
spring:
  mustache:
    suffix: .html
```

### Spring MVC example: main application (slide 57)
```java
@SpringBootApplication
public class SpringMvCdemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringMvCdemoApplication.class, args);
    }
}
```

### REST with Spring Boot (slide 58)
- Spring MVC for REST structures the app into:
  - **Model:** data models (Java objects)
  - **View:**
    - application (client): generates the view with templates
    - REST: **converts the model to JSON**
  - **Controller:** responds to HTTP requests from the client
- Storage uses the **H2 in-memory database**, via the **Spring Boot Data JPA** dependency.
  (note:) In Initializr these are "Spring Data JPA" and "H2 Database". Neither appears in the pom excerpt on slide 54, which belongs to the Mustache demo.

### Model + standard repository (slide 59)
```java
@Entity                 // persistence object; requires an ID attribute
@Getter                 // Lombok annotation
@Setter
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;
    private Double price;
    private String author;
}

public interface BookRepository extends JpaRepository<Book, Long> {
}
// "Automatic persistence layer with methods such as save, delete, findBy, etc."
```

### REST controller: GET (slide 60)
```java
@RestController
public class BookController {

    @Autowired
    private BookRepository bookRepository;

    @GetMapping("/books")
    public List<Book> getBooks() {
        return bookRepository.findAll();      // list of books returned as JSON
    }

    @GetMapping("/books/{id}")
    public Book getBookById(@PathVariable Long id) {
        return bookRepository.findById(id).get();
    }
}
```
- The controller class is annotated with **`@RestController`**.
- The repository is injected. Slide comment: "preferably as a **constructor argument** these days", i.e. use constructor injection rather than field `@Autowired`.
- A resource's ID usually goes in the URL and is read with **`@PathVariable`**.

### REST controller: query parameter (slide 61)
```java
@RestController
public class BookController {

    @Autowired
    private BookRepository bookRepository;

    @GetMapping("/books")
    public List<Book> getBooks(@RequestParam Optional<String> author) {
        if (author.isPresent()) {
            return bookRepository.findByAuthor(author.get());
        }
        return bookRepository.findAll();
    }
    ...
```
- This alternative uses an **optional URL parameter** to search by author. **`@RequestParam` and `@PathVariable` can be combined.**
- (note:) For this to compile, `BookRepository` must declare the derived query method `List<Book> findByAuthor(String author);`. The slide doesn't show it.

### Retrieve all Book resources (GET) (slide 62)
- A screenshot of a GET request to `/books` and the JSON response. (note:) Probably a REST client or browser. Not visible in the extraction.

### Add resource (POST) (slides 63–64)
```java
@PostMapping("/books")
public Book addBook(@RequestBody Book book) {
    return bookRepository.save(book);
}
```
- `@PostMapping` means the method expects a POST request.
- The request body is read through a parameter annotated with **`@RequestBody`**.
- The **new object is returned** to the client.
- For new objects, the **`Location` header is usually set with the ID**. (note:) The slide code doesn't do this. With `ResponseEntity.created(uri)` it would.
- Slide 64 is a screenshot of the POST request.

### Delete resource (DELETE) (slides 65–66)
```java
@DeleteMapping("/books/{id}")
public Book deleteBook(@PathVariable Long id) {
    Book del = bookRepository.findById(id).get();
    bookRepository.deleteById(id);
    return del;
}
```
- `@DeleteMapping` means the method expects a DELETE request. The resource is identified by the `@PathVariable id`.
- If the resource exists, it is **deleted and returned**.
- (note:) The extraction shows the first line as `Delete Book = ...` with `return del;`. It must be `Book del = ...` as written above.
- (note:) `findById(id).get()` throws `NoSuchElementException` when the ID is unknown, which gives a 500. In real code you'd return 404 (compare the Next.js handler on slide 31).
- Slide 66 is a screenshot of the DELETE request.

### REST endpoint summary (note: own table from slides 60–66)
| Method | Path | Annotation(s) | Repository call |
|---|---|---|---|
| GET | `/books` | `@GetMapping` (+ optional `@RequestParam author`) | `findAll()` / `findByAuthor()` |
| GET | `/books/{id}` | `@GetMapping`, `@PathVariable` | `findById(id).get()` |
| POST | `/books` | `@PostMapping`, `@RequestBody` | `save(book)` |
| DELETE | `/books/{id}` | `@DeleteMapping`, `@PathVariable` | `findById` + `deleteById` |

---

## 5. Architecture and how it fits the course project

From the slides:
- **Frontend:** a Next.js (React) app. Pages and components are rendered by **SSR (default), CSR (`"use client"`) or SSG**. It fetches **JSON via REST** (`fetch("/api/persons")`).
- **Next.js API routes (`app/api/*`)** can serve as a lightweight backend or **BFF (Backend-for-Frontend)** (slide 10).
- **Backend:** Spring Boot with Spring MVC `@RestController`s, **Spring Data JPA** and the **H2 in-memory DB**. It is packaged as a **runnable JAR with an embedded web server** (slides 52, 58).
- **Spring Boot is "a popular choice for developing microservices"** (slide 47). This is the only microservices mention in the deck.
- Messaging-related Spring modules are listed but not demonstrated:
  - **Spring JMS**
  - **Spring Messaging (STOMP)**
  - **Spring WebSocket**
- **Containers, Kubernetes, cloud services, message brokers, CI/CD:** *not covered in this deck.*

(note:) The likely target architecture is browser → Next.js (SSR/CSR, possibly as BFF) → REST/JSON → Spring Boot service(s) → DB. This matches slide 2's client-side architecture. Check it against the project assignment in other decks.

---

## 6. ShareWise / project requirements

- **"ShareWise" does not appear anywhere in this deck.**
- **No project requirements, deliverables, milestones, deadlines or grading info** in this deck.
- The running demo examples here are:
  - a **Persons list** (Next.js: `id, firstName, lastName, position`, e.g. Max Muster, CTO)
  - a **Greeting** page (Spring MVC + Mustache)
  - a **Book** REST API (Spring Boot: `id, title, price, author`).

---

## 7. Likely relevant for upcoming exercises/presentations

(note:) This section is my own judgement, based on what the slides demo in detail.

1. **Set up and run a Next.js app** with `create-next-app` (TypeScript/ESLint/Tailwind/`src/`/App Router). Know the `app/` structure, `page.js`, `layout.js`, `globals.css`, `public/`.
2. **React fundamentals:**
   - components, JSX, props (read-only; callbacks for child→parent)
   - `useState`/`useEffect`, the loading/error/data pattern (slide 19)
   - `key` in lists
3. **Next.js routing:**
   - folder = URL, static routes (`impressum/page.js`)
   - `<Link>` vs `<a>`
   - **dynamic API routes `api/persons/[id]/route.js`** with HTTP status codes 400/404/500
4. **Rendering strategies:** SSR vs CSR (`"use client"`, hydration) vs SSG, with pros and cons (TTFB, SEO, CDN, staleness). This is a classic exam/discussion topic.
5. **React architecture:** "V in MVC", component-based paradigm, Flux/Redux, one-way data flow vs two-way binding (Angular).
6. **Spring concepts:**
   - IoC/DI, bean container, stereotype annotations (`@Component/@Repository/@Service/@Controller`)
   - module overview (Core, AOP, Data Access, Web, Test)
   - convention over configuration
7. **Spring Boot REST CRUD:**
   - `@RestController`, `@GetMapping/@PostMapping/@DeleteMapping`
   - `@PathVariable`, `@RequestParam`, `@RequestBody`
   - `@Entity` + `JpaRepository`, H2, Lombok (`@Getter/@Setter`)
   - constructor injection, `Location` header on POST
8. **Spring MVC + Mustache:** `@Controller` returning a template name, `Model.addAttribute`, `spring.mustache.suffix`.
9. **Versions:** Spring Boot **4.0.6**, starter `spring-boot-starter-webmvc`; Next.js via `create-next-app@latest`; dev server on **localhost:3000**.

### Setup to-dos for students
- [ ] Install **Node.js + npm** (needed for `npx`/`npm run dev`). (note:) The version is not given on the slides.
- [ ] Run `npx create-next-app@latest my-react-app` and answer the wizard: TypeScript Yes, ESLint Yes, Tailwind (optional), `src/` Yes, App Router Yes.
- [ ] `cd my-react-app && npm run dev`, then check the welcome page at http://localhost:3000.
- [ ] Rebuild the Persons demo:
  - `PersonsList`, `PersonListItem`, `Home` with `useEffect` fetch
  - an `app/api/persons/route.js` plus a dynamic `app/api/persons/[id]/route.js`
  - try `"use client"` and see the error without it
- [ ] Add an `impressum/page.js` static route and `<Link>` navigation.
- [ ] Install a **JDK** and an IDE (**IntelliJ** is used on the slides). (note:) The JDK version is not stated. Spring Boot 4 needs Java 17+.
- [ ] Create a Spring Boot project via **Spring Initializr** (IntelliJ or https://start.spring.io) with **Maven**, Spring Boot **4.0.x**, and dependencies:
  - **Spring Web (webmvc)**
  - **Mustache**
  - **Lombok**
  - **Spring Data JPA**
  - **H2**
- [ ] Enable **annotation processing** for Lombok in the IDE. (note:) Not on the slides, but usually required in IntelliJ.
- [ ] Build the Greeting demo (`@Controller`, Mustache template, `spring.mustache.suffix:.html`).
- [ ] Build the Book REST API (`@Entity Book`, `BookRepository` + `findByAuthor`, `BookController` GET/POST/DELETE). Test with a REST client and package with Maven `package` → run the JAR.
- [ ] Optional: connect the Next.js frontend to the Spring Boot REST backend (fetch JSON). (note:) This is not shown explicitly but follows from the "Next.js + Spring Boot" stack.
