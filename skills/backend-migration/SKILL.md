---
name: backend-migration
description: Continue the Nestar to Petoria backend migration while preserving the current NestJS architecture. Use when renaming, removing or adding backend domain concepts (Property → Product leftovers, Agent/Seller, enums, collections, batch jobs) or when updating the migration docs in docs/ai.
---

# Petoria Backend Migration

## Before Editing

1. Read `AGENTS.md`, then `docs/ai/BACKEND_MIGRATION.md`, `docs/ai/DECISIONS.md`, `docs/ai/COMPLETED_TASKS.md`, `docs/ai/NEXT_STEPS.md`.
2. Work on the `modification` branch (see `DECISIONS.md` D8). Check `git status` is clean or understood.
3. Pick the task from `NEXT_STEPS.md` and state the plan (files, renames, breaking changes) before changing code.

## Current State (keep in sync with docs/ai)

- Phase 1 (identity rename Nestar → Petoria) is done.
- Phase 2 (`Property` → `Product` domain, ERD-based) is done: `components/product`, `libs/dto/product`, `libs/enums/product.enum.ts`, `schemas/Product.model.ts`, collection `products`.
- Database is `/Petoria` (new, empty). No legacy data migration is required.
- `MemberType.USER | AGENT | ADMIN` are unchanged. Products are owned by `AGENT` members.

## Rules

- Follow the existing module → resolver → service pattern with DI. DTOs, enums and types go in `apps/petoria-api/src/libs`, and Mongoose schemas in `apps/petoria-api/src/schemas`.
- `petoria-batch` imports schemas/DTOs/enums from `../../petoria-api/src/...`. Update both apps together.
- Rename with `git mv` so history is kept. Never delete and re-create a file just to rename it.
- Never reintroduce `property*` names or real-estate fields (address, square, beds, rooms, barter, rent, constructedAt).
- A rename must cover every layer in one change: enum, schema, ObjectType DTO, Input/Update/Inquiry DTOs, `libs/config.ts` sort lists and lookups, services (`$lookup from`, `targetKey` strings in `*StatsEditor`), resolvers, group enums (`LikeGroup`, `ViewGroup`, `CommentGroup`, `NotificationGroup`), `Member` counters, `Notification` refs, batch jobs and constants.
- String keys are not type-checked (`targetKey: 'memberProducts'`, `$lookup from: 'products'`, `availableProductSorts`). Grep for them explicitly.
- GraphQL renames are breaking for Petoria-next. Record them in `docs/ai/BACKEND_MIGRATION.md` (GraphQL Changes) and `docs/ai/FRONTEND_MIGRATION.md`.

## Leftover Sweep

```bash
grep -rniE "propert|nestar|apartment|villa|beds|rooms|square|barter|rent\b|constructedAt" apps --include=*.ts
```

The expected result is no matches.

## Validation

```bash
npx tsc -p apps/petoria-api/tsconfig.app.json --noEmit
npx tsc -p apps/petoria-batch/tsconfig.app.json --noEmit
npm run build
npx eslint "apps/**/*.ts"
```

- Use `npx eslint` without `--fix`. `npm run lint` rewrites files.
- For a runtime check, port 3007 may be taken by another local server. Boot on a free port with `PORT_API=3017 node dist/apps/petoria-api/main`, then introspect `/graphql` (`__type(name: "Product")`, query and mutation field names) and stop the process.

## Finish

- Update `docs/ai/COMPLETED_TASKS.md` (files changed and the validation table) and `docs/ai/NEXT_STEPS.md`. Add a decision to `docs/ai/DECISIONS.md` if one was made.
- Commit with the project style, for example `feat: ...` or `fix: ...`.
