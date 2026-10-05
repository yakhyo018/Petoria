---
name: product-logic
description: Review Petoria product GraphQL, DTO, schema, enum, filter and naming consistency. Use after changing anything under product (resolver, service, DTOs, enums, Product.model) or before a frontend integration, to confirm all layers agree.
---

# Petoria Product Logic Review

Read-only review unless fixes are requested. Report findings as a table: file:line, issue, suggested fix.

## Source of Truth

| Item | Expected |
| --- | --- |
| Enum `ProductType` | `PET`, `FOOD`, `TOY`, `ACCESSORY` |
| Enum `ProductSpecies` | `DOG`, `CAT`, `BIRD`, `FISH` |
| Enum `ProductGender` | `MALE`, `FEMALE` |
| Enum `ProductStatus` | `ACTIVE`, `SOLD`, `DELETE` |
| Enum `ProductLocation` | Korean city list (see `product.enum.ts`) |
| Collection | `products` (model name `Product`) |
| Owner role | `MemberType.AGENT` |

Required fields, from the ERD: `productType`, `productSpecies`, `productGender`, `productStatus` (default ACTIVE), `productLocation`, `productTitle`, `productPrice`, `productViews`/`productLikes`/`productComments`/`productRank` (default 0), `productImages`, `memberId`, timestamps. Optional fields: `productDesc`, `soldAt`, `deletedAt`.

## Files

- `apps/petoria-api/src/libs/enums/product.enum.ts`
- `apps/petoria-api/src/schemas/Product.model.ts`
- `apps/petoria-api/src/libs/dto/product/product.ts` (ObjectType `Product`, `Products`)
- `apps/petoria-api/src/libs/dto/product/product.input.ts` (`ProductInput`, `ProductsInquiry`, `AgentProductsInquiry`, `AllProductsInquiry`, `OrdinaryInquiry`)
- `apps/petoria-api/src/libs/dto/product/product.update.ts` (`ProductUpdate`)
- `apps/petoria-api/src/components/product/product.{resolver,service,module}.ts`
- `apps/petoria-api/src/libs/config.ts` (`availableProductSorts`, `lookupFavorite`, `lookupVisited`)
- `apps/petoria-api/src/components/{like,view,comment}/*.service.ts`
- `apps/petoria-batch/src/batch.service.ts`

## Checklist

1. **Schema ↔ ObjectType**: every schema field has an `@Field` in `Product`, with the same name, a compatible type (`Int` for counters, `Number` for price) and matching nullability.
2. **Schema ↔ Input**: required schema fields without a default are `@IsNotEmpty()` in `ProductInput`. `memberId` is set from `@AuthMember`, not from client input.
3. **Update DTO**: all editable fields are `@IsOptional()` and nullable. `soldAt`/`deletedAt` are server-set, not `@Field`.
4. **Enums**: every enum is `registerEnumType`'d, used in the schema `enum:` and in the DTO `@Field(() => Enum)`. Values match the Source of Truth.
5. **Filters** (`shapeMatchQuery`): every `PISearch` field (`locationList`, `typeList`, `speciesList`, `genderList`, `pricesRange`, `periodsRange`, `text`, `memberId`) is applied to the matching `product*` field, and there are no unused or unknown filters.
6. **Sorts**: `availableProductSorts` names exist on the schema.
7. **Counters**: `targetKey` strings (`productViews`, `productLikes`, `productComments`, `memberProducts`) exist on their schemas. Create adds `+1` to `memberProducts`, while SOLD/DELETE subtracts `1`.
8. **Status lifecycle**: `SOLD` sets `soldAt`, `DELETE` sets `deletedAt`. Public queries filter `ACTIVE`. `removeProductByAdmin` only removes `DELETE` items.
9. **Guards**: create/update/getAgentProducts use `@Roles(MemberType.AGENT)`, admin ops use `@Roles(MemberType.ADMIN)`, public reads use `WithoutGuard`.
10. **Cross-module**: `LikeGroup`/`ViewGroup`/`CommentGroup`/`NotificationGroup` use `PRODUCT`, `$lookup from: 'products'`, `Notification.productId` refs `Product`.
11. **Naming**: no `property`/real-estate leftovers. Run:
    ```bash
    grep -rniE "propert|apartment|villa|beds|rooms|square|barter|rent\b|constructedAt" apps --include=*.ts
    ```
12. **Runtime schema** (optional): boot the API on a free port and introspect `Product`, `ProductInput` and the enums to confirm the generated GraphQL matches.

## Output

Summarize: OK items, mismatches (with file:line), and recommended fixes ordered by impact. If fixes are applied, run the validation commands from `AGENTS.md`.
