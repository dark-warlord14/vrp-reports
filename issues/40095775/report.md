# Security: Use-after-free of CommandLineAPIScope object

| Field | Value |
|-------|-------|
| **Issue ID** | [40095775](https://issues.chromium.org/issues/40095775) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the user runs a command in the devtools console, the code that's run is given access to the console utility functions. This is implemented through the use of a CommandLineAPIScope object. This object has a specific lifetime, but it's possible for JavaScript code to continue to access the functions associated with this object even after it's been freed.

**VERSION**  

Chrome Version: Tested on 75.0.3770.142 (stable) and 77.0.3858.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. Navigate to a site and open the devtools console.
2. Run the following command:

Object.defineProperty(window, "$0", {configurable: false});

3. Run:

$0;

This will use the CommandLineAPIScope object which was created in step 1 (and ultimately freed). Because the object was freed, this command will intermittently crash the renderer (see below for an explanation of why this crash is likely to be intermittent).

Note that although the commands here are being run directly by the user, they could be run by a script on the page when the user enters other, unrelated, commands.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Timeline

### de...@gmail.com (2019-07-20)

The reason for this use-after-free issue is as follows:

The CommandLineAPIScope object is managed via a unique_ptr in the InjectedScript class:

https://cs.chromium.org/chromium/src/v8/src/inspector/injected-script.h?l=158&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

The unique_ptr is reset whenever the InjectedScript object is destroyed:

https://cs.chromium.org/chromium/src/v8/src/inspector/injected-script.cc?l=795&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

This is done when the evaluation of a command has finished and the InjectedScript object goes out of scope:

https://cs.chromium.org/chromium/src/v8/src/inspector/v8-runtime-agent-impl.cc?l=249&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

After you run the Object.defineProperty command in step 2, the $0 reference is prevented from being removed. It continues to refer to the original CommandLineAPIScope object.

That means that when you run the $0 command in step 3, the CommandLineAPIScope reference retrieved in the accessorGetterCallback function will be invalid:

https://cs.chromium.org/chromium/src/v8/src/inspector/v8-console.cc?l=786&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

In the description of the issue above, it's mentioned that the renderer will intermittently crash when running the command in step 3. This is because the scope variable isn't really used when the following branch is taken:

https://cs.chromium.org/chromium/src/v8/src/inspector/v8-console.cc?l=791&rcl=6ee5e916e2850ae9ae916fdbf285893db6d437e0

When this branch isn't taken, the scope variable will be used and the renderer will likely crash. This ultimately depends on the contents of the freed memory.

### de...@gmail.com (2019-07-20)

Also, one small correction to the original post: the CommandLineAPIScope object is created in step 2, not step 1.

### in...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools]

### in...@chromium.org (2019-07-22)

alph@, can you help with an owner for this security issue.

### sh...@chromium.org (2019-08-04)

alph: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-19)

yangguo: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-10-17)

Friendly security sheriff ping - Is there any progress on this? Is there another person we could assign this to?

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ya...@chromium.org (2020-04-16)

[Empty comment from Monorail migration]

### ya...@chromium.org (2020-04-17)

Reduced test case for inspector-test in V8. Run e.g. with `out.gn/x64.debug/inspector-test test/inspector/protocol-test.js test.js`

let {Protocol} = InspectorTest.start(
  "Regression test for 986051");

Protocol.Runtime.enable();
(async function() {
  InspectorTest.log("Regression test");
  evaluateRepl('Object.defineProperty(globalThis, "$0", {configurable: false});');
  evaluateRepl('$0');
  InspectorTest.completeTest();
})();

async function evaluateRepl(expression) {
  InspectorTest.logMessage(await Protocol.Runtime.evaluate({
    expression: expression,
    includeCommandLineAPI: true,
    replMode: true,
  }));
}

### ya...@chromium.org (2020-04-17)

[Empty comment from Monorail migration]

[Monorail components: -Platform>DevTools Platform>DevTools>JavaScript]

### ya...@chromium.org (2020-04-17)

Ok. Having read through the code, and the helpful comments... this is what happens:

Upon every debug-evaluate (both Runtime.evaluate, and Debugger.evaluateOnCallFrame), we can optionally include the command line API, which includes things like debug(), monitor(), $0, or 0_.

These command line API are implemented as an object, where these functions are installed. For every debug-evaluate call, we create a CommandLineAPIScope that lives for the duration of the debug-evaluate call. In the constructor of this scope, we install a number of accessors onto the global object. In the destructor we remove these accessors.

In the accessor, we load the actual API implementations from the command line API, and based on pattern matching of whether it's an accessor (e.g. $0) or function (e.g. debug()),  the accessor returns the call result or returns the value itself. The accessor also checks whether the CommandLineAPIScope has already been destructed based on a field on it (which has been passed to the accessor as data). Checking a field after destruction seems like a bad idea.

The correct implementation should simply provide the command line API object as a context extension when evaluating.

### ya...@chromium.org (2020-04-17)

[Empty comment from Monorail migration]

### sz...@chromium.org (2020-04-17)

I am not sure I understand the last line fully. So instead of doing an indirection via the accessor we install the callbacks directly on to the corresponding global/context? Do we just leave the API functions on the global or remove them again after a Runtime.evaluate finishes?

A possible solution could look like:
  1) The first time code is evaluated, we install the API functions. This way, a page does not have access to the functions unless the user enters something into the console
  2) When we create the API function callbacks, we pass the creating context as part of Data to the implementation. This way we can ensure that the executing context matches the creation context. This way we would restrict the API functions to a single context and prevent them from leaking cross context (should solve https://crbug.com/chromium/1069486)

### ya...@chromium.org (2020-04-17)

I have a minimal fix that addresses the security issue of use-after-free for CommandLineAPIScope. I'll open another bug for a clean up of this whole thing as suggested in https://crbug.com/chromium/986051#c17.

### ya...@chromium.org (2020-04-17)

What I'm suggesting in the last line is that instead of polluting the global object before debug-evaluate, and attempt to clean it up, we should pass the command line API object as a context extension object, similar to what we do with CompileFunctionInContext [0]. I wonder how easy that is for DebugEvaluate::{Global, Local}.

Your suggestion (1) would be bad if page scripts execute between developers interacting with the console. I'm not sure about (2). It sounds good, but are we not executing everything in the same native context?

[0] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/api/api.cc;l=2552?q=compilefunctionincontext&ss=chromium&originalUrl=https:%2F%2Fcs.chromium.org%2F

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3b60af8669916f3b019745f19144392f6b4f6b12

commit 3b60af8669916f3b019745f19144392f6b4f6b12
Author: Yang Guo <yangguo@chromium.org>
Date: Fri Apr 17 13:36:02 2020

[inspector] guard against missing CommandLineAPIScope

Fixed: chromium:986051
Change-Id: I01ef94fe43ac5c8734890706a6dccd01e008bfec
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2153215
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67204}

[modify] https://crrev.com/3b60af8669916f3b019745f19144392f6b4f6b12/src/inspector/v8-console.cc
[modify] https://crrev.com/3b60af8669916f3b019745f19144392f6b4f6b12/src/inspector/v8-console.h
[add] https://crrev.com/3b60af8669916f3b019745f19144392f6b4f6b12/test/inspector/runtime/regress-986051-expected.txt
[add] https://crrev.com/3b60af8669916f3b019745f19144392f6b4f6b12/test/inspector/runtime/regress-986051.js


### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M83. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-04-22)

+adetaylor to review/approve

Please answer questions in https://crbug.com/chromium/986051#c26.

### ad...@google.com (2020-04-22)

I think I'm going to disagree with Sheriffbot here and reject the M83 merge. This is medium severity, but the fix is less than 100% trivial, so I think we should wait for it to release organically in M84.

### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $3,000 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/986051?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095775)*
