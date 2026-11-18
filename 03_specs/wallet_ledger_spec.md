# VELOOP Rewards — Wallet Ledger Specification

> **PROPOSED SCHEMA — NOT YET IMPLEMENTED.**
> This table supersedes the existing `Wallet_Transactions` table in
> `05_data_model/er_diagram.dbml`, which is a single-entry design that
> cannot enforce balance invariants or support reversal tracking. If any
> production code currently writes to `Wallet_Transactions`, a migration
> is required (see §5).

---

## 1. Purpose and Three Non-Negotiable Invariants

The `ledger_entries` table establishes an immutable, double-entry financial ledger for all virtual economies (XP, Gems, Tokens, and Virtual Currency) in VELOOP Rewards. A single-entry model only records point adjustments without preserving financial conservation or enabling deterministic audits. Double-entry bookkeeping guarantees that every point created, transferred, or liquidated has an offsetting source and destination.

Three fundamental invariants govern this schema:

- **INV-1: Balance Conservation**:
  For every `transaction_id`, $\sum (\text{amount WHERE direction='debit'}) = \sum (\text{amount WHERE direction='credit'})$. Money is conserved. No currency is created or destroyed without balancing system accounts.
- **INV-2: Append-Only Immutability**:
  Entries are append-only. An entry can be reversed (via a new entry with `reversal_of` set) but never edited or deleted.
- **INV-3: Event Provenance & Lineage**:
  Every entry has a `reference_type` and `reference_id` pointing to the business event (`task_reward`, `daily_reward`, `spin`, `referral`, `withdrawal`, `reversal`, `adjustment`) that caused it.

---

## 2. Entity: ledger_entries

The `ledger_entries` entity stores discrete accounting debit and credit postings. Every business transaction comprises two or more balanced ledger entries sharing the same `transaction_id`.

### Field Specifications

| Field Name | Data Type | Required | Allowed Values | Validation Rules | Example Value | Sensitivity Classification |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **`entry_id`** | String (PK) | Yes | Alphanumeric string | Unique primary key; format `ENT_` + 6 or more alphanumeric characters | `ENT_001928` | Internal |
| **`transaction_id`** | String | Yes | Alphanumeric string | Non-null; groups balancing entries; format `TXN_` + UUIDv4 or timestamped hash | `TXN_982347102938` | Internal |
| **`user_id`** | String (FK) | Yes | Matches `Users.user_id` | Foreign key referencing `Users.user_id`; system accounts use reserved entity IDs | `VLUSR000102` | Internal |
| **`account_type`** | Enum | Yes | `user_wallet`, `reward_pool`, `system_clearing`, `withdrawal_clearing` | Non-null categorical accounting classification | `user_wallet` | Internal |
| **`direction`** | Enum | Yes | `debit`, `credit` | Non-null; indicates balance deduction or addition | `credit` | Internal |
| **`amount`** | Decimal(18,4) | Yes | Positive numeric values | Strictly $> 0.0000$; 4-decimal precision; non-null | `50.0000` | **Restricted** |
| **`currency_unit`** | Enum | Yes | `VE`, `XP`, `GEM`, `TOKEN` | Non-null denomination; default `XP` | `XP` | Internal |
| **`balance_after`** | Decimal(18,4) | Nullable | Numeric $\ge 0.0000$ | Running balance snapshot post-commit; populated only for `account_type='user_wallet'` | `1250.0000` | **Restricted** |
| **`created_at`** | Timestamp with TZ | Yes | ISO 8601 UTC | Monotonic server timestamp; default `CURRENT_TIMESTAMP` | `2026-09-15T14:32:00.000Z` | Internal |
| **`reference_type`** | Enum | Yes | `task_reward`, `daily_reward`, `spin`, `referral`, `withdrawal`, `reversal`, `adjustment` | Non-null business origin domain | `task_reward` | Internal |
| **`reference_id`** | String | Yes | Alphanumeric string | Foreign reference ID to originating business event (`activity_id`, `withdrawal_id`, `referral_id`, etc.) | `ACT_004912` | Internal |
| **`reversal_of`** | String (FK) | Nullable | Matches `ledger_entries.entry_id` | Nullable pointer; required if `reference_type = 'reversal'`, pointing to original `entry_id` | `ENT_001920` | Internal |
| **`status`** | Enum | Yes | `posted`, `reversed` | Operational status of entry; default `posted` | `posted` | Internal |
| **`correlation_id`** | String | Nullable | Alphanumeric string | Optional distributed tracing ID spanning client requests, microservices, and gateway webhooks | `CORR_9182736450` | Internal |

> **Sensitivity Classification Policy**:
> - `amount` and `balance_after` are classified as **Restricted** because they expose user financial balances and platform liability balances.
> - All other columns are classified as **Internal** for operational analytics and audit verification.

---

## 3. Balance Invariant Enforcement (INV-1)

To guarantee that money is strictly conserved, VELOOP requires a defense-in-depth enforcement architecture operating across three distinct operational layers:

### A) Database Constraints & Deferred Verification
At the database layer, transactions committing to `ledger_entries` must evaluate zero net balance across the `transaction_id`. For databases supporting deferred constraints (e.g., PostgreSQL), a deferred constraint trigger validates balance neutrality at transaction commit:

```sql
-- Database-level check trigger on ledger commit
CREATE OR REPLACE FUNCTION verify_transaction_balance() 
RETURNS TRIGGER AS $$
DECLARE
    net_imbalance DECIMAL(18,4);
BEGIN
    SELECT SUM(CASE WHEN direction = 'debit' THEN amount ELSE -amount END)
    INTO net_imbalance
    FROM ledger_entries
    WHERE transaction_id = NEW.transaction_id;

    IF ABS(net_imbalance) > 0.0001 THEN
        RAISE EXCEPTION 'INV-1 Violation: Transaction % is imbalanced by %', 
            NEW.transaction_id, net_imbalance;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER trg_verify_ledger_balance
AFTER INSERT ON ledger_entries
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION verify_transaction_balance();
```

### B) Nightly Reconciliation Query
Every night at 00:05 UTC, an automated financial integrity job executes across all transactions posted in the previous 24 hours. Any non-zero imbalance triggers a P1 critical engineering and finance incident:

```sql
SELECT transaction_id,
       SUM(CASE WHEN direction='debit' THEN amount ELSE -amount END)
         AS imbalance
FROM ledger_entries
GROUP BY transaction_id
HAVING ABS(imbalance) > 0.0001;
```

### C) Application-Layer Pre-Commit Validation
Prior to dispatching SQL batch inserts to the database, the wallet service constructs ledger entries in atomic pairs (or multi-leg groups) inside an in-memory builder. The builder validates that $\sum \text{debits} == \sum \text{credits}$ before opening the database connection. If any imbalance exists, the request aborts before network transmission, returning an HTTP 500 internal error.

---

## 4. KPI Unblock Queries

The introduction of `ledger_entries` resolves critical analytical blockers, enabling unhindered computation of financial, task reward, and reversal metrics:

### K45 — Wallet Credits Total
*Measures the aggregate volume of currency credited to user wallets across all reward and platform mechanisms.*

```sql
-- K45: Wallet credits total
SELECT 
    currency_unit,
    SUM(amount) AS total_wallet_credits
FROM ledger_entries
WHERE account_type = 'user_wallet'
  AND direction = 'credit'
  AND status = 'posted'
GROUP BY currency_unit;
```

### K29 — Average Reward per Completed Task
*Computes the mean numeric reward credited to user wallets for validated task completions.*

```sql
-- K29: Average reward per completed task
SELECT 
    COUNT(DISTINCT le.reference_id) AS rewarded_completed_tasks,
    SUM(le.amount) AS total_task_rewards_credited,
    ROUND(SUM(le.amount) / NULLIF(COUNT(DISTINCT le.reference_id), 0), 2) AS avg_reward_per_completed_task
FROM ledger_entries le
WHERE le.account_type = 'user_wallet'
  AND le.direction = 'credit'
  AND le.reference_type = 'task_reward'
  AND le.status = 'posted';
```

*Alternative joined implementation linking to `task_activity`:*
```sql
-- K29: Average reward per completed task (joined to task_activity)
SELECT 
    COUNT(ta.activity_id) AS completed_tasks,
    SUM(le.amount) AS total_task_rewards_credited,
    ROUND(SUM(le.amount) / NULLIF(COUNT(ta.activity_id), 0), 2) AS avg_reward_per_completed_task
FROM task_activity ta
JOIN ledger_entries le 
  ON ta.activity_id = le.reference_id
 AND le.reference_type = 'task_reward'
 AND le.account_type = 'user_wallet'
 AND le.direction = 'credit'
 AND le.status = 'posted'
WHERE ta.task_status = 'Completed';
```

### K30 — Reward Distribution by Task Type
*Breaks down distributed rewards across categorical task groupings.*

```sql
-- K30: Reward distribution by task_type
SELECT 
    COALESCE(tm.task_category, ta.task_category, 'Unknown') AS task_category,
    COUNT(le.entry_id) AS reward_payout_count,
    SUM(le.amount) AS total_reward_amount,
    ROUND(SUM(le.amount) * 100.0 / SUM(SUM(le.amount)) OVER (), 2) AS pct_of_total_rewards
FROM ledger_entries le
JOIN task_activity ta 
  ON le.reference_id = ta.activity_id
 AND le.reference_type = 'task_reward'
 AND le.account_type = 'user_wallet'
 AND le.direction = 'credit'
 AND le.status = 'posted'
LEFT JOIN task_master tm
  ON ta.task_id = tm.task_id
GROUP BY COALESCE(tm.task_category, ta.task_category, 'Unknown')
ORDER BY total_reward_amount DESC;
```

### K32 — Reward Reversals (Count and %)
*Tracks the volume and proportion of reward credits that were subsequently reversed due to fraud or dispute.*

```sql
-- K32: Reward reversals (count and %)
SELECT 
    COUNT(CASE WHEN reference_type = 'reversal' OR reversal_of IS NOT NULL THEN 1 END) AS reversal_count,
    COUNT(*) AS total_ledger_entries,
    ROUND(
        COUNT(CASE WHEN reference_type = 'reversal' OR reversal_of IS NOT NULL THEN 1 END) * 100.0 
        / NULLIF(COUNT(*), 0), 
        4
    ) AS reversal_rate_pct,
    SUM(CASE WHEN reference_type = 'reversal' THEN amount ELSE 0 END) AS total_reversed_amount
FROM ledger_entries
WHERE account_type = 'user_wallet';
```

---

## 5. Migration Path from Wallet_Transactions to ledger_entries

To transition safely from the legacy single-entry `Wallet_Transactions` design to the double-entry `ledger_entries` schema without financial disruption or data loss, engineering must execute the following five-step migration:

1. **Step 1: Parallel Table Provisioning**
   Create `ledger_entries` in the production database alongside `Wallet_Transactions` with appropriate indexes on `(transaction_id)`, `(user_id, account_type)`, and `(reference_type, reference_id)`.
2. **Step 2: Historic Dual-Leg Backfill**
   Backfill historic rows: every row in `Wallet_Transactions` becomes at least 2 balancing rows in `ledger_entries`. For credits, debit `reward_pool` (or `system_clearing`) and credit `user_wallet`. For debits, debit `user_wallet` and credit `withdrawal_clearing`.
3. **Step 3: Baseline Reconciliation & Discrepancy Resolution**
   Reconcile opening balances against `Users.xp_balance`. The 10,941 XP discrepancy between recorded user balances and transaction sums (documented in Governance Assumption A009) must be formally reconciled and resolved first — do not migrate into an unreconciled state.
4. **Step 4: 30-Day Dual-Run Shadow Period**
   Run dual writes to both tables in parallel for 30 days. Execute the nightly reconciliation query (§3.B) continuously. If zero discrepancies occur over 30 consecutive days, switch all read traffic and reporting queries to `ledger_entries`.
5. **Step 5: Deprecation & Audit Preservation**
   Mark `Wallet_Transactions` as deprecated (soft deprecation; disable write endpoints; retain read-only table permissions; never hard delete). Keep `Wallet_Transactions` permanently for statutory audit trail and compliance verification.

---

## Data Authenticity Statement
This wallet ledger specification was prepared using simulated data created for analytical testing and product architecture modeling. No real financial ledgers, banking rails, payment gateway accounts, or monetary disbursements were accessed, analyzed, or included. All metrics, transaction models, and KPI formulas reflect simulated test environments.
