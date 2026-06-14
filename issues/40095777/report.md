# Security: Calling console utility functions causes data to be shared between contexts

| Field | Value |
|-------|-------|
| **Issue ID** | [40095777](https://issues.chromium.org/issues/40095777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Using the debug/monitor console utility functions, a user can break into the debugger when a particular function is called, or monitor when a function is called.

When either of these utility functions is invoked, the process of setting up the debug breakpoint causes data to ultimately be shared between contexts on the page. This then allows code running in one context to potentially access and modify objects within another context.

**VERSION**  

Chrome Version: Tested on 75.0.3770.142 (stable) and 77.0.3858.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. Install the attached extension (made up of manifest.json and content\_script.js). The extension in this case doesn't do anything. You don't need to install it if you already have an extension that runs a content script on http sites.
2. The other attached file (index.html) forms a simple website. Download this file and place it in a directory.
3. In the directory you downloaded the index.html file to, run the following command in a terminal:

python3 -m http.server 8080

4. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

5. Open the devtools console. Run the following line within the context of the main page:

startDebugging();

This function contains the following code:

debug(window.alert);  

window.document.testVariable = {};

6. Using the JavaScript contexts dropdown, switch to the extension context and run the following:

window.document.testVariable;

This shouldn't be set, given that the command here is run within the context of the extension. Instead, the variable (which was set in the context of the main page) is set and is printed to the console.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [content_script.js](attachments/content_script.js) (text/plain, 0 B)
- [index.html](attachments/index.html) (text/plain, 265 B)
- [manifest.json](attachments/manifest.json) (text/plain, 275 B)

## Timeline

### de...@gmail.com (2019-07-20)

From debugging through the code, it appears that the cause of this issue is the following:

As part of setting up the debug breakpoint, all lazy accessor pairs (i.e. getter/setter pairs) are overwritten to ensure that they hit the debug break trampoline:

https://cs.chromium.org/chromium/src/v8/src/debug/debug.cc?l=1257&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

When debugging and skipping over this code, the issues raised here don't occur. It looks like the functions that are instantiated (to replace the getter/setter functions) are associated with the context in which debug/monitor was called. When you then call the functions from another context, you can end up with data being shared between contexts or the renderer crashing (if some resulting access check fails).

window properties that have a getter associated with them are all then affected. This includes things like:

- clientInformation
- crypto
- document
- external
- history
- indexedDB
- ...

Note that attempting to access these properties from anything but the main context will tend to crash the renderer, due to failed access checks.

It appears that there is some form of caching involved, however. For example, if you access window.clientInformation from the main context, then access it from another context, the access will succeed. If, however, you access window.clientInformation in another context without accessing it in the main context first, the renderer will crash due to a failed access check.

If code running in another context happens to access one of the above window properties after debug/monitor has been called, it's possible that code in the main context might be able to run within that context. For example, code running in the context of the page might be able to run in the context of an extension's content script if that script happens to access some property on the document object.

The issue that's described above also applies to contexts that are cross-origin, but in the same renderer process. You can test that this is the case by going through the following steps:

1. Start a web server that uses the same IP address as the above server, but different port (it doesn't matter what content it's actually serving):

python3 -m http.server 8081

2. Navigate to http://localhost:8080/index.html, open the devtools and run the following commands:

open("http://127.0.0.1:8081/");
debug(window.alert);

3. Switch to the new window. Open the devtools and run:

window.document;

This should print the following error:

Uncaught DOMException: Blocked a frame with origin "http://127.0.0.1:8080" from accessing a cross-origin frame.

The problem here is that the accessor pairs have been replaced even though the contexts are cross-origin.

### in...@chromium.org (2019-07-22)

bmeurer@, can you please take a look.

### oc...@google.com (2019-07-25)

[Empty comment from Monorail migration]

[Monorail components: Platform>Apps>DevTools]

### bm...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### bm...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### bm...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### sz...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f51e0368eab8e25b1c030e49370187e44dbf111d

commit f51e0368eab8e25b1c030e49370187e44dbf111d
Author: Simon Zünd <szuend@chromium.org>
Date: Fri Aug 02 13:46:11 2019

Add regression tests that check the native context of accessors

This CL adds regression tests for two bugs where the wrong native
context is used when lazy accessors are instantiated.

The first bug injects an object created in context 1, into another
context 2. The object has an accessor pair installed via
FunctionTemplate. In context 2, the property descriptor of this
accessor is retrieved, causing the JSFunction to be instantiated
with the current context (context 2) instead of the creation
context of the object (context 1).

The second bug is similar. When breakpoints are set, the whole heap
is walked and all lazy accessor pairs are instantiated. This again
uses the current context instead of using the context from which
a AccessorPair originates.

Bug: chromium:986063, chromium:989909
Change-Id: Iaaea6e81f1b9f6b55fc7583b260aa9aea035a8d3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1730999
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63048}

[modify] https://crrev.com/f51e0368eab8e25b1c030e49370187e44dbf111d/test/unittests/api/access-check-unittest.cc
[modify] https://crrev.com/f51e0368eab8e25b1c030e49370187e44dbf111d/test/unittests/unittests.status


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b6c555bd88636af677c62927cedaf0ab6630ac59

commit b6c555bd88636af677c62927cedaf0ab6630ac59
Author: Simon Zünd <szuend@chromium.org>
Date: Mon Aug 05 10:06:08 2019

Add ApiNatives::InstantiateFunction that explicitly takes native context

This CL changes {CreateApiFunction} to take an explicit native context
to set on the newly created JSFunction. The CL also adds a new variant
of {ApiNatives::InstatiateFunction}, that takes a native context and passes
it through to {CreateApiFunction}.

This is a refactoring in preparation for a bugfix.
AccessorPairs can be instantiated lazily. At the time of
lazy instantiation, the current context does not necessarily match
the creation context of the holder of an AccessorPair.

Bug: chromium:986063, chromium:989909
Change-Id: Idea4b5052f2baff5c3d916f5ab8ed5017b60699b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1735308
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63063}

[modify] https://crrev.com/b6c555bd88636af677c62927cedaf0ab6630ac59/src/api/api-natives.cc
[modify] https://crrev.com/b6c555bd88636af677c62927cedaf0ab6630ac59/src/api/api-natives.h
[modify] https://crrev.com/b6c555bd88636af677c62927cedaf0ab6630ac59/src/init/bootstrapper.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8c3da74f18b28fe6621a036b8eb4bfdb19f0d7eb

commit 8c3da74f18b28fe6621a036b8eb4bfdb19f0d7eb
Author: Simon Zünd <szuend@chromium.org>
Date: Mon Aug 05 11:25:48 2019

Use correct native context when instantiating AccessorPairs

This CL changes the way AccessorPairs are collected for instantiation
when debug break trampolines are installed.
Instead of walking the heap and looking at AccessorPairs directly, we
look at all JSObjects and collect AccessorPairs via each objects
descriptor array. This way, we can associate the correct native
context with each collected AccessorPair.

The current native context is not always the correct context to instantiate
the getter and setter JSFunctions for an AccessorPair.

Bug: chromium:986063
Change-Id: I124a0802f4938b95f1ad75efc65eb05b66bcfc67
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1735310
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63071}

[modify] https://crrev.com/8c3da74f18b28fe6621a036b8eb4bfdb19f0d7eb/src/debug/debug.cc
[modify] https://crrev.com/8c3da74f18b28fe6621a036b8eb4bfdb19f0d7eb/test/unittests/unittests.status


### sz...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-13)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### la...@google.com (2019-08-23)

szuend@ - please respond to C#15 to consider the merge request

### sz...@chromium.org (2019-08-23)

Removing merge request labels. This security issue is not severe enough to back merge 3 CLs. The security issue "only" causes AccessorPairs to have to wrong native context and it can only happen when DevTools is open.

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e9873bf129511b04629f44c5bde656035533418a

commit e9873bf129511b04629f44c5bde656035533418a
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Wed Mar 03 16:35:13 2021

[debug] Instantiate accessors only once.

When retrieving an API accessor function (i.e. either the getter or the
setter) for which the lazy accessor mechanism is used (i.e. where the
actual JSFunction is created lazily and only the FunctionTemplateInfo)
is around, we thus far created a fresh JSFunction every time the
accessor function is requested, but that's observably wrong behavior,
since the accessors are JavaScript objects with identity. We currently
rely on the instantiation cache to guarantee identity, but there's no
reason why we couldn't instead just put the instantiated JSFunction into
the AccessorPair.

Fixing this to only instantiate the lazy accessor pair only once, upon
first time it's requested, coincidentally also simplifies (and fixes)
the API accessor breakpoint machinery. This was previously lacking
support for walking dictionary prototype objects and forcibly
instantiating the lazy accessor pairs with break points. However, all
this magic in the debugger is no longer necessary when we ensure that
the lazy accessor pair component is generally only instantiated once.

Bug: v8:178, v8:7596, chromium:986063, chromium:496666
Change-Id: I41d28378010716c96c8ecf7c3f1247765f8bc669
Fixed: chromium:1163547
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2731527
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73163}

[modify] https://crrev.com/e9873bf129511b04629f44c5bde656035533418a/src/debug/debug.cc
[modify] https://crrev.com/e9873bf129511b04629f44c5bde656035533418a/test/cctest/test-debug.cc
[modify] https://crrev.com/e9873bf129511b04629f44c5bde656035533418a/src/objects/objects.cc


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/986063?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095777)*
