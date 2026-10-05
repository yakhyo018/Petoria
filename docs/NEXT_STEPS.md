# Next Steps

Priority order: 1 = first.

## Backend Cleanup

| # | Task | Notes |
| --- | --- | --- |
| 1 | Decide the Mongo database name (`/Nestar` vs `/Petoria`) | `DECISIONS.md` D5 |
| 2 | Fix the lint setup: install `typescript-eslint`, `@eslint/js`, `globals`, upgrade eslint to v9 (flat config), or revert to `.eslintrc.js` | Pre-existing failure |
| 3 | Rewrite `README.md` (currently the NestJS template) with a Petoria description, setup, env vars and scripts | — |
| 4 | Finalize the Product domain spec: `productGender` and `productLocation` values, `AGENT` → `SELLER`?, collection strategy | `DECISIONS.md` D7 |
| 5 | Domain Migration: `property` component → `product` (module, resolver, service, DTOs, enums, schema) | Breaking change |
| 6 | Update related references: `LikeGroup`/`ViewGroup`/`NotificationGroup.PROPERTY`, `Member.memberProperties`, `Notification.propertyId`, `config.ts` sort/options lists | — |
| 7 | Batch: `batchTopProperties` → `batchTopProducts`, constants in `ib/config.ts`, ranking formula | — |
| 8 | Data migration script `properties` → `products` (field mapping in `BACKEND_MIGRATION.md`) | Needs backup first |
| 9 | Update external deploy scripts / Docker / PM2 to `dist/apps/petoria-*` | — |

## Frontend Migration

| # | Task | Notes |
| --- | --- | --- |
| 1 | Create a `modification` branch and do the safe rename (`package.json`, `_document.tsx`, layouts, Footer, empty-state texts) | Can run in parallel with backend step 4 |
| 2 | UI terminology relabel through i18n | `FRONTEND_MIGRATION.md` |
| 3 | GraphQL document rename after backend step 5 | — |
| 4 | Page and component renames and filters redesign | — |

## Testing

| # | Task | Notes |
| --- | --- | --- |
| 1 | Smoke test: `npm run start:dev` and `npm run start:dev:batch` against the dev DB, open the GraphQL playground, run `getProperties`, `login` | Not done yet |
| 2 | WebSocket chat connect/message test | — |
| 3 | Fix `test/app.e2e-spec.ts` expectations (`'Hello World!'` vs the actual welcome string) | Pre-existing |
| 4 | Add e2e tests for the Product resolver after the Domain Migration | — |
| 5 | Verify the data migration on a copy of the database | — |

## Documentation

| # | Task | Notes |
| --- | --- | --- |
| 1 | Keep `COMPLETED_TASKS.md` and `NEXT_STEPS.md` updated after each session | — |
| 2 | Export the final ERD (`petoria.dmm`) and add the image to `docs/` | — |
| 3 | Document the final GraphQL schema (Product) | After step 5 |
| 4 | Add the new prompts to `PROMPTS.md` | — |
