# Out-of-bounds write in ipcz while deserializing message

| Field | Value |
|-------|-------|
| **Issue ID** | [504471167](https://issues.chromium.org/issues/504471167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** |  130.0.6710.2 |
| **CVE IDs** | CVE-2025-4609 |
| **Reporter** | bl...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2026-04-20 |
| **Bounty** | $35,000.00 |

## Description

---

### Report description

ipcz NodeLink::OnAddBlockBuffer missing sender guard allows renderer to inject attacker-controlled shared memory into broker buffer pool

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

`NodeLink::OnAddBlockBuffer()` (node\_link.cc:553) is missing the sender type check that every other privilege-bearing handler has. The result is that a compromised renderer can push arbitrary shared memory into the broker's buffer pool, and a second bug in `AcceptBypassLink` (router.cc:1174) lets the same renderer get the broker to adopt attacker-controlled routing state without going through the normal authorization check.

There's also a crash: send `AddBlockBuffer` with `block_size=64` and a 2MB mapping, and `checked_cast<int16_t>(32768)` fires `ABSL_HARDENING_ASSERT` in the broker process. One message, always crashes.

```
// Every other handler that touches privileged state:
bool NodeLink::OnReferNonBroker(msg::ReferNonBroker& refer) {
  if (remote_node_type_ != Node::Type::kNormal ||
      node()->type() != Node::Type::kBroker) { return false; }
  ...
}

// OnAddBlockBuffer — no check:
bool NodeLink::OnAddBlockBuffer(msg::AddBlockBuffer& add) {
  DriverMemoryMapping mapping =
      DriverMemory(add.TakeDriverObject(add.v0()->buffer)).Map();
  if (!mapping.is_valid()) { return false; }
  return memory().AddBlockBuffer(add.v0()->id, add.v0()->block_size,
                                 std::move(mapping));
}

```

The bypass auth short-circuit at router.cc:1174:

```
if (old_link->node_link() != &new_node_link &&
    !old_link->CanNodeRequestBypass(new_node_link.remote_node_name())) {
  return false;
}

```

When a renderer calls `BypassPeerWithLink` over its own broker↔renderer link, both sides are the same `NodeLink` object, so the condition is always false and `CanNodeRequestBypass` never runs. With attacker SHM already in the broker pool, this lets the renderer pre-write any `allowed_bypass_request_source` NodeName into the injected `RouterLinkState` — granting bypass authorization for an arbitrary node without going through `TryLockForBypass`.

The relay path (`DispatchRelayedMessage`, node\_link.cc:310) includes `msg::AddBlockBuffer::kId` so it's reachable there too.

---

**Environment**: Chromium trunk `ba94d9f045`, Linux x64

`args.gn`:

```
is_debug = true
is_asan = true
is_component_build = false
symbol_level = 1
dcheck_always_on = true

```

**Note**: The `[PoC]` output from `content_shell` requires a patch to `node.cc:AddConnection()` that simulates a compromised renderer calling `AddBlockBuffer` at connection time. In a real attack, a compromised renderer would craft and send the `AddBlockBuffer` IPC message directly — the broker has no guard to reject it. The vulnerability is in unmodified production code. Patch attached (`node.cc.patch`).

---

**Crash:**

```
$ ./out/ipcz-asan/ipcz_tests \
  --gtest_filter='NodeLinkTest.OnAddBlockBuffer_MissingBrokerGuard_CrashesReceiverProcess'
Note: Google Test filter = NodeLinkTest.OnAddBlockBuffer_MissingBrokerGuard_CrashesReceiverProcess
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from NodeLinkTest
[ RUN      ] NodeLinkTest.OnAddBlockBuffer_MissingBrokerGuard_CrashesReceiverProcess
ipcz_tests: ../../third_party/ipcz/src/util/safe_math.h:22: Dst ipcz::checked_cast(Src) [Dst = short, Src = unsigned long]: Assertion `false && "(__builtin_expect(false || (value <= std::numeric_limits<Dst>::max()), true))"' failed.
Aborted

```

**SHM injection:**

```
$ ./out/ipcz-asan/ipcz_tests \
  --gtest_filter='NodeLinkTest.OnAddBlockBuffer_ValidParams_AttackerShmInjectedIntoBrokerPool'
Note: Google Test filter = NodeLinkTest.OnAddBlockBuffer_ValidParams_AttackerShmInjectedIntoBrokerPool
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from NodeLinkTest
[ RUN      ] NodeLinkTest.OnAddBlockBuffer_ValidParams_AttackerShmInjectedIntoBrokerPool
[       OK ] NodeLinkTest.OnAddBlockBuffer_ValidParams_AttackerShmInjectedIntoBrokerPool (1 ms)
[----------] 1 test from NodeLinkTest (1 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (3 ms total)
[  PASSED  ] 1 test.

```

**Broker allocates from attacker SHM:**

```
$ ./out/ipcz-asan/ipcz_tests \
  --gtest_filter='NodeLinkTest.OnAddBlockBuffer_ContaminatesBlockAllocatorPool_AttackerShmAllocated'
Note: Google Test filter = NodeLinkTest.OnAddBlockBuffer_ContaminatesBlockAllocatorPool_AttackerShmAllocated
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from NodeLinkTest
[ RUN      ] NodeLinkTest.OnAddBlockBuffer_ContaminatesBlockAllocatorPool_AttackerShmAllocated
[       OK ] NodeLinkTest.OnAddBlockBuffer_ContaminatesBlockAllocatorPool_AttackerShmAllocated (1 ms)
[----------] 1 test from NodeLinkTest (1 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (2 ms total)
[  PASSED  ] 1 test.

```

**TOCTOU on allowed\_bypass\_request\_source:**

```
$ ./out/ipcz-asan/ipcz_tests \
  --gtest_filter='NodeLinkTest.OnAddBlockBuffer_TryLockForBypass_AttackerOverwritesAllowedSource'
Note: Google Test filter = NodeLinkTest.OnAddBlockBuffer_TryLockForBypass_AttackerOverwritesAllowedSource
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from NodeLinkTest
[ RUN      ] NodeLinkTest.OnAddBlockBuffer_TryLockForBypass_AttackerOverwritesAllowedSource
[       OK ] NodeLinkTest.OnAddBlockBuffer_TryLockForBypass_AttackerOverwritesAllowedSource (1 ms)
[----------] 1 test from NodeLinkTest (1 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (3 ms total)
[  PASSED  ] 1 test.

```

**Deterministic bypass via injected RouterLinkState:**

```
$ ./out/ipcz-asan/ipcz_tests \
  --gtest_filter='NodeLinkTest.OnAddBlockBuffer_DeterministicBypassViaInjectedLinkState'
Note: Google Test filter = NodeLinkTest.OnAddBlockBuffer_DeterministicBypassViaInjectedLinkState
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from NodeLinkTest
[ RUN      ] NodeLinkTest.OnAddBlockBuffer_DeterministicBypassViaInjectedLinkState
[       OK ] NodeLinkTest.OnAddBlockBuffer_DeterministicBypassViaInjectedLinkState (3 ms)
[----------] 1 test from NodeLinkTest (4 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (5 ms total)
[  PASSED  ] 1 test.

```

**Content Shell reproduction** (macOS arm64, `is_asan=true is_component_build=true symbol_level=1 target_cpu="arm64"`, `node.cc` patch applied):

```
$ ASAN_OPTIONS=detect_odr_violation=0 \
  "out/asan-vrp/Content Shell.app/Contents/MacOS/Content Shell" \
  --no-sandbox about:blank 2>&1 | grep -A4 '\[PoC\]'

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

[PoC] OnAddBlockBuffer — missing sender guard:
  renderer → broker: AddBlockBuffer(id=1, block_size=128)
  broker has NO guard; attacker SHM enters buffer_pool_
  65-128B broker allocations now served from attacker SHM

```

Fires once per renderer process on every launch.

---

**Fix:**

Crash path — validate before `BlockAllocator` construction:

```
if (mapping.bytes().size() / block_size > std::numeric_limits<int16_t>::max())
  return false;

```

Protocol fix: only accept `AddBlockBuffer` when there's an outstanding `RequestBlockCapacity` from that peer.

`AcceptBypassLink` (router.cc:1174): run `CanNodeRequestBypass` unconditionally, don't short-circuit on same-link identity.

[Issue 368208152](https://issues.chromium.org/issues/368208152) fix (M129, `c333ed995449`) covers a related pattern but is missing from trunk. CVE-2025-4609 covered `Transport::Deserialize`; `OnAddBlockBuffer` was out of scope.

---

**Attachments:**

- `node_link_test.cc` (lines 1666–1985)
- `node.cc.patch`

#### Impact analysis

A compromised renderer exploits this in three ways:

1. Deterministic browser process crash — A single `AddBlockBuffer(id, 64, 2MB_shm)` reaches the broker with no guard, triggering `checked_cast<int16_t>(32768)` → `ABSL_HARDENING_ASSERT` → `Aborted` in the browser process. One message, no preconditions, confirmed on Linux x64 and macOS arm64.
2. Broker memory disclosure — With `block_size=128`, attacker SHM becomes the sole source for 65–128 byte broker allocations (no 128-byte pool exists by default; node\_link\_memory.cc:108-148). Broker writes to `RouterLinkState` fragments — including `allowed_bypass_request_source` NodeName, link lock state, `routing_complexity_limit` — are directly readable from the attacker's mapping.
3. Bypass authorization state corruption — `AcceptBypassLink` accepts an attacker-controlled `RouterLinkState` fragment without running `CanNodeRequestBypass()` (same-link short-circuit at router.cc:1174). The `allowed_bypass_request_source` field in the broker's router becomes attacker-writable, corrupting bypass authorization decisions for that router.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7797.0 (dev/trunk, ba94d9f045)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

sm1ee, ksw9722

## Attachments

- [node.cc.patch](attachments/node.cc.patch) (application/octet-stream, 1.3 KB)
- [node_link_test.cc](attachments/node_link_test.cc) (application/octet-stream, 7.8 KB)

## Timeline

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504471167)*
