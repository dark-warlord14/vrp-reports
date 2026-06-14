# Cross origin access with exception object + full exploit

| Field | Value |
|-------|-------|
| **Issue ID** | [40081296](https://issues.chromium.org/issues/40081296) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Unknown |
| **Reporter** | se...@gmail.com |
| **Assignee** | jl...@chromium.org |
| **Created** | 2015-01-30 |
| **Bounty** | $25,633.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36

Steps to reproduce the problem:
1. 
2. 
3. 

What is the expected behavior?

What went wrong?
The main bug in the exploit chain is UXSS.

src/third_party/WebKit/Source/bindings/core/v8/custom/V8WindowCustom.cpp:
---------------------------------
void V8Window::openMethodCustom(const v8::FunctionCallbackInfo<v8::Value>& info)
{
    LocalDOMWindow* impl = toLocalDOMWindow(V8Window::toImpl(info.Holder()));
    ExceptionState exceptionState(ExceptionState::ExecutionContext, "open", "Window", info.Holder(), info.GetIsolate());
    if (!BindingSecurity::shouldAllowAccessToFrame(info.GetIsolate(), impl->frame(), exceptionState)) {
        exceptionState.throwIfNeeded();
        return;
    }
---------------------------------

src/third_party/WebKit/Source/bindings/core/v8/ExceptionState.h:
---------------------------------
ExceptionState(Context context, const char* propertyName, const char* interfaceName, const v8::Handle<v8::Object>& creationContext, v8::Isolate* isolate)
    : m_code(0)
    , m_context(context)
    , m_propertyName(propertyName)
    , m_interfaceName(interfaceName)
    , m_creationContext(creationContext)
    , m_isolate(isolate) { }
---------------------------------

When a DOM method throws an exception, the creation context for the exception object is inherited from the object the method is called
on even if it's from a different origin. The created object doesn't have any access checks so an attacker can use it to obtain a reference
to e.g. the function constructor.

Repro:
---------------------------------
try {
	window.open.call(victimWindow)
} catch (ex) {
	fun = ex.constructor.constructor; //this is actually victimWindow.Function
	fun("alert(location)")();
}
---------------------------------
or:
---------------------------------
try { 
	location.assign.call(victimWindow.location) 
} catch (ex) {
	ex.constructor.constructor("alert(location)")();
}
---------------------------------
or:
---------------------------------
try { 
	victimWindow.opener = 1
} catch (ex) {
	ex.constructor.constructor("alert(location)")();
}
---------------------------------
etc.

---

The first part of the exploit is designed to cross the process boundary between a regular web page and the New Tab page.

The New Tab page is essentially just a web page hosted on Google's servers with the very limited set of special features.
The exploit needs just one of them - the ability to open "chrome://*" URLs.

Algorithm:
1) Load and UXSS a page at https://www.gooogle.com/. We can choose a nonexistent page so the webserver won't respond with
X-Frame-Options or CSP headers.
2) Load via XHR and parse a page at https://www.gooogle.com/ to find out which localized Google domain the exploit should
use for the NTP URL.
3) Load and UXSS a page at the localized domain (using the same trick with the 404 page).
4) Register a new ServiceWorker for the scope of the localized domain.
The exploit uses the FileSystem API to store the worker script at the URL that is allowed by the ServiceWorker API. This
seems to be either a bug or a very dangerous design decision.
5) Initiate a navigation to the NTP.
Now when the newly created privileged process requests the NTP contents our service worker will replace it with the second
part of the exploit.

The short second part is the transition from the NTP process to the component extension process.
There is an internal component extension in Chrome called "GaiaAuthExtension". The main page of the extension accepts the
"gaiaUrl" URI parameter as the source URL for the IFrame element. That's a good candidate for the transition. However that
extension is only accessible when the "chrome://chrome-signin/" page is opened in the browser. So the whole algorithm is:
6) Open "chrome://chrome-signin/" in a new tab.
7) Open the "GaiaAuthExtension" main page with the third part of the exploit encoded as a data: URL in the "gaiaUrl" param.

"GaiaAuthExtension" is a very powerful extension, for example, it has the permission to control all chrome:// pages.
The third part of exploit uses that power to gain RCE.

8) UXSS the top frame.
The extension implements CSP so window.Function wouldn't work. To bypass it the exploit gets the getOwnPropertyDescriptor
function from the exception object and then calls it on the top window object to read the "URL" and "document" properties.
"URL" is used to create a new blob: URL with the extension's security origin and "document" - to inject a new Script element
with its "src" attribute set to the blob: URL.
9) Open the Google Now extension page.
That's another component extension and it has the "webstorePrivate" permission the exploit needs.
10) Using the context of the Google Now extension initiate the theme installation process.
I've uploaded a theme to the Chrome Web Store with the .exe file inside. When installation is done the .exe will be stored
at the predictable location relative to the profile directory and installing a theme doesn't cause the confirmation dialog
to show up.
11) Open chrome://settings-frame/ and change the default download directory preference to the path of the downloaded .exe.
12) Open chrome://downloads/ and execute the "open downloads folder" command to run the .exe file.

Versions:
Google Chrome 40.0.2214.93
Google Chrome 42.0.2291.1 canary 

Did this work before? N/A 

Chrome version: 40.0.2214.93  Channel: n/a
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 16.0 r0

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 7.3 KB)
- [exploit_us.html](attachments/exploit_us.html) (text/html, 7.3 KB)

## Timeline

### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-01-30)

- https://crbug.com/chromium/453979 for the V8 binding UXSS
- https://crbug.com/chromium/387037 for opening chrome://downloads/ allowing to run .exe files

### ri...@chromium.org (2015-01-30)

Very nice bugs!

### wf...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-01-30)

serg you should compile your exploit binaries with msvcrt.dll and not msvcrt120.dll dependency :) did not work on my clean Windows box.  But yes, nice exploit chain!

### ri...@chromium.org (2015-01-30)

Patched copy for folks whose localized domain is already google.com.

The change is just replacing:

try {
        frame.contentWindow.opener = 1;
} catch (e) {
        exceptionObject = e;
}
googFunc = exceptionObject.constructor.constructor;

with:

googFunc = Function
try {
        frame.contentWindow.opener = 1;
} catch (e) {
        googFunc = exceptionObject.constructor.constructor;
}


### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-01-30)

- https://crbug.com/chromium/453982 created for step (4) (ServiceWorker API interaction with FileSystem API).

### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-01-30)

- https://crbug.com/chromium/453994 for step 7 and GaiaAuthExtension

### jl...@chromium.org (2015-01-30)

[Empty comment from Monorail migration]

### pa...@google.com (2015-01-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-31)

filed a bug for the gfe issue - https://b.corp.google.com/u/0/issues/19215893. Joel, can you please put the recommendations whatever  X-Frame-Options/CSP we need to block this in the internal bug.

### se...@gmail.com (2015-01-31)

[Comment Deleted]

### in...@chromium.org (2015-01-31)

from https://b/19215893
Matt Smart  <smart@google.com>  #2 Jan 31, 2015, 8:47:34 AM

There was a thread about this starting Jan. 11 and the conclusion from evn@
was that this was easily bypassed, so it wasn't useful to do at the GFE.
-----

+cc Eduardo, Michal for implications 

### in...@chromium.org (2015-01-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-01-31)

changing to RV-SecurityEmbargo based on comment in #17

### ri...@chromium.org (2015-02-02)

[Empty comment from Monorail migration]

### ev...@google.com (2015-02-02)

oh, haha.. nice :)

If you can use filesystem:/blob: URIs to load service workers we are pretty much doomed. Can we fix that?

We are working to add a 403 on all Service-Worker: script requests on GFE but of course that only works as long as one can't bypass this.

### in...@chromium.org (2015-02-02)

Eduardo, that should be fixed in https://code.google.com/p/chromium/issues/detail?id=453982#c14 [https://chromium.googlesource.com/chromium/src.git/+/22394d843a6c36eb2e6d7bdf4fb8e7c4b7ae8d68]

### ti...@google.com (2015-02-02)

Adding Restrict-View-Google as reporter wishes to remain anonymous.

### ti...@google.com (2015-02-02)

I'm reliably told that Restrict-View-Google is overkill here and that Restrict-View-SecurityEmbargo will do the job here.

### cl...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-02-05)

Assigning to jln@ who has been managing the response, to stop the missing_owner spam.

### cl...@chromium.org (2015-02-10)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-18)

Is there any work left in this bug other than https://crbug.com/chromium/387037?

Otherwise can we close it since that's what we did for previous umbrella bugs for exploits? (e.g. 386988)

### ti...@google.com (2015-02-18)

I say yes because the chain is broken.

### ti...@google.com (2015-03-03)

Fantastic report as always!

Reward amount was $15,000 for the Sandbox Escape + $7,500 for the Renderer RCE + $3,133.7 as a leet bonus for being awesome.

Total: $25,633.70


### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### ev...@google.com (2015-09-25)

[Empty comment from Monorail migration]

### ev...@google.com (2016-02-17)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-27)

Removing embargo as agreed with Sergei.

### [Deleted User] (2020-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-27)

This issue was migrated from crbug.com/chromium/453937?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/387037, crbug.com/chromium/453979, crbug.com/chromium/453982, crbug.com/chromium/453994]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081296)*
