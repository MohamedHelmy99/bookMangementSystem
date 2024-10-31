# API Documentation

This document provides details about the available API endpoints and their usage.

## Base URL

All endpoints are prefixed with `/api`

## Authentication Endpoints

### Register User
- **URL:** `/auth/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "message": "User registered successfully",
      "user_id": "integer"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Email already registered"
    }
    ```
    OR
    ```json
    {
      "message": "Username already taken"
    }
    ```

### Login
- **URL:** `/auth/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Login successful",
      "user_id": "integer"
    }
    ```
- **Error Response:**
  - **Code:** 401
  - **Content:**
    ```json
    {
      "message": "Invalid credentials"
    }
    ```

### Logout
- **URL:** `/auth/logout`
- **Method:** `POST`
- **Authentication:** Required
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Successfully logged out"
    }
    ```

## Books Endpoints

### Get All Books
- **URL:** `/books`
- **Method:** `GET`
- **Authentication:** Required
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "books": [
        {
          "id": "integer",
          "title": "string",
          "author": "string",
          "isbn": "string",
          "published_year": "integer"
        }
      ]
    }
    ```

### Get Single Book
- **URL:** `/books/<id>`
- **Method:** `GET`
- **Authentication:** Required
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "id": "integer",
      "title": "string",
      "author": "string",
      "isbn": "string",
      "published_year": "integer"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Book not found"
    }
    ```

### Create Book
- **URL:** `/books`
- **Method:** `POST`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "title": "string",
    "author": "string",
    "isbn": "string",
    "published_year": "integer"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "message": "Book created successfully",
      "book_id": "integer"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Book with this ISBN already exists"
    }
    ```

### Update Book
- **URL:** `/books/<id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "title": "string (optional)",
    "author": "string (optional)",
    "isbn": "string (optional)",
    "published_year": "integer (optional)"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Book updated successfully"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Book not found"
    }
    ```

### Delete Book
- **URL:** `/books/<id>`
- **Method:** `DELETE`
- **Authentication:** Required
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Book deleted successfully"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Book not found"
    }
    ```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication. The API uses JWT tokens for authentication, which are handled through HTTP-only cookies.

When a user logs in or registers, the API will set a JWT cookie that will be automatically included in subsequent requests. This cookie is automatically managed by the browser and will be used to authenticate requests to protected endpoints.

## Error Handling

The API returns appropriate HTTP status codes and error messages in JSON format for different types of errors:

- 200: Success
- 201: Resource created
- 400: Bad request
- 401: Unauthorized
- 404: Resource not found
- 500: Server error 