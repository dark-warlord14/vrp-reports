# Heap-Use-After-Free via stale set iterator dereference in HostResolverDnsTask::OnTransactionSorted

| Field | Value |
|-------|-------|
| **Issue ID** | [501792454](https://issues.chromium.org/issues/501792454) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network>DoH |
| **Platforms** | Windows |
| **Chrome Version** | 148.0.7763.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | er...@google.com |
| **Created** | 2026-04-12 |
| **Bounty** | $4,000.00 |

## Description

# VRP Report

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

Please provide a brief explanation of the security issue.

### Summary

Use-after-free in `HostResolverDnsTask::OnTransactionSorted()` where a
`std::set<TransactionInfo>::iterator` is captured by an async address-sort
callback and dereferenced after the underlying set element has been erased
by `CancelNonFatalTransactions()`.

### Analysis

Chrome's DNS resolver sorts address results (RFC 6724) after each transaction
completes via an async `AddressSorter` callback. The bug is in how
`HostResolverDnsTask` captures a `std::set` iterator into that callback —
the iterator can be invalidated by a concurrent transaction cancellation
before the callback fires.

[`SortTransactionAndHandleResults()`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=710)
re-inserts a completed A-record `TransactionInfo` back into
[`transactions_in_progress_`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.h;l=245)
(a `std::set`) and captures the resulting iterator in the closure passed to
`AddressSorter::Sort()`:

```
// host_resolver_dns_task.cc:740-749
auto insertion_result =
    transactions_in_progress_.insert(std::move(transaction_info));

client_->GetAddressSorter()->Sort(
    endpoints_to_sort,
    base::BindOnce(&HostResolverDnsTask::OnTransactionSorted,
                   weak_ptr_factory_.GetWeakPtr(),
                   insertion_result.first,          // ← iterator captured
                   std::move(transaction_results)));

```

If a subsequent transaction (e.g. AAAA) fails non-fatally while a
`kFatalOrEmpty` transaction (HTTPS) is still pending,
[`CancelNonFatalTransactions()`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=973-979)
erases the re-inserted A entry from the set, freeing its tree node:

```
// host_resolver_dns_task.cc:979
std::erase_if(transactions_in_progress_, has_non_fatal_or_empty_error);
//            ↑ erases A(kFallback), invalidating the captured iterator

```

When the sort callback fires,
[`OnTransactionSorted()`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=756)
dereferences the now-dangling iterator, reading freed memory:

```
// host_resolver_dns_task.cc:761-763
CHECK(transaction_info_it != transactions_in_progress_.end());   // UB
if (transactions_in_progress_.find(*transaction_info_it) == ...) // reads freed node

```

Note that, while the attached ASAN trace shows a heap-use-after-free read as the first corrupted state, I've tentatively evaluated the bug capable of RCE primitives (see Exploitability section).

### Detail: Race Window

Both the iterator capture (in `SortTransactionAndHandleResults`) and the
erasure (in `CancelNonFatalTransactions`) are reached from the same function:
[`OnDnsTransactionComplete`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=495),
which fires once per incoming DoH response on the IO thread. The race isn't
between threads — it's between successive event loop tasks on the same IO
thread, with a thread-pool sort roundtrip in between. The diagram below
shows how the three DNS response arrivals interleave.

```
IO Thread                                             Thread Pool
════════                                              ═══════════

┌─ DoH response: A record (valid address) ─────────────────────────────────┐
│                                                                          │
│  OnDnsTransactionComplete(A)           [line 495]                        │
│    └─ extract A from transactions_in_progress_                           │
│ !  └─ SortTransactionAndHandleResults() [line 651]                       │
│         └─ re-insert A into transactions_in_progress_ [line 741]         │
│         └─ AddressSorterWin::Sort()    [line 745]                        │
│              └─ PostTaskAndReply ──────────────────► Run SIO_ADDRESS_    │
│                   returns immediately                LIST_SORT           │
│                   (iterator captured                      │              │
│                    in reply callback)                     │              │
└────────────────────────────────────────────────────────── │ ─────────────┘
                                                            │
┌─ DoH response: AAAA record (SERVFAIL) ────────────────    │  ────────────┐
│                                                           │              │
│  OnDnsTransactionComplete(AAAA)        [line 495]         │              │
│    └─ extract AAAA from set                               │              │
│    └─ error_behavior == kFallback, not fatal              │              │
│    └─ OnFailure(allow_fallback=true)   [line 540]         │              │
│         └─ OnDeferredFailure()         [line 1009]        │              │
│              └─ AnyPotentiallyFatalTransactionsRemain()?  │              │
│                   YES: HTTPS(kFatalOrEmpty) in set        │              │
│ !            └─CancelNonFatalTransactions() [line 1019]   │              │
│                   └─ std::erase_if()   [line 979]         │              │
│                        erases A(kFallback)                │              │
│                        *** ITERATOR INVALIDATED ***       │              │
└───────────────────────────────────────────────────────    │  ────────────┘
                                                            │
┌─ PostTaskAndReply fires (sort complete) ◄─────────────────┘ ────────────┐
│                                                                         │
│! OnTransactionSorted (stale_iterator)  [line 756]                       │
│    └─ CHECK(it != end())               [line 761]  ← UB                 │
│    └─ find(*it)                        [line 763]  ← READS FREED MEMORY │
│    └─ extract(it)                      [line 770]  ← TREE CORRUPTION    │
│                                                                         │
│  *** ASAN CRASH ***                                                     │
└─────────────────────────────────────────────────────────────────────────┘

```

The attacker controls the timing by controlling when the DoH server sends
each response. The ~1-5ms window is the thread-pool roundtrip for
`SIO_ADDRESS_LIST_SORT` + `PostTaskAndReply` overhead. The AAAA SERVFAIL
must arrive and be processed on the IO thread event loop during this window.

### Reachability

The diagram above shows three DNS response types (A, AAAA, HTTPS) driving the
race. These exist because when Chrome resolves an HTTPS hostname,
`HostResolverDnsTask` issues up to three parallel DNS transactions — one for
each record type. Each transaction carries an
[error behavior](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.h;l=127)
that determines how the task handles its failure:

- **A and AAAA** default to `kFallback` — on failure, the task falls back
  to the system resolver
- **HTTPS** can be assigned `kFatalOrEmpty` — on failure, remaining
  non-fatal transactions are cancelled

The `kFatalOrEmpty` assignment only happens when Chrome is using
DNS-over-HTTPS (DoH) in secure mode and a specific flag is enabled:

```
// host_resolver_dns_task.cc:381-386
if (query_types.Has(DnsQueryType::HTTPS) &&
    features::kUseDnsHttpsSvcbEnforceSecureResponse.Get() && secure_) {
  transactions_needed_.emplace_back(DnsQueryType::HTTPS,
                                    TransactionErrorBehavior::kFatalOrEmpty);
}

```

This is the link between the error behaviors and the race: when AAAA fails
with `kFallback`, `OnFailure` ([line 540](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=540))
checks whether any `kFatalOrEmpty` transaction is still pending. If yes
(HTTPS hasn't responded), it calls `CancelNonFatalTransactions()`, which
erases the parked A transaction — invalidating the sort callback's iterator.
This is why all three transaction types are required, and why the HTTPS
response must be withheld.

The sort is only async on **Windows**, where
[`AddressSorterWin::Sort()`](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/address_sorter_win.cc;l=56-60)
posts to a thread pool. On Linux it completes synchronously (no race window).
An attacker controlling a DoH server triggers the race by responding to A
immediately, delaying AAAA SERVFAIL by ~2ms, and never responding to HTTPS.

Feature flags required (not all enabled by default):

| Flag | Purpose |
| --- | --- |
| `HappyEyeballsV3` | Gates the sort path ([line 649](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=649)) |
| `UseDnsHttpsSvcb:UseDnsHttpsSvcbEnforceSecureResponse/true` | Makes HTTPS use `kFatalOrEmpty` ([line 382](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_dns_task.cc;l=382)) |
| `EnableIPv6ReachabilityOverride` | Forces AAAA queries without IPv6 connectivity ([line 798](https://source.chromium.org/chromium/chromium/src/+/refs/tags/147.0.7727.49:net/dns/host_resolver_manager.cc;l=798)) |

Note: `UseDnsHttpsSvcb` (the parent feature) is already `FEATURE_ENABLED_BY_DEFAULT` —
only its `EnforceSecureResponse` sub-parameter defaults to `false`.

### Exploitability

The crash occurs in the **Network Service** process (sandboxed, AppContainer/LPAC
on Windows). The UAF is not limited to a single read — if the freed ~48-byte
tree node is reclaimed with attacker-controlled content, the code path provides
three escalating primitives:

**1. Read** (line 763): `*transaction_info_it` dereferences the stale iterator,
reading `type`, `error_behavior`, and `transaction` pointer from freed memory.
This is what ASAN catches.

**2. Write-what-where** (line 770): if `find()` returns non-end (attacker
controls reclaimed data to match a set element's sort key),
`extract(transaction_info_it)` unlinks the freed node from the red-black tree.
The rebalancing routine follows parent/left/right pointers stored in the
reclaimed allocation and **writes** to those targets:

```
// line 770 — extract uses the STALE iterator, not the find() result
TransactionInfo transaction_info =
    std::move(transactions_in_progress_.extract(transaction_info_it).value());
//          ↑ unlinks freed node: reads attacker-controlled parent/child pointers,
//            writes to those addresses during tree rebalancing

```

**3. Arbitrary free** (destructor): the move-constructed `TransactionInfo`
contains a `std::unique_ptr<DnsTransaction>` field. If the attacker placed a
controlled pointer at that offset in the reclaimed allocation, `~unique_ptr`
calls `delete` on it — freeing an arbitrary address. This can be chained
with heap feng shui for type confusion or vtable corruption.

Heap reclamation is feasible: the attacker controls the DoH server and can
trigger ~48-byte allocations in the Network Service by sending crafted DNS
responses (TXT records, CNAME chains, SVCB parameters) within the 1-5ms
race window. `MITIGATION_DYNAMIC_CODE_DISABLE` prevents shellcode, so code
execution requires ROP/JOP after the write primitive.

Primitives 2 and 3 would typically allow for ACE.

### Security Impact

This is effectively a **0-click** RCE vulnerability: a
**direct remote-to-privileged-process chain** with no renderer or broker hop.

Chrome resolves HTTPS hostnames on startup without user interaction (Safe
Browsing, sync, component updates, speculative preconnects), so no navigation
is required — opening Chrome is sufficient. A malicious or compromised DoH
provider can trigger the bug on every DNS resolution for every connected
client. In a network MITM scenario, an attacker intercepting the DoH
connection can target every Chrome instance on the network.

The crash occurs in the Network Service process (AppContainer/LPAC on
Windows). The required flags are not all enabled by default, which limits
current exposure.

## VERSION

Chrome Version: 147.0.7727.49 (Early Stable 01.04)  

Operating System: Windows 11 Home 24H2 26100.8037 x86\_64  

Code verified on latest Dev channel checkout 149.0.7778.3

## REPRODUCTION CASE

Attached: dns\_sort\_uaf\_trigger.py

### Steps to reproduce:

pip install dnslib cryptography  

python3 src/net/dns/dns\_sort\_uaf\_trigger.py --user-data-dir=c:\tmp\chrome-test --chrome-path=....chrome.exe

Note: crashes reliably 9++/10 times on asan build in my tests. The race may take a moment to complete.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION  

Type of crash: Network Service (Utility Process)  

Crash State:

```
=================================================================
==2856==ERROR: AddressSanitizer: heap-use-after-free on address 0x1255efc211f0 at pc 0x7ffb0e208429 bp 0x009f671fe9a0 sp 0x009f671fe9e8
READ of size 1 at 0x1255efc211f0 thread T9
==2856==*** WARNING: Failed to initialize DbgHelp!              ***
==2856==*** Most likely this means that the app is already      ***
==2856==*** using DbgHelp, possibly with incompatible flags.    ***
==2856==*** Due to technical reasons, symbolization might crash ***
==2856==*** or produce wrong results.                           ***
    #0 0x7ffb0e208428 in net::HostResolverDnsTask::OnTransactionSorted /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:806
    #1 0x7ffb0e2112cf in base::internal::Invoker<base::internal::FunctorTraits<void (net::HostResolverDnsTask::*&&)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > >, bool, std::__Cr::vector<net::IPEndPoint,std::__Cr::allocator<net::IPEndPoint> >),base::WeakPtr<net::HostResolverDnsTask> &&,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long> &&,std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > > &&>,base::internal::BindState<1,1,0,void (net::HostResolverDnsTask::*)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > >, bool, std::__Cr /mnt/data/code/chromium/src/base/functional/bind_internal.h:1069
    #2 0x7ffb0e210f8d in base::internal::Invoker<base::internal::FunctorTraits<void (net::HostResolverDnsTask::*&&)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > >, bool, std::__Cr::vector<net::IPEndPoint,std::__Cr::allocator<net::IPEndPoint> >),base::WeakPtr<net::HostResolverDnsTask> &&,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long> &&,std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > > &&>,base::internal::BindState<1,1,0,void (net::HostResolverDnsTask::*)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, std::__Cr::set<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> >,std::__Cr::less<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > >,std::__Cr::allocator<std::__Cr::unique_ptr<net::HostResolverInternalResult,std::__Cr::default_delete<net::HostResolverInternalResult> > > >, bool, std::__Cr /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #3 0x7ffb0e2aa01f in net::`anonymous namespace'::AddressSorterWin::Job::OnComplete /mnt/data/code/chromium/src/net/dns/address_sorter_win.cc:195
    #4 0x7ffb0e2aaa03 in base::internal::Invoker<base::internal::FunctorTraits<void (net::`anonymous namespace'::AddressSorterWin::Job::*&&)(),scoped_refptr<net::`anonymous namespace'::AddressSorterWin::Job> &&>,base::internal::BindState<1,1,0,void (net::`anonymous namespace'::AddressSorterWin::Job::*)(),scoped_refptr<net::`anonymous namespace'::AddressSorterWin::Job> >,void ()>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #5 0x7ffb21676a51 in base::internal::PostTaskAndReplyRelay::RunReply /mnt/data/code/chromium/src/base/threading/post_task_and_reply_impl.h:63
    #6 0x7ffb216767e4 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay &&>,base::internal::BindState<0,1,0,void (*)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay>,void ()>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #7 0x7ffb216fb2e8 in base::TaskAnnotator::RunTaskImpl /mnt/data/code/chromium/src/base/task/common/task_annotator.cc:229
    #8 0x7ffb216cb521 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl /mnt/data/code/chromium/src/base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475
    #9 0x7ffb216ca383 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork /mnt/data/code/chromium/src/base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346
    #10 0x7ffb21555ebe in base::MessagePumpForIO::DoRunLoop /mnt/data/code/chromium/src/base/message_loop/message_pump_win.cc:837
    #11 0x7ffb2154f434 in base::MessagePumpWin::Run /mnt/data/code/chromium/src/base/message_loop/message_pump_win.cc:87
    #12 0x7ffb216cd26f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run /mnt/data/code/chromium/src/base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650
    #13 0x7ffb21772c6c in base::RunLoop::Run /mnt/data/code/chromium/src/base/run_loop.cc:135
    #14 0x7ffb215ff06d in base::Thread::Run /mnt/data/code/chromium/src/base/threading/thread.cc:361
    #15 0x7ffb2bc2c735 in content::`anonymous namespace'::ChildIOThread::Run /mnt/data/code/chromium/src/content/child/child_process.cc:69
    #16 0x7ffb215ff600 in base::Thread::ThreadMain /mnt/data/code/chromium/src/base/threading/thread.cc:436
    #17 0x7ffb2152989e in base::`anonymous namespace'::ThreadFunc /mnt/data/code/chromium/src/base/threading/platform_thread_win.cc:112
    #18 0x7ffba34ddc6e in _asan_wrap_CreateThread+0x14e (z:\out\experiments_win\clang_rt.asan_dynamic-x86_64.dll+0x18005dc6e)
    #19 0x7ffbeffce8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #20 0x7ffbf056c48b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c48b)

0x1255efc211f0 is located 32 bytes inside of 48-byte region [0x1255efc211d0,0x1255efc21200)
freed by thread T9 here:
    #0 0x7ffba34df036 in operator delete+0x96 (z:\out\experiments_win\clang_rt.asan_dynamic-x86_64.dll+0x18005f036)
    #1 0x7ffb0e20c5e0 in net::HostResolverDnsTask::CancelNonFatalTransactions /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:979
    #2 0x7ffb0e20931f in net::HostResolverDnsTask::OnDeferredFailure /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:1019
    #3 0x7ffb0e20463e in net::HostResolverDnsTask::OnFailure /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:1009
    #4 0x7ffb0e1ff8ac in net::HostResolverDnsTask::OnDnsTransactionComplete /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:540
    #5 0x7ffb0e20fff0 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HostResolverDnsTask::*&&)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, unsigned short, int, const net::DnsResponse *),net::HostResolverDnsTask *,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long> &&,unsigned short &&>,base::internal::BindState<1,1,0,void (net::HostResolverDnsTask::*)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, unsigned short, int, const net::DnsResponse *),base::internal::UnretainedWrapper<net::HostResolverDnsTask,base::unretained_traits::MayNotDangle,0>,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>,unsigned short>,void (int, const net::DnsResponse *)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #6 0x7ffb0e1c0f11 in net::`anonymous namespace'::DnsTransactionImpl::DoCallback /mnt/data/code/chromium/src/net/dns/dns_transaction.cc:551
    #7 0x7ffb0e1c865d in net::`anonymous namespace'::DnsTransactionImpl::OnAttemptComplete /mnt/data/code/chromium/src/net/dns/dns_transaction.cc:787
    #8 0x7ffb0e1c8e73 in base::internal::Invoker<base::internal::FunctorTraits<void (net::`anonymous namespace'::DnsTransactionImpl::*&&)(unsigned int, bool, base::TimeTicks, int),net::`anonymous namespace'::DnsTransactionImpl *,unsigned int &&,bool &&,base::TimeTicks &&>,base::internal::BindState<1,1,0,void (net::`anonymous namespace'::DnsTransactionImpl::*)(unsigned int, bool, base::TimeTicks, int),base::internal::UnretainedWrapper<net::`anonymous namespace'::DnsTransactionImpl,base::unretained_traits::MayNotDangle,0>,unsigned int,bool,base::TimeTicks>,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #9 0x7ffb0e1818b2 in net::DnsHTTPAttempt::ResponseCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:344
    #10 0x7ffb0e181ff4 in net::DnsHTTPAttempt::OnReadCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:265
    #11 0x7ffb0e18246b in net::DnsHTTPAttempt::OnReadCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:296
    #12 0x7ffb0e1812c4 in net::DnsHTTPAttempt::OnResponseStarted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:250
    #13 0x7ffb234bfc2d in net::URLRequestJob::NotifyFinalHeadersReceived /mnt/data/code/chromium/src/net/url_request/url_request_job.cc:534
    #14 0x7ffb234beb2b in net::URLRequestJob::NotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_job.cc:490
    #15 0x7ffb27a59cc7 in net::URLRequestHttpJob::NotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:655
    #16 0x7ffb27a605b6 in net::URLRequestHttpJob::SaveCookiesAndNotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:1039
    #17 0x7ffb27a5d87e in net::URLRequestHttpJob::OnStartCompleted /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:1300
    #18 0x7ffb27a6a51b in base::internal::Invoker<base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,base::internal::BindState<1,1,0,void (net::URLRequestHttpJob::*)(int),base::internal::UnretainedWrapper<net::URLRequestHttpJob,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #19 0x7ffb2398b33b in net::HttpCache::Transaction::DoLoop /mnt/data/code/chromium/src/net/http/http_cache_transaction.cc:999
    #20 0x7ffb239840ad in net::HttpCache::Transaction::OnIOComplete /mnt/data/code/chromium/src/net/http/http_cache_transaction.cc:4059
    #21 0x7ffb239ae29e in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpCache::Transaction::*const &)(int),const base::WeakPtr<net::HttpCache::Transaction> &>,base::internal::BindState<1,1,0,void (net::HttpCache::Transaction::*)(int),base::WeakPtr<net::HttpCache::Transaction> >,void (int)>::Run /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #22 0x7ffb27a1c711 in net::HttpNetworkTransaction::OnIOComplete /mnt/data/code/chromium/src/net/http/http_network_transaction.cc:997
    #23 0x7ffb27a39dc3 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*&&)(int),net::HttpNetworkTransaction *>,base::internal::BindState<1,1,0,void (net::HttpNetworkTransaction::*)(int),base::internal::UnretainedWrapper<net::HttpNetworkTransaction,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #24 0x7ffb238bc17b in net::HttpStreamParser::OnIOComplete /mnt/data/code/chromium/src/net/http/http_stream_parser.cc:376
    #25 0x7ffb238c8f2e in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamParser::*&&)(int),base::WeakPtr<net::HttpStreamParser> &&>,base::internal::BindState<1,1,0,void (net::HttpStreamParser::*)(int),base::WeakPtr<net::HttpStreamParser> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #26 0x7ffb23559dc2 in net::SSLClientSocketImpl::DoReadCallback /mnt/data/code/chromium/src/net/socket/ssl_client_socket_impl.cc:881
    #27 0x7ffb2355933c in net::SSLClientSocketImpl::RetryAllOperations /mnt/data/code/chromium/src/net/socket/ssl_client_socket_impl.cc:1501

previously allocated by thread T9 here:
    #0 0x7ffba34de46f in operator new+0x8f (z:\out\experiments_win\clang_rt.asan_dynamic-x86_64.dll+0x18005e46f)
    #1 0x7ffb0e216732 in std::__Cr::__tree<net::HostResolverDnsTask::TransactionInfo,std::__Cr::less<net::HostResolverDnsTask::TransactionInfo>,std::__Cr::allocator<net::HostResolverDnsTask::TransactionInfo> >::__emplace_unique<net::HostResolverDnsTask::TransactionInfo>::<lambda_1>::operator() /mnt/data/code/chromium/src/out/experiments_win/../../third_party/libc++/src/include/__tree:1043
    #2 0x7ffb0e2054ff in net::HostResolverDnsTask::SortTransactionAndHandleResults /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:741
    #3 0x7ffb0e200321 in net::HostResolverDnsTask::OnDnsTransactionComplete /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:651
    #4 0x7ffb0e20fff0 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HostResolverDnsTask::*&&)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, unsigned short, int, const net::DnsResponse *),net::HostResolverDnsTask *,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long> &&,unsigned short &&>,base::internal::BindState<1,1,0,void (net::HostResolverDnsTask::*)(std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>, unsigned short, int, const net::DnsResponse *),base::internal::UnretainedWrapper<net::HostResolverDnsTask,base::unretained_traits::MayNotDangle,0>,std::__Cr::__tree_const_iterator<net::HostResolverDnsTask::TransactionInfo,std::__Cr::__tree_node<net::HostResolverDnsTask::TransactionInfo,void *> *,long long>,unsigned short>,void (int, const net::DnsResponse *)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #5 0x7ffb0e1c0f11 in net::`anonymous namespace'::DnsTransactionImpl::DoCallback /mnt/data/code/chromium/src/net/dns/dns_transaction.cc:551
    #6 0x7ffb0e1c865d in net::`anonymous namespace'::DnsTransactionImpl::OnAttemptComplete /mnt/data/code/chromium/src/net/dns/dns_transaction.cc:787
    #7 0x7ffb0e1c8e73 in base::internal::Invoker<base::internal::FunctorTraits<void (net::`anonymous namespace'::DnsTransactionImpl::*&&)(unsigned int, bool, base::TimeTicks, int),net::`anonymous namespace'::DnsTransactionImpl *,unsigned int &&,bool &&,base::TimeTicks &&>,base::internal::BindState<1,1,0,void (net::`anonymous namespace'::DnsTransactionImpl::*)(unsigned int, bool, base::TimeTicks, int),base::internal::UnretainedWrapper<net::`anonymous namespace'::DnsTransactionImpl,base::unretained_traits::MayNotDangle,0>,unsigned int,bool,base::TimeTicks>,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #8 0x7ffb0e1818b2 in net::DnsHTTPAttempt::ResponseCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:344
    #9 0x7ffb0e181ff4 in net::DnsHTTPAttempt::OnReadCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:265
    #10 0x7ffb0e18246b in net::DnsHTTPAttempt::OnReadCompleted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:296
    #11 0x7ffb0e1812c4 in net::DnsHTTPAttempt::OnResponseStarted /mnt/data/code/chromium/src/net/dns/dns_http_attempt.cc:250
    #12 0x7ffb234bfc2d in net::URLRequestJob::NotifyFinalHeadersReceived /mnt/data/code/chromium/src/net/url_request/url_request_job.cc:534
    #13 0x7ffb234beb2b in net::URLRequestJob::NotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_job.cc:490
    #14 0x7ffb27a59cc7 in net::URLRequestHttpJob::NotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:655
    #15 0x7ffb27a605b6 in net::URLRequestHttpJob::SaveCookiesAndNotifyHeadersComplete /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:1039
    #16 0x7ffb27a5d87e in net::URLRequestHttpJob::OnStartCompleted /mnt/data/code/chromium/src/net/url_request/url_request_http_job.cc:1300
    #17 0x7ffb27a6a51b in base::internal::Invoker<base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,base::internal::BindState<1,1,0,void (net::URLRequestHttpJob::*)(int),base::internal::UnretainedWrapper<net::URLRequestHttpJob,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:982
    #18 0x7ffb2398b33b in net::HttpCache::Transaction::DoLoop /mnt/data/code/chromium/src/net/http/http_cache_transaction.cc:999
    #19 0x7ffb239840ad in net::HttpCache::Transaction::OnIOComplete /mnt/data/code/chromium/src/net/http/http_cache_transaction.cc:4059
    #20 0x7ffb239ae29e in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpCache::Transaction::*const &)(int),const base::WeakPtr<net::HttpCache::Transaction> &>,base::internal::BindState<1,1,0,void (net::HttpCache::Transaction::*)(int),base::WeakPtr<net::HttpCache::Transaction> >,void (int)>::Run /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #21 0x7ffb27a1c711 in net::HttpNetworkTransaction::OnIOComplete /mnt/data/code/chromium/src/net/http/http_network_transaction.cc:997
    #22 0x7ffb27a39dc3 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*&&)(int),net::HttpNetworkTransaction *>,base::internal::BindState<1,1,0,void (net::HttpNetworkTransaction::*)(int),base::internal::UnretainedWrapper<net::HttpNetworkTransaction,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #23 0x7ffb238bc17b in net::HttpStreamParser::OnIOComplete /mnt/data/code/chromium/src/net/http/http_stream_parser.cc:376
    #24 0x7ffb238c8f2e in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamParser::*&&)(int),base::WeakPtr<net::HttpStreamParser> &&>,base::internal::BindState<1,1,0,void (net::HttpStreamParser::*)(int),base::WeakPtr<net::HttpStreamParser> >,void (int)>::RunOnce /mnt/data/code/chromium/src/base/functional/bind_internal.h:989
    #25 0x7ffb23559dc2 in net::SSLClientSocketImpl::DoReadCallback /mnt/data/code/chromium/src/net/socket/ssl_client_socket_impl.cc:881
    #26 0x7ffb2355933c in net::SSLClientSocketImpl::RetryAllOperations /mnt/data/code/chromium/src/net/socket/ssl_client_socket_impl.cc:1501
    #27 0x7ffb23534993 in net::SocketBIOAdapter::OnSocketReadIfReadyComplete /mnt/data/code/chromium/src/net/socket/socket_bio_adapter.cc:212

Thread T9 created by T0 here:
    #0 0x7ffba34ddb84 in _asan_wrap_CreateThread+0x64 (z:\out\experiments_win\clang_rt.asan_dynamic-x86_64.dll+0x18005db84)
    #1 0x7ffb215287fb in base::`anonymous namespace'::CreateThreadInternal /mnt/data/code/chromium/src/base/threading/platform_thread_win.cc:178
    #2 0x7ffb215fe098 in base::Thread::StartWithOptions /mnt/data/code/chromium/src/base/threading/thread.cc:228
    #3 0x7ffb2bc2b682 in content::ChildProcess::ChildProcess /mnt/data/code/chromium/src/content/child/child_process.cc:152
    #4 0x7ffb1ad321fb in content::UtilityMain /mnt/data/code/chromium/src/content/utility/utility_main.cc:459
    #5 0x7ffb1d24270f in content::RunOtherNamedProcessTypeMain /mnt/data/code/chromium/src/content/app/content_main_runner_impl.cc:762
    #6 0x7ffb1d244e7b in content::ContentMainRunnerImpl::Run /mnt/data/code/chromium/src/content/app/content_main_runner_impl.cc:1152
    #7 0x7ffb1d238c6f in content::RunContentProcess /mnt/data/code/chromium/src/content/app/content_main.cc:358
    #8 0x7ffb1d239412 in content::ContentMain /mnt/data/code/chromium/src/content/app/content_main.cc:371
    #9 0x7ffb0d1f2b06 in ChromeMain /mnt/data/code/chromium/src/chrome/app/chrome_main.cc:191
    #10 0x7ff6c6fe4807 in MainDllLoader::Launch /mnt/data/code/chromium/src/chrome/app/main_dll_loader_win.cc:204
    #11 0x7ff6c6fe2074 in main /mnt/data/code/chromium/src/chrome/app/chrome_exe_main_win.cc:351
    #12 0x7ff6c74dc253 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #13 0x7ffbeffce8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #14 0x7ffbf056c48b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c48b)

SUMMARY: AddressSanitizer: heap-use-after-free /mnt/data/code/chromium/src/net/dns/host_resolver_dns_task.cc:806 in net::HostResolverDnsTask::OnTransactionSorted

Shadow bytes around the buggy address:
  0x1255efc20f00: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa
  0x1255efc20f80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x1255efc21000: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fa
  0x1255efc21080: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x1255efc21100: f7 fa fd fd fd fd fd fa f7 fa 00 00 00 00 01 fc
=>0x1255efc21180: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd[fd]fd
  0x1255efc21200: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd
  0x1255efc21280: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x1255efc21300: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd
  0x1255efc21380: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x1255efc21400: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==2856==ADDITIONAL INFO

==2856==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb0e2a916a in net::`anonymous namespace'::AddressSorterWin::Sort /mnt/data/code/chromium/src/net/dns/address_sorter_win.cc:45
    #1 0x7ffb0e2a916a in net::`anonymous namespace'::AddressSorterWin::Sort /mnt/data/code/chromium/src/net/dns/address_sorter_win.cc:45
    #2 0x7ffb23517d28 in net::TCPSocketDefaultWin::DidSignalRead /mnt/data/code/chromium/src/net/socket/tcp_socket_win.cc:1233


Command line: `"z:\out\experiments_win\chrome.exe" --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=network --no-sandbox --ignore-certificate-errors --ignore-certificate-errors --user-data-dir="C:\Users\vboxuser\AppData\Local\Temp\chrome_uaf_f_1ygfh9" --no-pre-read-main-dll --start-stack-profiler --metrics-shmem-handle=2008,i,3746193491608001009,15187171776149990343,524288 --field-trial-handle=1868,i,4975595586424900620,14881627865771818368,262144 --enable-features=EnableIPv6ReachabilityOverride,HappyEyeballsV3 --variations-seed-version --pseudonymization-salt-handle=1912,i,4791457670012039030,13231652684840353526,4 --trace-process-track-uuid=3190708989122997041 --mojo-platform-channel-handle=2108 /prefetch:11`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2856==END OF ADDITIONAL INFO

==2856==ABORTING
...

```

CREDIT INFORMATION  

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?  

Reporter credit: Alisa Esage (@alisaesage)

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 25.5 KB)
- [dns_sort_uaf_trigger.py](attachments/dns_sort_uaf_trigger.py) (text/x-python, 19.9 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### al...@gmail.com (2026-04-12)

The bug was introduced by the combination of two commits:

### Introducing Commit (Iterator Capture)

```
commit 0bd8e99542eff70d7a0ea1183ef790332ad230e2
Author: Eric Orth
Date:   2024-01-25
Subject: Sort DNS results after each transaction

```

[View commit on Chromium Code Search](https://source.chromium.org/chromium/chromium/src/+/0bd8e99542eff70d7a0ea1183ef790332ad230e2)

This commit added `SortTransactionAndHandleResults()` and
`OnTransactionSorted()`, which capture a `std::set::iterator` in the async
sort callback (lines 737-770). The [comment on line 744](https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=744) — *"Sort() potentially
calls OnTransactionSorted() synchronously"* — shows the developer considered
the synchronous case but not the async case where `CancelNonFatalTransactions()`
can interleave and invalidate the iterator.

### Enabling Commit (Erasure Path)

```
commit aab4c068f88a1cf418109df013d0afcb050e7081
Author: Kenichi Ishibashi
Date:   2024-01-16
Subject: Separate HostResolverManager::DnsTask into a separate file

```

[View commit on Chromium Code Search](https://source.chromium.org/chromium/chromium/src/+/aab4c068f88a1cf418109df013d0afcb050e7081)

This commit moved `CancelNonFatalTransactions()` (with its `std::erase_if` on
`transactions_in_progress_`, line 979) into the new file. The erasure logic
predates the sort code — the bug was introduced when the sort was added nine
days later without accounting for the existing cancellation path.

### al...@gmail.com (2026-04-12)

deleted

### ch...@google.com (2026-04-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-13)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### df...@google.com (2026-05-09)

dschinazi, could you help provide status, or reassign.

### ba...@google.com (2026-05-11)

I believe that this is fixed by <https://crrev.com/c/7748992>.

erichorth@: Could you confirm?

### vm...@google.com (2026-05-23)

🤖 Automated message from the deduper 🤖 - This is a potential duplicate of [b/497588858](https://issues.chromium.org/issues/497588858)

### ch...@google.com (2026-08-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501792454)*
