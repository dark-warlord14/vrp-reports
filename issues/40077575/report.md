# Escalate access to browser internals

| Field | Value |
|-------|-------|
| **Issue ID** | [40077575](https://issues.chromium.org/issues/40077575) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Reporter** | da...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-05-20 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.81 Safari/537.36

Steps to reproduce the problem:
1. Set up a Setter for console._commandLineAPI

  ```javascript
console.__defineSetter__('_commandLineAPI', function(e){
  var internal = arguments.callee.caller.arguments.callee.caller.arguments[1];
  internal.databaseId(42424242);
});
```
2. Open the JS Console / Inspector, Use the console (Enter a couple of characters)
4. Watch the crash (Verify that you have access to the InjectedScriptHost-object)

What is the expected behavior?
Privilege Escalation to internal scope and/or Crash

What went wrong?
The code path from public to internal scope has not been removed

Did this work before? N/A 

Chrome version: 27.0.1453.81  Channel: stable
OS Version: OS X 10.7.5

There are more internal interfaces like this, they all seem rather unfuzzed

## Attachments

- [chrome_bug_console_commandLineAPI.html](attachments/chrome_bug_console_commandLineAPI.html) (text/plain; charset=us-ascii, 191 B)

## Timeline

### ts...@chromium.org (2013-05-20)

Severity medium because of the interaction required.

V8InjectedScriptHost::databaseIdMethodCustom() trusting that its args[0] is always an object.

283	    Database* database = V8Database::toNative(v8::Handle<v8::Object>::Cast(args[0]))



### ts...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-05-20)

Kentaro, could you please take a look.  Thanks!

### ts...@chromium.org (2013-05-20)

Even better, changing the example to call internal.database(document) winds up with Database* database pointing at an HTMLDocument in the line above.

### ts...@chromium.org (2013-05-20)

I've put up a quick patch at https://codereview.chromium.org/15496007/ to cover the missing validation.

There is still a big issue as to why the InjectedScriptHost can be obtained by the webpage.

### sc...@gmail.com (2013-05-20)

[Empty comment from Monorail migration]

### da...@gmail.com (2013-05-20)

I'm happy to fix it if you're busy.

### ha...@chromium.org (2013-05-20)

> I've put up a quick patch at https://codereview.chromium.org/15496007/ to cover the missing validation.

LGTMed the patch.

> I'm happy to fix it if you're busy.

I'm out of office today. I can take a look tomorrow, but feel free to steal it:)

### bu...@chromium.org (2013-05-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=150726

------------------------------------------------------------------------
r150726 | tsepez@chromium.org | 2013-05-21T00:57:24.449989Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/custom/V8InjectedScriptHostCustom.cpp?r1=150726&r2=150725&pathrev=150726

Validate types of arguments passed to V8InjectedScriptHost custom methods.

This adds the typical argument checks to databaseIdMethodCustom() and
storageIdMethodCustom().

BUG=242322
R=haraken@chromium.org

Review URL: https://chromiumcodereview.appspot.com/15496007
------------------------------------------------------------------------

### in...@chromium.org (2013-05-21)

Is there more work pending in this ?

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### da...@gmail.com (2013-05-21)

The primary bug that I wanted to report is: You can access InternalScriptHost. You shouldn't be able to do that.
Do you guys want me to propose a patch? I'm not extremely familiar with the Chromium Source, so it'll take me the night probably.

### ts...@chromium.org (2013-05-21)

Yes, the problem is external script host.  The patch I landed is just a quick fix to stop the current issue, and would act as a second line of defense in a world where there is no script host access.

In some sense, its a bad design if the ISH provides the debugger with power over the page that the page doesn't have itself. A fix along those lines would be better.

Daniel, you're welcome to try a patch, but I think that you'll find the learning curve fairly steep. I wouldn't spend too much time on it. 



### pa...@chromium.org (2013-05-22)

But we welcome your security interest and continued hacking :)

### ha...@chromium.org (2013-05-22)

pfeldman, yurys: This looks like a design issue of how InjectedScriptHost should be exposed to JavaScript. It is possible to forbid all exposes (simply by not creating a JS wrapper of InjectedScriptHost), but it wouldn't be an expected solution since we want to access InjectedScriptHost's methods in some debugger JS contexts. WDYT?


### ha...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### yu...@chromium.org (2013-05-22)

@haraken: I'm not sure what you meant by "It is possible to forbid all exposes (simply by not creating a JS wrapper of InjectedScriptHost)", could you elaborate?

@tzepez: ISH shouldn't provide the script with more privileges than it has and I don't think it does at the moment. There was XSS possibility caused by InjectedScriptHost::inspectedObject but that was fixed by returning null if calling function doesn't have access to it due to same origin policy (see https://code.google.com/p/chromium/issues/detail?id=178336 for details).



### ha...@chromium.org (2013-05-22)

> @haraken: I'm not sure what you meant by "It is possible to forbid all exposes (simply by not creating a JS wrapper of InjectedScriptHost)", could you elaborate?

We can just remove wrap(InjectedScriptHost*) and redirect toV8(InjectedScriptHost*) to return another proper JS wrapper. (e.g. IDBAny is doing the same thing.) This means that you cannot get InjectedScriptHost's wrapper in any way. I don't think this is what we want to do. (e.g. we want to access InjectedScriptHost's wrapper from some debug contexts.)

### ha...@chromium.org (2013-05-22)

So I'd like to understand how (or when) InjectedScrippHost's wrapper should be exposed.


### pf...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-05-22)

So apart from the possiblities of flaws in the ISH methods, it doesn't seem like there are security issues with allowing the ISH to be visible to the page.

It might be nice to have a comment explaining that you can't add methods to ISH that grant power beyond what the page already has been granted.

One thing that's odd to me is the lines in InjectedScriptHost.js:

                inspectedWindow.console._commandLineAPI = new CommandLineAPI(this._commandLineAPIImpl, isEvalOnCallFrame ? object : null);
                expression = "with ((window && window.console && window.console._commandLineAPI) || {}) {\n" + expression + "\n}";
 
Why do we need to hold this in a member of inspectedWindow.console? Couldn't we just use a local var instead and still pull off the same "with" trick?  I didn't see any other places in the code where JS access to _commandLineAPI is reqiured. That would kill the __getter__ trick used here.


### pf...@chromium.org (2013-05-22)

@tsepez: var won't work since you need to reference it from the eval string.

### ts...@chromium.org (2013-05-22)

@haraken - Are we going to make the change you suggested in #18?  If not, please close this out.

### ts...@chromium.org (2013-05-22)

@pfeldman - My JS-fu isn't as strong as yours, but I meant that instead of doing:
  eval("with (x) { " + expression + "}");
do:
  with (x) { eval(expression) };
which I think results in an eval being performed with x in its scope chain.



### yu...@chromium.org (2013-05-22)

@tsepez: "with (x) { eval(expression) };" will result in a local eval which means that context of _evaluateOn function will be in the evaluated script scope chain. Also eval can be overridden in the inspected page and we use eval function passed as argument which performs global eval and wrapping it into with(x) {} will have no effect.

### yu...@chromium.org (2013-05-22)

@haraken: I'm still not following you, the only purpose of InjectedScriptHost is to provide devtools injected script with access to the native parts of inspector backend, what kind of "another proper JS wrapper" exposing same functionality can be returned from toV8(InjectedScriptHost*)?

### ha...@chromium.org (2013-05-23)

@yuyrs: Now I understood the situation and understood that my idea is off the point. Please ignore the "another JS wrapper" idea.

I'm still not sure how to fix the issue. Let me ask a couple of questions:

- Is it OK to expose ISH wrappers to web pages, as tsepez@ mentioned?

- If we want to expose ISH wrappers only to devtools, how can we do it? Is there any inspector objects that have the same expose policy? (Then we can implement the same thing to ISH wrappers.)

### ts...@chromium.org (2013-05-23)

I'm going to close this one out based on c17 - I don't think there's anything more we can do here, then.

### in...@chromium.org (2013-05-23)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-05-23)

Codereview up at https://codereview.chromium.org/15808005/ which adds a comment along the lines of C17.

### sc...@gmail.com (2013-05-28)

M27 is r151278
M28 is r151279

### sc...@gmail.com (2013-06-03)

@daniel.zulla: thanks for the report: It qualifies for a $500 Chromium Security Reward!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### da...@gmail.com (2013-06-04)

Much appreciated, thank you!

### da...@gmail.com (2013-06-07)

Is there something that I have to do for the reward? I do not know the procedure there. Thanks!

### pa...@chromium.org (2013-06-14)

Hey Daniel,

We do a monthly payout sweep. Someone should be in touch next week to get your personal information so we can send out the reward.

### pa...@chromium.org (2013-06-24)

Sorry Daniel, I got delayed by a few things and just kicked off payment for this one today. Someone in our finance team should be in touch this week.

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/242322?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077575)*
