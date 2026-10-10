// Petoria sample data seed. Goes through the public GraphQL API so passwords are hashed and
// counters (memberProducts, productLikes, productViews, ...) are updated by the real business logic.
//
// Usage: node scripts/seed/seed.mjs            (API at http://localhost:3007/graphql)
//        PETORIA_API=http://host:port/graphql node scripts/seed/seed.mjs
//        node scripts/seed/seed.mjs --force   (re-run likes/comments/follows/articles even if already seeded)
//
// Safe to re-run: existing members log in, existing seller catalogs are reused.

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const API = process.env.PETORIA_API ?? 'http://localhost:3007/graphql';
const FORCE = process.argv.includes('--force');

const data = JSON.parse(await readFile(path.join(HERE, 'data.json'), 'utf8'));

async function gql(query, variables = {}, token) {
	const res = await fetch(API, {
		method: 'POST',
		headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
		body: JSON.stringify({ query, variables }),
	});
	const json = await res.json();
	if (json.errors?.length) throw new Error(json.errors.map((e) => e.message).join('; '));
	return json.data;
}

async function upload(token, fileNames, target) {
	const many = fileNames.length > 1;
	const form = new FormData();
	form.append(
		'operations',
		JSON.stringify({
			query: many
				? 'mutation ($files: [Upload!]!, $target: String!) { imagesUploader(files: $files, target: $target) }'
				: 'mutation ($file: Upload!, $target: String!) { imageUploader(file: $file, target: $target) }',
			variables: many ? { files: fileNames.map(() => null), target } : { file: null, target },
		}),
	);
	form.append(
		'map',
		JSON.stringify(
			Object.fromEntries(fileNames.map((_, i) => [String(i), [many ? `variables.files.${i}` : 'variables.file']])),
		),
	);
	for (const [i, name] of fileNames.entries()) {
		const buf = await readFile(path.join(HERE, 'images', name));
		form.append(String(i), new Blob([buf], { type: 'image/jpeg' }), name);
	}
	const res = await fetch(API, {
		method: 'POST',
		headers: { authorization: `Bearer ${token}`, 'apollo-require-preflight': 'true' },
		body: form,
	});
	const json = await res.json();
	if (json.errors?.length) throw new Error(json.errors.map((e) => e.message).join('; '));
	return many ? json.data.imagesUploader : [json.data.imageUploader];
}

/** MEMBERS **/

async function ensureMember(m) {
	const login = { memberNick: m.memberNick, memberPassword: data.password };
	try {
		const { signup } = await gql(
			'mutation ($input: MemberInput!) { signup(input: $input) { _id accessToken } }',
			{ input: { ...login, memberPhone: m.memberPhone, memberType: m.memberType } },
		);
		const [memberImage] = await upload(signup.accessToken, [`avatar-${m.memberNick}.jpg`], 'member');
		await gql(
			'mutation ($input: MemberUpdate!) { updateMember(input: $input) { _id } }',
			{
				input: {
					_id: signup._id,
					memberImage,
					memberFullName: m.memberFullName,
					memberDesc: m.memberDesc,
					...(m.memberAddress ? { memberAddress: m.memberAddress } : {}),
				},
			},
			signup.accessToken,
		);
		console.log(`+ member ${m.memberNick} (${m.memberType})`);
		return { ...signup, created: true };
	} catch (err) {
		const { login: member } = await gql('mutation ($input: LoginInput!) { login(input: $input) { _id accessToken } }', {
			input: login,
		}).catch(() => {
			throw new Error(`Cannot sign up or log in ${m.memberNick}: ${err.message}`);
		});
		console.log(`= member ${m.memberNick} exists`);
		return { ...member, created: false };
	}
}

const members = {};
for (const m of data.members) members[m.memberNick] = await ensureMember(m);

/** PRODUCTS **/

const products = {};
let createdProducts = 0;
const sellers = [...new Set(data.products.map((p) => p.seller))];

for (const seller of sellers) {
	const { accessToken } = members[seller];
	const { getAgentProducts } = await gql(
		'query ($input: AgentProductsInquiry!) { getAgentProducts(input: $input) { list { _id productTitle } } }',
		{ input: { page: 1, limit: 100, search: {} } },
		accessToken,
	);
	const existing = new Map(getAgentProducts.list.map((p) => [p.productTitle, p._id]));

	for (const p of data.products.filter((item) => item.seller === seller)) {
		if (existing.has(p.productTitle)) {
			products[p.key] = existing.get(p.productTitle);
			continue;
		}
		const productImages = await upload(accessToken, [`${p.key}-1.jpg`, `${p.key}-2.jpg`], 'product');
		const { key, seller: _seller, ...input } = p;
		const { createProduct } = await gql(
			'mutation ($input: ProductInput!) { createProduct(input: $input) { _id } }',
			{ input: { ...input, productImages } },
			accessToken,
		);
		products[key] = createProduct._id;
		createdProducts++;
		console.log(`+ product ${p.productTitle}`);
	}
}

if (!createdProducts && !FORCE) {
	console.log('Catalog already seeded. Skipping likes, views, comments, follows and articles (use --force to add them again).');
	process.exit(0);
}

/** VIEWS + LIKES **/

const productViewers = ['minji', 'jisoo', 'alexlee', 'happypaws', 'meowmart', 'birdnest', 'aquazone'];
for (const nick of productViewers) {
	const likes = new Set(data.likes[nick] ?? []);
	for (const [key, productId] of Object.entries(products)) {
		// Popular products get more viewers: skip some views for a natural spread
		if ((key.length + nick.length) % 3 === 0 && !likes.has(key)) continue;
		const { getProduct } = await gql(
			'query ($id: String!) { getProduct(productId: $id) { _id meLiked { myFavorite } } }',
			{ id: productId },
			members[nick].accessToken,
		);
		if (likes.has(key) && !getProduct.meLiked?.[0]?.myFavorite) {
			await gql('mutation ($id: String!) { likeTargetProduct(productId: $id) { _id } }', { id: productId }, members[nick].accessToken);
		}
	}
}
console.log('+ product views and likes');

/** PRODUCT COMMENTS **/

for (const c of data.productComments) {
	await gql(
		'mutation ($input: CommentInput!) { createComment(input: $input) { _id } }',
		{ input: { commentGroup: 'PRODUCT', commentContent: c.text, commentRefId: products[c.product] } },
		members[c.author].accessToken,
	);
}
console.log(`+ ${data.productComments.length} product comments`);

/** FOLLOWS + SELLER LIKES **/

for (const [nick, targets] of Object.entries(data.follows)) {
	for (const target of targets) {
		await gql('mutation ($id: String!) { subscribe(input: $id) { _id } }', { id: members[target]._id }, members[nick].accessToken).catch(
			(err) => console.log(`  follow ${nick} -> ${target}: ${err.message}`),
		);
	}
}
for (const [nick, targets] of Object.entries(data.sellerLikes)) {
	for (const target of targets) {
		await gql('mutation ($id: String!) { likeTargetMember(memberId: $id) { _id } }', { id: members[target]._id }, members[nick].accessToken);
	}
}
console.log('+ follows and seller likes');

/** COMMUNITY **/

const articleIds = [];
for (const [i, a] of data.articles.entries()) {
	const token = members[a.author].accessToken;
	const [articleImage] = await upload(token, [`article-${i + 1}.jpg`], 'article');
	const { createBoardArticle } = await gql(
		'mutation ($input: BoardArticleInput!) { createBoardArticle(input: $input) { _id } }',
		{ input: { articleCategory: a.articleCategory, articleTitle: a.articleTitle, articleContent: a.articleContent, articleImage } },
		token,
	);
	articleIds.push(createBoardArticle._id);
}
for (const [i, id] of articleIds.entries()) {
	for (const nick of ['minji', 'jisoo', 'alexlee'].slice(0, (i % 3) + 1)) {
		await gql('query ($id: String!) { getBoardArticle(articleId: $id) { _id } }', { id }, members[nick].accessToken);
		await gql('mutation ($id: String!) { likeTargetBoardArticle(articleId: $id) { _id } }', { id }, members[nick].accessToken);
	}
}
for (const c of data.articleComments) {
	await gql(
		'mutation ($input: CommentInput!) { createComment(input: $input) { _id } }',
		{ input: { commentGroup: 'ARTICLE', commentContent: c.text, commentRefId: articleIds[c.article] } },
		members[c.author].accessToken,
	);
}
console.log(`+ ${articleIds.length} articles with views, likes and comments`);

console.log(`Done. All sample accounts use the password from scripts/seed/data.json.`);
