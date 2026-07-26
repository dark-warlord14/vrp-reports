# Heap-Use-After-Free via stale set iterator dereference in HostResolverDnsTask::OnTransactionSorted

| Field | Value |
|-------|-------|
| **Issue ID** | [497588858](https://issues.chromium.org/issues/497588858) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network>DoH |
| **Platforms** | Windows |
| **Chrome Version** | 148.0.7763.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | er...@google.com |
| **Created** | 2026-03-30 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. Download ASAN Chromium
   Download [win32-release\_x64\_asan-win32-release\_x64-1606852.zip](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1606852.zip?generation=1774837012395179&alt=media)
2. Generate TLS certificate

```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 1 -nodes -subj "/CN=127.0.0.1" -addext "subjectAltName=IP:127.0.0.1"

```

3. Start the malicious DoH server

```
python -m pip install h2
python dns_server.py

```

4. Launch Chrome

```
chrome.exe --user-data-dir=%TEMP%\userdir1 --ignore-certificate-errors --enable-features="EnableIPv6ReachabilityOverride,UseHostResolverCache,UseDnsHttpsSvcb:UseDnsHttpsSvcbEnforceSecureResponse/true"

```

5. Configure Chrome to use the evil DoH server
   In Chrome, navigate to `chrome://settings/security`, enable "Use secure DNS", select "Add custom DNS service provider", and enter:

```
https://127.0.0.1:8443/dns-query

```

6. Navigate
   In Chrome, navigate to `https://pwn2addr.com`. Then network process crashes with `heap-use-after-free` in `OnTransactionSorted`.

# Problem Description

`HostResolverDnsTask` resolves a hostname by running concurrent DNS transactions. It manages them through two collections: `transactions_needed_` (a queue of transactions waiting to start) and `transactions_in_progress_` (a `std::set` of active transactions).

```
  base::circular_deque<TransactionInfo> transactions_needed_;
  // Active transactions have iterators pointing to their entry in this set, so
  // individual entries should not be modified or removed until completion or
  // cancellation of the transaction.
  std::set<TransactionInfo> transactions_in_progress_;

```

In the vulnerable configuration, three transactions are started: HTTPS, AAAA, and A. Each carries an `error_behavior` that determines how failures are handled. `PushTransactionsNeeded` assigns HTTPS `kFatalOrEmpty` when `kUseDnsHttpsSvcbEnforceSecureResponse` is enabled in secure (DoH) mode; AAAA and A get the default `kFallback`:

```
void HostResolverDnsTask::PushTransactionsNeeded(DnsQueryTypeSet query_types) {
  DCHECK(transactions_needed_.empty());

  if (query_types.Has(DnsQueryType::HTTPS) &&
      features::kUseDnsHttpsSvcbEnforceSecureResponse.Get() && secure_) {
    query_types.Remove(DnsQueryType::HTTPS);
    transactions_needed_.emplace_back(DnsQueryType::HTTPS,
                                      TransactionErrorBehavior::kFatalOrEmpty); // [1]
  }
  ...
}

```

`kFatalOrEmpty` keeps the HTTPS transaction alive in `transactions_in_progress_`, which later enables the `CancelNonFatalTransactions` path.

All three transactions start concurrently. The AAAA response arrives first. `OnDnsTransactionComplete` extracts the AAAA entry and, because `kUseHostResolverCache` is enabled, routes to `SortTransactionAndHandleResults`, which re-inserts the transaction info and captures a raw `std::set` iterator into an async sort callback:

```
void HostResolverDnsTask::SortTransactionAndHandleResults(
    TransactionInfo transaction_info,
    Results transaction_results) {
  ...
  if (!endpoints_to_sort.empty()) {
    auto insertion_result =
        transactions_in_progress_.insert(std::move(transaction_info));
    CHECK(insertion_result.second);

    // Sort() potentially calls OnTransactionSorted() synchronously.
    client_->GetAddressSorter()->Sort(
        endpoints_to_sort,
        base::BindOnce(&HostResolverDnsTask::OnTransactionSorted,
                       weak_ptr_factory_.GetWeakPtr(), insertion_result.first, // [2]
                       std::move(transaction_results)));
  }
  ...
}

```

On Windows, `AddressSorterWin::Sort` delegates to `Job::Start`, which posts the work to a ThreadPool and delivers the result back asynchronously:

```
static void Start(const std::vector<IPEndPoint>& endpoints,
                  CallbackType callback) {
  auto job = base::WrapRefCounted(new Job(endpoints, std::move(callback)));
  base::ThreadPool::PostTaskAndReply( // [3]
      FROM_HERE,
      {base::MayBlock(), base::TaskShutdownBehavior::CONTINUE_ON_SHUTDOWN},
      base::BindOnce(&Job::Run, job),
      base::BindOnce(&Job::OnComplete, job));
}

```

This makes `OnTransactionSorted` fire on a later message loop iteration. The iterator captured at [2] is now live in the pending callback.

While the sort is in flight, the A response arrives with SERVFAIL. Because A's `error_behavior` is `kFallback`, this chains through `OnFailure` -> `OnDeferredFailure`. There, `AnyPotentiallyFatalTransactionsRemain()` returns true (the HTTPS `kFatalOrEmpty` transaction is still pending), so `CancelNonFatalTransactions` runs and erases the AAAA node:

```
void HostResolverDnsTask::CancelNonFatalTransactions() {
  auto has_non_fatal_or_empty_error = [](const TransactionInfo& info) {
    return info.error_behavior != TransactionErrorBehavior::kFatalOrEmpty;
  };

  base::EraseIf(transactions_needed_, has_non_fatal_or_empty_error);
  std::erase_if(transactions_in_progress_, has_non_fatal_or_empty_error); // [4]
}

```

The iterator captured at [2] now points to freed heap memory. When the sort callback fires, `OnTransactionSorted` dereferences it:

```
void HostResolverDnsTask::OnTransactionSorted(
    std::set<TransactionInfo>::iterator transaction_info_it,
    Results transaction_results,
    bool success,
    std::vector<IPEndPoint> sorted) {
  CHECK(transaction_info_it != transactions_in_progress_.end());

  if (transactions_in_progress_.find(*transaction_info_it) == // [5]
      transactions_in_progress_.end()) {
    // If no longer in `transactions_in_progress_`, transaction was cancelled.
    // Do nothing.
    return;
  }
  TransactionInfo transaction_info =
      std::move(transactions_in_progress_.extract(transaction_info_it).value());
  ...
}

```

The `find(*transaction_info_it)` [5] dereferences the freed RB-tree node, triggering the heap-use-after-free.

# Additional Comments

Due to the character limit, I've included it here.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=385;drc=17be6785d7aec5454634e11c712a69a645a1c86b>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=748;drc=17be6785d7aec5454634e11c712a69a645a1c86b>
[3] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/address_sorter_win.cc;l=56;drc=17be6785d7aec5454634e11c712a69a645a1c86b>
[4] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=979;drc=17be6785d7aec5454634e11c712a69a645a1c86b>
[5] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=763;drc=17be6785d7aec5454634e11c712a69a645a1c86b>

# Summary

Heap-Use-After-Free via stale set iterator dereference in HostResolverDnsTask::OnTransactionSorted

# Custom Questions

#### Type of crash:

network

#### Crash state:

Please see the attached `asan.log`

#### Reporter credit:

pwn2addr

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 51.1 KB)
- [dns_server.py](attachments/dns_server.py) (text/x-python, 6.9 KB)
- [reproduce.webm](attachments/reproduce.webm) (video/webm, 4.0 MB)

## Timeline

### pw...@gmail.com (2026-03-30)

### Bisect commit

```
Commit: 0bd8e99542eff70d7a0ea1183ef790332ad230e2
Date: 2024-01-25
Subject: Sort DNS results after each transaction
Link: https://chromium-review.googlesource.com/c/chromium/src/+/4950391

```

This commit introduced per-transaction address sorting behind the `kUseHostResolverCache` feature flag.

### ja...@google.com (2026-03-31)

[security triage]
Triaging this as high severity for UAF in the network process.
I have not reproduced it yet. Adding tags for now.

### ja...@google.com (2026-03-31)

Hi ericorth@, assigning to you for now. To be clear, I haven't had a chance to reproduce this yet, but the reporter provided the ASAN and a poc.

### ch...@google.com (2026-03-31)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### er...@google.com (2026-03-31)

The good news is that this only occurs with HostResolverCache (my HostCache rewrite project, which is not yet launched anywhere) or Happy Eyeballs v3 (which I don't believe is lauched, @bashi can you confirm?).  Otherwise, the sort operation (and its async completion call) only happens after the completion of all transactions and doesn't need to reference back into `transactions_in_progress_`.  Also requires the unlaunched UseDnsHttpsSvcbEnforceSecureResponse behavior that we've tried to launch before but could never get the HTTPS query performant enough to finish out.  Otherwise the failed transaction would cancel the entire task and avoid the problem code through a weak ptr deletion.  So this bug only happens with unlaunched behavior.  I'll drop the priority and severity accordingly.

The overall problem is the `transactions_in_progress_.find(*transaction_info_it) == transactions_in_progress_.end()` at https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_dns_task.cc;l=763;drc=405f385dce2db578ff3b2301686d231ee8f0b042.  That's the code that attempts to check if the transaction is still alive after sort.  But the check relies on accessing the iterator to the potentially deleted set element, which is not valid, so the check isn't doing what it's supposed to be doing.  Oops.

### er...@google.com (2026-03-31)

Or actually, according to https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-no-impact I'm supposed to keep the severity at S1 but add a no-impact hotlist.  Guess I'll do that...

### er...@google.com (2026-03-31)

Or that guidance doesn't seem to have been updated since Chrome bugs switched to buganizer because the hotlist doesn't exist as far as I know.  I guess P2/S2 is the right way to mark this?

### er...@google.com (2026-03-31)

Nope.  I was wrong.  The hotlist exists: https://b.corp.google.com/hotlists/5433277 I just don't have the permission to add stuff to it.  So I'll change this back to P1/S1 and whoever controls that hotlist, please add this since this bug should not be possible without enabling unlaunched features.

### er...@google.com (2026-03-31)

I'll try to fix this later this week or next week (which should be fine timelinewise once this gets properly marked as Security_Impact-None).

### ja...@google.com (2026-04-01)

[security triage]
Thanks for taking a look ericorth@

I'll update the severity to no impact on the basis of [comment#6](https://issues.chromium.org/issues/497588858#comment6)

If you were able to reproduce it, please add that to the bug as well. Thanks!

### ja...@google.com (2026-04-01)

[security triage]

setting impact to Extended Stable based on the bisect provided by the reporter (0bd8e99542eff70d7a0ea1183ef790332ad230e2).

### er...@google.com (2026-04-02)

Have not yet attempted a repro, but I can confirm through manual analysis of the code that a flaw exists that at least enters undefined territory and that UAF seems to be a very plausible result.

### er...@google.com (2026-04-09)

Did some experimentation.  Built a unit test that cancels in-progress transactions and then unblocks a delayed async address sort operation.  But no luck with a crash, building with or without ASan.  I'll plan to poke at it a bit tomorrow with a debugger to see what's going on in more detail.

### er...@google.com (2026-04-10)

Confirmed UAF via debugging.  The iterator contains a tree node pointer that gets freed by the erase operation.  Derefing the iterator derefs the freed pointer.  Garbage memory is passed to the set find() call.

Still can't get ASan to complain about it or crash, so maybe I just have something wrong in my ASan config (even though I think I just have it set up with Chrome defaults).

But we are confirmed.  I'll figure out a fix.  Probably just need to add another weak ptr to better handle the cancellation.

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  main  

Author:  Eric Orth [ericorth@chromium.org](mailto:ericorth@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7748992>

Fix UAF after individual-transaction sort

---


Expand for full commit details
```
     
    Was passing an iterator into the `transactions_in_progress_` std::set 
    bound through the callback of the async sort operation. The code tried 
    to check the iterator was still a member of the set to avoid usage after 
    transaction cancellation, but it doesn't work right because the iterator 
    itself is not safe to use after removal from the set (results in use- 
    after-free). 
     
    Fix is to add WeakPtrs to the TransactionInfo objects and pass that 
    through the callbacks rather than iterators. Required wrapping 
    TransactionInfo in unique_ptr (for pointer stability), and that results 
    in a bit of code churn. 
     
    Also, for extra safety and cohesion, converted the 
    OnDnsTransactionComplete() callback to use WeakPtrs instead of iterators 
    as well. Note that the previous code here was safe because the async DNS 
    transaction call was cancelled on cancellation/deletion of the 
    TransactionInfo, and thus OnDnsTransactionComplete() was never called 
    after cancellation. 
     
    Fixed: 497588858 
    Change-Id: I3ec9d5246bd219d60a66bf2634679525fa7eeba2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7748992 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: Eric Orth <ericorth@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1614447}

```

---

Files:

- M `net/dns/BUILD.gn`
- M `net/dns/host_resolver_dns_task.cc`
- M `net/dns/host_resolver_dns_task.h`
- M `net/dns/host_resolver_dns_task_unittest.cc`

---

Hash: [707cc2572f4de73d5999b908dc79a1ea272188f8](https://chromiumdash.appspot.com/commit/707cc2572f4de73d5999b908dc79a1ea272188f8)  

Date: Tue Apr 14 14:48:47 2026


---

### aj...@google.com (2026-04-22)

Medium, as has preconditions.

### aj...@google.com (2026-04-22)

No, it could be a network attacker.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Moderately mitigated (sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pw...@gmail.com (2026-04-23)

Hi,

Could you reconsider the "Moderately mitigated (sandboxed)" classification? The crash is in the NetworkService, which is not actually sandboxed by default on Windows today:

1. kNetworkServiceSandbox is FEATURE\_DISABLED\_BY\_DEFAULT on main. Both attempts to flip it (c6bd7f0 on 2025-11-25 and a0ad012 on 2026-03-10) were reverted within days; the most recent revert (41a8f03) landed on 2026-03-13.
2. docs/security/process-sandboxes-by-platform.md still lists Windows Network as "unsandboxed" as of its 2026-04-15 update, 8 days before this decision. The doc explicitly tracks "the default configuration of the Stable Chrome channel (i.e. 100% of clients)".
3. Precedent 399995424 - same process (network.mojom.NetworkService), same component, heap-use-after-free - was awarded $10,000 with the rationale "memory corruption in a highly-privileged process (network stack)".

That said, I may well be missing something. If the panel applied a different consideration here, I'd appreciate hearing it.

### aw...@chromium.org (2026-04-29)

IIUC to have the amount reconsidered we need to add it to the Security-VRP-Reassessment-Request hotlist (8186354) <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md#i-don_t-agree-with-the-reward-amount_can-i-get-the-reward-reassessed>

Adding that

### aj...@google.com (2026-04-29)

The network service on windows is now sandboxed - we will update our documentation.

### pw...@gmail.com (2026-04-30)

Thank you for rechecking this and clarifying.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497588858)*
