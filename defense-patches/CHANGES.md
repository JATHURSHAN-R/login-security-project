# Defense Patches

Three changes were applied to the Spring Boot Stock Management System to defend against brute-force attacks.

---

## Patch 1 — User Entity (User.java)

Added two fields to track failed login attempts and account lockout state.

**File:** `src/main/java/.../entity/User.java`

```java
@Column(name = "failed_login_attempts", nullable = false)
private int failedLoginAttempts = 0;

@Column(name = "locked_until")
private LocalDateTime lockedUntil;
```

Hibernate automatically created these columns in the `users` table via `spring.jpa.hibernate.ddl-auto=update`.

---

## Patch 2 — RateLimiterService.java (new file)

Created a new service that tracks request counts per IP address using a sliding window algorithm.

**File:** `src/main/java/.../service/RateLimiterService.java`

- Uses `ConcurrentHashMap` for thread-safe IP tracking
- Window: 1 minute
- Limit: 5 requests per IP per window
- Returns `true` (rate limited) when count exceeds limit

---

## Patch 3 — AuthServiceImpl.java

Updated the `login()` method with four new checks:

1. **Rate limit check** — rejects request with `RuntimeException` if IP is over limit
2. **Account lockout check** — rejects request if `lockedUntil` is in the future
3. **Failed attempt tracking** — increments `failedLoginAttempts` on wrong password; locks account for 15 minutes after 5 failures
4. **Counter reset** — clears `failedLoginAttempts` and `lockedUntil` on successful login

---

## Patch 4 — AuthController.java

Updated the `login()` endpoint to return `HTTP 429 Too Many Requests` specifically for rate limit errors, instead of the default `400 Bad Request`.

```java
if (e.getMessage().contains("Too many requests")) {
    return ResponseUtil.error(HttpStatus.TOO_MANY_REQUESTS, e.getMessage());
}
```

This allows the Python brute-forcer to correctly detect and handle rate limiting via status code.