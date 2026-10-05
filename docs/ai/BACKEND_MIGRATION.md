# Backend Migration: Nestar to Petoria

## Original Project Summary

| Item | Value |
| --- | --- |
| Name | Nestar |
| Domain | Real-estate marketplace (properties, agents, community board) |
| Repository | `yakhyo018/Nestar` |
| Stack | NestJS 10 monorepo, GraphQL (Apollo Server 4, code-first), Mongoose 8, MongoDB Atlas, WebSocket (`ws`), `@nestjs/schedule` |
| Apps | `apps/nestar-api` (GraphQL API + WebSocket chat), `apps/nestar-batch` (cron ranking jobs) |
| Auth | JWT (`@nestjs/jwt`), bcryptjs, guards: `AuthGuard`, `RolesGuard`, `WithoutGuard` |
| Roles | `USER`, `AGENT`, `ADMIN` |

## New Project Summary

| Item | Value |
| --- | --- |
| Name | Petoria |
| Domain | Pet shop marketplace (pets, food, toys, accessories) |
| Repository | `yakhyo018/Petoria` (public), working branch `modification` |
| Frontend | `yakhyo018/Petoria-next` (cloned from `nestar-next`, migration not started) |
| Stack | Unchanged from Nestar |
| Apps | `apps/petoria-api`, `apps/petoria-batch` |

## Backend Migration Goal

Migrate Nestar into Petoria in two isolated phases:

1. **Safe Rename Layer (done)**: rename project/app identity from Nestar to Petoria without changing business behavior, GraphQL contract, DTOs, Mongoose models or MongoDB collections.
2. **Domain Migration (done)**: replace the real-estate `Property` domain with the pet-shop `Product` domain from the Petoria ERD. This is a breaking GraphQL/data change.

## Naming Changes

| Area | Before | After | Status |
| --- | --- | --- | --- |
| npm package name | `nestar` | `petoria` | Done |
| `package-lock.json` root name | `nestar` | `petoria` | Done |
| API app folder | `apps/nestar-api` | `apps/petoria-api` | Done (`git mv`, history kept) |
| Batch app folder | `apps/nestar-batch` | `apps/petoria-batch` | Done (`git mv`, history kept) |
| `nest-cli.json` projects | `nestar-api`, `nestar-batch`, `nestart-batch` | `petoria-api`, `petoria-batch` | Done (stale `nestart-batch` entry removed) |
| npm scripts | `start:dev:batch`, `start:prod`, `start:prod:batch`, `test:e2e` pointing to `nestar-*` | point to `petoria-*` | Done |
| Build output | `dist/apps/nestar-*` | `dist/apps/petoria-*` | Done |
| API welcome string | `Welcome to Nestar API server!` | `Welcome to Petoria API server!` | Done |
| Batch welcome string | `Welcome to Nestar BATCH Server!` | `Welcome to Petoria BATCH Server!` | Done |
| Batch e2e test import | `NestarBatchModule` (did not exist) | `BatchModule` | Done (fixes broken import) |
| `.env` Mongo database label | `/Nestar` | `/Petoria` | Done (new empty database, see `DECISIONS.md` D5) |

## Module Changes

Phase 1 changed paths only. Phase 2 renamed the `property` component to `product`.

| Module | Path | Change |
| --- | --- | --- |
| `AppModule` | `apps/petoria-api/src/app.module.ts` | Path only |
| `ComponentsModule` | `apps/petoria-api/src/components/components.module.ts` | Path only |
| `PropertyModule` → `ProductModule` (`PropertyResolver`/`PropertyService` → `ProductResolver`/`ProductService`) | `components/property/*` → `components/product/product.*` | Renamed (`git mv`) |
| `AuthModule`, `MemberModule`, `BoardArticleModule`, `CommentModule`, `LikeModule`, `ViewModule`, `FollowModule` | `apps/petoria-api/src/components/*` | Imports/references to Product only |
| DTOs, enum, schema | `libs/dto/property/*` → `libs/dto/product/*`, `libs/enums/property.enum.ts` → `product.enum.ts`, `schemas/Property.model.ts` → `Product.model.ts` | Renamed (`git mv`) and rewritten to ERD fields |
| `DatabaseModule` | `apps/petoria-api/src/database`, `apps/petoria-batch/src/database` | Path only |
| `SocketModule` | `apps/petoria-api/src/socket` | Path only |
| `BatchModule` | `apps/petoria-batch/src/batch.module.ts` | Relative imports `../../nestar-api/...` → `../../petoria-api/...` |

## GraphQL Changes

Phase 1: none. Phase 2: all Property operations, types and enums were renamed to Product. This is a **breaking change** for clients. Verified by introspecting the running API.

| Resolver | Queries | Mutations |
| --- | --- | --- |
| Member | `getMember`, `getAgents`, `getAllMembersByAdmin` | `signup`, `login`, `updateMember`, `checkAuth`, `checkAuthRoles`, `likeTargetMember`, `updateMemberByAdmin`, `imageUploader`, `imagesUploader` |
| Product | `getProduct(productId)`, `getProducts`, `getFavorites`, `getVisited`, `getAgentProducts`, `getAllProductsByAdmin` | `createProduct`, `updateProduct`, `likeTargetProduct(productId)`, `updateProductByAdmin`, `removeProductByAdmin(productId)` |
| BoardArticle | `getBoardArticle`, `getBoardArticles`, `getAllBoardArticlesByAdmin` | `createBoardArticle`, `updateBoardArticle`, `likeTargetBoardArticle`, `updateBoardArticleByAdmin`, `removeBoardArticleByAdmin` |
| Comment | `getComments` | `createComment`, `updateComment`, `removeCommentByAdmin` |
| Follow | `getMemberFollowings`, `getMemberFollowers` | `subscribe`, `unsubscribe` |

The WebSocket gateway (`socket.gateway.ts`, event `message`) is unchanged.

| Before (Nestar) | After (Petoria) |
| --- | --- |
| `createProperty` / `updateProperty` | `createProduct` / `updateProduct` |
| `getProperty(propertyId)` / `getProperties` | `getProduct(productId)` / `getProducts` |
| `getAgentProperties` | `getAgentProducts` (`MemberType.AGENT` kept, see D7) |
| `likeTargetProperty(propertyId)` | `likeTargetProduct(productId)` |
| `getAllPropertiesByAdmin`, `updatePropertyByAdmin`, `removePropertyByAdmin(propertyId)` | `getAllProductsByAdmin`, `updateProductByAdmin`, `removeProductByAdmin(productId)` |
| `getFavorites`, `getVisited` | Same names, return `Products` |
| Types `Property`, `Properties`, `PropertyInput`, `PropertiesInquiry`, `AgentPropertiesInquiry`, `AllPropertiesInquiry`, `PropertyUpdate` | `Product`, `Products`, `ProductInput`, `ProductsInquiry`, `AgentProductsInquiry`, `AllProductsInquiry`, `ProductUpdate` |
| Enums `PropertyType`, `PropertyStatus`, `PropertyLocation` | `ProductType`, `ProductStatus`, `ProductLocation`, plus new `ProductSpecies`, `ProductGender` |
| Enum value `PROPERTY` in `LikeGroup`, `ViewGroup`, `CommentGroup`, `NotificationGroup` | `PRODUCT` |
| Search filters `roomsList`, `bedsList`, `squaresRange`, `options` (barter/rent) | Removed. New `speciesList`, `genderList` |
| `ALPISearch.propertyStatus`, `propertyLocationList` | `productStatus`, `productLocationList` |
| Input type `SquaresRange` | Removed |
| `Member.memberProperties` | `Member.memberProducts` |

## MongoDB Collection and Schema Changes

| Item | Before | After |
| --- | --- | --- |
| Database (`.env`) | `/Nestar` | `/Petoria` (new, empty, so no data migration is needed) |
| Mongoose model / collection | `Property` / `properties` | `Product` / `products` |
| `Member.memberProperties` | int | `memberProducts` |
| `Notification.propertyId` (ref `Property`) | ObjectId | `productId` (ref `Product`). The ERD still shows `propertyId`, see D7 |
| Group value `PROPERTY` in `likes.likeGroup`, `views.viewGroup`, `comments.commentGroup`, `notifications.notificationGroup` | `PROPERTY` | `PRODUCT` |
| Collections `members`, `likes`, `views`, `comments`, `follows`, `boardArticles`, `notices`, `notifications` | — | Names unchanged |

`products` schema (`schemas/Product.model.ts`), matching the Petoria ERD (`petoria.dmm`):

| Field | Type | NN | Values / default | Was |
| --- | --- | --- | --- | --- |
| `_id` | ObjectId | Yes | | `_id` |
| `productType` | enum | Yes | `PET \| FOOD \| TOY \| ACCESSORY` | `propertyType` (`APARTMENT \| VILLA \| HOUSE`) |
| `productSpecies` | enum | Yes | `DOG \| CAT \| BIRD \| FISH` | New |
| `productGender` | enum | Yes | `MALE \| FEMALE` | New (fixed by `AGENTS.md`, see D7) |
| `productStatus` | enum | Yes (default) | `ACTIVE \| SOLD \| DELETE`, default `ACTIVE` | `propertyStatus` |
| `productLocation` | enum | Yes | Kept from Nestar: `SEOUL \| BUSAN \| INCHEON \| DAEGU \| GYEONGJU \| GWANGJU \| CHONJU \| DAEJON \| JEJU` | `propertyLocation` |
| `productTitle` | string | Yes | | `propertyTitle` |
| `productPrice` | number (double) | Yes | | `propertyPrice` |
| `productViews`, `productLikes`, `productComments`, `productRank` | number (int) | Yes (default) | default `0` | `property*` |
| `productImages` | string[] | Yes | | `propertyImages` |
| `productDesc` | string | No | | `propertyDesc` |
| `memberId` | ObjectId → `Member` | Yes | | `memberId` |
| `soldAt`, `deletedAt` | date | No | | same |
| `createdAt`, `updatedAt` | date | Yes | timestamps | same |

Removed fields: `propertyAddress`, `propertySquare`, `propertyBeds`, `propertyRooms`, `propertyBarter`, `propertyRent`, `constructedAt`.

Unique index (kept from Nestar): `{ productType, productLocation, productTitle, productPrice }`.

## Compatibility Notes

- The GraphQL contract is **not** compatible with the old Nestar frontend. Petoria-next must migrate its `apollo/*` documents (see `FRONTEND_MIGRATION.md`).
- The Petoria database is new, so no `properties` → `products` data migration is needed. If Nestar data is ever imported, the field mapping above applies, and `PROPERTY` group values must be rewritten to `PRODUCT`.
- `dist/` must be rebuilt. Deploy scripts must run `dist/apps/petoria-api/main` and `dist/apps/petoria-batch/main`.
- The batch job `batchTopProperties` is now `batchTopProducts` (cron name `BATCH_TOP_PRODUCTS`). The agent rank formula uses `memberProducts`.
