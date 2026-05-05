# API Documentation — NoteFlow

## Base URL

API URL prefix from `config/urls.py` is:

```text
/api/
```

Local development URL when using `runserver` on the default port:

```text
http://127.0.0.1:8000/api/
```

Docker Compose exposes the Django `web` service on port `8000` and nginx on port `80`:

```text
http://127.0.0.1:8000/api/
http://127.0.0.1/api/
```

All DRF router endpoints in the current project use trailing slash.

Verified local behavior with `python manage.py runserver` on `http://127.0.0.1:8000/`:

- `GET /`: `404`
- `GET /notes/`: `200`
- `GET /api/note/?page=1` without authentication: `403`
- `GET /notes/register/`: works
- `GET /notes/login/`: works

## Authorization

JWT is Missing / Not found in the current code.

- `POST /api/token/`: Missing / Not found.
- `POST /api/token/refresh/`: Missing / Not found.
- `djangorestframework-simplejwt`: Missing / Not found in `requirements.txt`.
- `DEFAULT_AUTHENTICATION_CLASSES` with JWT authentication: Missing / Not found in `settings.py`.

The frontend-requested JWT header would be:

```http
Authorization: Bearer <access_token>
```

However, this header is not supported by the current code unless JWT authentication is added later.

Current DRF view permissions still require authentication for most API endpoints. Since no custom DRF authentication classes are configured in `settings.py`, DRF defaults apply unless overridden outside this repository. In the checked local server, `GET /api/note/?page=1` without authentication returns `403`.

## Pagination

`NoteViewSet` uses `NotePagination`:

- default page size: `5`
- query param for page number: `page`
- query param for page size: `page_size`
- max page size: `100`

Paginated note responses use this shape:

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

## Data Objects

### Note response fields

Response fields documented from `NoteSerializer` and the `Note` model. The declared `date` serializer field is excluded from response examples because it is Missing / Not found on the `Note` model:

```json
{
  "id": 1,
  "name": "Example note",
  "description": "Example description",
  "category": 1,
  "category_name": "Category name",
  "files": [
    {
      "id": 1,
      "file": "/media/notes/files/example.pdf",
      "name": "example.pdf",
      "url": "/media/notes/files/example.pdf",
      "uploaded_at": "2026-04-01T18:17:00Z"
    }
  ],
  "created_at": "2026-04-01T18:17:00Z",
  "updated_at": "2026-04-01T18:17:00Z",
  "user": "username",
  "likes_count": 0,
  "isliked": false,
  "views_count": 0,
  "tags": [1]
}
```

Important serializer/model mismatch:

- `date` exists in `NoteSerializer`.
- `date` is Missing / Not found on the `Note` model.
- The existing template JavaScript submits `date` to `POST /api/note/`.
- This may cause create/update requests to fail if `date` is sent.

### Category response fields

Fields declared by `CategorySerializer`:

```json
{
  "id": 1,
  "name": "Category name",
  "slug": "category-slug"
}
```

### User response fields

Fields declared by `UserSerializer`:

```json
{
  "id": 1,
  "username": "username"
}
```

Password fields are Missing / Not found in the API serializer.

## Endpoints

### POST /api/token/

Purpose: obtain JWT access and refresh tokens.

Auth required: not required, but endpoint is Missing / Not found.

Query params: none found.

Request body: Missing / Not found.

Success response example: Missing / Not found.

Possible errors:

- 404: endpoint is not registered in `urls.py`.

### POST /api/token/refresh/

Purpose: refresh JWT access token.

Auth required: not required, but endpoint is Missing / Not found.

Query params: none found.

Request body: Missing / Not found.

Success response example: Missing / Not found.

Possible errors:

- 404: endpoint is not registered in `urls.py`.

### GET /api/

Purpose: DRF router API root.

Auth required: not required by project code for the router root.

Query params: none found.

Request body: none.

Success response example:

```json
{
  "user": "http://127.0.0.1:8000/api/user/",
  "note": "http://127.0.0.1:8000/api/note/",
  "category": "http://127.0.0.1:8000/api/category/"
}
```

Possible errors:

- 404: wrong API prefix or trailing slash.

### GET /api/note/

Purpose: list notes. The current `list()` implementation also creates `View` records for notes in the returned page when the request user is authenticated.

Auth required: yes.

Query params:

- `page`: page number.
- `page_size`: page size, max `100`.
- `search`: searches `name`, `description`, `user__username`.
- `from`: filters by `created_at__date__gte`.
- `to`: filters by `created_at__date__lte`.
- `category`: filters by exact category name.

Request body: none.

Success response example:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Example note",
      "description": "Example description",
      "category": 1,
      "category_name": "Category name",
      "files": [],
      "created_at": "2026-04-01T18:17:00Z",
      "updated_at": "2026-04-01T18:17:00Z",
      "user": "username",
      "likes_count": 0,
      "isliked": false,
      "views_count": 0,
      "tags": []
    }
  ]
}
```

Possible errors:

- 400: invalid query value.
- 403: request is not authenticated in the checked local server.

### POST /api/note/

Purpose: create note for the authenticated user.

Auth required: yes.

Query params: none found.

Request body: `multipart/form-data` is supported by configured DRF parsers. JSON is configured too, but `files_upload` is a required write-only file list.

Fields:

- `name`: required, min length `3`, max length `100`.
- `description`: optional, can be blank.
- `category`: optional category id.
- `tags`: optional list of tag ids.
- `files_upload`: required list of uploaded files.
- `date`: declared by serializer, but Missing / Not found on `Note` model.

Success response example:

```json
{
  "id": 1,
  "name": "Example note",
  "description": "Example description",
  "category": 1,
  "category_name": "Category name",
  "files": [
    {
      "id": 1,
      "file": "/media/notes/files/example.pdf",
      "name": "example.pdf",
      "url": "/media/notes/files/example.pdf",
      "uploaded_at": "2026-04-01T18:17:00Z"
    }
  ],
  "created_at": "2026-04-01T18:17:00Z",
  "updated_at": "2026-04-01T18:17:00Z",
  "user": "username",
  "likes_count": 0,
  "isliked": false,
  "views_count": 0,
  "tags": []
}
```

Possible errors:

- 400: validation error, missing `files_upload`, `name` shorter than 3 characters, invalid category id, invalid tag id, or serializer/model mismatch if `date` is sent.
- 403: request is not authenticated in the checked local server.

### GET /api/note/{id}/

Purpose: retrieve one note by id. The current `retrieve()` implementation also creates a `View` record for the note when the request user is authenticated.

Auth required: yes.

Query params: none found.

Request body: none.

Success response example:

```json
{
  "id": 1,
  "name": "Example note",
  "description": "Example description",
  "category": 1,
  "category_name": "Category name",
  "files": [],
  "created_at": "2026-04-01T18:17:00Z",
  "updated_at": "2026-04-01T18:17:00Z",
  "user": "username",
  "likes_count": 0,
  "isliked": false,
  "views_count": 1,
  "tags": []
}
```

Possible errors:

- 403: request is not authenticated in the checked local server.
- 404: note id does not exist.

### PUT /api/note/{id}/

Purpose: replace a note owned by the authenticated user.

Auth required: yes; object write permission requires note author.

Query params: none found.

Request body: same serializer fields as `POST /api/note/`. For full update, required serializer fields must be sent.

Success response example: same shape as `GET /api/note/{id}/`.

Possible errors:

- 400: validation error.
- 403: request is not authenticated in the checked local server, or authenticated user is not the note author.
- 404: note id does not exist.

### PATCH /api/note/{id}/

Purpose: partially update a note owned by the authenticated user.

Auth required: yes; object write permission requires note author.

Query params: none found.

Request body: any subset of writable note fields:

- `name`
- `description`
- `category`
- `tags`
- `files_upload`
- `date`, but it is Missing / Not found on the `Note` model.

Success response example: same shape as `GET /api/note/{id}/`.

Possible errors:

- 400: validation error.
- 403: request is not authenticated in the checked local server, or authenticated user is not the note author.
- 404: note id does not exist.

### DELETE /api/note/{id}/

Purpose: delete a note owned by the authenticated user.

Auth required: yes; object write permission requires note author.

Query params: none found.

Request body: none.

Success response example:

```text
204 No Content
```

Possible errors:

- 403: request is not authenticated in the checked local server, or authenticated user is not the note author.
- 404: note id does not exist.

### GET /api/note/{id}/like/

Purpose: toggle like for the authenticated user on a note.

Auth required: yes.

Query params: none found.

Request body: none.

Success response examples:

```json
{
  "liked": true
}
```

```json
{
  "liked": false
}
```

Status codes:

- `201 Created`: like was created.
- `200 OK`: existing like was removed.

Possible errors:

- 403: request is not authenticated in the checked local server.
- 404: note id does not exist.

### POST /api/note/{id}/like/

Purpose: same as `GET /api/note/{id}/like/`; toggles like for the authenticated user on a note.

Auth required: yes.

Query params: none found.

Request body: none.

Success response examples:

```json
{
  "liked": true
}
```

```json
{
  "liked": false
}
```

Possible errors:

- 403: request is not authenticated in the checked local server.
- 404: note id does not exist.

### GET /api/note/liked/

Purpose: list notes liked by the authenticated user.

Auth required: yes.

Query params:

- `page`: page number.
- `page_size`: page size, max `100`.

Request body: none.

Success response example:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Example note",
      "description": "Example description",
      "category": 1,
      "category_name": "Category name",
      "files": [],
      "created_at": "2026-04-01T18:17:00Z",
      "updated_at": "2026-04-01T18:17:00Z",
      "user": "username",
      "likes_count": 1,
      "isliked": true,
      "views_count": 0,
      "tags": []
    }
  ]
}
```

Possible errors:

- 403: request is not authenticated in the checked local server.

### GET /api/category/

Purpose: list categories.

Auth required: yes.

Query params: none found.

Request body: none.

Success response example:

```json
[
  {
    "id": 1,
    "name": "Category name",
    "slug": "category-slug"
  }
]
```

Possible errors:

- 403: request is not authenticated in the checked local server.

### GET /api/category/{id}/

Purpose: retrieve one category by id.

Auth required: yes.

Query params: none found.

Request body: none.

Success response example:

```json
{
  "id": 1,
  "name": "Category name",
  "slug": "category-slug"
}
```

Possible errors:

- 403: request is not authenticated in the checked local server.
- 404: category id does not exist.

### GET /api/user/

Purpose: list users.

Auth required: yes.

Query params: none found.

Request body: none.

Success response example:

```json
[
  {
    "id": 1,
    "username": "username"
  }
]
```

Possible errors:

- 403: request is not authenticated in the checked local server.

### POST /api/user/

Purpose: create a user through `UserViewSet`.

Auth required: no.

Query params: none found.

Request body:

```json
{
  "username": "username"
}
```

Success response example:

```json
{
  "id": 1,
  "username": "username"
}
```

Possible errors:

- 400: missing username or duplicate username.

Important limitation:

- Password fields are Missing / Not found in `UserSerializer`.
- This is not equivalent to the web registration form at `POST /notes/register/`.

### GET /api/user/{id}/

Purpose: retrieve one user by id.

Auth required: yes.

Query params: none found.

Request body: none.

Success response example:

```json
{
  "id": 1,
  "username": "username"
}
```

Possible errors:

- 403: request is not authenticated in the checked local server.
- 404: user id does not exist.

### PUT /api/user/{id}/

Purpose: replace a user object.

Auth required: yes; current `UserViewSet` uses `IsOwner` for update.

Query params: none found.

Request body:

```json
{
  "username": "new_username"
}
```

Success response example:

```json
{
  "id": 1,
  "username": "new_username"
}
```

Possible errors:

- 400: validation error.
- 403: request is not authenticated in the checked local server, or owner permission fails.
- 404: user id does not exist.

Important limitation:

- `IsOwner` checks `obj.user == request.user`.
- Django `User` objects do not have a `user` field in the current model.
- User update/delete permissions may not work as intended.

### PATCH /api/user/{id}/

Purpose: partially update a user object.

Auth required: yes; current `UserViewSet` uses `IsOwner` for partial update.

Query params: none found.

Request body:

```json
{
  "username": "new_username"
}
```

Success response example:

```json
{
  "id": 1,
  "username": "new_username"
}
```

Possible errors:

- 400: validation error.
- 403: request is not authenticated in the checked local server, or owner permission fails.
- 404: user id does not exist.

### DELETE /api/user/{id}/

Purpose: delete a user object.

Auth required: yes; current `UserViewSet` uses `IsOwner` for destroy.

Query params: none found.

Request body: none.

Success response example:

```text
204 No Content
```

Possible errors:

- 403: request is not authenticated in the checked local server, or owner permission fails.
- 404: user id does not exist.

## Web Pages

The following non-API Django template routes exist under `/notes/`:

- `GET /notes/`
- `GET /notes/create/`
- `GET /notes/register/`
- `POST /notes/register/`
- `GET /notes/login/`
- `POST /notes/login/`
- `POST /notes/logout/`
- `GET /notes/{slug}/`

These are server-rendered pages, not JSON API endpoints.

## File Uploads

Standalone file upload endpoints are Missing / Not found.

Existing upload behavior is attached to note create/update:

- `POST /api/note/`
- `PUT /api/note/{id}/`
- `PATCH /api/note/{id}/`

The serializer accepts `files_upload` as a write-only list of uploaded files and returns uploaded files through the read-only `files` field.

## Missing for frontend

- JWT login endpoint is Missing / Not found: `POST /api/token/`.
- JWT refresh endpoint is Missing / Not found: `POST /api/token/refresh/`.
- `Authorization: Bearer <access_token>` is not supported by current settings.
- API registration with password is Missing / Not found; `UserSerializer` only exposes `id` and `username`.
- Current API profile endpoint is Missing / Not found.
- Standalone file upload endpoint is Missing / Not found.
- `date` is declared in `NoteSerializer` and submitted by existing JS, but `date` is Missing / Not found on `Note` model.
- Tag API endpoints are Missing / Not found, although `Tag` model and `TagSerializer` exist.
- Category creation/update/delete API endpoints are Missing / Not found; `CategoryViewSet` is read-only.
- User update/delete permissions may not work as intended because `IsOwner` checks `obj.user`, but Django `User` has no `user` field.
