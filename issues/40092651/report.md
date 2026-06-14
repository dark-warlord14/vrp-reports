# DocumentLoader use after free in KURL::strippedForUseAsReferrer

| Field | Value |
|-------|-------|
| **Issue ID** | [40092651](https://issues.chromium.org/issues/40092651) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-07-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

as per discussion with inferno.

one day I was able to reproduce the 456 inside 3176 bug in a browser with valgrind, but otherwise these are reproducing in DumpRenderTree compiled with asan.

stack is either:

Reply: ==7030== ERROR: AddressSanitizer crashed on address 0x00007fffc30b92c8 at pc 0x1806482 bp 0x7fffffffa0b0 sp 0x7fffffff9f20  

READ of size 1 at 0x00007fffc30b92c8 thread T0  

0x00007fffc30b92c8 is located 456 bytes inside of 3176-byte region [0x00007fffc30b9100,0x00007fffc30b9d68)  

freed by thread T0 here:  

previously allocated by thread T0 here:  

Stats: 0M freed by 0 calls  

Stats: 0M really freed by 0 calls  

WebCore::KURL::strippedForUseAsReferrer() [0x1806482]  

WebCore::FrameLoader::setOutgoingReferrer() [0x21b9177]  

WebCore::DocumentWriter::begin() [0x21a153b]  

WebCore::DocumentWriter::replaceDocument() [0x21a09e5]  

WebCore::ScriptController::executeIfJavaScriptURL() [0x1aac187]  

WebCore::SubframeLoader::requestFrame() [0x221ea8a]

or

Reply: ==20114== ERROR: AddressSanitizer crashed on address 0x00007fffc359a308 at pc 0xd5607d bp 0x7fffffff90f0 sp 0x7fffffff90b0  

READ of size 8 at 0x00007fffc359a308 thread T0  

0x00007fffc359a308 is located 8 bytes inside of 16-byte region [0x00007fffc359a300,0x00007fffc359a310)  

freed by thread T4 here:  

previously allocated by thread T4 here:  

Thread T4 created by T0 here:  

Stats: 0M freed by 0 calls  

Stats: 0M really freed by 0 calls  

WebCore::KURLGooglePrivate::init<>() [0x180bfdb]  

WebCore::KURL::KURL() [0x180b7ca]  

WebCore::blankURL() [0x18067a7]  

WebCore::Document::completeURL() [0x1d5b190]  

WebCore::HTMLLinkElement::parseMappedAttribute() [0x161d4ec]  

WebCore::StyledElement::attributeChanged() [0x1e78858]  

WebCore::Element::setAttributeMap() [0x1da449f]

with varying offset and size.

**VERSION**  

Chrome Version: DumpRenderTree on trunk compiled with asan  

Operating System: linux 64 bit

**REPRODUCTION CASE**

attached a bunch of files and DumpRenderTree logs.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: drt

## Attachments

- [kurl.zip](attachments/kurl.zip) (application/zip; charset=binary, 309.5 KB)
- [118.html](attachments/118.html) (text/html; charset=iso-8859-1, 13.5 KB)
- [vg-google-chrome-unstable-89330.txt](attachments/vg-google-chrome-unstable-89330.txt) (text/plain; charset=us-ascii, 36.9 KB)
- [js-test-post.js](attachments/js-test-post.js) (text/plain; charset=us-ascii, 233 B)
- [yesh.html](attachments/yesh.html) (text/html; charset=us-ascii, 47.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 6.3 KB)
- [back.html](attachments/back.html) (text/html; charset=us-ascii, 726 B)
- [asan-symbols.txt](attachments/asan-symbols.txt) (text/plain; charset=us-ascii, 18.9 KB)
- [documentloader.html](attachments/documentloader.html) (text/html; charset=us-ascii, 726 B)
- [456.html](attachments/456.html) (text/plain; charset=us-ascii, 81.8 KB)
- [asan456.txt](attachments/asan456.txt) (text/x-c; charset=us-ascii, 10.5 KB)

## Timeline

### in...@chromium.org (2011-07-14)

This should be definitely fixed in browser, dont care about DumpRenderTree.

I just cced you. http://code.google.com/p/chromium/issues/detail?id=84946. I found this as well. 

Do a fresh checkout (gclient revert, rm -rf ./out) and please verify which ones are left. 


### in...@chromium.org (2011-07-14)

Looks like the fix from Oliver is not enough, miaubiz can still repro it.

### mi...@gmail.com (2011-07-14)

here's a repro vg log coming up in just a minute

### mi...@gmail.com (2011-07-14)


Google Chrome	14.0.814.0 (Official Build 91661) dev
OS	Linux
WebKit	535.1 (trunk@90501)



### ab...@chromium.org (2011-07-14)

japhet is this the same HTMLLinkElement bug, or is this one different?

### ja...@chromium.org (2011-07-14)

abarth, if you mean http://code.google.com/p/chromium/issues/detail?id=87593, I'd say the odds are pretty small that they're the same root issue, but I've been wrong lots of times before.

### mi...@gmail.com (2011-07-16)

sorry for not checking back. same situation after rm -rf out and gclient revert, browser doesn't crash with current revisions, but DumpRenderTree is showing the same crashes.

### in...@chromium.org (2011-07-16)

Miaubiz, if you make reduced testcases for the 2 crash stacks that crash DumpRenderTree and are valid bugs, that will qualify for a higher reward. DumpRenderTree testcases can be test framework specific, but many times, we have layouttestcontroller specific commands that DumpRenderTree understands but the browser needs manual interaction for that. So, DumpRenderTree might infact be pointing to a real problem that the dev didnt fix properly or is a different problem altogether.

### in...@chromium.org (2011-07-16)

For reduced testcases, you can run ASAN on DumpRenderTree for best reduction.

### mi...@gmail.com (2011-07-17)

got it reproing in the browser now with the attached file and the attached js-test-post.js in js/resources relative to the html file.

### in...@chromium.org (2011-07-17)

Nice Miaubiz. Thanks for confirming this reproduces in browser with ASAN.

2 small things
1) ASAN no longer symbolizes by default. Which makes harder to understand your stacks.  Here is a way to give proper ones. Add this ./out/Release/chrome test.html 2>&1 | third_party/asan/scripts/asan_symbolize.py | c++filt
2) I think you have two bugs here in DocumentLoader. From your initial description, it looked like one of them might be fixed. Here is what you can do. Update to latest trunk and see which ones reproduce in DumpRenderTree. I am now not much worried for a browser repro. If you can provide one more comment with reduced repro (DumpRenderTree/Browser) for each of two stacks, you will increase your chances of higher reward and i can seperate the 2nd stack into a new bug (or you can file one yourself). If you are unable to reduce, that is ok, but please let me know and i can start to work on that. I just want rewarded fully for your awesome bug and efforts.

### mi...@gmail.com (2011-07-17)

I got it down to 25 lines and no external resources or weird shit btw.

### mi...@gmail.com (2011-07-17)

still working on this but here goes. it sometimes takes like 20 reloads for it to crash asan

### in...@chromium.org (2011-07-17)

Perfect. 25 lines for 2 different stacks ? or just 1 stack. Please take your time, no hurry. File a new bug if you have the second repro reduced.

### mi...@gmail.com (2011-07-17)

thanks for that symbols thing

### mi...@gmail.com (2011-07-17)

I'm getting craches with this one all the time now

### in...@chromium.org (2011-07-18)

Sad that it just hit by our fuzzers. Miaubiz, you are fast and you win :)

### in...@chromium.org (2011-07-18)

A slight more reduction using my minimizer

<div><script>
iframe1 = document.createElement('iframe');
document.body.appendChild(iframe1);
document1 = iframe1.contentDocument.implementation.createHTMLDocument("document");
iframe1 = document.createElement('iframe');
document.body.appendChild(iframe1);
document1 = iframe1.contentDocument.implementation.createHTMLDocument("document");
eval("");
  xyz();
</script>
<script>
  for(var a=0;a<18;a++) {
    iframe1 = document.createElement('iframe');
    iframe1.setAttribute("src", "javascript:''");
    document.body.appendChild(iframe1);
  }
</script>

### ma...@google.com (2011-07-19)

[Empty comment from Monorail migration]

### kc...@chromium.org (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-05)

Here's another DocumentLoader lifetime issue, Scott. Fancy it?
In fact looking at the repro, it makes me wonder if your recent patch didn't already have some affect here?

The challenge is it's probably difficult to reproduce a crash / error here without ASAN or Valgrind.

### sc...@chromium.org (2011-08-05)

Thanks (? :) No promises, as I'm still feeling pretty lost in that code, but I'll at least have a look and see what I can figure out.

### in...@chromium.org (2011-08-17)

Better repro with ClusterFuzz

<iframe src="javascript:''"></iframe>
<a><summary><pre><pre><pre><pre><pre><iframe src="javascript:''"></iframe>

<a>

### in...@chromium.org (2011-08-17)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=66360

### in...@chromium.org (2011-08-22)

miaubiz, can you still reproduce this on trunk. I can no longer reproduce this. Seems like something has fixed this, checking with you to make sure that i am right ?

### mi...@gmail.com (2011-08-22)

I'm still seeing this sporadically, but harder to repro than before.

### in...@chromium.org (2011-08-22)

do you have a repro that still reproduces ?

### sc...@gmail.com (2011-08-22)

@miaubiz: we just landed http://trac.webkit.org/changeset/93521, which fixes some lifetime issues in the document loader. Can you still repro it with that change?

### mi...@gmail.com (2011-08-22)

here's the one that was crashing for earlier build.. 93477.. I did rm -rf out and will get back to you in like an hour when it's done.

### mi...@gmail.com (2011-08-22)

here's the stack for that 456.html with dirty 93477

### sc...@gmail.com (2011-08-22)

BTW, I doubt Chromium has rolled WebKit to include that revision just yet, as it is very fresh. You could always manually hack your DEPS to point to that revision of WebKit.

### mi...@gmail.com (2011-08-22)

still there with:

Chromium	15.0.860.0 (Developer Build 97689-dirty)
OS	Linux
WebKit	535.2 (trunk@93523)

and the above repro.

@scarybeasts: :D

### mi...@gmail.com (2011-08-22)

by which I mean, with webkit git I only have to do 'git co master' or 'git co gclient' to switch between gclient and master.

### sc...@gmail.com (2011-08-22)

@japhet: seems this is a lifetime issue in a similar area to the other recent fix. Mind taking a look?

### ja...@chromium.org (2011-08-24)

Could I ask someone else to take this bug?  I don't have a linux box, so it's going to be tough for me to reproduce a bug that requires asan.

Sorry :(

### sc...@gmail.com (2011-08-24)

Adam expressed an interest :)

FWIW, I would expect valgrind to catch something like this easily too. Not sure how good our Mac / Valgrind environment is?

Anyway, given to Adam.

### mi...@gmail.com (2011-08-25)

@scarybeasts: there's so many frames being destroyed and created that valgrind hates it and just gives a million lines of v8 jit :(

vex amd64->IR: unhandled instruction bytes: 0xFF 0xFF 0x1 0x0 0x0 0x0 0x74 0x0
==4879== valgrind: Unrecognised instruction at address 0x2a9ace470e46.
==4879==    at 0x2A9ACE470E46: ???
==4879==    by 0x2A9ACE470C17: ???
==4879==    by 0x2A9ACE45E3A7: ???
==4879==    by 0x2A9ACE45B404: ???
==4879==    by 0x2A9ACE46AF70: ???
==4879==    by 0x2A9ACE46ABF4: ???
==4879==    by 0x2A9ACE46B7E7: ???
==4879==    by 0x2A9ACE46ACBE: ???
==4879==    by 0x2A9ACE45124D: ???
==4879==    by 0x2A9ACE46B151: ???
==4879==    by 0x2A9ACE46ABF4: ???
==4879==    by 0x2A9ACE45124D: ???
==4879==    by 0x2A9ACE467300: ???
==4879==    by 0x2A9ACE455000: ???
==4879==    by 0x11A81AA: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Object***, bool*) (in /usr/lib/chromium-browser/chromium-browser)


### sc...@gmail.com (2011-08-29)

<beg/>
Adam, if we can get an unrisky change landed by Weds, we can get this fix into the final Beta.

### ab...@chromium.org (2011-08-29)

pls don't beg.  /me looks now.

### ab...@chromium.org (2011-08-30)

I understand it.  Great bug.

### ab...@chromium.org (2011-08-30)

@scarybeast: The patch is very non-risky and posted upstream for review.

### in...@chromium.org (2011-08-30)

WoW!! Right on time. http://trac.webkit.org/changeset/94112

### ab...@chromium.org (2011-08-30)

I aim to please.

### sc...@gmail.com (2011-08-30)

Merged to M14: http://trac.webkit.org/changeset/94125

### sc...@gmail.com (2011-09-08)

@miaubiz: nice find, thanks for taking the trouble to work on the big repro and minimize it down. Certainly that helps qualify it for a $1000 Chromium Security Reward :)

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/89330?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092651)*
