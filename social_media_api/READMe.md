1. **Model Changes** (CustomUser updates).
2. **New Endpoints** (follow, unfollow, feed).
3. **Authentication requirements**.
4. **Example requests/responses**.

# 📘 API Documentation

## **User Model Changes**

````python

### 🔹 Key Additions:

- `bio`: User biography.
- `profile_picture`: Optional user profile picture.
- `followers`: Many-to-many relationship for user follow system.

---

## **Authentication**

All endpoints require **JWT Authentication**.
Include your access token in headers:

```http
Authorization: Bearer <your_token>
````

---

## **Endpoints**

### 🔹 **Follow a User**

`POST /api/accounts/<int:user_id>/follow/`

**Description:** Allows the authenticated user to follow another user.

**Request Example:**

```http
POST /api/accounts/5/follow/
Authorization: Bearer <token>
```

**Response Example:**

```json
{
  "message": "You are now following user 5"
}
```

---

### 🔹 **Unfollow a User**

`POST /api/accounts/<int:user_id>/unfollow/`

**Description:** Allows the authenticated user to unfollow another user.

**Request Example:**

```http
POST /api/accounts/5/unfollow/
Authorization: Bearer <token>
```

**Response Example:**

```json
{
  "message": "You unfollowed user 5"
}
```

---

### 🔹 **Get User Feed**

`GET /api/accounts/feed/`

**Description:** Returns posts from users that the authenticated user follows.

**Request Example:**

```http
GET /api/accounts/feed/
Authorization: Bearer <token>
```

**Response Example:**

```json
[
  {
    "id": 12,
    "author": "john_doe",
    "content": "My first post!",
    "created_at": "2025-08-22T09:00:00Z"
  },
  {
    "id": 13,
    "author": "mary_smith",
    "content": "Excited to join!",
    "created_at": "2025-08-22T09:30:00Z"
  }
]
```

---

## **Notes**

- Users cannot follow themselves.
- Duplicate follows are prevented.
- Feed only shows posts from users you follow.
- Admin panel supports managing custom users (`bio`, `profile_picture`, `followers`).

## 👍 Likes

### Like a Post

`POST /posts/<id>/like/`

Request:

```json
{}
```
