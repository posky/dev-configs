---
name: nestjs-swagger-jsdoc
description: Write and refine Swagger decorators and JSDoc in NestJS codebases. Use when Codex needs to document controllers, DTOs, services, utilities, or custom decorators with @nestjs/swagger and JSDoc, including ApiOperation/ApiResponse/ApiProperty usage, multipart or wrapped response schemas, and method descriptions with params, returns, and throws. If the user does not specify which file, symbol, or endpoint to document, ask which target to update before editing.
---

# NestJS Swagger JSDoc

## Overview

Use this skill to add or improve API documentation in NestJS projects without changing behavior.
Prefer existing project patterns over new abstractions, and keep documentation scoped to the exact target the user requested.

## Required Workflow

1. Confirm the target first.
2. If the user did not name a file, symbol, controller, DTO, service, or endpoint, ask which part to document before editing.
3. Read the target file end to end, then read directly referenced DTOs, response types, helper decorators, and response wrappers/helpers needed to document that target correctly.
4. If the runtime response shape is affected by an interceptor, serializer, or shared response envelope, read that path before writing Swagger annotations.
5. Reuse the repository's established Swagger and JSDoc style.
6. Edit only the explicitly requested scope unless the user asks for a broader sweep.
7. Keep the default documentation language in Korean unless the user explicitly asks for another language or the surrounding file clearly uses another language.

## Scope Rules

- Do not expand a request for one file into a whole module cleanup.
- Do not add JSDoc everywhere just because the project has `eslint-plugin-jsdoc`.
- Do not invent new response wrapper shapes. Document the real response shape already returned by the code.
- Do not replace reusable helpers such as pagination schema builders when the project already has them.

## Swagger Rules

### Controllers

- Add class-level tags with the existing tag constant or project convention.
- Apply the repository's auth decorator pattern when the endpoint is protected.
- Add `@ApiOperation` to each documented endpoint with a short summary and a concrete description.
- Add success and failure response decorators that match the actual code path.
- When the route returns a wrapped object or generic response, describe the wrapper shape rather than only the inner DTO.

### DTOs

- Add `@ApiProperty` or `@ApiPropertyOptional` to externally visible request and response DTO fields.
- Align Swagger metadata with validation and transformation decorators already present in the DTO.
- Reflect `enum`, `example`, `nullable`, array shape, and size limits only when they are supported by the code.
- Reuse existing constants for limits where the file already exposes them.

### Non-trivial Schemas

- For pagination, wrapped objects, or nested DTO references, prefer existing schema helpers such as `getSchemaPath` or repository-specific builders.
- For multipart endpoints, document `multipart/form-data`, request body schema, and file field expectations explicitly.
- For plain message responses, document the returned object shape instead of forcing a DTO when the project does not use one.

Read [references/swagger-patterns.md](./references/swagger-patterns.md) when you need concrete controller and DTO patterns.

## JSDoc Rules

- Prefer JSDoc on service methods, meaningful private helpers, utilities, and custom decorators.
- Skip trivial methods whose name and signature already make the behavior obvious.
- Describe domain behavior, key conditions, and failure cases, not just the type signature.
- Use `@param`, `@returns`, and `@throws` when they add real maintenance value.
- Keep descriptions Korean by default and match the terminology already used in the file.

Read [references/jsdoc-patterns.md](./references/jsdoc-patterns.md) when you need concrete method and helper patterns.

## Python Tooling

- If this skill ever needs to run a bundled Python helper or validator, use `uv run` instead of `python`.
- Resolve bundled helper paths from the skill directory first.
- Example:
  ```bash
  uv run /path/to/nestjs-swagger-jsdoc/scripts/example.py
  ```

## Completion Checklist

- Verify the documented target was explicitly requested or confirmed.
- Verify Swagger annotations match the actual request and response behavior.
- Verify wrapped or transformed responses against interceptors, serializers, or shared envelope helpers before documenting the schema.
- Verify JSDoc text matches method behavior, parameters, return values, and thrown domain errors.
- Keep edits minimal and within the requested scope.
