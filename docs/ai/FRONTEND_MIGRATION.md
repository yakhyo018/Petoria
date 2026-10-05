# Frontend Migration Plan: nestar-next to Petoria-next

Status: **Not started.** The repo is cloned and connected to `yakhyo018/Petoria-next`. Backend migration comes first (see `DECISIONS.md` D6).

Stack: Next.js (pages router), Apollo Client (`apollo/client.ts`, `apollo/user/*`, `apollo/admin/*`), next-i18next, SCSS, MUI.

## Step-by-step Plan

| Step | Task | Depends on |
| --- | --- | --- |
| 1 | Create a `modification` branch from `develop` | — |
| 2 | Safe rename: `package.json` name `nestar-next` → `petoria-next`, `<title>`/meta in `pages/_document.tsx`, logos/brand text in `LayoutHome`, `LayoutFull`, `LayoutBasic`, `Footer` | — |
| 3 | Replace "Nestar" in empty-state texts (`MyProperties`, `MyFavorites`, `RecentlyVisited`, `MemberProperties`, `MemberFollowers`, `MemberFollowings`, `community/index`, `account/join`) | 2 |
| 4 | Update `.env.development` / `.env.local` API URLs if the backend port or host changes | Backend deploy |
| 5 | UI terminology: relabel Property → Product, Agent → Seller in i18n strings and visible text only | 2 |
| 6 | Backend Domain Migration is done. Rename GraphQL documents in `apollo/user/*` and `apollo/admin/*` and regenerate types in `libs/types` | Backend phase 2 |
| 7 | Rename pages and components (table below) and update routes and links | 6 |
| 8 | Replace real-estate filters (beds, rooms, square, rent/barter) with species, gender and type filters | 6 |
| 9 | Swap images and assets in `public/` for pet-shop content | — |
| 10 | Build, lint and manual QA of all pages, including admin | 2–9 |

`CHANGELOG.md` (about 650 "nestar-next" mentions) is kept as history and is not rewritten.

## Page Mapping

| Nestar page | Petoria page |
| --- | --- |
| `pages/index.tsx` | `pages/index.tsx` (pet-shop home) |
| `pages/property/index.tsx` | `pages/product/index.tsx` |
| `pages/property/detail.tsx` | `pages/product/detail.tsx` |
| `pages/agent/index.tsx` | `pages/seller/index.tsx` |
| `pages/agent/detail.tsx` | `pages/seller/detail.tsx` |
| `pages/mypage/index.tsx` | Unchanged |
| `pages/member/index.tsx` | Unchanged |
| `pages/community/*` | Unchanged |
| `pages/cs/index.tsx`, `pages/about/index.tsx`, `pages/account/join.tsx` | Unchanged (text only) |
| `pages/_admin/properties/index.tsx` | `pages/_admin/products/index.tsx` |
| `pages/_admin/users`, `community`, `cs/*` | Unchanged |

## Component Mapping

| Nestar component | Petoria component |
| --- | --- |
| `property/PropertyCard.tsx`, `property/Filter.tsx`, `property/Review.tsx` | `product/ProductCard.tsx`, `product/Filter.tsx`, `product/Review.tsx` |
| `common/PropertyBigCard.tsx` | `common/ProductBigCard.tsx` |
| `common/AgentCard.tsx` | `common/SellerCard.tsx` |
| `homepage/PopularProperties`, `TopProperties`, `TrendProperties` (+ `*Card`) | `PopularProducts`, `TopProducts`, `TrendProducts` (+ `*Card`) |
| `homepage/TopAgents`, `TopAgentCard` | `TopSellers`, `TopSellerCard` |
| `mypage/AddNewProperty`, `MyProperties`, `PropertyCard` | `AddNewProduct`, `MyProducts`, `ProductCard` |
| `member/MemberProperties` | `member/MemberProducts` |
| `admin/properties/*` | `admin/products/*` |
| `agent/ReviewCard.tsx` | `seller/ReviewCard.tsx` |
| `Chat.tsx`, `Top.tsx`, `Footer.tsx`, `layout/*` | Unchanged (brand text only) |

## GraphQL Query/Mutation Rename Plan

The backend has already renamed these operations, so the current frontend documents will fail against Petoria API until they are updated.

| Current | Planned |
| --- | --- |
| `GET_PROPERTY`, `GET_PROPERTIES` | `GET_PRODUCT`, `GET_PRODUCTS` |
| `GET_AGENT_PROPERTIES` | `GET_AGENT_PRODUCTS` (`getAgentProducts`) |
| `GET_AGENTS` | Unchanged (`AGENT` kept) |
| `CREATE_PROPERTY`, `UPDATE_PROPERTY` | `CREATE_PRODUCT`, `UPDATE_PRODUCT` |
| `LIKE_TARGET_PROPERTY` | `LIKE_TARGET_PRODUCT` |
| `GET_ALL_PROPERTIES_BY_ADMIN`, `UPDATE_PROPERTY_BY_ADMIN`, `REMOVE_PROPERTY_BY_ADMIN` | `GET_ALL_PRODUCTS_BY_ADMIN`, `UPDATE_PRODUCT_BY_ADMIN`, `REMOVE_PRODUCT_BY_ADMIN` |
| `GET_FAVORITES`, `GET_VISITED` | Unchanged names, fields `property*` → `product*` |
| Field selections `propertyTitle`, `propertyPrice`, `propertyImages`, … | `productTitle`, `productPrice`, `productImages`, … |
| Removed fields `propertyBeds`, `propertyRooms`, `propertySquare`, `propertyRent`, `propertyBarter`, `propertyAddress`, `constructedAt` | Remove from documents and UI |
| Arguments `propertyId` | `productId` |
| Search `roomsList`, `bedsList`, `squaresRange`, `options` | `speciesList`, `genderList` |
| — | New fields `productSpecies`, `productGender` |

## UI Terminology Changes

| Nestar | Petoria |
| --- | --- |
| Nestar | Petoria |
| Property / Properties | Product / Products |
| Agent / Agents | Seller / Sellers |
| Apartment, Villa, House | Pet, Food, Toy, Accessory |
| Beds, Rooms, Square | Species, Gender |
| Rent / Barter | Removed |
| "Find your home" style copy | Pet-shop copy |
| My Properties | My Products |
| Recently Visited | Unchanged |
