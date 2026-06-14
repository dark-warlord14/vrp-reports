# Sandboxed iframe Document can end up sharing execution context/type system with iframe's initial about:blank Document

| Field | Value |
|-------|-------|
| **Issue ID** | [40050506](https://issues.chromium.org/issues/40050506) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>IFrame, Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@microsoft.com |
| **Assignee** | da...@microsoft.com |
| **Created** | 2019-10-23 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version       : 78.0.3888.0 (Developer Build) (64-bit)
Other browsers tested:
Chromium Edge: FAIL
Firefox: Other interop issues with iframe about:blank and sandboxing prevent the issue from reproing.
Pre-Chromium Edge: Same as Firefox

There is an issue where an iframe navigated from its initial un-sandboxed about:blank document to a sandboxed same-domain page can end up reusing the execution context/JavaScript realm of the initial, non-sandboxed about:blank document.

This can cause crashes if we poke things in the right way, since an object that should be considered cross-origin (because the sandbox gives it an opaque origin) can bleed into the top-level page, with the result that access checks which are never expected to fail can now fail.

For instance we observed a crash on this stack:

[13684:2932:1023/145124.890:FATAL:v8_dom_wrapper.cc(50)] Check failed: !scope.AccessCheckFailed(). 
[0x0]   base!base::debug::BreakDebugger + 0x21   
[0x1]   base!logging::LogMessage::~LogMessage + 0x7a3   
[0x2]   blink_platform!blink::V8DOMWrapper::CreateWrapper + 0x170   
[0x3]   blink_platform!blink::ScriptWrappable::Wrap + 0x11e   
[0x4]   blink_core!blink::V8SetReturnValueFast<v8::PropertyCallbackInfo<v8::Value> > + 0x1a4   
[0x5]   blink_core!blink::V8SetReturnValueFast<v8::PropertyCallbackInfo<v8::Value> > + 0x2a   
[0x6]   blink_core!blink::node_list_v8_internal::IndexedPropertyGetter + 0xda   
[0x7]   blink_core!blink::V8NodeList::IndexedPropertyGetterCallback + 0x20   
[0x8]   v8!v8::internal::PropertyCallbackArguments::BasicCallIndexedGetterCallback + 0x174   
[0x9]   v8!v8::internal::PropertyCallbackArguments::CallIndexedGetter + 0x1f5   
[0xa]   v8!v8::internal::`anonymous namespace'::GetPropertyWithInterceptorInternal + 0x373   
[0xb]   v8!v8::internal::JSObject::GetPropertyWithInterceptor + 0xe8   
[0xc]   v8!v8::internal::Object::GetProperty + 0x266   
[0xd]   v8!v8::internal::Runtime::GetObjectProperty + 0x1da   
<snip for brevity/>

This can be reproduced by:
1) Unpacking the change attached to this bug [without building the fix in the patch yet :-) ]
2) Comment out the following assert in the test file sandbox-new-execution-context.html (otherwise the test will fail on that line before hits the crash):
assert_equals(iframeAboutBlankDocument.__proto__.changeFromSandboxedIframe, undefined,
     "Sandboxed iframe contents should not have been able to mess with type system of about:blank document");
3) Run the test over HTTP and watch it crash

Perhaps more importantly, there is also a sandbox escape here, albeit a very scoped one.  If the iframe's sandbox has 'allow-scripts', then the iframe can mess with its type system.  The initial, un-sandboxed about:blank document erroneously shares this type system, so any use of this document is now suspect due to the iframe's potentially malicious modifications to its type system.

To observe this, put back the assert mentioned above in sandbox-new-execution-context.html from the attached change patch.  This assert will fail without the fix, demonstrating that the sandboxed iframe was able to make a change to a shared prototype that is visible via the un-sandboxed about:blank document.

The idea of reusing an iframe's initial about:blank document's type system for a same-domain iframe navigation is enshrined in the spec.  From https://html.spec.whatwg.org/#initialise-the-document-object :
4. If browsingContext's only entry in its session history is the about:blank Document that was added when browsingContext was created, and navigation is occurring withreplacement enabled, and that Document has the same origin as origin, then do nothing.
Otherwise: [do the stuff to create a new type system]

However, the origin used here should already take the iframe's sandbox flags into account and thus the same-origin check here should return false, per the earlier step 2 at the same link:

2. Let origin be the result of determining the origin given browsingContext, request's url, sandboxFlags, incumbentNavigationOrigin, and activeDocumentNavigationOrigin.

The code bug in Blink is that the iframe's sandbox flags aren't taken into account when making this consideration.   FrameLoader::ShouldReuseDefaultView() does take the CSP's sandbox flags into consideration, but the iframe sandbox is missed, thus the type system is erroneously reused during the ensuing navigation.  The issue can be fixed by adding this additional check to FrameLoader::ShouldReuseDefaultView().  The attached .patch makes this fix and includes a test. 
 Hopefully there's an area expert who can review this; I have no prior familiarity with this part of the code and the related navigation infrastructure is fairly complicated.

One last clarifying note about the attached test, since it's non-obvious why the sandbox should apply to the document for sandbox-new-execution-context-iframe.html but not to the initial about:blank Document.  The sandbox flags are applied when a Document is created, so the about:blank Document isn't sandboxed since it is synchronously created upon connecting the iframe via appendChild, prior to setting the sandbox flags.  The Document for sandbox-new-execution-context-iframe.html is created only later, asynchronously, after the fetch for its HTML file is complete, so it does pick up the sandbox flags even though iframe.sandbox was set after setting iframe.src and after the iframe is connected via appendChild.
Relevant spec links:
https://html.spec.whatwg.org/#the-iframe-element
https://html.spec.whatwg.org/#creating-a-new-browsing-context
https://html.spec.whatwg.org/#navigate
https://html.spec.whatwg.org/#process-a-navigate-response
https://html.spec.whatwg.org/#navigate-html
https://html.spec.whatwg.org/#initialise-the-document-object

Due to the potential security implications here I've attached the fix to this bug as a .patch file rather than making a publicly visible Gerrit review.  Please reach out with any questions, or if there's anything else I can help with in getting this resolved.


## Attachments

- [0001-Prevent-sandboxed-iframe-document-from-sharing-execu.patch](attachments/0001-Prevent-sandboxed-iframe-document-from-sharing-execu.patch) (text/plain, 6.2 KB)

## Timeline

### da...@microsoft.com (2019-10-23)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-10-24)

japhet@: can you take a look at this? Feel free to re-assign as needed.

Also CCing yhirano@ just for added visibility.

### ja...@chromium.org (2019-10-24)

daniec@, it looks like there's a way to upload a private change to gerrit (https://gerrit-review.googlesource.com/Documentation/user-upload.html#private). Do you want to try uploadng the fix that way and see if you can send it out for review to me while it's still private?

Failing that, it's probably ok to do the review publicly if need be.

### da...@microsoft.com (2019-10-24)

I gave this a try and it looks like I might not have the right permissions to make private reviews.  Is this something that can be granted?  "Private changes are disabled" 
 in the error message sort of implies that these can't be done at all for this repo, but I would guess that there must be some way to do private reviews for more severe issues.

S:\Chromium2\src\out\debug_x64>git cl upload --private
Running presubmit upload checks ...

<snip>

remote: Processing changes: refs: 1, done
To https://chromium.googlesource.com/chromium/src
 ! [remote rejected]           5bf426a545ce363dc0857741b2660c66f3746ae5 -> refs/for/refs/heads/master%wip,m=Initial_upload,private (private changes are disabled)
error: failed to push some refs to 'https://chromium.googlesource.com/chromium/src'

saving CL description to C:\Users\daniec/.git_cl_description_backup

Failed to create a change. Please examine output above for the reason of the failure.
Hint: run command below to diagnose common Git/Gerrit credential problems:
  git cl creds-check

If git-cl is not working correctly, file a bug under the Infra>SDK component including the files below.
Review the files before upload, since they might contain sensitive information.
Set the Restrict-View-Google label so that they are not publicly accessible.


### ja...@chromium.org (2019-10-24)

Ok, yeah, just go ahead and upload it like a normal patch. Feel free to add me and dcheng for review.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a66313865400db81d62316f4381d5062b8552a33

commit a66313865400db81d62316f4381d5062b8552a33
Author: Daniel Clark <daniec@microsoft.com>
Date: Wed Oct 30 02:52:07 2019

Prevent sandboxed iframe Document from sharing execution context with initial about:blank Document

This change fixes an issue where a sandboxed iframe can be created such
that it contains a sandboxed Document with an opaque origin that still
shares a script context with the iframe's initial un-sandboxed
about:blank Document.  The scenario is set up in the following manner:
1) Create a new iframe dynamically, and set its src to a same-domain page
   that we are going to sandbox.
2) Insert the iframe into a Document, and synchronously grab a reference
   to its initial about:blank Document.
3) Synchronously set iframe.sandbox = "allow-scripts" (this is still
   before the same-domain page has loaded in the frame).
4) The iframe’s navigation to the same-domain page occurs, asynchronously.
   FrameLoader::ShouldReuseDefaultView is called to determine the mode in
   which to load the new page.  FrameLoader::ShouldReuseDefaultView fails
   to check the iframe’s sandbox flags (it only looks at the CSP ones),
   so the navigation proceeds without resetting the type system of the
   iframe.  The result is that the newly loaded page shares the type
   system of the initial about:blank Document.
5) Code in the sandboxed iframe is now free to make changes to its type
   system that can affect any usage of the about:blank Document since
   they share the same type system.  This is a sandbox escape in that if
   the same-domain page that the iframe is navigated to contains
   user-generated code, it could run outside the iframe.  It can also
   result in crashes if we poke things in the right way, since an object
   that should be considered cross-origin can bleed into the top-level
   page, with the result that access checks which are never expected to
   fail can now fail.

This change fixes the issue by making FrameLoader::ShouldReuseDefaultView()
check the iframe's sandbox flags via FrameLoader::EffectiveSandboxFlags(),
in addition to the existing check for CSP sandbox flags.

Bug: 1017441
Change-Id: Ide1b13e16b0e0428a243ff47b6e17ae25ad0ff0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1881315
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Dan Clark <daniec@microsoft.com>
Cr-Commit-Position: refs/heads/master@{#710629}

[modify] https://crrev.com/a66313865400db81d62316f4381d5062b8552a33/third_party/blink/renderer/core/loader/frame_loader.cc
[add] https://crrev.com/a66313865400db81d62316f4381d5062b8552a33/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/sandbox-new-execution-context-iframe.html
[add] https://crrev.com/a66313865400db81d62316f4381d5062b8552a33/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/sandbox-new-execution-context.html


### ja...@chromium.org (2019-10-30)

Reassigning back to daniec@, since I didn't actually do any of the work here and shouldn't take credit :)

### da...@microsoft.com (2019-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-05)

Requesting merge to beta M79 because latest trunk commit (710629) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-05)

This bug requires manual review: M79 has already been promoted to the beta branch, so this requires manual review
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
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-05)

+adetaylor@ for M79 merge review

### ad...@chromium.org (2019-11-05)

Merging to M79 feels right to me if this looks good in canary.

### go...@chromium.org (2019-11-05)

How is the change looking in canary? 

### go...@chromium.org (2019-11-08)

Can anyone test on canary and update result here? Canary verification is needed before we approve merge to M79. 

### da...@microsoft.com (2019-11-08)

I confirmed that the test I submitted with the change passes in:
Google Chrome	80.0.3963.0 (Official Build) canary (64-bit) (cohort: Clang-64)
Revision	72f306374beb66be714ba86d9a132322e5d2c7e3-refs/branch-heads/3963@{#1}
OS	Windows 10 OS Version 1903 (Build 19018.1)
JavaScript	V8 8.0.198

http://localhost:8001/html/browsers/sandboxing/sandbox-new-execution-context.html
This is a testharness.js-based test.
PASS iframe with sandbox should load with new execution context
Harness: the test ran to completion.

And for completeness' sake I confirmed that it still fails as expected in stable:

Google Chrome	78.0.3904.87 (Official Build) (64-bit) (cohort: Stable)
Revision	20c21f4010010f32462ea8e1d6af30cef66d48c8-refs/branch-heads/3904@{#840}
OS	Windows 10 OS Version 1903 (Build 19018.1)
JavaScript	V8 7.8.279.19

http://localhost:8001/html/browsers/sandboxing/sandbox-new-execution-context.html 
This is a testharness.js-based test.
FAIL iframe with sandbox should load with new execution context assert_equals: Sandboxed iframe contents should not have been able to mess with type system of about:blank document expected (undefined) undefined but got (string) "change from sandboxed iframe"
Harness: the test ran to completion.

### go...@chromium.org (2019-11-08)

Approving merge to M79 branch 3945 based on comments #14 and #17. Please merge ASAP. Thank you.

### go...@chromium.org (2019-11-11)

Please merge to M79 branch 3945 ASAP. Thank you.

### da...@microsoft.com (2019-11-11)

Sorry, I'm a bit new to this process.  Is the expectation that I as the fixer of the bug am handling the merge to an M79 branch?  Or is there a branch owner that drives this/kicks it off via some automated process?

### go...@chromium.org (2019-11-12)

Re #20, yes, we expect developer to merge the change to release branch after approval.

For now, I've merged the change to M79 branch 3945 - https://chromium.googlesource.com/chromium/src.git/+/d34c6d46a0ff31c436d01e0e5ffd01fc5cc99375. Please check and confirm it looks good to you. Thank you.

### da...@microsoft.com (2019-11-12)

LGTM, thanks for taking care of it.

### sh...@chromium.org (2019-11-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@microsoft.com (2019-11-12)

Removing Merge-Approved-79 tag as this merge was done at  https://chromium.googlesource.com/chromium/src.git/+/d34c6d46a0ff31c436d01e0e5ffd01fc5cc99375

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

daniec@microsoft.com - how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### da...@microsoft.com (2019-12-06)

adetaylor@google.com - if it's not too late yet could you please credit "Johnathan Norman and Daniel Clark of Microsoft Edge Team"?  Thanks!

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/1017441?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>IFrame, Blink>SecurityFeature>IFrameSandbox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050506)*
