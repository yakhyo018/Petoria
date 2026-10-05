# Next Steps

Priority order: 1 = first.

## Backend Cleanup

| # | Task | Notes |
| --- | --- | --- |
| 1 | Seed the `/Petoria` DB: admin account, a few agents, sample products for every `ProductType`/`ProductSpecies` | DB is empty |
| 2 | Confirm enum values with product requirements: `ProductGender` (MALE/FEMALE/UNISEX), `ProductLocation` (Korean cities) | `DECISIONS.md` D7 |
| 3 | Decide `MemberType.AGENT` → `SELLER` (also `getAgents`, `getAgentProducts`, `batchTopAgents`) | Optional, breaking |
| 4 | Update the ERD: `notifications.propertyId` → `productId`, reference names `properties_views`/`properties_likes` | Code already uses `productId` |
| 5 | Review the unique index `{productType, productLocation, productTitle, productPrice}` for a shop (same product in many listings?) | — |
| 6 | Reduce the 204 lint warnings by typing aggregate results and request objects | — |
| 7 | Rewrite `README.md` (NestJS template) with Petoria setup, env vars, scripts | — |
| 8 | Fix `.prettierrc` (contains an unsupported `extends` option, Prettier warns on every file) | — |
| 9 | Update external deploy scripts / Docker / PM2 to `dist/apps/petoria-*` | — |

## Frontend Migration

| # | Task | Notes |
| --- | --- | --- |
| 1 | Safe rename on the `modification` branch (`package.json`, `_document.tsx`, layouts, Footer, empty-state texts) | — |
| 2 | Rename GraphQL documents in `apollo/user/*`, `apollo/admin/*` to Product operations and fields | Required: the backend contract already changed |
| 3 | Rename pages/components (`property/*` → `product/*`) and replace filters (beds/rooms/square → species/gender) | `FRONTEND_MIGRATION.md` |
| 4 | UI terminology and assets | — |

## Testing

| # | Task | Notes |
| --- | --- | --- |
| 1 | Mutation flow in the GraphQL playground: `signup` (AGENT) → `createProduct` → `getProduct` → `likeTargetProduct` → `getFavorites`/`getVisited` → `updateProduct` (SOLD) → admin `removeProductByAdmin` | Checks `memberProducts`/`productLikes`/`productViews` counters |
| 2 | `createComment` with `commentGroup: PRODUCT` updates `productComments` | — |
| 3 | WebSocket chat connect/message test | — |
| 4 | Fix e2e specs (`'Hello World!'` expectations) and add Product resolver e2e tests | Pre-existing |
| 5 | Run batch jobs manually (`batchRollback`, `batchTopProducts`, `batchTopAgents`) against seeded data | — |

## Documentation

| # | Task | Notes |
| --- | --- | --- |
| 1 | Keep `COMPLETED_TASKS.md` / `NEXT_STEPS.md` updated each session | — |
| 2 | Export the final ERD image into `docs/` | — |
| 3 | Add a GraphQL operations reference with example queries for the frontend team | — |
