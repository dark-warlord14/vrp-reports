# Security: Application can actively circumvent Mixed Content policy in PNA origin trial

| Field | Value |
|-------|-------|
| **Issue ID** | [323583084](https://issues.chromium.org/issues/323583084) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>CORS>PrivateNetworkAccess |
| **Platforms** | Mac |
| **Chrome Version** | 121.0.0.0 |
| **Reporter** | me...@danielbaulig.de |
| **Assignee** | ly...@chromium.org |
| **Created** | 2024-02-03 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Enable Permission Prompt for Private Network Access experiment in about:flags or use an origin with active Origin Trial PrivateNetworkAccessPermissionPrompt
2. Install a Service Worker on a secure origin with the following code:

```
  const request = event.request;
  if (!request.url.startsWith(location.origin)) {
    // Skip cross origin requests
    return false;
  }
  event.respondWith(fetch(request));
});

```

3. Send a PNA enabled request from the application context, e.g.

`fetch('http://privatehost.local', { targetAddressSpace: 'private' })`

I've put together a minimal repro at the following URL: <https://www.danielbaulig.de/pna-sw-bug/>
Since the origin is not part of the Origin Trial, the experiment flag will need to be enabled.

# Problem Description

Expected behavior: A PNA preflight request should be sent to the `privatehost.local` host and the actual request should only be sent upon successful response and user confirmation. With PNA Permission Prompt experiment disabled the UA will prevent the request due to the Mixed Content policy.

Actual behavior:
No PNA preflight request is sent and no user confirmation prompted. The Mixed Content policy will also not prevent the request from being sent. The UA will send the request as instructed by the application, circumventing both the Mixed Content policy and PNA Permission Dialog.

More details relating to the bug can be found in <https://github.com/WICG/private-network-access/issues/126#issue-2104329281>

# Summary

Security: Application can actively circumvent Mixed Content policy in PNA origin trial

# Custom Questions

#### Which component does this fall under?

Not sure - I don't know

#### Does this work in other browsers?

Yes - This is just a Chrome problem

# Additional Data

Category: API   

Chrome Channel: Stable   

Regression: N/A

## Timeline

### aj...@google.com (2024-02-05)

CC'ing owners and adding foundin. S3/Low severity.

### ly...@google.com (2024-02-20)

Discussed with @phao offline. This bug caused because the IP address space of documents fetched via service worker are not correctly set and we currently don't send any preflight for requests from documents with unknown ip address space.

I disabled PNA permission prompt to relax mixed content check for documents fetched via service worker.

@phao is looking into setting correct IP address space for the documents mentioned above.

We will also enable PNA preflights from documents with unknown ip address space in the future. Unknown IP addresses should be served as public IP addresses.

### ap...@google.com (2024-02-20)

Project: chromium/src
Branch: main

commit 2f0159210955293550cd5cc81e5463d71b87d2d9
Author: Yifan Luo <lyf@chromium.org>
Date:   Tue Feb 20 12:10:38 2024

    [Private Network Access] Disable permission prompt for documents fetched via service worker
    
    This CL disabled PNA permission prompt for documents requested from service worker, because the IP address space of these documents are not set.
    
    Bug: b/323583084
    Change-Id: I0c98c855ca6c70250adfffcfc8bf283d5b627ab0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5306924
    Reviewed-by: Jonathan Hao <phao@chromium.org>
    Reviewed-by: Yifan Luo <lyf@chromium.org>
    Reviewed-by: Mike West <mkwst@chromium.org>
    Commit-Queue: Yifan Luo <lyf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1262637}

M       third_party/blink/renderer/core/loader/mixed_content_checker.cc

https://chromium-review.googlesource.com/5306924


### me...@danielbaulig.de (2024-02-20)

Great to know that a quick patch was landed!

Since I've been using the PNA Permission Dialog origin trial to build a Progressive Web App for IOT device control and management, I'm curious to better understand when I can expect the PNA permission prompt for documents served from Service Worker to get reactivated again? This is something my web app heavily relies on. Can I expect that to happen in the short to medium term (weeks or maybe a couple months) or something that I should expect to take longer?

I also wanted to say thank you for the work on PNA and the Permission Dialog. The ability for secure origins to access the private address space (given user consent) enables a whole set of additional applications that were previously not really possible using the web platform. I hope we can see this feature ship more widely and to more platforms, soon!

### ly...@google.com (2024-02-22)

> Since I've been using the PNA Permission Dialog origin trial to build a Progressive Web App for IOT device control and management, I'm curious to better understand when I can expect the PNA permission prompt for documents served from Service Worker to get reactivated again? This is something my web app heavily relies on. Can I expect that to happen in the short to medium term (weeks or maybe a couple months) or something that I should expect to take longer?

[phao@chromium.org](mailto:phao@chromium.org) is currently working on it as priority.

> I also wanted to say thank you for the work on PNA and the Permission Dialog. The ability for secure origins to access the private address space (given user consent) enables a whole set of additional applications that were previously not really possible using the web platform. I hope we can see this feature ship more widely and to more platforms, soon!

"Thank you so much for the kind words, and thanks for your feedback and help with testing along the way! We're really excited about the potential of PNA Permissions. It's always encouraging to hear from developers who share our vision of a more secure and capable web platform. We'll keep working to make PNA a success and push for wider adoption!"

### pe...@google.com (2024-02-22)

Merge rejected: M122 is already shipping to stable and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-02-26)

Merge review required: M122 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### ly...@google.com (2024-02-26)

1. Why does your merge fit within the merge criteria for these milestones?
   **This is a security bug influenced websites using permission prompt origin trial and users with permission prompt chrome flag on.**
2. What changes specifically would you like to merge? Please link to Gerrit.
   **<https://chromium-review.googlesource.com/c/chromium/src/+/5306924>**
3. Have the changes been released and tested on canary?
   **Yes**
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
   **Yes, `#private-network-access-permission-prompt`**
5. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
   **I already tested it mantually, but it would be nicer if the test team can double test it. The reporter already detailed described the reproduction process, please follow that.**

### pe...@google.com (2024-02-26)

Merge review required: M123 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

### pg...@google.com (2024-02-26)

Marking the bug as fixed (fixed in main, may need backmerges) so that our automation can identify it easily (:

### am...@chromium.org (2024-02-26)

removing merge labels since this is a low severity security issue (S3) and does not qualify for backmerge

### ap...@google.com (2024-02-29)

Project: chromium/src
Branch: main

commit cf0b087b7fd76135a2bf9745a46fda3b01001b02
Author: Yifan Luo <lyf@chromium.org>
Date:   Thu Feb 29 13:53:26 2024

    [Private Network Access] Add test for service worker fetching document
    
    Bug: b/323583084
    Change-Id: I031d4ebd81d105e01a66eea10bf2bfefa781cd19
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5307002
    Reviewed-by: Mike West <mkwst@chromium.org>
    Commit-Queue: Yifan Luo <lyf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1266949}

A       third_party/blink/web_tests/external/wpt/fetch/private-network-access/resources/service-worker-fetch-all.js
M       third_party/blink/web_tests/external/wpt/fetch/private-network-access/resources/support.sub.js
A       third_party/blink/web_tests/external/wpt/fetch/private-network-access/service-worker-fetch-document-treat-as-public.tentative.https.window-expected.txt
A       third_party/blink/web_tests/external/wpt/fetch/private-network-access/service-worker-fetch-document-treat-as-public.tentative.https.window.js
A       third_party/blink/web_tests/external/wpt/fetch/private-network-access/service-worker-fetch-document.tentative.https.window-expected.txt
A       third_party/blink/web_tests/external/wpt/fetch/private-network-access/service-worker-fetch-document.tentative.https.window.js
M       third_party/blink/web_tests/external/wpt/fetch/private-network-access/service-worker-fetch.tentative.https.window.js
A       third_party/blink/web_tests/virtual/pna-workers-disabled/external/wpt/fetch/private-network-access/service-worker-fetch-document-treat-as-public.tentative.https.window-expected.txt
A       third_party/blink/web_tests/virtual/pna-workers-disabled/external/wpt/fetch/private-network-access/service-worker-fetch-document.tentative.https.window-expected.txt
A       third_party/blink/web_tests/virtual/pna-workers-enabled/external/wpt/fetch/private-network-access/service-worker-fetch-document-treat-as-public.tentative.https.window-expected.txt
A       third_party/blink/web_tests/virtual/pna-workers-enabled/external/wpt/fetch/private-network-access/service-worker-fetch-document.tentative.https.window-expected.txt

https://chromium-review.googlesource.com/5307002


### ap...@google.com (2024-03-13)

Project: chromium/src
Branch: main

commit 041e2b44b5139de8075e73aa659937a281cd83b5
Author: Jonathan Hao <phao@chromium.org>
Date:   Wed Mar 13 18:48:28 2024

    [Private Network Access] Get client IP address space from the service worker that loads the main document
    
    This is to fix https://github.com/WICG/private-network-access/issues/126
    
    The issue is that when the main document is fetched by a service worker,
    the URLResponseHead's remote_endpoint doesn't have an IP address, which
    makes sense because the service worker doesn't always have to forward
    the fetch to an actual network fetch.  This results in the render frame
    host and the loaders it created having kUnknown IP address space, which
    in turn causes the Private Network Access policy to be allow [1].
    
    Also even if the service worker did fetch from file scheme, the service
    worker can still modify the content, so the client address space
    shouldn't be local, otherwise a public service worker can bypass PNA.
    
    This CL stores the service worker version's IP address space in the
    URLResponseHead of the document (main resource) it loads, and then use
    that to calculate the document's IP address space.
    
    [1]
    https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/private_network_access_util.cc;l=113-117;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090
    
    Bug: 40241368,323583084
    Change-Id: I8751e52cb5e1faa8394531c90d68664e8bd641e8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5308035
    Auto-Submit: Jonathan Hao <phao@chromium.org>
    Reviewed-by: Adam Rice <ricea@chromium.org>
    Commit-Queue: Jonathan Hao <phao@chromium.org>
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1272321}

M       content/browser/renderer_host/private_network_access_util.cc
M       content/browser/service_worker/service_worker_main_resource_loader.cc
M       content/browser/service_worker/service_worker_main_resource_loader_unittest.cc
M       services/network/public/cpp/ip_address_space_util.cc
M       services/network/public/cpp/ip_address_space_util.h
M       services/network/public/cpp/ip_address_space_util_unittest.cc
M       services/network/url_loader.cc

https://chromium-review.googlesource.com/5308035


### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-14)

Congratulations Daniel! The Chrome VRP Panel has decided to award you $3,000 for this report. A member of the Google p2p-vrp finance team will be in touch with you soon regarding payment. In the meantime, please let us know the name or tag/handle you would like us to use in acknowledging you publicly for this finding. Thank you for your efforts and reporting this issue to us!

### me...@danielbaulig.de (2024-03-20)

Thank you, you can use my full legal name (Daniel Baulig). By when should I expect to hear from the P2P-VRP finance team member?

### am...@chromium.org (2024-03-20)

Thanks for the response!
p2p-vrp should generally reach out within 24-48 hours from when we send them the reward information. Since that does not appear to have happened, I have pinged the ticket related to this batch of payments.

### me...@danielbaulig.de (2024-04-03)

Sorry to be following up on this here again. The VRP payment process is a little intransparent and hard to follow, I apologize. I completed Supplier Enrollment with Google Buying Support and provided my personal and payment information last week. So far I have not heard back from anyone regarding the actual payment, e.g. if it was issued or by when I should expect it to be issued. I tried following up on some of the email threads that were generated in the process, but it's frankly unclear to me who the right POC is to follow up with. Thank you!

### pe...@google.com (2024-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/323583084)*
