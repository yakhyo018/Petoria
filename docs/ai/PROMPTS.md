# Useful Prompts

## Prompts From This Session

### Set Up the New Project

```text
This is a new project named Petoria, migrated from Nestar. Study the screenshots.
First create two folders, Petoria and Petoria-next, by cloning the existing Nestar
and nestar-next projects, and connect them to new public git repos.
```

Use this when starting a fork or migration of an existing repo into a new project identity.

### Analyze the Current Backend

```text
Analyze current Nestar monorepo structure to transform existing NestJS Monorepo
Nestar platform into Petshop platform.
```

Use this when starting from an unknown backend state and you need a structural map before planning the domain migration.

### Plan a Safe Rename Layer

```text
Safe rename Layer (No Business logic change)
Rename all visible project/app identifiers from Nestar to Petoria. Do Not change
domain logic. Keep APIs and database collections unchanged. Update package
names, environment labels constants. Run lint and typecheck after refactoring.
Please make plan first!
```

Use this when the goal is branding/project identity migration only.

### Implement the Safe Rename Plan

```text
PLEASE IMPLEMENT THIS PLAN:
Rename visible project/app identity from Nestar to Petoria without changing
business/domain behavior. Keep GraphQL APIs, DTOs, schemas, Mongoose model
names, and database collections unchanged.
```

Use this after a complete plan exists and implementation is approved.

### Create Migration Documentation

```text
Create a new folder: docs
Inside it, generate: BACKEND_MIGRATION.md, DECISIONS.md, FRONTEND_MIGRATION.md,
COMPLETED_TASKS.md, NEXT_STEPS.md, PROMPTS.md.
Use everything completed and discussed in this session. Each file must summarize
the current Nestar → Petoria migration state. Do not change application source
code. Only create documentation files. Be precise and technical. Use markdown
tables where useful.
```

Use this at the end of every session to persist the context.

## Reusable Prompts for the Next Session

### Resume Context

```text
Read AGENTS.md and docs/ai/*.md in Petoria. Summarize the current migration state, open decisions,
and the top 3 tasks from NEXT_STEPS.md. Do not change code yet.
```

### Fix Lint Setup

```text
The lint script fails because eslint.config.mjs imports typescript-eslint, @eslint/js
and globals, which are not installed. Propose the minimal fix (deps vs config),
apply it, run lint, and report the remaining lint errors without auto-fixing
business code.
```

### Plan the Property → Product Domain Migration

```text
Using the target products schema in docs/ai/BACKEND_MIGRATION.md, plan the
Property → Product domain migration for petoria-api and petoria-batch:
module/resolver/service/DTO/enum/schema renames, GraphQL operation renames,
related references (LikeGroup, ViewGroup, NotificationGroup, memberProperties,
Notification.propertyId, batch jobs) and a MongoDB data migration script.
List breaking changes. Make plan first, do not implement.
```

### Implement the Domain Migration

```text
PLEASE IMPLEMENT THE APPROVED PRODUCT DOMAIN PLAN on the modification branch.
After each module: run tsc --noEmit for both apps and nest build.
Do not touch the frontend. Update docs/ai/COMPLETED_TASKS.md and docs/ai/NEXT_STEPS.md
at the end.
```

### Smoke Test Backend

```text
Start petoria-api and petoria-batch in dev mode against the dev database,
run getProperties/getProducts, login and a WebSocket message test, and report
results with logs. Do not change code.
```

### Frontend Safe Rename

```text
In Petoria-next, on a new modification branch, rename visible Nestar branding to
Petoria (package.json, _document.tsx, layouts, Footer, empty-state texts).
Do not change GraphQL documents, routes or components. Keep CHANGELOG.md as
history. Run build and lint after.
```
