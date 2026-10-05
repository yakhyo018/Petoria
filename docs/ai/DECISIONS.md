# Architectural Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D1 | New repositories cloned from Nestar with full git history | Accepted |
| D2 | Two-phase migration: Safe Rename Layer first, Domain Migration later | Accepted |
| D3 | Keep GraphQL API, DTOs, Mongoose models and collections unchanged in phase 1 | Accepted (phase 1 done) |
| D4 | Rename app folders with `git mv` | Accepted |
| D5 | Switch `.env` Mongo database name `/Nestar` → `/Petoria` | Accepted |
| D6 | Backend first, frontend after | Accepted |
| D7 | Domain model `Product` from the Petoria ERD | Accepted, implemented |
| D8 | Work on a `modification` branch | Accepted |

## D1. Clone with full history

- **Decision**: `Petoria` was created with `git clone` from the local `Nestar` repo, `Petoria-next` from `nestar-client` (`nestar-next`). The `origin` remotes were replaced with `yakhyo018/Petoria` and `yakhyo018/Petoria-next`. `master` and `develop` were pushed.
- **Why**: Keeps the commit history (69 backend, 30 frontend commits) for blame and context. Cloning skips `node_modules`, `dist` and `.next`.
- **Safety check**: Before the public push, all history was scanned. No `.env` file was ever committed, and the `MONGO_*` and `SECRET_TOKEN` values do not appear in any commit. `.env` files were copied manually and are git-ignored.
- **Risks**: The public history contains Nestar naming and authorship.
- **Alternatives**: A fresh repo with a single squashed commit. This was rejected because it loses history.

## D2. Two-phase migration

- **Decision**: Phase 1 renames identity only. Phase 2 changes the domain (`Property` → `Product`).
- **Why**: Rename changes are mechanical and verifiable by build and typecheck. Domain changes break the API contract, so mixing them makes regressions hard to locate.
- **Risks**: The codebase temporarily mixes the "Petoria" brand with "Property/Agent" domain names.
- **Alternatives**: A big-bang rewrite, rejected as too risky.

## D3. Freeze API and data contract in phase 1

- **Decision**: No changes to GraphQL operation names, types, enums, DTOs, Mongoose model names, collections or fields.
- **Why**: The existing frontend and stored data keep working, so phase 1 is zero-risk for clients.
- **Risks**: None at runtime. The technical debt is tracked in `NEXT_STEPS.md`.

## D4. `git mv` for app folders

- **Decision**: `apps/nestar-api` → `apps/petoria-api`, `apps/nestar-batch` → `apps/petoria-batch`.
- **Why**: Git records them as renames (86 files, `R` status), so `git log --follow` and blame keep working.
- **Risks**: Hard-coded paths outside the repo (deploy scripts, PM2 configs, Docker) must be updated to `dist/apps/petoria-*`.

## D5. Mongo database name

- **Decision**: `MONGO_DEV` and `MONGO_PROD` now end with `/Petoria` (was `/Nestar`). Same Atlas cluster.
- **Why**: Clean project identity, and the Petoria data is isolated from Nestar.
- **Risks**: `/Petoria` starts empty. Nestar members, properties and articles are not visible. MongoDB creates the database and collections on first write.
- **Alternatives**: Keep `/Nestar` (data available, naming mismatch), or copy data with `mongodump --db Nestar` + `mongorestore --nsFrom 'Nestar.*' --nsTo 'Petoria.*'`.

## D6. Backend first

- **Decision**: Finish Petoria backend (rename, then domain) before touching Petoria-next. The frontend repo is only connected to GitHub.
- **Why**: The frontend depends on the GraphQL contract. Migrating it before the contract is final would mean doing the work twice.

## D7. Domain model `Product`

- **Decision**: `Property` was replaced by `Product` everywhere (module, resolver, service, DTOs, enums, schema, collection `products`, GraphQL operations, group enums, batch), following the Petoria ERD.
- **Why**: Petoria is a pet shop. Real-estate fields (address, square, beds, rooms, barter, rent, constructedAt) have no meaning here.
- **Choices made where the ERD gives no values**:
  - `productGender`: `MALE | FEMALE`, as fixed by `AGENTS.md`. An earlier `UNISEX` value was removed. The field is NN, so non-pet products (food, toys, accessories) must still pick a value. Revisit if this becomes a problem.
  - `productLocation`: kept the Nestar Korean city list.
  - `MemberType.AGENT` kept, so the operation is `getAgentProducts`. Renaming to `SELLER` is a separate decision.
  - `notifications.propertyId` → `productId`, so all references are consistent. The ERD still shows `propertyId` and should be updated.
  - Unique index `{type, location, title, price}` kept.
- **Risks**: Breaking GraphQL change for the frontend. The enum values above may need adjustment once product requirements are final.
- **Alternatives**: Keep `Property` internally and relabel only in the UI. Rejected because it leaves a permanent naming mismatch.

## D8. `modification` branch

- **Decision**: All migration work happens on `modification`, branched from `develop`. `master` and `develop` stay identical to Nestar.
- **Why**: Easy diff against the original, and a clean way to roll back.
