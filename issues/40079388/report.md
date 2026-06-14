# Malicious page can escalate to content script privilege level when content script modifies page DOM

| Field | Value |
|-------|-------|
| **Issue ID** | [40079388](https://issues.chromium.org/issues/40079388) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DOM, Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2014-04-21 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36

Steps to reproduce the problem:
1. The page JavaScript registers a listener for the DOMSubtreeModified event on the document.
2. The content script modifies the DOM in some way.
3. The page JavaScript listener is called.
4. The page JavaScript then uses "arguments.callee.caller" to get a reference to the content script function which modified the DOM.
5. The page JavaScript uses the constructor method of the content script function to create a new malicious content script function.
6. The page JavaScript calls the newly created function, which is executed in the isolated world of the content script!

What is the expected behavior?

What went wrong?
The page JavaScript is able to escalate to the privilege level of the content script, simply because the content script modified the page DOM.

Did this work before? N/A 

Chrome version: 34.0.1847.116  Channel: n/a
OS Version: 6.2 (Windows 8)
Flash Version: Shockwave Flash 13.0 r0

Back in May 2013 I reported a security issue with the "isolated world" mechanism used by Chrome extensions.
The vulnerability provides malicious pages with a technique for executing arbitrary attacker-supplied 
JavaScript in a target isolated world environment, escalating to the privilege level of the associated 
content script.

The technique made use of two weaknesses in the isolated world mechanism:

1) It's too easy for the page JavaScript to get a reference to content script functions using event listeners 
and ".caller".

2) Once the page JavaScript has got a reference to a content script function, it can use the constructor 
method to create a new content script function.

An example sequence of events is given below:

-The page JavaScript registers a listener for the DOMSubtreeModified event on the document.
-The content script modifies the DOM in some way.
-The page JavaScript listener is called.
-The page JavaScript then uses "arguments.callee.caller" to get a reference to the content script function which modified the DOM.
-The page JavaScript uses the constructor method of the content script function to create a new malicious content script function.
-The page JavaScript calls the newly created function, which is executed in the isolated world of the content script!

This technique was found to be effective against a large number of Chrome extensions - any extension which 
modifies the DOM after the page JavaScript has executed is at risk. 

Along with the issue description, two proof of concept files were submitted : "AdblockPOC.html" and 
"LastPassPOC.html". The AdBlock POC showed how the technique could be used to alter the extension's settings, 
whitelisting sites without the user's permission and was chosen because of its simplicity and the popularity 
of the extension. The LastPass POC demonstrated how the technique could be used by a malicious page to steal 
login credentials from the LastPass extension and was chosen as a more high severity example.

Shortly after submitting the bug report, the issue was marked as a duplicate and merged into https://crbug.com/chromium/87520.
At the time, access to https://crbug.com/chromium/87520 (https://code.google.com/p/chromium/issues/detail?id=87520) was not 
publicly available and it was not possible for us to check how closely https://crbug.com/chromium/87520 resembled the one 
we had reported.

However, having recently revisited this piece of research, a number of things came to light:

1) https://crbug.com/chromium/87520 is now marked as closed and is publicly accessible. While https://crbug.com/chromium/87520 does concern page 
JavaScript escalating to the content script level, it describes a different, less widely applicable 
technique to the one we identified.

2) The two weaknesses on which our technique is based are both still present and exploitable. (Though, there 
does seem to have been an attempt to fix the function constructor weakness - the specific code used in the 
original POC files, ".constructor('return window')" no longer works).  

3) Our issue, 240207, has now also been marked as closed and made publicly accessible 
(https://code.google.com/p/chromium/issues/detail?id=240207). Despite the fact that the technique described 
there is still effective!

Though the original (now publicly available) POC files thankfully no longer work, they can be made to work with 
relatively few modifications. Two new POC files, "NewAdblockPOC.html" and "NewLastPassPOC.html", which work 
against the latest version of Chrome ("34.0.1847.116 m" at the time of writing) have been created.

The new AdBlock POC file is very similar to the original, while the new LastPass POC file has been adapted 
further and no longer makes use of the function constructor weakness at all. Instead, it's able to steal login 
credentials simply by obtaining a reference to the right content script function and then using ".arguments" 
to get a reference to a content script port object. This was done to demonstrate that weakness no. 1 poses a 
threat to extension security in and of itself.

Like before, these POC files need to be placed on a server to be tested, neither will work if the page URL 
starts with "file://".

## Attachments

- [NewLastPassPOC.html](attachments/NewLastPassPOC.html) (text/html, 4.5 KB)
- [NewAdblockPOC.html](attachments/NewAdblockPOC.html) (text/html, 1.4 KB)
- [main.html](attachments/main.html) (text/html, 180 B)
- [frame.html](attachments/frame.html) (text/html, 235 B)

## Timeline

### fe...@chromium.org (2014-04-21)

adamk@, can you take a look at this?

Triaging as Medium because it could be a bigger vulnerability in an extension that does something silly like eval() a string sent from the content script to the background page.

### fe...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-04-21)

+haraken, who's been trying to stamp out isolated world leakage in preparation for Blink-in-JS.

### ab...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### ab...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-04-21)

Also +danno, as I recall there being some recent fixes

### ad...@chromium.org (2014-04-21)

V8's code for arguments.callee.caller is:

https://code.google.com/p/chromium/codesearch#chromium/src/v8/src/accessors.cc&q=FunctionGetCaller&sq=package:chromium&l=1090

which is as naive as can be: it just looks for the nearest JS function up the callstack from the function it's called on. Given that V8 doesn't know anything about isolated worlds, it's not clear to me what Accessors::FunctionGetCaller should do here.

### da...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ha...@chromium.org (2014-04-22)

> which is as naive as can be: it just looks for the nearest JS function up the callstack from the function it's called on.

It seems strange to me to allow .caller to look up the call stack that crosses embedder stacks.

[V8 func A] => [V8 func B] => [DOM] => [V8 func C]

If we call arguments.callee.caller from C, I'd expect that arguments.callee.caller returns undefined. It seems dangerous to allow .caller to look up cross the embedder boundary.


### fe...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-04-22)

I agree that the 'caller' getter working across embedder boundaries seems strange. But it's possible there are web-compat issues here: Firefox also exposes the calling function across synchronous event dispatches.

### ad...@chromium.org (2014-04-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-04-23)

A strawman fix for this would be to add some notion of "isolated worlds" to V8. For example, imagine (strawman, remember):

v8::Context::TagWithWorldId(int id);

And then the FunctionGetCaller code could null out any caller whose context's world ID differs from the function instance on which 'caller' is being fetched.

### ha...@chromium.org (2014-04-23)

> v8::Context::TagWithWorldId(int id);

I think Firefox is doing something like this. (I haven't checked the implementation, but they were saying that Firefox adds compartment (=world in Blink terminology) tags to the JS engine to detect cross-world references. tasak@ is also thinking about adding the tags to V8.)

### da...@chromium.org (2014-04-24)

[Empty comment from Monorail migration]

### ve...@chromium.org (2014-04-24)

Can we do the same as what we do in MayAccessPreCheck?

Hence check whether requester's frame->context()->native_context() == function->caller()->context()->native_context() or requester_native_context->security_token() == caller_native_context->security_token()?

If that's not sufficient, full access checks will need to support checking global objects in addition to global proxies. We cannot trust that a frame's global proxy is still attached to the frame's global object since navigation can be done by the client doing .caller to succeed security checks.

I'd strongly prefer not adding new security concepts (such as tags) to V8.

### dc...@chromium.org (2014-04-28)

okay, we've discussed this here, and we're going to see if verwaest's suggestion is robust enough to handle all cases.

### ve...@chromium.org (2014-04-29)

Stack trace formatting has the same problem as .caller:

<script>
Error.prepareStackTrace = function f(a,b) { return b; }
function l() {
  try { throw Error(); } catch (e) {
    var stack = e.stack;
    for (var i = 0; i < stack.length; i++) {
      var f = stack[i].getFunction();
      try {
        if (f.constructor != constructor.constructor &&
            f.constructor("return chrome.i18n.getMessage(\"@@extension_id\")")() ==
                "gighmmpiobklfepjocnamgkkbiglidom") {
          var BGcall = f.constructor("return BGcall")();
          BGCall("add_custom_filter", "@@||youtube.com/$document");
          break;
        }
      } catch (e) { }
    }
  }
}
document.addEventListener("DOMSubtreeModified", l);
</script>

### ad...@chromium.org (2014-05-02)

I think dcarney is driving this now.

### ad...@chromium.org (2014-05-05)

This is also a problem for cross-origin frames: unload events fire synchronously. See attached test case. The attempt to read an expando property on the parent window fails (appropriately) with a security error when read directly, but using arguments.callee.caller.constructor to eval code in the parent origin allow access to the expando inside an onunload handler in the child frame.

### dc...@chromium.org (2014-05-06)

update: i've got a fix which is waiting to spend some time in M37 canary before getting backmerged to m36

### in...@chromium.org (2014-05-14)

Fix changeset link ? We should keep bug in status=Fixed if the fix is in. Merge tracking flags will come soon from Sheriffbot.

### cl...@chromium.org (2014-05-14)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-18)

dcarney@ - can you please update this bug with the changeset link for the fix?

### dc...@chromium.org (2014-05-19)

potential cl is here:

https://codereview.chromium.org/261103002/

it causes some inspector issues.  yurys is looking into it

### yu...@chromium.org (2014-05-19)

@dcarney: I see only debugger related tests are failing:
  http/tests/inspector/network/load-resource-when-paused.html [ Timeout ]
  inspector/sources/debugger/debugger-no-pause-on-antibreakpoint.html [ Timeout ]
  inspector/sources/debugger/debugger-pause-in-internal.html [ Timeout ]
  inspector/sources/debugger/debugger-pause-on-exception.html [ Timeout ]
  inspector/sources/debugger/reveal-not-skipped.html [ Timeout ]
this is likely because you are trying to get security token for debug context.


### yu...@chromium.org (2014-05-19)

All of the failing tests use "pause on exception" functionality. DevTools debugger treats all exceptions with empty call stack as syntax errors and automatically resumes execution [1]. In general, filtering call stack returned from v8::StackTrace::CurrentStackTrace based on the current context inside v8 seems wrong to me - this way we cannot show actual call stack to the user in DevTools. Is it possible to do the filtering only when we return result to the user code and skip that step when devtools requests current call stack?


https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/bindings/v8/ScriptDebugServer.cpp&q=ScriptDebugServer::handleV8DebugEvent&sq=package:chromium&type=cs&l=473

### ti...@chromium.org (2014-05-22)

aandrey@ - can you please address the yurys@'s question in c#30 to keep this moving?

### dc...@chromium.org (2014-05-22)

One half of the fix has already rolled into chrome.  I'm not sure if it's in canary.  Another patch will go in next week if this one sticks.

### ti...@chromium.org (2014-05-22)

Cool - I'll leave this alone until next week.

### ti...@chromium.org (2014-05-30)

dcarney@ - Happy next week! Are you in a position to patch the other half of the fix?


### ti...@chromium.org (2014-05-30)

samuel.power256@ - This report received a $1000 cash reward. Congratulations! Our finance team will be in contact within a week or two to discuss payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@chromium.org (2014-05-30)

Moving state back to "Started" until the other half of the fix lands.

### cl...@chromium.org (2014-05-31)

dcarney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-06-06)

bump dcarney@ - can you please provide an update?

### cl...@chromium.org (2014-06-08)

dcarney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### dc...@chromium.org (2014-06-11)

sorry, have been sick/on vacation and haven't updated this.  the second fix will go into v8 tomorrow and chrome probably on friday

### cl...@chromium.org (2014-06-20)

dcarney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-06-27)

Hey Dan - did the fix in c#40 land? If so, please mark this bug as fixed.

### dc...@chromium.org (2014-06-27)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-07)

Thanks Dan! Can you please provide the changeset/CLs so that the release manager can assess how complex your change is when requesting a merge?

### dc...@chromium.org (2014-07-14)

these are the cls:

https://codereview.chromium.org/261103002/
https://codereview.chromium.org/294073002/


### ti...@chromium.org (2014-07-14)

I'm assuming that these aren't going to ship with M36 as I don't see r21366 and r21793 in go/v8rel.

I'll leave this out of the release notes for M36 and put in the release notes for M36 patch 1 just to be safe.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-22)

Bump dcarney@ - re: c#46. Have these fixes been merged?

### in...@chromium.org (2014-08-02)

Are these merged to M37 ?

### jo...@chromium.org (2014-08-05)

both CLs look like they made it into the 3.27 branch

### am...@chromium.org (2014-08-06)

Removing the merge request label per #50

### ti...@chromium.org (2014-09-26)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-10-03)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/365359?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Platform>Extensions]
[Monorail blocking: crbug.com/chromium/341032]
[Monorail mergedwith: crbug.com/chromium/240207]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079388)*
