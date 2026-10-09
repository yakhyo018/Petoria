# Next Steps

Priority order: 1 = first.

## Backend Cleanup

| # | Task | Notes |
| --- | --- | --- |
| 1 | Seed the `/Petoria` DB: admin account, a few agents, sample products for every `ProductType`/`ProductSpecies` | DB is empty |
| 2 | Confirm with product requirements: `productGender` is NN with only `MALE`/`FEMALE` (how to handle food/toys/accessories?), `ProductLocation` (Korean cities) | `AGENTS.md`, `DECISIONS.md` D7 |
| 3 | Decide `MemberType.AGENT` → `SELLER` (also `getAgents`, `getAgentProducts`, `batchTopAgents`) | Optional, breaking |
| 4 | Update the ERD: `notifications.propertyId` → `productId`, reference names `properties_views`/`properties_likes` | Code already uses `productId` |
| 5 | Review the unique index `{productType, productLocation, productTitle, productPrice}` for a shop (same product in many listings?) | — |
| 6 | Reduce the 204 lint warnings by typing aggregate results and request objects | — |
| 7 | Rewrite `README.md` (NestJS template) with Petoria setup, env vars, scripts | — |
| 8 | Fix `.prettierrc` (contains an unsupported `extends` option, Prettier warns on every file) | — |
| 9 | Update external deploy scripts / Docker / PM2 to `dist/apps/petoria-*` | — |

## Frontend Migration

Steps 1–4 below were done on 2026-10-07 (see `COMPLETED_TASKS.md`).

| # | Task | Notes |
| --- | --- | --- |
| 1 | Replace raster assets that still show real estate: `public/img/apartmentMain.png`, `public/img/product/*` (detail fallback), community images. Homepage hero and page banners no longer use photos | Real pet-shop photos needed |
| 2 | Replace the placeholder type banners `public/img/banner/types/*.svg` with photos | — |
| 3 | Decide how `productGender` should work for FOOD/TOY/ACCESSORY (form always requires it because the backend field is NN) | Linked to Backend Cleanup #2 |
| 4 | QA with seeded data: product cards, detail page, add/edit product, likes, comments, admin products page, chat | Needs Backend Cleanup #1 (seed) |
| 5 | Homepage "Events" section still shows Korean city festivals; replace with pet events or remove | Optional |
| 6 | Rewrite `README.md` (Next.js template) for Petoria-next | — |

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
| 2 | Export the final ERD image into `docs/ai/` | — |
| 3 | Add a GraphQL operations reference with example queries for the frontend team | — |
