# Security: Self-update service worker to stay alive

| Field | Value |
|-------|-------|
| **Issue ID** | [40090287](https://issues.chromium.org/issues/40090287) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ya...@gmail.com |
| **Assignee** | ya...@gmail.com |
| **Created** | 2018-01-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Service workers can self update to keep at least one version running.  

This is reproducible at least in Chrome and Firefox (Spec bug?).

**REPRODUCTION CASE**

1. Create index.html to load SW
   
    <!DOCTYPE html>
    <script>
   navigator.serviceWorker.register('/sw.js');
   </script>
2. Create sw.js, and make sure the file will change every time the SW updates.  
   
   One simple way of doing this is by adding the current timestamp to sw.js.  
   
   (I attached a simple Go program for this).  
   
   // Time: {now}  
   
   function wait(ms) {  
   
   // This is only to show  
   
   const i = setInterval(() => console.log('is alive'), 1000);  
   
   return new Promise(resolve => setTimeout(() => {  
   
   clearInterval(i);  
   
   resolve();  
   
   }, ms));  
   
   }
   
   self.addEventListener('activate', event => {  
   
   // Don't wait too long or the worker will be killed and this does not work.  
   
   event.waitUntil(wait(120000).then(() => {  
   
   self.registration.update();  
   
   }));  
   
   });
3. Open the html file (<http://localhost:5000/index.html>).  
   
   This will register the SW and fire the |activate| event, which will wait some time and then self-update the SW. Because we include a unique timestamp in sw.js, SW will update and fire the |activate| event on the new worker.  
   
   This can be repeated forever to keep at least one version running. You can verify this in chrome://serviceworker-internals

On a side note: There are other bugs which can be reproduced in Chrome with similar steps:

1. If you do these steps above and wait for some time, you will see that there are many |redundant| SWs registered. They are no longer running and will be gone after closing chrome.
2. If you refresh the page or open a new tab, chrome waits for the SW to be activated, even when there a no listeners for |fetch| registered, which results in a long loading time. This behavior is not limited to |fetch| events.

## Attachments

- [sw.go](attachments/sw.go) (text/plain, 1.0 KB)

## Timeline

### ya...@gmail.com (2018-01-24)

[Empty comment from Monorail migration]

### ya...@gmail.com (2018-01-24)

If you modify the activate event handler in sw.js like this, the SW will start every time the user opens chrome.

self.addEventListener('activate', event => {
  self.registration.sync.register('foo');
  // Don't wait too long or the worker will be killed and this does not work.
  event.waitUntil(wait(120000).then(() => {
    self.registration.update();
  }));
});


### fa...@chromium.org (2018-01-25)

Thanks for the detailed report and I agree this is important. This is a known issue but I guess we didn't have a bug yet. There might be discussion on the spec. I didn't think of the background sync aspect too.

We had a similar issue with postMessage/fetch event where we clamp down on the time allotted for the event to make sure you can't recursively extend your time-to-live.

We might consider doing this here for update() but it seems a bit tricky and there are possibly holes. An simple solution could be to disallow update() when there are no open clients.

### fa...@chromium.org (2018-01-25)

Actually I'm not sure about the Background Sync mechanism in c#2. It looks like sync.register() should fail if the service worker has no clients?
https://developers.google.com/web/updates/2015/12/background-sync#permissions

### ya...@gmail.com (2018-01-25)

It looks like I was a little too fast and the background sync part only works if Chrome is closed when there is a client or shortly after.

We could introduce a global time-to-live mechanism in ServiceWorkerRegistration and also kill all versions if the global TTL expired. We would also have to make sure that install/activate event does not extend that time, or only if there is a client attached.

We should have a spec discussion whether we want to disallow update() when there are no clients, or the calling worker is not activated. Do we have data if sites are doing this?

### fa...@chromium.org (2018-01-26)

Yeah, the install/activate interaction is worrisome. Typically these each grant 5 minutes of runtime, which is because we expect them to be doing somewhat heavy async things.

It seems odd if update() from a worker spawns a worker that doesn't get that time. We might consider clamping only initial script evaluation time, but that is not an effective mitigation.

Ben Kelly of Mozilla had a great idea. We could delay self update() by a increasingly large amount, eventually letting the worker die before the update starts (and aborting the update request). The delay would be reset to 0 once there is a client for the registration.

I don't see downsides to implementing this now, it should be transparent to devs and only impact sites doing a strange likely malicious thing. WDYT?

### fa...@chromium.org (2018-01-26)

One slight worry is a worker that does update() in push and expecting it to work even without clients.

Another possibility is the delay resets once the worker gets an event that's not an install/active event. Essentially, one event grants you the right to update, and we allow limited update otherwise that eventually dies.

### fa...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-01-26)

Yannic, would you be interested in doing implementation for this?

### ya...@gmail.com (2018-01-28)

I like the version in #7 better because workers calling update() in push (or periodic sync?) will still work.

Implementing this sounds interesting. I'll give it a try!

### ya...@gmail.com (2018-01-28)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-01-29)

That's great news. Thanks!

One complication is the new S13nServiceWorker implementation doesn't route some events to the browser process. But those events are only fetch events or (to be implemented) message events, so those imply a client exists.  So we might consider doing both: reset the delay when there is a client or when an event comes in.

### me...@chromium.org (2018-01-29)

Your friendly security sheriff here: I don't fully understand the implications of this bug to assign it a severity rating. Is keeping a SW always running worse than having a background tab with the same site?

### fa...@chromium.org (2018-01-30)

Yes, it's worse because the SW keeps running even after the tab is closed.

Our basic guarantee is the SW will go away soon after all tabs using it are closed. More technically, SW lifetime is based on events. Sites usually can't generate events to keep the SW alive when there are no tabs open. There are some exceptions like push messages, but these have been carefully designed to prevent abuse. E.g., a push message must result in a notification, so the user knows the site is being used in the background, and can revoke permissions if desired.

This is a class of bug where a site/SW can keep itself alive in a way we didn't really want it to. Previous related issues include https://bugs.chromium.org/p/chromium/issues/detail?id=647943 and https://bugs.chromium.org/p/chromium/issues/detail?id=648836

The Service Worker Security FAQ touches upon this in some sections:
https://chromium.googlesource.com/chromium/src/+/master/docs/security/service-worker-security-faq.md#do-service-workers-live-forever
https://chromium.googlesource.com/chromium/src/+/master/docs/security/service-worker-security-faq.md#do-service-workers-keep-running-after-i-close-the-tab

### pa...@chromium.org (2018-01-30)

This bug is a violation of what the FAQ promises:

https://chromium.googlesource.com/chromium/src/+/master/docs/security/service-worker-security-faq.md#Do-Service-Workers-keep-running-after-I-close-the-tab

If necessary, please update the FAQ as part of any fix.

I'm going to call that Low severity, per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md.

Has there been a Firefox bug filed? It sounds like they know, but I want to be sure.

### ya...@gmail.com (2018-01-30)

Yes, a Firefox bug has been filled: https://bugzilla.mozilla.org/show_bug.cgi?id=1432846

### sh...@chromium.org (2018-01-31)

[Empty comment from Monorail migration]

### ya...@gmail.com (2018-02-06)

A few things I noticed working on this:

- We shouldn't reset the delay on postMessage if it is coming from a service worker to prevent workers from resetting the delay.
- Should we store the delay in ServiceWorkerDatabase?

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ec96e9da29ec26491de4be2464e0735404546e62

commit ec96e9da29ec26491de4be2464e0735404546e62
Author: Yannic Bonenberger <contact@yannic-bonenberger.com>
Date: Tue Jul 24 14:56:58 2018

Add LayoutTest for update() from workers without controllers

Bug: 805496
Change-Id: Idb1cc63960409eeb8117d74267f5df33f401eb08
Reviewed-on: https://chromium-review.googlesource.com/932101
Commit-Queue: Yannic Bonenberger <contact@yannic-bonenberger.com>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#577538}
[modify] https://crrev.com/ec96e9da29ec26491de4be2464e0735404546e62/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/test-helpers.js
[add] https://crrev.com/ec96e9da29ec26491de4be2464e0735404546e62/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/update-no-controllee-worker.js
[add] https://crrev.com/ec96e9da29ec26491de4be2464e0735404546e62/third_party/WebKit/LayoutTests/http/tests/serviceworker/update-no-controllee.https-expected.txt
[add] https://crrev.com/ec96e9da29ec26491de4be2464e0735404546e62/third_party/WebKit/LayoutTests/http/tests/serviceworker/update-no-controllee.https.html


### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b86a5cf3e919f0819589d056493278527771943e

commit b86a5cf3e919f0819589d056493278527771943e
Author: Yannic Bonenberger <contact@yannic-bonenberger.com>
Date: Wed Jul 25 14:16:13 2018

[ServiceWorker] Delay update() from workers without controllers

This CL delays the execution of update() for an increasing amount
of time if the calling worker doesn't control a client. The delay
is reset every time a controller is added to the worker, or an
event is dispatched. postMessage from service workers,
|install| and |activate| don't reset the delay.

Bug: 805496
Change-Id: I9c25ba4315ce6a915634ecdf6405db8774c40929
Reviewed-on: https://chromium-review.googlesource.com/900763
Commit-Queue: Yannic Bonenberger <contact@yannic-bonenberger.com>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#577875}
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_consts.cc
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_consts.h
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_object_host.cc
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_registration.h
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_registration_object_host.cc
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_registration_object_host.h
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_registration_unittest.cc
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/b86a5cf3e919f0819589d056493278527771943e/content/browser/service_worker/service_worker_version_unittest.cc
[delete] https://crrev.com/7beedc820bff35f6f06074d8d9fb66b27f48ca02/third_party/WebKit/LayoutTests/http/tests/serviceworker/update-no-controllee.https-expected.txt


### me...@chromium.org (2018-07-27)

Is this fixed now?

### ya...@gmail.com (2018-07-27)

Verified that this is fixed in 70.0.3504.0

(CVE from Firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1432846)

### fa...@chromium.org (2018-07-30)

Thanks Yannic!

### fa...@chromium.org (2018-07-30)

+wanderview FYI

### sh...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

Thanks for the report, yannic.bonenberger@! The VRP panel decided to award $500 for this. A member of our finance team will be in touch to arrange payment. Also, how would you like to appear on the Chrome release notes?

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### ya...@gmail.com (2018-08-07)

Wow, thanks, awhalley@! I did not expect that this qualifies for a reward. You can contact me at the email I use in this bug tracker to arrange what happens with the money.

You can use "Yannic Bonenberger" in the release notes.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/805496?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090287)*
