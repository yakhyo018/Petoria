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
2. **Domain Migration (planned)**: replace the real-estate `Property` domain with a pet-shop `Product` domain (see the ERD target below). This is a breaking change and is planned separately.

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
| `.env` Mongo database label | `/Nestar` | `/Nestar` | **Not changed**, pending decision (see `DECISIONS.md` D5) |

## Module Changes

No NestJS module was renamed, added or removed.

| Module | Path | Change |
| --- | --- | --- |
| `AppModule` | `apps/petoria-api/src/app.module.ts` | Path only |
| `ComponentsModule` | `apps/petoria-api/src/components/components.module.ts` | Path only |
| `AuthModule`, `MemberModule`, `PropertyModule`, `BoardArticleModule`, `CommentModule`, `LikeModule`, `ViewModule`, `FollowModule` | `apps/petoria-api/src/components/*` | Path only |
| `DatabaseModule` | `apps/petoria-api/src/database`, `apps/petoria-batch/src/database` | Path only |
| `SocketModule` | `apps/petoria-api/src/socket` | Path only |
| `BatchModule` | `apps/petoria-batch/src/batch.module.ts` | Relative imports `../../nestar-api/...` → `../../petoria-api/...` |

## GraphQL Changes

**None.** The schema is byte-for-byte compatible with Nestar. Current operations:

| Resolver | Queries | Mutations |
| --- | --- | --- |
| Member | `getMember`, `getAgents`, `getAllMembersByAdmin` | `signup`, `login`, `updateMember`, `checkAuth`, `checkAuthRoles`, `likeTargetMember`, `updateMemberByAdmin`, `imageUploader`, `imagesUploader` |
| Property | `getProperty`, `getProperties`, `getFavorites`, `getVisited`, `getAgentProperties`, `getAllPropertiesByAdmin` | `createProperty`, `updateProperty`, `likeTargetProperty`, `updatePropertyByAdmin`, `removePropertyByAdmin` |
| BoardArticle | `getBoardArticle`, `getBoardArticles`, `getAllBoardArticlesByAdmin` | `createBoardArticle`, `updateBoardArticle`, `likeTargetBoardArticle`, `updateBoardArticleByAdmin`, `removeBoardArticleByAdmin` |
| Comment | `getComments` | `createComment`, `updateComment`, `removeCommentByAdmin` |
| Follow | `getMemberFollowings`, `getMemberFollowers` | `subscribe`, `unsubscribe` |

WebSocket gateway (`socket.gateway.ts`, transport `websocket`): event `message`, unchanged.

Planned rename for the Domain Migration phase:

| Current | Planned |
| --- | --- |
| `createProperty` / `updateProperty` | `createProduct` / `updateProduct` |
| `getProperty` / `getProperties` | `getProduct` / `getProducts` |
| `getAgentProperties` | `getSellerProducts` (if `AGENT` → `SELLER`, see D7) |
| `likeTargetProperty` | `likeTargetProduct` |
| `getAllPropertiesByAdmin`, `updatePropertyByAdmin`, `removePropertyByAdmin` | `getAllProductsByAdmin`, `updateProductByAdmin`, `removeProductByAdmin` |
| `getFavorites`, `getVisited` | Unchanged names, return type `Products` |
| Types `Property`, `Properties`, `PropertyInput`, `PropertiesInquiry`, `PropertyUpdate` | `Product`, `Products`, `ProductInput`, `ProductsInquiry`, `ProductUpdate` |
| Enums `PropertyType`, `PropertyStatus`, `PropertyLocation` | `ProductType`, `ProductStatus`, `ProductLocation`, plus new `ProductSpecies`, `ProductGender` |
| Enum values `LikeGroup.PROPERTY`, `ViewGroup.PROPERTY`, `NotificationGroup.PROPERTY` | `PRODUCT` |

## MongoDB Collection and Schema Changes

Safe Rename Layer: **no collection or schema changes.**

| Item | Status |
| --- | --- |
| Mongoose model `Property` | Unchanged |
| Collection `properties` | Unchanged |
| Collections `members`, `likes`, `views`, `comments`, `follows`, `boardArticles`, `notices`, `notifications` | Unchanged |
| Schema fields such as `propertyTitle`, `propertyPrice`, `propertyRooms` | Unchanged |
| `.env` database name `/Nestar` | Unchanged (pending decision) |

Target `products` collection (from the Petoria ERD, MongoDB diagram `petoria.dmm`):

| Field | Type | NN | Source in `properties` |
| --- | --- | --- | --- |
| `_id` | ObjectId | Yes | `_id` |
| `productType` | enum `PET \| FOOD \| TOY \| ACCESSORY` | Yes | `propertyType` (`APARTMENT \| VILLA \| HOUSE`) |
| `productSpecies` | enum `DOG \| CAT \| BIRD \| FISH` | Yes | New |
| `productGender` | enum (values TBD) | Yes | New |
| `productStatus` | enum | Yes | `propertyStatus` (`ACTIVE \| SOLD \| DELETE`) |
| `productLocation` | enum | Yes | `propertyLocation` (Korean cities) |
| `productTitle` | string | Yes | `propertyTitle` |
| `productPrice` | double | Yes | `propertyPrice` |
| `productViews`, `productLikes`, `productComments`, `productRank` | int | Yes | `property*` counters |
| `productImages` | string[] | Yes | `propertyImages` |
| `productDesc` | string | No | `propertyDesc` |
| `memberId` | ObjectId | Yes | `memberId` |
| `soldAt`, `deletedAt` | date | No | `soldAt`, `deletedAt` |
| `createdAt`, `updatedAt` | date | Yes | timestamps |

Fields dropped from the real-estate model: `propertyAddress`, `propertySquare`, `propertyBeds`, `propertyRooms`, `propertyBarter`, `propertyRent`, `constructedAt`.

Related references to update in the Domain Migration: `Member.memberProperties` counter, `Notification.propertyId`, `likeRefId` / `viewRefId` / `commentRefId` targets with group `PROPERTY`, batch job `batchTopProperties`.

## Compatibility Notes

- Clients (Petoria-next, existing Nestar frontend) keep using the current GraphQL operations until the Domain Migration is approved.
- The frontend can show Petoria / pet-shop terminology while still calling the `Property` GraphQL operations internally.
- The database stays compatible with the Nestar schema; both apps can point to the same database.
- `dist/` must be rebuilt after the rename; old `dist/apps/nestar-*` outputs are obsolete. Deploy scripts that run `dist/apps/nestar-api/main` must switch to `dist/apps/petoria-api/main`.
- A `Property` → `Product` migration affects API contracts, DTOs, Mongoose models, batch jobs, frontend queries and stored data, and needs a data migration script.
