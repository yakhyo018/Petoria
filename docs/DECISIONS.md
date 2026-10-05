# Architectural Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D1 | New repositories cloned from Nestar with full git history | Accepted |
| D2 | Two-phase migration: Safe Rename Layer first, Domain Migration later | Accepted |
| D3 | Keep GraphQL API, DTOs, Mongoose models and collections unchanged in phase 1 | Accepted |
| D4 | Rename app folders with `git mv` | Accepted |
| D5 | Keep `.env` Mongo database name `/Nestar` for now | Pending |
| D6 | Backend first, frontend after | Accepted |
| D7 | Target domain model `Product` from the Petoria ERD | Proposed |
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

- **Decision**: Pending. `MONGO_DEV` and `MONGO_PROD` still end with `/Nestar`.
- **Option A, keep `/Nestar`**: Existing data stays available. The name is internal only.
- **Option B, switch to `/Petoria`**: Clean branding, but connects to a new empty database. It needs seed data or a `mongodump`/`mongorestore` copy.
- **Recommendation**: Keep `/Nestar` until the Domain Migration. Then create `/Petoria` with migrated `products` data in a single step.

## D6. Backend first

- **Decision**: Finish Petoria backend (rename, then domain) before touching Petoria-next. The frontend repo is only connected to GitHub.
- **Why**: The frontend depends on the GraphQL contract. Migrating it before the contract is final would mean doing the work twice.

## D7. Target domain model

- **Decision (proposed)**: Replace `Property` with `Product` as defined in the ERD (`productType`, `productSpecies`, `productGender`, …). See `BACKEND_MIGRATION.md`.
- **Open questions**:
  - Values of `productGender` and `productLocation`.
  - Whether `MemberType.AGENT` becomes `SELLER`.
  - Whether to rename the `properties` collection or create a new `products` collection.
  - The ERD still shows `notifications.propertyId`; it should be `productId`.
- **Risks**: Breaking API change and data migration.
- **Alternatives**: Keep `Property` internally and only relabel in the UI. This is cheap, but leaves a permanent naming mismatch.

## D8. `modification` branch

- **Decision**: All migration work happens on `modification`, branched from `develop`. `master` and `develop` stay identical to Nestar.
- **Why**: Easy diff against the original, and a clean way to roll back.
