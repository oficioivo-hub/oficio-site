# Webhook delivery and retries

When an event occurs, we send a `POST` request to every endpoint registered for that
event type. Delivery is asynchronous: the response to your API call does not wait for
your endpoint.

## Success criteria

An endpoint is considered to have accepted an event when it returns any `2xx` status
code within 10 seconds. Any other outcome — a non-`2xx` status, a timeout, or a
connection error — counts as a failed attempt.

## Retry schedule

Failed deliveries are retried up to 8 times over 24 hours, using exponential backoff
with jitter:

| Attempt | Delay after previous attempt |
|---|---|
| 1 | immediate |
| 2 | 30 seconds |
| 3 | 2 minutes |
| 4 | 10 minutes |
| 5 | 1 hour |
| 6 | 3 hours |
| 7 | 6 hours |
| 8 | 12 hours |

After the eighth failed attempt the event is marked `exhausted` and no further attempts
are made.

## Idempotency

Every event carries a unique `event_id` that stays the same across retries. Your
endpoint must treat repeated deliveries of the same `event_id` as the same event. We
recommend storing processed IDs for at least 7 days.

## Ordering

We do not guarantee ordering. Two events created milliseconds apart may arrive in
either order. If your integration depends on order, compare the `created_at` field
rather than relying on arrival time.

## Disabling an endpoint

An endpoint that fails continuously for 72 hours is disabled automatically. We email
the account owner and keep the failed events for 30 days. Re-enabling the endpoint does
not replay them; you can replay events manually from the dashboard.

## Testing

Use the dashboard's "Send test event" button to deliver a synthetic `ping` event. Test
events follow the same retry schedule but are excluded from the automatic disable rule.
