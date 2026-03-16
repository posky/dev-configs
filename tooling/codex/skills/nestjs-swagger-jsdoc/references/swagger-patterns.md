# Swagger Patterns

Use this reference when documenting NestJS controllers and DTOs with `@nestjs/swagger`.

## Controller Pattern

Prefer this order on each endpoint:

1. Failure response decorators
2. Success response decorator
3. `@ApiOperation`
4. Auth/public decorators
5. HTTP method decorator

Typical protected controller shape:

```ts
@ApiBearerAuthToken()
@ApiTags(API_TAGS.ADMIN.POST._value)
@Controller()
export class PostAdminController {
  @ApiBadRequestResponse({ description: '요청 본문이 유효하지 않은 경우' })
  @ApiOkResponse({ description: '게시글 목록 조회 성공', schema: paginationResponseSchema(PostListAdminResponseDto) })
  @ApiOperation({
    summary: '게시글 목록 조회',
    description: '페이지네이션, 정렬, 카테고리 및 검색어 조건을 기반으로 게시글 목록을 조회합니다.',
  })
  @Get()
  async getListPosts(@Query() query: ListPostsAdminDto) {}
}
```

Typical public controller shape:

```ts
@ApiTags(API_TAGS.POST._value)
@Controller()
export class PostController {
  @ApiOkResponse({
    description: '게시글 상세 조회 성공',
    schema: {
      properties: {
        post: { $ref: getSchemaPath(PostResponseDto) },
      },
    },
  })
  @ApiOperation({
    summary: '게시글 상세 조회',
    description: '게시글 ID를 기반으로 게시글 상세 정보를 조회합니다.',
  })
  @PublicEndpoint()
  @Get(':postId')
  async getDetailPost(@Param('postId', ParseIntPipe) postId: number) {}
}
```

## Response Shape Rules

- If the route returns a `RetType` wrapper with `data`, document the wrapped object shape.
- If the route returns only a message, use an inline object schema with a `msg` property.
- If the route returns paginated data, prefer the existing pagination schema helper instead of rebuilding the schema inline.

Pagination example:

```ts
@ApiOkResponse({
  description: '게시글 목록 조회 성공',
  schema: paginationResponseSchema(PostListResponseDto),
})
```

Wrapped object example:

```ts
@ApiOkResponse({
  description: '게시글 상세 조회 성공',
  schema: {
    properties: {
      post: { $ref: getSchemaPath(PostAdminResponseDto) },
    },
  },
})
```

Message response example:

```ts
@ApiOkResponse({
  description: '게시글 삭제 성공',
  schema: {
    type: 'object',
    properties: {
      msg: {
        type: 'string',
        example: '게시글이 성공적으로 삭제되었습니다.',
      },
    },
  },
})
```

## Multipart Pattern

When the endpoint accepts uploaded files:

- Add `@ApiConsumes('multipart/form-data')`.
- Add `@ApiBody` with a schema that matches the actual field structure.
- Document file count, size, or field restrictions only if the code already enforces them.

Example:

```ts
@ApiBody({
  description: '업로드할 파일들.',
  schema: {
    type: 'object',
    additionalProperties: {
      type: 'array',
      items: {
        type: 'string',
        format: 'binary',
      },
    },
  },
})
@ApiConsumes('multipart/form-data')
```

## DTO Pattern

Prefer `@ApiProperty` for required fields and `@ApiPropertyOptional` for optional fields.
Keep Swagger metadata aligned with validators and existing constants.

Example:

```ts
const MAX_TITLE_LENGTH = 200;

export class CreatePostDto {
  @ApiProperty({
    description: '게시글 제목',
    example: '제목',
    maxLength: MAX_TITLE_LENGTH,
  })
  @IsNotEmpty()
  @IsString()
  @MaxLength(MAX_TITLE_LENGTH)
  title: string;

  @ApiPropertyOptional({
    description: '첨부파일 1 (UUID)',
    example: '123e4567-e89b-12d3-a456-426614174000',
    required: false,
    nullable: true,
  })
  @IsOptional()
  @IsUUID()
  fileId1?: null | string;
}
```

## What To Read Before Editing

- Read the target controller file end to end.
- Read the DTOs used by `@Body()`, `@Query()`, and response mapping.
- Read helper decorators used for auth or public access.
- Read interceptors, serializers, and shared response helpers when they change the runtime response envelope.
- Read shared schema helpers before writing inline schema by hand.
