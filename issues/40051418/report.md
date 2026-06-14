# Use after free in Logger::MapEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40051418](https://issues.chromium.org/issues/40051418) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gk...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2020-02-03 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
The second and third argument of `Logger::MapEvent`, `Map from` and `Map to` are not protected by Handle. And they are used after `GetAbstractPC` triggers a GC, which moves them.
In `Logger::MapEvent`, `DisallowHeapAllocation no_gc;` says that there will be no gc in this scope. But, it is just like a comment and does not block a GC.

```
void JSObject::MigrateSlowToFast(Handle<JSObject> object,
                                 int unused_property_fields,
                                 const char* reason) {
  ...
  Handle<Map> old_map(object->map(), isolate);
  ...
  Handle<Map> new_map = Map::CopyDropDescriptors(isolate, old_map);
  ...
  if (instance_descriptor_length == 0) {
    ...
    if (FLAG_trace_maps) {
      LOG(isolate, MapEvent("SlowToFast", *old_map, *new_map, reason)); <-- `*old_map` and `*new_map`, raw pointers are passed here.
    }
    return;
  }
  ...
}
```

```
void Logger::MapEvent(const char* type, Map from, Map to, const char* reason, <-- `from` and `to` are raw pointers.
                      HeapObject name_or_sfi) {
  DisallowHeapAllocation no_gc;
  ...
  if (!isolate_->bootstrapper()->IsActive()) {
    pc = isolate_->GetAbstractPC(&line, &column); <-- `GetAbstractPC` may call a GC.
  }
  Log::MessageBuilder msg(log_.get());
  msg << "map" << kNext << type << kNext << timer_.Elapsed().InMicroseconds()
      << kNext << AsHex::Address(from.ptr()) << kNext                     <-- `from` is used here.
      << AsHex::Address(to.ptr()) << kNext << AsHex::Address(pc) << kNext <-- `to` is used here .
      << line << kNext << column << kNext << reason << kNext;
  ...
}
```

Patch:
We can fix this bug by relocating `GetAbstractPC` after the last usage of `from` and `to`.

```
void Logger::MapEvent(const char* type, Map from, Map to, const char* reason,
                      HeapObject name_or_sfi) {
  DisallowHeapAllocation no_gc;
  ...

  Log::MessageBuilder msg(log_.get());
  msg << "map" << kNext << type << kNext << timer_.Elapsed().InMicroseconds()
      << kNext << AsHex::Address(from.ptr()) << kNext
      << AsHex::Address(to.ptr()) << kNext;

  if (!isolate_->bootstrapper()->IsActive()) {
    pc = isolate_->GetAbstractPC(&line, &column);
  }
  msg << AsHex::Address(pc) << kNext
      << line << kNext << column << kNext << reason << kNext;
  ...
}
```

Did this work before? N/A 

Chrome version: 79.0.3945.130  Channel: stable
OS Version: OS X 10.15.2
Flash Version:

## Timeline

### mm...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### mm...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### mm...@google.com (2020-02-03)

Please add Security_Severity label or change the issue type to Bug if it's not a security vulnerability


### ca...@chromium.org (2020-02-04)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-02-07)

Friendly ping for further triage

### cl...@chromium.org (2020-02-11)

The DisallowHeapAllocation scope will actually make us fail in debug mode if we ever allocate something on the JS heap (which might trigger a GC).

Not sure though if it's actually guaranteed that this never happens here.
Lowering severity though, since logging is only enabled with special flags or via DevTools AFIAK.

Peter, can you take a look at this one also?

### pe...@chromium.org (2020-02-11)

This particular bug is gated on FLAG_trace_maps so there is no impact on production.
Maya can you please assign to someone on the V8 team

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3fb9a70b6bccfa8f92ab2800a94d54c730841a79

commit 3fb9a70b6bccfa8f92ab2800a94d54c730841a79
Author: Maya Lekova <mslekova@chromium.org>
Date: Thu Feb 13 13:36:45 2020

[logging] Handlify a few Objects to prevent UAF

The GC suspect was GetAbstractPC.

Fixed: v8:9990, v8:9987, chromium:1048038
Change-Id: I86a27e2098589dbf6af0808d6770c5e69987f1f7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2050394
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66259}

[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/ic/ic.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.h
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/js-objects.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/map.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/runtime/runtime-classes.cc


### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Congrats! The Panel decided to award $500 for this report 

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-03-16)

[Empty comment from Monorail migration]

### ms...@chromium.org (2020-03-19)

[Empty comment from Monorail migration]

### gk...@gmail.com (2020-04-01)

Do you have a plan to assign a CVE for this issue?
Thanks.

### ms...@chromium.org (2020-04-01)

Since this is a bug in a feature guarded by a flag which is "off" by default, it doesn't need a CVE IMO. Oliver, could you please double-check this?

### oc...@google.com (2020-04-01)

+adetaylor. Adrian, do we give CVEs for such cases?

### ad...@chromium.org (2020-04-02)

Is this off *by default* or *always*? If it's off for 100% of users, it should be marked Security_Impact-None, and no, it won't get a CVE. If it's on for even 0.1% of users, this will be credited in the Chrome release notes and get a CVE at that time.

From https://crbug.com/chromium/1048038#c7 I assume the former, but please confirm.

### ms...@chromium.org (2020-04-02)

It's off for 100% of users.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3fb9a70b6bccfa8f92ab2800a94d54c730841a79

commit 3fb9a70b6bccfa8f92ab2800a94d54c730841a79
Author: Maya Lekova <mslekova@chromium.org>
Date: Thu Feb 13 13:36:45 2020

[logging] Handlify a few Objects to prevent UAF

The GC suspect was GetAbstractPC.

Fixed: v8:9990, v8:9987, chromium:1048038
Change-Id: I86a27e2098589dbf6af0808d6770c5e69987f1f7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2050394
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66259}

[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/ic/ic.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.h
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/js-objects.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/map.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/runtime/runtime-classes.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3fb9a70b6bccfa8f92ab2800a94d54c730841a79

commit 3fb9a70b6bccfa8f92ab2800a94d54c730841a79
Author: Maya Lekova <mslekova@chromium.org>
Date: Thu Feb 13 13:36:45 2020

[logging] Handlify a few Objects to prevent UAF

The GC suspect was GetAbstractPC.

Fixed: v8:9990, v8:9987, chromium:1048038
Change-Id: I86a27e2098589dbf6af0808d6770c5e69987f1f7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2050394
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66259}

[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/ic/ic.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.h
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/js-objects.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/map.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/runtime/runtime-classes.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3fb9a70b6bccfa8f92ab2800a94d54c730841a79

commit 3fb9a70b6bccfa8f92ab2800a94d54c730841a79
Author: Maya Lekova <mslekova@chromium.org>
Date: Thu Feb 13 13:36:45 2020

[logging] Handlify a few Objects to prevent UAF

The GC suspect was GetAbstractPC.

Fixed: v8:9990, v8:9987, chromium:1048038
Change-Id: I86a27e2098589dbf6af0808d6770c5e69987f1f7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2050394
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66259}

[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/ic/ic.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.h
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/js-objects.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/map.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/runtime/runtime-classes.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3fb9a70b6bccfa8f92ab2800a94d54c730841a79

commit 3fb9a70b6bccfa8f92ab2800a94d54c730841a79
Author: Maya Lekova <mslekova@chromium.org>
Date: Thu Feb 13 13:36:45 2020

[logging] Handlify a few Objects to prevent UAF

The GC suspect was GetAbstractPC.

Fixed: v8:9990, v8:9987, chromium:1048038
Change-Id: I86a27e2098589dbf6af0808d6770c5e69987f1f7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2050394
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66259}

[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/ic/ic.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/logging/log.h
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/js-objects.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/objects/map.cc
[modify] https://crrev.com/3fb9a70b6bccfa8f92ab2800a94d54c730841a79/src/runtime/runtime-classes.cc


### ad...@chromium.org (2020-04-02)

Thanks (re https://crbug.com/chromium/1048038#c20).

### [Deleted User] (2020-05-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-21)

This issue was migrated from crbug.com/chromium/1048038?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051418)*
