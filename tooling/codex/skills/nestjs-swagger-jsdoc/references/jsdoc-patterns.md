# JSDoc Patterns

Use this reference when documenting NestJS services, utilities, and custom decorators.

## When To Add JSDoc

Prefer JSDoc when a function has at least one of these properties:

- domain-specific behavior
- non-obvious filtering or branching
- side effects such as database writes or cache updates
- important error contracts
- helper behavior that callers would otherwise have to reverse engineer

Skip JSDoc when the function is trivial and the name already explains the behavior.

## Service Method Pattern

Prefer a short summary, then concrete tags.

```ts
/**
 * 갤러리를 생성합니다.
 *
 * @param author 작성자 이름
 * @param dto 갤러리 생성 요청 데이터
 * @returns 생성된 갤러리
 * @throws {KError} 유효하지 않은 썸네일 파일 ID가 포함된 경우(BAD_REQUEST)
 * @throws {KError} 저장 중 알 수 없는 오류가 발생한 경우(INTERNAL_SERVER_ERROR)
 */
async createGallery(author: string, dto: CreateGalleryDto): Promise<Gallery> {}
```

## Helper Method Pattern

Use a short summary and explain the hidden rule or invariant.

```ts
/**
 * 공개된 갤러리 목록 조회 where 조건을 생성합니다.
 *
 * @param dto 목록 조회 조건
 * @returns Prisma 갤러리 where 조건
 */
private buildListGalleriesWhereInput(dto: ListGalleriesDto): Prisma.GalleryWhereInput {}
```

If behavior has important constraints, add bullet-style prose before tags.

```ts
/**
 * 공개된 갤러리 목록을 조회합니다. (일반 사용자용)
 *
 * - `isPosted=true` 조건이 항상 적용됩니다.
 * - 검색어가 존재하면 제목/본문 OR 조건으로 부분 검색합니다.
 * - 정렬은 DTO의 allowlist 정책을 따릅니다.
 *
 * @param dto 목록 조회 조건(페이지네이션/정렬/검색)
 * @returns 공개된 갤러리 목록
 */
async listGalleries(dto: ListGalleriesDto): Promise<Gallery[]> {}
```

## Decorator And Utility Pattern

For reusable decorators or utilities, explain the purpose rather than restating the implementation.

```ts
/**
 * Swagger 문서를 위한 Bearer 토큰 인증 데코레이터를 적용합니다.
 *
 * @returns 적용된 데코레이터
 */
export function ApiBearerAuthToken() {}
```

## Writing Rules

- Keep the first sentence action-oriented and specific.
- Name the domain object exactly as the code does.
- Describe thrown errors only when callers need that information.
- Prefer Korean terminology already used in the file.
- Do not restate obvious TypeScript types in prose.
- Do not add empty `@returns` or `@throws` tags just for symmetry.

## What To Read Before Editing

- Read the whole target file.
- Read the callers or immediate usages when behavior is inferred from call context.
- Read related DTOs or error helpers when they determine what the method guarantees.
