# Project Notes — Login Security Project

## Target Application

- **Name:** Stock Management System
- **Repo:** https://github.com/JATHURSHAN-R/Stock-Management-System
- **Stack:** Spring Boot, MySQL, Java 17
- **Auth endpoint:** `POST /api/auth/login`
- **Auth type:** Stateless REST API — JSON credentials, token response (no CSRF)

---

## Attack Flow

```
1. Read username and wordlist from CLI arguments
2. For each password in wordlist:
   a. POST /api/auth/login with JSON body
   b. Check response:
      200 + success:true  → correct password found, stop
      400                 → wrong password, try next
      429                 → rate limited, wait 5 seconds, retry same password
3. Print result
```

---

## Detection Logic

| HTTP Status | Body | Meaning | Action |
|-------------|------|---------|--------|
| 200 | `success: true` | Correct password | Stop, report |
| 400 | `success: false` | Wrong password | Next attempt |
| 429 | `Too many requests` | Rate limited | Wait, retry |

---

## Defense Design Decisions

**Why ConcurrentHashMap for rate limiting?**
Spring Boot handles requests on multiple threads simultaneously. A regular `HashMap` would have race conditions — two threads could read the same count and both increment from the same base value. `ConcurrentHashMap.merge()` is atomic, so counts are always accurate.

**Why in-memory rate limiting instead of a database?**
For a demo project, in-memory is simpler and faster. The tradeoff is that the counter resets when the app restarts. In production, Redis would be used for persistent distributed rate limiting.

**Why 15-minute lockout?**
Long enough to make brute-forcing impractical, short enough that a legitimate user who mistyped their password isn't locked out for hours. Production systems typically use progressive lockout (5 min → 15 min → 1 hour).

**Why check rate limit before account lockout?**
Rate limiting is the first line of defense — it stops the request at the IP level before any database lookup happens. This reduces database load during an attack.

---

## Key Concepts Learned

- HTTP is stateless — every request starts from zero
- REST APIs use JSON + tokens instead of form submissions + CSRF tokens
- Status codes are the signal: 200/400/429 each mean something specific
- `requests.Session()` handles cookies automatically across calls
- `allow_redirects=False` is needed for traditional form-based login detection
- `ConcurrentHashMap` is required for thread-safe shared state in Java
- JPA `ddl-auto=update` automatically migrates schema when entity fields change

---

## Legal Scope

All testing was performed against a locally hosted application on the author's own machine. No external systems were targeted at any point.