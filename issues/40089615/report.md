# Security: Chrome does not percent-escape the URL passed to external handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40089615](https://issues.chromium.org/issues/40089615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>PlatformIntegration |
| **Platforms** | Linux, Mac, Windows |
| **CVE IDs** | CVE-2017-12939 |
| **Reporter** | ri...@fshnstudent.info |
| **Assignee** | mg...@chromium.org |
| **Created** | 2017-11-16 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

URL handlers are not handled correctly.The special character " is not encoded or removed which makes it possible to inject special command line arguments in different programs.

VERSION
Chrome Version: Google Chrome 62.0.3202.94 
Operating System: Windows 7 SP1

REPRODUCTION CASE
To explain this vulnerability better I'm going to explain it using an example.

We have an application in this case Unity3D, which registers the com.unity3d.kharma as an URL protocol.

In the registry , the command responsible for handling this URL is as following.

"C:\Program Files\Unity\Editor\Unity.exe" -openurl "%1"

The %1 is the part is the URL that is passed. 

For example the following link 
<a href='com.unity3d.kharma:http://example.com'> Test </a>

Will call:

"C:\Program Files\Unity\Editor\Unity.exe" -openurl "com.unity3d.kharma:http://example.com"

The problem is that Google Chrome does not encode or remove the " character which makes it possible to insert additional commands.

Example POC:

<a href='com.unity3d.kharma:http://example.com" --other-commandline "'> Test </a>

Inspecting the started process with Process Explorer (As in image Google Chrome URL Handler Behavior) we see that the command line arguments are successfully injected.

This bug makes it possible to exploit URL handlers that are correctly implemented.

The expected behavior (for example Firefox) , the special character " gets URL encoded which makes it impossible to inject other command line arguments.
You can see that in Firefox URL Handler Behavior image.

Thanks,

Rio



## Attachments

- [Google Chrome URL Handler Behaviour.png](attachments/Google Chrome URL Handler Behaviour.png) (image/png, 55.1 KB)
- [Firefox URL Handler Behaviour.png](attachments/Firefox URL Handler Behaviour.png) (image/png, 15.5 KB)
- [POC.png](attachments/POC.png) (image/png, 7.0 KB)
- [correct behaviour.png](attachments/correct behaviour.png) (image/png, 7.2 KB)
- [Picture1.png](attachments/Picture1.png) (image/png, 29.2 KB)

## Timeline

### el...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

[Monorail components: Internals>PlatformIntegration]

### el...@chromium.org (2017-11-16)

Thanks for the report; this was previously logged in the issue I've duplicated it to.

If you're aware of any protocol handlers that are actually exploitable in this way (something dangerous happens with the extra arguments) this would be very helpful data in arguing that we should incur the compatibility hit of making a change here.

### ri...@fshnstudent.info (2017-11-16)

Yes I have reported a vulnerability in Unity3D CVE-2017-12939 which was exploitable only through Gooogle Chrome. 
I will release the exploit details tomorrow.


### do...@chromium.org (2017-11-16)

+mgiuca for visibility.

### mg...@chromium.org (2017-11-17)

*** REWARD PANEL: READ THE FOLLOWING PARAGRAPH ***

As per https://crbug.com/713935#c23, de-duplicating since I think this is a separate issue to what's primarily being discussed in that bug. Note https://crbug.com/713935#c5 does mention the escaping issue, though it was very unclear what the problem was, whereas this report is quite clear -- something for the panel to keep in mind when assessing this.

The root cause here is that when launching an external protocol handler, Chrome does not percent-escape the URL. This affects all platforms, but in different ways.

On Windows it is the most bad, since Windows has no concept of separate command-line arguments; the command line is one long string. Therefore, the unescaped URL can be used to escape out of the quoted "%1" argument and supply an arbitrary number of additional arguments to the program, as we see here.

On Linux and Mac, it should be less of a problem, since no matter what you put in the string, it counts as a single argument. However, on Linux, as shown in https://crbug.com/713935#c5, you can still do some weird stuff like use "*" to pass a list of filenames in the current directory into the handler application (though there is no clear security problem with this).

I was curious about the history of this since this article elawrence@ linked in the other bug (https://blogs.msdn.microsoft.com/ieinternals/2011/07/13/understanding-protocols/) from 2011-07 explicitly shows a screenshot of Chrome behaving correctly. It turns out this regressed in 2011-09 in r102449 and has been broken for six years. That CL accidentally changed "escaped_url" to "url" during a refactor (we actually do escape the URL, but since that CL, we pass the unescaped URL through to the external handler). The fix is straightforward but I want to make sure tests cover it.

### mg...@chromium.org (2017-11-17)

rio.sherri: "Yes I have reported a vulnerability in Unity3D CVE-2017-12939 which was exploitable only through Gooogle Chrome. I will release the exploit details tomorrow."

Per https://www.google.com/about/appsecurity/chrome-rewards/, please note that if you make the details of this exploit public (in particular, the Chrome part), you will be ineligible for a bug bounty. Similar disclosure rules may apply from Unity. If Unity is okay with it, you may discuss the details of the Unity exploit from the command line, without mentioning launching from the web via Chrome. You should not mention this Chrome issue, as it has not been made public. Eventually, this issue will become public, once a fix is rolled out.

Thanks

Matt

### mg...@chromium.org (2017-11-17)

It turns out this is quite hard to test (and that may speak to URL encoding issues elsewhere in the system). While defense in depth is good, in theory we shouldn't need to "escape" the URL in ExternalProtocolHandler, because an unescaped URL *is not a valid URL* and we should not be receiving them.

It's quite hard to write a test case to check against this, since GURL's string constructor doesn't let you create an unescaped URL. The implication is that a GURL with unescaped characters like ' ' and '"' should not be allowed to exist, and thus there is a bug at some deeper part of the system (whatever is creating a GURL object for the purpose of navigation).

### ri...@fshnstudent.info (2017-11-17)

Hi Matt,
Its not a problem, I can wait regarding making the unity vulnerability public. If you want the details of the exploit and how it worked I can share here since I have Unity permission.

### el...@chromium.org (2017-11-17)

RE #5: This isn't reward-eligible anyway; the limitation in our escaping was already public: https://bugs.chromium.org/p/chromium/issues/detail?id=711020#c15. In https://bugs.chromium.org/p/chromium/issues/detail?id=713935#c3, I noted that the ultimate problem here is that there are no widely-observed standards for non-standard protocols and thus anything we change would have a compatibility impact. In https://blogs.msdn.microsoft.com/ieinternals/2011/07/13/understanding-protocols/, I explained the decisions made by the IE team about handling of application protocol URLs.

RE #7: While space is a character that should be converted to %20, double-quotes (") are not a reserved character in URLs and this character is not encoded (e.g. in a HTTP URL) by any browser. 


### mm...@chromium.org (2017-11-17)

[Empty comment from Monorail migration]

### ri...@fshnstudent.info (2017-11-17)

I think there is a misunderstanding.
By following the MSDN suggestion on protocol handlers the value passed to CreateProcess or similar functions should not contain any " because it will break the command line arguments.
Also Im not talking about the URL in general but the data passed to the program which handles the URL protocol.

So lets imagine a program has two parameters.
One is -tel and the other -execute.

The URL protocol value would be:
program.exe -tel "datapassed through chrome"

What Chrome does is calls the program with the parameter but allows the " character which can break the command line parameters.

So passing the value 123" -execute command "
The call would become

program.exe -tel "123" -execute command ""

In firefox the call would become

program.exe -tel "123%22%20-execute%20command%20%22"

Which will not break the command line arguments.

If I have not explained well let me know and I can demonstrate you with a real world example.

### mm...@chromium.org (2017-11-17)

I don't understand the reasoning not to encode " symbol.

Lack of "no widely-observed standards for non-standard protocols" doesn't sound like a reason to allow web-sites inject arbitrary arguments to be passed to custom protocol handlers.

A chance of compatibility impact also doesn't seem to be a very strong argument. Protocol handlers can have a one arbitrary argument passed from the web. If there are handlers that rely on the fact that they can pass multiple arguments when using a particular browser, it sounds like they are relying on an Undefined Behavior, and that's only their fault.

I feel like I'm missing something important, am I?

### mm...@chromium.org (2017-11-17)

Right, IMHO c#11 is a short and clear explanation why it's really bad issue and should be fixed ASAP.

### el...@chromium.org (2017-11-17)

Is the current proposal here to %-escape SPACE to %20 and DQUOTE to %22? Or is something broader proposed?

As outlined in the resources referenced earlier, Application Protocols are inherently powerful (one click escape of the Chrome sandbox) and historically dangerous (a popular vector for exploits in the late 90s and early 00s). Their security relies upon the implementer doing the right thing and following best practices guidance that is not easily found.

> A chance of compatibility impact also doesn't seem to be a very strong argument.

It's a fair point of view-- As a security team member, I like it. Other browser security teams have made different tradeoffs. Microsoft (who owns the ShellExecute implementation on Windows) has two browsers, Edge and Internet Explorer. Both permit unescaped quotes and spaces to pass through the invocation codepath into the command line arguments of the target application. (See the "Alert with Quotes" link at https://www.bayden.com/test/protocol/.) Probably more surprisingly, you'll find that not only does IE/Edge not escape quotes, but they actually *decode* %22 sequences into quotation marks before passing to the application. Why? Because that's how Application Protocols have worked since the 1990s, and our attempts to change things in the IE8-IE11 timeframe failed due to compatibility problems. 

> Protocol handlers can have a one arbitrary argument passed from the web.
> If there are handlers that rely on the fact that they can pass multiple arguments 
> when using a particular browser, it sounds like they are relying on an Undefined 
> Behavior, and that's only their fault.

The misunderstanding here is the conflation of "A URL containing quotation marks, which is entirely legal" with "Multiple arguments." A properly-behaving Application Protocol handler accepts a single string URL from the web and does not consider embedded quotes to be delimiters between multiple arguments. (Some Windows execution modalities don't even have the old C-style argc/argv paradigm for parsing input.) In contrast to quotes, unescaped spaces in URIs *are* illegal and certainly *should be* escaped.


### ri...@fshnstudent.info (2017-11-17)

Hi, 
Since you mentioned the alert sample protocol.
I don't think is a good idea to allow injection of other command line parameters (even if it has been since 90s)

<a href='alert:123123123" --other-command'> POC </a>

If you check the image attached there is an additional parameter and is not treated as one.
And in the second image the expected behavior.

Also I'm reporting the security issue even on IE/Edge.


### el...@chromium.org (2017-11-17)

Re #15: To be clear, the tool and test page in question were built almost a decade ago when I was the security PM for Internet Explorer, and your "POC.png" demonstrates the behavior that we had resigned ourselves to.

I'd be very interested to hear whether Microsoft has changed their opinion about how this interface should behave.

### ri...@fshnstudent.info (2017-11-17)

RE #16: Will let you know as soon as they respond.

### mm...@chromium.org (2017-11-17)

Eric, thanks for the answer above!

### sh...@chromium.org (2017-11-18)

[Empty comment from Monorail migration]

### ri...@fshnstudent.info (2017-11-18)

Re #15: I kindly disagree and correct me if I'm wrong.
I don't think that is intended behavior. So basically there are 2 types of URL handlers.

For example in windows 10 there is a URL Handler protocol called: 
ms-quick-assist and the corresponding command : 

"%SystemRoot%\system32\quickassist.exe" %1

This does not have the quotes and you can pass multiple parameters, which is an intended behavior.

The other type that I'm discussing is URL Handlers which are defined with quotes and normally would allow only one parameter. As the example Alert protocol which has the following command line:

"C:\windows\alert.exe" "%1"

When the arguments are passed if they are inside "" they are treated as one but when they are passed without the "" , they are treated as different arguments as shown in Picture1.png

If a program wants more the one command line argument that's ok and they should not use the quotes. But the problem is when the programs defined with the quotes and expect one argument can receive multiple ones.

Hope I have explained it well.

Thanks




### el...@chromium.org (2017-11-18)

Windows has exactly one "type" of Application Protocol handler. The lack of quotes for QuickAssist is merely a (not uncommon) oversight. 

### mg...@chromium.org (2017-11-20)

Wow... a lot of discussion over the weekend.

TL;DR: Spaces and quotes are illegal in a valid URL. Let's just escape spaces, quotes, and other illegal characters so we guarantee only a single command-line argument is passed to the handler, which matches Firefox and reverts back to Chrome's behaviour of 2011 before this was inadvertently broken.

I'm a bit confused why there's so much debate over the resolution. This has a very clear fix since we already encode the URL, and previously we were using the encoded URL, but we regressed so as to not use it. I have a working patch, just need to write a regression test.

The resolution *does* encode the quote character. A sample test page is:

    <a href="foo:url part&quot; --extra &quot;file">bad external url</a>

The current behaviour is to run a command with arguments:

    "foo:url part" --extra "file"

The fix runs the command with arguments:

    "foo:url%20part%22%20--extra%20%22file"

This is in line with the URL standard. U+0022 (") is not a valid URL character (https://url.spec.whatwg.org/#url-code-points) so it is always safe to encode it as %22.

Addressing the comments above:

#8: Thanks. There's no need to share the details of the Unity exploit. From our perspective, we want to stop arbitrary command-line passing to external handlers, so we don't need the specifics of the Unity bug.

#9

> RE #5: This isn't reward-eligible anyway; the limitation in our escaping was already public:
> https://bugs.chromium.org/p/chromium/issues/detail?id=711020#c15.

Let's let the panel decide on the reward situation eventually (rather than disclosing this to public). That bug was marked Fixed in April yet there is still an unescaped URL being passed to an external handler.

> I noted that the ultimate problem here is that there are no widely-observed standards for
> non-standard protocols and thus anything we change would have a compatibility impact.

This has nothing to do with protocols. It's about removing illegal characters from URLs before embedding them in strings which expect valid URLs. As shown in that post, Chrome used to do this correctly (before 2011) and Firefox does it correctly. This change would be bringing Chrome in line with standards. I'll address IE below.

> While space is a character that should be converted to %20, double-quotes (") are not a
> reserved character in URLs and this character is not encoded (e.g. in a HTTP URL) by any browser. 

You're using RFC 3986 (https://www.ietf.org/rfc/rfc3986.txt) terminology. In RFC 3986, "reserved" characters are valid characters that have special meaning in URL syntax, so *must not* be percent-encoded or the meaning of the URL changes. U+0022 is neither reserved, nor unreserved; it is simply illegal, so if it appears in a URL, it is safe to encode it (which turns an invalid URL into a valid one).

(Note: I've been told by standards team to use URL Standard as the source of truth on URL matters -- https://url.spec.whatwg.org. This makes matters *much* harder because they don't supply a grammar, but I think you can come to the same conclusion about U+0022.)

#11: This is correct.

#14:

> Is the current proposal here to %-escape SPACE to %20 and DQUOTE to %22? Or is something broader proposed?

The proposal is specifically to change "url" to "escaped_url" on line 246 of external_protocol_handler.cc.

https://cs.chromium.org/chromium/src/chrome/browser/external_protocol/external_protocol_handler.cc?l=246

I'm not implementing a new escape mechanism; we already escape the URL, we just forgot to use the escaped one.

This means we're encoding the URL using net::EscapeExternalHandlerValue, which according to the documentation, escapes "everything except alphanumerics and -_.!~*'() and the restricted chracters [sic] (;/?:@&=+$,#[]) and a valid percent escape sequence (%XX)." In other words, this will escape the following characters:

- ASCII control codes
- Non-ASCII characters
- space
- ", <, >, \, ^, `, {, |, }

Seems correct to me.

> [Edge and Internet Explorer] permit unescaped quotes and spaces to pass through the invocation
> codepath into the command line arguments of the target application.

That seems like broken behaviour to me. Quote is simply an illegal character in URLs, which means any application that wants to take a string with a quote in it should accept %22 as a quote character.

> The misunderstanding here is the conflation of "A URL containing quotation marks, which is entirely legal"
> with "Multiple arguments." A properly-behaving Application Protocol handler accepts a single string URL from
> the web and does not consider embedded quotes to be delimiters between multiple arguments.

Quotation marks are illegal in URLs. It's true that this is exacerbated by Windows' command-line modal, which
essentially embeds command lines within a delimiter-based syntax (unlike Unix, where the model is an array of
strings). If quotes were legal in URLs, we might want to resort to command-line escaping the quotes (e.g.,
escaping " as ""). But IIRC this is not reliable since different runtimes parse quotes differently. So we are
fortunate that quote is illegal in URLs so we can just escape them as %22.

#20 and #21 are irrelevant, since regardless of whether the handler is set up with quotes around the %1, we
should still only pass a single command-line argument.

### mg...@chromium.org (2017-11-21)

CL is up (private): https://chromium-review.googlesource.com/c/chromium/src/+/778747/

### bu...@chromium.org (2017-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2401e58572884b3561e4348d64f11ac74667ef02

commit 2401e58572884b3561e4348d64f11ac74667ef02
Author: Matt Giuca <mgiuca@chromium.org>
Date: Thu Nov 23 04:31:49 2017

Launching an external protocol handler now escapes the URL.

Fixes bug introduced in r102449.

Bug: 785809
Change-Id: I9e6dd1031dd7e7b8d378b138ab151daefdc0c6dc
Reviewed-on: https://chromium-review.googlesource.com/778747
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: Ben Wells <benwells@chromium.org>
Cr-Commit-Position: refs/heads/master@{#518848}
[modify] https://crrev.com/2401e58572884b3561e4348d64f11ac74667ef02/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/2401e58572884b3561e4348d64f11ac74667ef02/chrome/browser/external_protocol/external_protocol_handler_unittest.cc


### mg...@chromium.org (2017-11-23)

Fixed.

Summary for panel (see also https://crbug.com/chromium/785809#c5):

- This issue was similar to one already fixed in https://crbug.com/chromium/711020. But that had already been marked fixed when this was reported, so it is a different issue.
- This issue was vaguely made known to us in https://crbug.com/713935#c5. However, the ramifications weren't made clear (since that report only talks about a minor exploit using the Gopher protocol on Linux), and it was buried inside a very long report of a different issue.
- By contrast, this report quite clearly identified the issue and the consequences with command-line syntax escape on Windows.

In my opinion, we wouldn't have realised the specific issue without this report.

On the other hand, dropping the severity to Medium, due to: "which are not harmful on their own but potentially harmful when combined with other bugs". The exploit that was fixed here only allows an attacker to take advantage of security bugs in other software the user has installed. Theoretically, this is always possible, by design, with the external handler feature (if installed software has a bug parsing its URL argument). By escaping the quoted URL command-line argument, it slightly increases the attack surface (as shown here with Unity), because it allows an attacker to provide arbitrary command line arguments to native software. But I don't consider this "high" severity.

### mg...@chromium.org (2017-11-23)

Also, I think we should *not* merge this to 63, given a) how close it is to stable release, b) how long this issue has been in stable, 6 years, and c) the potential compatibility risk of breaking software that is expecting unescaped characters in command-line arguments. So not requesting a merge.

### bu...@chromium.org (2017-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51d62ca4ad777a73d35b91b27f39acbb5d8a4053

commit 51d62ca4ad777a73d35b91b27f39acbb5d8a4053
Author: Matt Giuca <mgiuca@chromium.org>
Date: Thu Nov 23 07:01:22 2017

Revert "Launching an external protocol handler now escapes the URL."

This reverts commit 2401e58572884b3561e4348d64f11ac74667ef02.

Reason for revert: Broke unit_tests on builders.
https://ci.chromium.org/buildbot/chromium.linux/Linux%20Tests%20%28dbg%29%281%29%2832%29/46140

Original change's description:
> Launching an external protocol handler now escapes the URL.
> 
> Fixes bug introduced in r102449.
> 
> Bug: 785809
> Change-Id: I9e6dd1031dd7e7b8d378b138ab151daefdc0c6dc
> Reviewed-on: https://chromium-review.googlesource.com/778747
> Commit-Queue: Matt Giuca <mgiuca@chromium.org>
> Reviewed-by: Eric Lawrence <elawrence@chromium.org>
> Reviewed-by: Ben Wells <benwells@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#518848}

TBR=benwells@chromium.org,mgiuca@chromium.org,elawrence@chromium.org

Change-Id: I74fa862034e6fba34ddb0b2ef848c700d5287c83
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 785809
Reviewed-on: https://chromium-review.googlesource.com/787031
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Cr-Commit-Position: refs/heads/master@{#518868}
[modify] https://crrev.com/51d62ca4ad777a73d35b91b27f39acbb5d8a4053/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/51d62ca4ad777a73d35b91b27f39acbb5d8a4053/chrome/browser/external_protocol/external_protocol_handler_unittest.cc


### mg...@chromium.org (2017-11-23)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-11-23)

Had to revert because tests failed (on the builders only, but not try bots... what). Will have to investigate tomorrow.

### el...@chromium.org (2017-11-23)

Re #25: I’m not sure who the “known to us” and “we wouldn’t have realized” refers to, but I explicitly identified the lack of escaping in the affected function when making the fix to https://crbug.com/chromium/711020, and noted the same in https://bugs.chromium.org/p/chromium/issues/detail?id=711020#c15. 

https://crbug.com/chromium/713935 isn’t a different issue at all— it’s exactly the same issue. What we lacked with 713935 is a specific example of a popular protocol handler that contained a security vulnerability. Given that the change necessary to address this would be compatibility-impacting, and our behavior matches the longstanding behavior of popular browsers, it was difficult to make the case that we should harm compatibility without a real-world example of a still vulnerable client.

### mg...@chromium.org (2017-11-23)

#30:

Re https://crbug.com/chromium/711020: I haven't been following that issue and I am not familiar with its details. Regardless of whether the lack of escaping was identified in that issue, it was already dealt with in a way that seems to have been specific to the mailto protocol, and closed as Fixed, in April. Were it not for this bug report, we wouldn't have taken further action which was required to address the general problem in ExternalProtocolHandler.

Re https://crbug.com/chromium/713935: "What we lacked with 713935 is a specific example of a popular protocol handler that contained a security vulnerability." I don't see it that way: At least for me personally, the context I was missing was that U+0022 (quote character) was not escaped, allowing for the website to break out of the quoted "%1" and pass an arbitrary number of command line arguments on Windows. That wasn't mentioned in the bug report in https://crbug.com/chromium/713935. I see now that you mentioned it in https://crbug.com/713935#c17 but only in passing.

I think this reporter deserves credit for a) explicitly spelling out the issue with quote escaping on Windows, and b) providing an example of a full-stack exploit with Unity.

### bu...@chromium.org (2017-11-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/36fd3c9a6ba9fce9dd80c442c3ba5decd8e4c065

commit 36fd3c9a6ba9fce9dd80c442c3ba5decd8e4c065
Author: Matt Giuca <mgiuca@chromium.org>
Date: Mon Nov 27 01:12:35 2017

Reland "Launching an external protocol handler now escapes the URL."

This is a reland of 2401e58572884b3561e4348d64f11ac74667ef02
Original change's description:
> Launching an external protocol handler now escapes the URL.
> 
> Fixes bug introduced in r102449.
> 
> Bug: 785809
> Change-Id: I9e6dd1031dd7e7b8d378b138ab151daefdc0c6dc
> Reviewed-on: https://chromium-review.googlesource.com/778747
> Commit-Queue: Matt Giuca <mgiuca@chromium.org>
> Reviewed-by: Eric Lawrence <elawrence@chromium.org>
> Reviewed-by: Ben Wells <benwells@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#518848}

Bug: 785809
Change-Id: Ib8954584004ff5681654398db76d48cdf4437df7
Reviewed-on: https://chromium-review.googlesource.com/788551
Reviewed-by: Ben Wells <benwells@chromium.org>
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Cr-Commit-Position: refs/heads/master@{#519203}
[modify] https://crrev.com/36fd3c9a6ba9fce9dd80c442c3ba5decd8e4c065/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/36fd3c9a6ba9fce9dd80c442c3ba5decd8e4c065/chrome/browser/external_protocol/external_protocol_handler_unittest.cc


### mg...@chromium.org (2017-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-08)

HI rio.sherri@ thanks for the report - the VRP panel decided to award $500 - a member of our finance team will be in touch to arrange payment. Also, how would you like to be credited if this is mentioned in release notes?

### aw...@chromium.org (2017-12-08)

[Empty comment from Monorail migration]

### ri...@fshnstudent.info (2017-12-08)

Thank you very much for the bounty. Please credit me as 0x09AL.

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mg...@chromium.org (2017-12-17)

I'm not sure why sheriffbot added Merge-Request-64. I think it just looked at the label.

This is already in the 64 branch (git log branch-heads/3282 shows commit 36fd3c9a6b), unless I'm mistaken. Removing the label.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@sdbn-solutions.de (2018-03-06)

[Comment Deleted]

### mg...@chromium.org (2018-03-07)

Not sure why #47 was deleted, but for posterity I'll respond to it because it's a reasonable question:

> We're using a software which has an protocol handler to pass a filepath (and config infos) to a
> software. This filepath maybe a network path like "\\servername\file.txt". This change now causes
> that the filepath get encoded to "%5C%5Cservername%5Cfile.txt" and the handler application isn't
> able to decode this. Is there a possibility to disable this url encoding?"

No, there isn't (for security). But aside from security, this question suggests the wrong semantics (and I'm confused about how this would even work).

The command-line argument passed to an external protocol handler is *always* a URL, not some other path or arbitrary string. External protocol handlers register a particular scheme, such as "foo", and then they launch when the user clicks a link that begins with "foo:", passing the full URL, including the scheme. So it has never been possible to pass a bare network path like "\\servername\file.txt" to your external handler. It would always have been prefixed by the scheme and a colon (':').

Since the thing we are passing to the handler is a URL, it makes sense that we escape characters that are illegal in a URL; in other words, we normalize the URL passed to the external handler by parsing and serializing it according to the URL standard [1]. If the external application does not recognise the string as a URL (e.g., it expects a Windows network path), then it isn't a correct external handler application, and needs to be modified or wrapped in script that processes the URL and converts it into an input appropriate for the program in question.

[1] https://url.spec.whatwg.org

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### al...@gmail.com (2022-10-20)

This bug requires manual review: Reverts referenced https://stemhave.com/programming-help.html in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

### pa...@gmail.com (2023-06-28)

I'm at the same point as described in https://crbug.com/chromium/785809#c48

We're using a software which has an protocol handler to pass a filepath (and config infos) to a
software. This filepath maybe a network path like "\\servername\file.txt". This change now causes
that the filepath get encoded to "%5C%5Cservername%5Cfile.txt" and the handler application isn't
able to decode this. Is there a possibility to disable this url encoding?"

I'm getting áéíóú unicode encoded breaking file paths.
I'm not sure if it is browser work to enforce specs and normalize URL

This bug is Unity.exe only, and not browser fault 



### is...@google.com (2023-06-28)

This issue was migrated from crbug.com/chromium/785809?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/788086]
[Monorail mergedinto: crbug.com/chromium/713935]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089615)*
