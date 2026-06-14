# Universal XSS in DocumentLoader::createWriterFor + full-chain exploit

| Field | Value |
|-------|-------|
| **Issue ID** | [40083619](https://issues.chromium.org/issues/40083619) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2016-02-02 |
| **Bounty** | $25,633.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
This is somewhat of a remake of the last year's exploit (https://code.google.com/p/chromium/issues/detail?id=453937).
Most of the steps in the two exploit chains are similar so it might be useful to take a look at the old report.

I. UXSS in DocumentLoader::createWriterFor.

third_party/WebKit/Source/core/loader/DocumentLoader.cpp:735:
PassRefPtrWillBeRawPtr<DocumentWriter> DocumentLoader::createWriterFor(const Document* ownerDocument, const DocumentInit& init,
const AtomicString& mimeType, const AtomicString& encoding, bool dispatch, ParserSynchronizationPolicy parsingPolicy)
{
    LocalFrame* frame = init.frame();

    ASSERT(!frame->document() || !frame->document()->isActive());
    ASSERT(frame->tree().childCount() == 0);

    if (!init.shouldReuseDefaultView())
        frame->setDOMWindow(LocalDOMWindow::create(*frame));

    RefPtrWillBeRawPtr<Document> document = frame->localDOMWindow()->installNewDocument(mimeType, init);
    if (ownerDocument) {
        document->setCookieURL(ownerDocument->cookieURL());
        document->setSecurityOrigin(ownerDocument->securityOrigin());

DocumentLoader calls |setSecurityOrigin| instead of |updateSecurityOrigin|, so while the document inherits the correct SecurityOrigin
from the owner, its associated v8 context is left with the old security token which is used for access checks.

Repro:
<body>
<script>
var frame = document.body.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/intl/en/ads/";
frame.onload = function () {
    frame.onload = null;
    frame.contentWindow.frames[0].location = "data:text/html,<script>(" + function () {
        frame = document.documentElement.appendChild(document.createElement("iframe"));
        frame.contentWindow.setTimeout("parent.document.open()", 0);
        setTimeout(function () { location = "javascript:'<script>parent.eval(\"alert(location)\")</scr" + "ipt>'" }, 0);
    } + "())</scr" + "ipt>";
}
</script>
</body>

Note the |document.open()| call in the repro is used to set the document URL to "about:blank" which forces the javascript: generated
document to inherit the origin from the parent frame's document.

II. Transition to the New Tab page process using the Cache API.

Since the NTP service worker uses the Cache API which is now also available from a global context, it is an easy task.
The exploit applies the UXSS bug against the google's domain to inject the script into the NTP cache entry and then loads the NTP URL.
After a process swap the service worker returns the poisoned entry.

III. Transition to the GAIA auth extension process via a browser restart.

The New Tab page has the function named |navigateContentWindow| that allows opening any URL including the chrome:// scheme and bypasses
the popup blocker. Once the injected script has been loaded it opens "chrome://chrome-signin/" in a new tab to make the GAIA auth extension
accessible to other pages. Then the UXSS is used again to create an HTML5 filesystem file object within the context of the extension page.
The exploit writes itself into that file and loads the associated filesystem: URL in another tab to bypass the Content Security Policy enforced
by the extension. In the context of that new page the exploit makes a new navigation entry in which the URL of the main frame is
"chrome-extension://mfffpogegjflfpflabcdkioaeobkgjik/main.html" and the URL of the child frame is the filesystem: URL created above.
Poisoned navigation entries have been used for privilege escalation before (e.g. https://code.google.com/p/chromium/issues/detail?id=171839),
this time, the successful attack also requires forcing the browser to restart, and then restore the session. This can be done by navigating to
the chrome://restart URL. When the restoration is done, the exploit runs inside the privileged extension process.

IV. Abusing chrome://settings, chrome://downloads and the chrome webstore for code execution.

Now the exploit is able to script any chrome:// page through the chrome.tabs API. The steps for code execution outside the sandbox are:
1. (in the context of chrome://settings-frame) Set the default download path to "%USERDATADIR%\Extensions\ghmkgdjpadfalecomlhllfckggkcdppi\1.2_0".
2. (any) Initiate a download of some .exe file considered safe by SafeBrowsing (particularly the exploit downloads the chrome installer).
The downloaded file is saved as "%USERDATADIR%\Extensions\ghmkgdjpadfalecomlhllfckggkcdppi\1.2_0\RunCalc.exe".
3. (the chrome webstore) - Install the theme with id "ghmkgdjpadfalecomlhllfckggkcdppi". That's the theme with an .exe file inside used
for the last year's exploit. The file downloaded in the previous step is not overwritten though since the theme is installed in "%USERDATADIR%\Extensions\ghmkgdjpadfalecomlhllfckggkcdppi\1.2_1".
4. (chrome://settings-frame) Switch to the default theme. The whole "%USERDATADIR%\Extensions\ghmkgdjpadfalecomlhllfckggkcdppi" directory
is deleted. 
5. (the chrome webstore) - Install the same theme again. Now the payload .exe is at the path referenced by the download entry.
6. (chrome://downloads) - Open the downloaded file.

Version:

Google Chrome 48.0.2564.97 (Официальная сборка) m (64 бит)

The second attached file contains a bunch of alerts so it's easier to see what the exploit is doing step by step.

--

I would like to remain anonymous for this report.

Did this work before? N/A 

Chrome version: 48.0.2564.97  Channel: n/a
OS Version: 6.3
Flash Version: Shockwave Flash 20.0 r0

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 12.2 KB)
- [exploit_with_alerts.html](attachments/exploit_with_alerts.html) (text/html, 12.3 KB)
- [exx_canary.html](attachments/exx_canary.html) (text/html, 12.3 KB)

## Timeline

### mb...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-02)

|navigateContentWindow| has already been called out in the past for being too powerful. Marking it as a blocker: this really needs to be addressed by the NTP team.

### dc...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-02)

Thanks for the great report!

Unfortunately the next stable release cut is being brought forward to 4pm PST today due to a severe non-security regression, so we may have to consider pushing another out-of-band release when this is fixed.

### ke...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-02-02)

Assigning to Tim since the actual bug fixes should happen in the blocking bugs.

### ke...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-02-03)

Very nice.  And yes, I'm frustrated that https://crbug.com/chromium/509313 (navigateContentWindow) hasn't been fixed yet.

Is this expected to repro on M50 as well?  I'm seeing a SecurityError early in the repro (on the "the frame inside google.com" stage) there, unlike on M48.

Side note: it appears that running with --isolate-extensions prevents this attack (even on M48), since the GaiaAuthExtension is loaded in an out-of-process iframe in the extension process, rather than in the hijacked NTP.  It seems like that mode would generally prevent a UXSS in a web process (or even the NTP) from accessing extension origins.

Nasko and I will continue to look at additional lines of defense.  So far, the UXSS, navigateContentWindow, and preventing .exe files in themes seem important.

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-02-03)

haha, I changed the HTML spec last week to introduce that security error :)

### jo...@chromium.org (2016-02-03)

https://codereview.chromium.org/1611523002 - we could easily merge that back to break this chain

### se...@gmail.com (2016-02-03)

@creis That exception is thrown due to @jochen's recent changes in |document.open()|.
Those are not critical to the exploit though so I've modified the repro to work on Canary.

### la...@google.com (2016-02-03)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ne...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### tr...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### fi...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-02-05)

[Comment Deleted]

### go...@chromium.org (2016-02-05)

Any update on this? 

fyi: We're planning to cut Stable candidate @ 4:00 pm PST this Fri and release on Tuesday. 

### dc...@chromium.org (2016-02-05)

I've made a merge request to for https://crbug.com/chromium/509313: I'm waiting one final review on https://codereview.chromium.org/1675473002 to land it so we can merge that fix to M48 as well.

### ti...@google.com (2016-02-08)

Marking as fixed based on resolution of https://crbug.com/chromium/583345.

### ti...@google.com (2016-02-09)

Removing release tag as change was reverted on the blocking bug. (This isn't shipping with the M48 release today).

### dc...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-02-18)

timwillis: Should this be marked as fixed now (as per your comment in #23)?

### ti...@google.com (2016-02-18)

raymes: Yes, and it's shipping today in the next stable.

### ti...@google.com (2016-02-18)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-18)

Hey Serg - Awesome report as always. The panel decided on $25,633.7 for this report as follows:

$15k for the sandbox escape
$7.5k for the UXSS
+$3,133.7 discretionary leet bonus for excellent report quality and reproduction steps.

We'll put this in the release notes with the next version and I'll start payment next week. Thanks again!

### ti...@google.com (2016-02-18)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-27)

Removing embargo as agreed with Sergei.

### [Deleted User] (2020-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xu...@gtempaccount.com (2021-02-16)

Could anyone paste the link to the patch? The issue was fixed in #583345, which again references #583513. But not anyone in our team has access to #583513.

### is...@google.com (2021-02-16)

This issue was migrated from crbug.com/chromium/583431?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/509313, crbug.com/chromium/583445]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083619)*
