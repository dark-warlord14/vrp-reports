# Security: CORB not enforced for WebSocket requests 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094352](https://issues.chromium.org/issues/40094352) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebSockets, Internals>Sandbox>SiteIsolation, Platform>DevTools>Network, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@piosek.pl |
| **Assignee** | yo...@chromium.org |
| **Created** | 2019-03-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

CORB policy is not enforced for WebSocket requests. It is possible to create new WebSocket object with connection URL which refers to resource for which Content-Type header is set e.g. to text/html. In such situation CORB policy violation doesn't occurs.

**VERSION**  

Chrome Version: 73.0.3683.86 stable  

Operating System: macOS 10.14.3

**REPRODUCTION CASE**

1. Create new WebSocket object with URL set to any resource (endpoint) which response should be protected with CORB, e.g.: var ws = new WebSocket("wss://httpbin.org/html")

Result: response is not blocked (e.g. response headers are not overwritten)  

Excepted result: response should be blocked with CORB

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: <https://twitter.com/piochu>

## Attachments

- [CORB_WebSocket.mp4](attachments/CORB_WebSocket.mp4) (video/mp4, 861.9 KB)

## Timeline

### ke...@chromium.org (2019-03-22)

Thanks for the report.

creis, lukasza: WDYT?

### ma...@piosek.pl (2019-03-22)

Update, I just noticed that example with httpbin.org might not be as good as should be, because X-Content-Type-Options header is not present in their responses. However if you replace this URL with other for which required header is added (e.g. new WebSocket("wss://w00t.pl/?xss=abc");), then this issue still exists.

### lu...@chromium.org (2019-03-22)

Thanks for the report marcin@!

Some questions to verify the impact / scope of this bug (and differences, if any from https://crbug.com/chromium/924972):

- I assume that only the response headers (but not the response body) are disclosed to a cross-origin renderer process?

- Are the response headers disclosed to a cross-origin rendeder process if DevTools are *not* opened? (https://crbug.com/chromium/849483 tracks the work for avoiding the disclosure when the DevTools are present)

[Monorail components: Internals>Sandbox>SiteIsolation]

### yh...@chromium.org (2019-03-25)

As a websocket request always attaches origin, I think it's corresponding to CORS and out of scope of CORB.

[Monorail components: Blink>Network>WebSockets]

### ri...@chromium.org (2019-03-25)

The difference seems to be that https://crbug.com/chromium/924972 only concerns cookie headers, whereas this issue concerns all headers.

My concerns:
* If we change this it will make debugging cross-origin WebSocket failures using DevTools incredibly difficult.
* I don't know how to resolve this and still permit extensions to have access to the headers. +jam, any ideas?

### ke...@chromium.org (2019-03-25)

Flagging and assigning an owner since this sounds like a legitimate bypass.

### ma...@piosek.pl (2019-03-25)

@lukasza, I am still researching the matter but by way of answering one of your questions from https://crbug.com/chromium/944619#c3, please note the video I attached. In that video, you can see that the value of the Content-Length header is changing. In my opinion, it is a result of the fact that the content of the response may also be disclosed in renderer process.

### ri...@chromium.org (2019-03-26)

#7 To clarify, the content of the response will not be disclosed to the renderer process. It is discarded in the network process as soon as we discover that the WebSocket handshake has failed.

The only thing that is being disclosed to the render process is the response headers.

### ri...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

### ri...@chromium.org (2019-03-26)

We also disclose information via diagnostic console messages. For example, the "Error during WebSocket handshake: Unexpected response code: 200".

If we block the headers we should logically also block those helpful console messages, but again this would make debugging failures hard.

Also, it appears that the CORB console error messages are also disclosing information about the response to the render process?

### lu...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-26)

We should be able to send information to DevTools securely without going through the renderer by using content/browser/devtools as long as we have all the context we need within the browser process. This is related to https://crbug.com/chromium/849483 but I think we can do this without moving _all_ of our devtools network instrumentation to the browser process.

Simply sending a console message saying there was an error with the websocket should be simple. If we want to attribute the error to a javascript location or network request would take more work.

### ri...@chromium.org (2019-03-26)

#12 The console messages have a source location, and the network tab has an "Initiator" field which links to the place the WebSocket was constructed.

It would be an obvious regression if we removed these (but not as bad as removing all diagnostic information).

### ke...@chromium.org (2019-03-26)

Lowering the severity -- I hadn't realized when I originally set it that DevTools had to be open for this to happen.

### lu...@chromium.org (2019-03-26)

ricea@, would it be okay if I reassigned this bug to you? (I am not as familiar with WebSockets as you are)

I wonder if you could please help with answering the questions from https://crbug.com/chromium/944619#c3.  In particular, it would be very helpful if you could confirm if CORB is bypassable only if DevTools are opened:
- This would reinforce the decision to lower the severity of this bug in https://crbug.com/chromium/944619#c14
- It would help us understand the overall shape of Site Isolation protections in M75
- It would help us determine the priority of fixing this bug VS bumping up priority of fixing https://crbug.com/chromium/849483.

### ri...@chromium.org (2019-03-26)

#15 The response headers are sent to the renderer even if DevTools is not open. I just verified this by logging the headers.

The reason for it is that the WebSocket mojo interface is proxied via the browser process, so that extensions can examine the headers. But the browser process doesn't know whether or not it should forward the headers to the renderer, so it always does.

### ja...@chromium.org (2019-03-26)

I see that the URLLoader interface supports CORB with the should_report_corb_blocking field in UrlLoaderCompletionStatus: https://cs.chromium.org/chromium/src/services/network/public/cpp/url_loader_completion_status.h?l=72&rcl=324086b58601cd1f03f7c10966b8fecc1324024a

Could we take a similar approach with WebSockets? Perhaps by adding a CORB parameter to WebSocketClient's OnFailChannel, and calling it instead of OnFinishOpeningHandshake for CORB? Or does that somehow screw with the proxy for extensions?

I didn't see anyone address c#4 - are we sure WebSockets should be CORB, not CORS?

### yh...@chromium.org (2019-03-27)

Sorry, #4 was wrong. I didn't understand it was about the failure case.

I think we shouldn't provide status code and headers for failed handshake to cross-origin URL. Removing such information will regress developers experience, but I think in this case security is more important. We will be able to put sensitive information to devtools when https://crbug.com/chromium/849483 is fixed. We can put some console messages without exposing sensitive information to mitigate the pain (c.f., [1]).

1: third_party/blink/renderer/platform/loader/cors/cors_error_string.cc


### dg...@chromium.org (2019-05-08)

[Empty comment from Monorail migration]

### ma...@piosek.pl (2019-05-16)

I apologize for my directness, but I see that work on this application may take some time. However, I would like to know if based on the c#16 it can be considered that this report qualifies for the VRP [1]?

[1] https://www.google.com/about/appsecurity/chrome-rewards/ (section "Site Isolation special rewards", "Bugs that cause cross-site CORB-eligible responses not to be blocked")

### lu...@chromium.org (2019-05-16)

+1 to yhirano@'s idea from https://crbug.com/chromium/944619#c18 to strip response headers before delivering them to the renderer process, if the response corresponds to a failed WebSocket handshake to a cross-origin URL.  Is this something that we could possibly implement in M76?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ma...@piosek.pl (2019-08-19)

It has been over 3 months since label "reward-topanel" was added. According to c#6 and c#16 issue was considered as valid CORB bypass. Based on this, could I ask for feedback about VRP? 

Of course if there is something wrong with my report I would appreciate feedback.

### lu...@chromium.org (2019-09-09)

RE: https://crbug.com/chromium/944619#c24: marcin@

I apologize for letting this issue fall through the cracks and not be acted upon for quite a while.  I suspect that the "reward-topanel" might have been ignored because the VRP panel doesn't usually consider bugs until they've been fixed.  Let me loop in awhalley@ to confirm this.

### lu...@chromium.org (2019-09-09)

Based on https://crbug.com/chromium/944619#c16 from ricea@ ("the response headers are sent to the renderer even if DevTools is not open") let me also bump up the severity of this bug back-up (undoing the medium->low downgrade from https://crbug.com/chromium/944619#c14).

### lu...@chromium.org (2019-09-09)

awhalley@, could you PTAL at the question in https://crbug.com/chromium/944619#c24 (and at my attempt to answer it in https://crbug.com/chromium/944619#c25)?

I believe this is a valid Site Isolation bypass and should be considered for the Site Isolation special rewards from https://www.google.com/about/appsecurity/chrome-rewards

### lu...@chromium.org (2019-09-09)

ricea@, do we know what the next steps should be for this bug?  Does the fix depend on any DevTools refactoring, or is there a smaller fix available?

My apologies for missing earlier that this bug's severity might be incorrect.  The corrected severity means (per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-medium-severity) that the bug should be "assigned priority Pri-1 and assigned to the current stable milestone".

### ja...@chromium.org (2019-09-10)

I don't think DevTools has any more network instrumentation refactoring planned, https://crbug.com/chromium/849483 should probably be closed.
We have instrumentation in the browser process that can be hooked into with content/browser/devtools/devtools_instrumentation.h.
As I mentioned in https://crbug.com/chromium/944619#c17 I think a CORB flag should be plumbed either to the renderer process or to the browser instrumentation I mentioned. If we have a DevTools requestId (now present in network::ResourceRequest) then we can match it to a certain request, and if we have headers that we want to show in DevTools, we can emit those from the browser process as well.

[Monorail components: Platform>DevTools>Network]

### yh...@chromium.org (2019-09-10)

Talked offline with ricea@.

We need to deal with both extensions and devtools. jarhar@, can you make changes to WebSocket support for devtools?
I think we can make changes for extensions.

The changes will be big so it is impossible to merge the fixes to M77. Merging to M78 is possible but I'm not comfortable with the idea.

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2019-09-10)

ricea: Uh oh! This issue still open and hasn't been updated in the last 167 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2019-09-10)

RE: https://crbug.com/chromium/944619#c29: jarhar@:

I am not sure why you mention a "CORB flag" in https://crbug.com/chromium/944619#c29 and "should_report_corb_blocking" in https://crbug.com/chromium/944619#c17.  I think the failure of a WebSocket handshake should be reported directly to the DevTools renderer process (and not disclosed to the web renderer process) *independent* from whether CORB is enabled / whether CORB blocked a particular response / whether CORB thinks that the blocking should be reported as a DevTools console message (i.e. should_report_corb_blocking).

RE: https://crbug.com/chromium/944619#c30: yhirano@:

Thank you for pointing out that there are two separate requirements here: 1) giving extensions access to the headers and 2) helping diagnose handshake failures via DevTools console messages and DevTools network instrumentation.  I assume that in #1 extensions only need *read* access (i.e. that read-write access is already covered by network::mojom::TrustedHeaderClient).

Let's first figure out how the right fix looks like and then consider whether it can be merged to any release branches.  I understand that the fix may end up too complicated/risky for a merge.

If I understand correctly, to avoid disclosing the headers to a web renderer, we need to avoid exposing network::mojom::WebSocketHandshakeClient::OnResponseReceived to web renderers, which in turn means that DevTools functionality that depends on WebSocketChannelImpl::OnResponseReceived and InspectorNetworkAgent::DidReceiveWebSocketHandshakeResponse needs to be refactored somehow.  Did I get this right?  I have no idea how refactoring would look like, but I do hope that jarhar@'s work in https://crbug.com/chromium/849483 can help with that.

I am not sure how the extensions can be supported going forward.  Is the idea here to have the browser process provide an additional interface when calling network::mojom::NetworkContext::CreateWebSocket?  To address the security bug, this additional interface would have to be separate from WebSocketHandshakeClient (which I assume is needed by the renderer for OnConnectionEstablished).  I don't understand whether this additional interface could be avoided by reusing TrustedHeaderClient (which is already a parameter of network::mojom::NetworkContext::CreateWebSocket) - maybe the extra performance penalty can be avoided by changing NetworkContext::CreateWebSocket to 1) make TrustedHeaderClient parameter mandatory / non-optional and 2) having a new parameter |bool allow_trusted_header_client_to_modify_headers| (defaulting to false - in this default case the performance can be avoided by not waiting for the response from the TrustedHeaderClient).

Am I making sense above?  :-)  This is an area of code that I am not very familiar with - I think it is quite likely that some things I wrote above are not quite right.  I hope that my ramblings above were somewhat helpful and that I did not just add noise and/or confuse matters any further...

### ja...@chromium.org (2019-09-10)

https://crbug.com/chromium/944619#c30
I'm happy to help but unfortunately I'm switching from the DevTools team to the DOM team in two weeks. caseq@ can help if I can't after I switch teams.

https://crbug.com/chromium/944619#c32
Yeah I suppose we don't have to report CORB blocking the same was as we are currently doing with URLLoader. Is the goal just to show in DevTools that the websocket failed? If so, we should be able to emit the right events to make that happen from content/browser/devtools/ securely if we have a DevTools request id present. I added it to network::ResourceRequest earlier this year, and we would have to add it to the websocket mojo interface separately to emit events for the right websocket since the interface is separate from URLLoader.

### yh...@chromium.org (2019-09-13)

Thanks, jarhar@. I'm tentatively assigning you as an OWNER because the devtools work is blocking to the other part. Feel free to unassign yourself when you need to work on other things.

caseq@, are you fine with the plan?

### ja...@chromium.org (2019-09-20)

My understanding of the goal here is to simply stop exposing raw headers to the renderer process via WebSocketHandshakeClient::OnResponseReceived and/or WebSocketHandshakeClient::OnOpeningHandshakeStarted. We can get the raw headers to DevTools securely the same way I did in URLLoader by adding plumbing into and out of network service. I just put together a mock patch that shows what interface changes would be necessary to make this happen as well for websockets: https://chromium-review.googlesource.com/c/chromium/src/+/1817148
Alternatively, we could just emit a DevTools console message saying that a WebSocket was blocked due to CORB which would only require one method in the NetworkServiceClient interface. Aaron did something just like this in this patch: https://chromium-review.googlesource.com/c/chromium/src/+/1600541

Assuming my understanding of the goal is correct, I think we can just stop sending raw headers to the renderer over WebSocketHandshakeClient's OnResponseReceived and OnOpeningHandshakeStarted in the CORB case today and file a bug to fix it in DevTools later, perhaps first by adding a simple console message and later by securely plumbing raw headers. We had a very similar issue in DevTools lately where we couldn't even get any raw headers for all cross origin HTTP requests: https://bugs.chromium.org/p/chromium/issues/detail?id=868407
This stayed broken in DevTools for multiple releases and was a much more significant use case than CORB on WebSockets in my opinion.

With this in mind, I don't think a fix for this security bug should be blocked by DevTools. I just talked to caseq about this bug, and we think that ownership of the DevTools aspect of this bug should be owned by the new DevTools owners. +yangguo

### lu...@chromium.org (2019-09-20)

RE: Alternatively, we could just emit a DevTools console message saying that a WebSocket was blocked due to CORB

AFAIU CORB is not in the picture at all (CORB applies only to regular http/https requests and doesn't apply to WebSocket handshakes and/or traffic - this is why leaking http response headers from a WebSockets handshake is a CORB bypass;  CORB requires knowing the MIME type of the content flowing over the network which is something that doesn't apply to WebSockets handshake failures).

That said, I guess WebSockets could stop sending (to the renderer) the response headers of a failed handshake in case of *all* cross-origin handshake failures.  If this broad suppression is acceptable (and I guess this is what "This stayed broken in DevTools for multiple releases [...]" argues) then this would indeed solve the security bug.  ricea@ / yhirano@ - WDYT? 

### ja...@chromium.org (2019-09-20)

Thanks for the explanation, +1 to stop sending response headers to the renderer process in the case of failure.

I just very briefly looked at the websocket code and it looks like the error message about the status code in the reporter's video is sent to the renderer process when network service breaks the mojo interface. I wonder if we will even lose this message? I think it's probably the most helpful part to debug websocket failures.

### sh...@chromium.org (2019-09-24)

ricea: Uh oh! This issue still open and hasn't been updated in the last 181 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2019-09-25)

OK, for devtools, we'll stop sending the information when the opening handshake fails.

For extensions (Web Request API), I have a question - Is it OK to omit onHeadersReceived[1] for failed WebSocket opening handshake? It seems good to me because it aligns with what CORB (and CORS after OOR-CORS ships) does. rdevlin.cronin@chromium.org (or karandeepb@chromium.org), are you fine with that? Do we need any announcement? I'm assigning this to you for the question.

1: https://developer.chrome.com/extensions/webRequest#event-onHeadersReceived

### yh...@chromium.org (2019-09-27)

ping

### yh...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### ka...@chromium.org (2019-09-30)

Talked with yhirano@ offline. Omitting onHeadersReceived for failed websocket handshakes sounds good. So the flow should be  onBeforeRequest, onBeforeSendHeaders, onSendHeaders, onErrorOccurred. This should be ok since we document that onErrorOccurred can be dispatched at any point of time during the request anyway. 'extraHeaders' can still be used to bypass this behavior. 

### yh...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/06a7f290e23932b6c9835361aac9fbbf565813f0

commit 06a7f290e23932b6c9835361aac9fbbf565813f0
Author: Yoichi Osato <yoichio@chromium.org>
Date: Sat Oct 12 01:41:14 2019

[WebSocket] Do not send response headers for failed handshake.

This patch changes network service to restrict sending the headers to
the renderer not to leak info if handshake was failed.

This also changes WebRequest API and devtools event listening as failed
when handshake was failed.

Change-Id: I03160b06546711365273180a8020239e09528a47
Bug: 944619
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1847592
Commit-Queue: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/master@{#705363}

[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/chrome/test/data/extensions/api_test/webrequest/test_websocket_auth.js
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/extensions/browser/api/web_request/web_request_proxying_websocket.cc
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/extensions/browser/api/web_request/web_request_proxying_websocket.h
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/services/network/public/mojom/websocket.mojom
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/services/network/websocket.cc
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/renderer/modules/websockets/websocket_channel_impl.h
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/renderer/modules/websockets/websocket_channel_impl_test.cc
[modify] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/web_tests/FlagExpectations/disable-site-isolation-trials
[delete] https://crrev.com/6b068eb8ca4a3c7350bdafa22fc0cf0636ef8b74/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-headers-for-websocket-expected.txt
[delete] https://crrev.com/6b068eb8ca4a3c7350bdafa22fc0cf0636ef8b74/third_party/blink/web_tests/http/tests/inspector-protocol/network/raw-headers-for-websocket.js
[add] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/web_tests/http/tests/inspector-protocol/websocket/handshake-response-expected.txt
[add] https://crrev.com/06a7f290e23932b6c9835361aac9fbbf565813f0/third_party/blink/web_tests/http/tests/inspector-protocol/websocket/handshake-response.js


### lu...@chromium.org (2019-10-14)

Going forward, Site Isolation bypasses leading to cross-site data disclosure should be treated as high severity - please see r698638.

We have also recently updated Chrome VRP Site Isolation special rewards [1] to explicitly cover cross-site data disclosure.

[1] https://www.google.com/about/appsecurity/chrome-rewards/index.html#special

### yo...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-17)

lukasza@ per https://crbug.com/chromium/944619#c32 do you think we should merge this to M78? Changes are obviously non-trivial, but we do like to merge high severity fixes to the current stable branch. Also, bear in mind, people will start to see if this is exploitable as of 5 days ago when the fix was posted in git. I'm insufficiently familiar with how rapidly people can weaponize exploits that defeat site isolation, nor how general an information leak this could give, so I'll rely on your judgement about whether this is realistically going to get exploited in the next six weeks.

Unless you or yoichio@ are concerned about the stability of the fix, I would err on the side of merging to M78?

If either/both of you agree please add Merge-Request-78. I suspect it's too late for the initial release, but it should land in one of the M78 security refreshes.

### lu...@chromium.org (2019-10-17)

adetaylor@, I'll defer to creis@ for the merge decision/feedback

### yo...@chromium.org (2019-10-18)

Since the patch is not trivial and API changing and no guarantee of zero-regression, it is not good to merge to M78 unless strong security demand.

### cr...@chromium.org (2019-10-18)

Given https://crbug.com/chromium/944619#c50 about the risk, I think we should probably avoid the merge.  I agree it would have been nice to include in M78, but I'm not confident enough to vouch for it this late in the M78 stable schedule.

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $2,000 for this report :) 

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-01)

Not requesting merge to beta (M79) because latest trunk commit (705363) appears to be prior to beta branch point (706915). If this is incorrect, please replace the Merge-na label with Merge-Request-79. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-11-21)

Congrats! The Panel re-visited this report and decided to reward an additional $8,000. 

### ma...@piosek.pl (2019-11-23)

Cool, thanks!

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/944619?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Network>WebSockets, Internals>Sandbox>SiteIsolation, Platform>DevTools>Network, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094352)*
