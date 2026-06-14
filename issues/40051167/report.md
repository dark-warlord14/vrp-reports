# v8_i18n::BCP47ToICUFormat() - crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40051167](https://issues.chromium.org/issues/40051167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sl...@gmail.com |
| **Assignee** | ci...@chromium.org |
| **Created** | 2011-11-12 |
| **Bounty** | $1,000.00 |

## Description

Crashes on windows stable (15.0.874.120 [108895]), dev (17.0.932.0 [108826]) and canary (17.0.936.1 [109705]). Can't reproduce it on linux.
It doesn't crash every time. Try to open crash1.html in new tab if it not crashes (reload does not lead to crash).

(14d0.15c8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00000166 ebx=00b80000 ecx=00001ad0 edx=506c7500 esi=00b81ad1 edi=0000009d
eip=644795ac esp=0019e8a8 ebp=0019e968 iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
chrome_634f0000!v8_i18n::BCP47ToICUFormat+0x7c:
644795ac 88940d58ffffff  mov     byte ptr [ebp+ecx-0A8h],dl ss:0023:001a0390=d0

ExceptionAddress: 644795ac (chrome_634f0000!v8_i18n::BCP47ToICUFormat+0x0000007c)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 001a0390
Attempt to write to address 001a0390

ChildEBP RetAddr  
0019e968 644793bb chrome_634f0000!v8_i18n::BCP47ToICUFormat+0x7c
0019ebb0 644792f2 chrome_634f0000!v8_i18n::LanguageMatcher::CompareToSupportedLocaleIDList+0xa4
0019ed0c 64476c19 chrome_634f0000!v8_i18n::LanguageMatcher::GetBestMatchForString+0x2e
0019eea8 645c98df chrome_634f0000!v8_i18n::Locale::JSLocale+0x136
0019ef0c 645c9cb3 chrome_634f0000!v8::internal::HandleApiCallHelper<0>+0x19f
0019efe8 6456ebd5 chrome_634f0000!v8::internal::Builtin_HandleApiCall+0x13
0019f020 6456f60c chrome_634f0000!v8::internal::Invoke+0x115
0019f058 6453ae57 chrome_634f0000!v8::internal::Execution::Call+0x11c
0019f098 6422faf8 chrome_634f0000!v8::Function::Call+0xf7
0019f0d8 6422f9bf chrome_634f0000!WebCore::V8Proxy::instrumentedCallFunction+0xca
0019f10c 64281c48 chrome_634f0000!WebCore::V8Proxy::callFunction+0x82
0019f148 6418be20 chrome_634f0000!WebCore::V8EventListener::callListenerFunction+0x6d
0019f190 6418bcdf chrome_634f0000!WebCore::V8AbstractEventListener::invokeEventHandler+0xcf
0019f1d0 6437dba6 chrome_634f0000!WebCore::V8AbstractEventListener::handleEvent+0x69
0019f200 6437dae3 chrome_634f0000!WebCore::EventTarget::fireEventListeners+0xb6
0019f21c 6429c380 chrome_634f0000!WebCore::EventTarget::fireEventListeners+0x2c
0019f248 6429c417 chrome_634f0000!WebCore::DOMWindow::dispatchEvent+0xb6
0019f258 6429c20f chrome_634f0000!WebCore::DOMWindow::dispatchTimedEvent+0x31
0019f28c 64365d62 chrome_634f0000!WebCore::DOMWindow::dispatchLoadEvent+0x8e
0019f2b8 641feeaf chrome_634f0000!WebCore::Document::implicitClose+0xff
0019f2c0 641fedb6 chrome_634f0000!WebCore::FrameLoader::checkCallImplicitClose+0x4d
0019f2d4 63cb761b chrome_634f0000!WebCore::FrameLoader::checkCompleted+0x8f
0019f308 6418edd0 chrome_634f0000!WebKit::FrameLoaderClientImpl::dispatchDidFinishDocumentLoad+0x18
0019f310 6418ed94 chrome_634f0000!WebCore::DocumentWriter::endIfNotLoadingMainResource+0x3a
0019f318 64204cc8 chrome_634f0000!WebCore::DocumentWriter::end+0x11
0019f320 6420176e chrome_634f0000!WebCore::DocumentLoader::finishedLoading+0x29
[...]

>dv /V
0019e970 @ebp+0x08       locale_id = 0x00b80000 "Aa???"
0019e974 @ebp+0x0c          result = 0x0019eb08 "@???"
0019e8b8 @ebp-0xb0          status = U_ZERO_ERROR (0n0)
0019e8bc @ebp-0xac     locale_size = 0n1698568
0019e8c0 @ebp-0xa8          locale = char [157] "Aa???"

chrome_634f0000!v8_i18n::BCP47ToICUFormat+0x66:
64479596 114184          adc     dword ptr [ecx-7Ch],eax
64479599 d275f9          sal     byte ptr [ebp-7],cl
6447959c 2bce            sub     ecx,esi
6447959e 8d7001          lea     esi,[eax+1]
644795a1 8a10            mov     dl,byte ptr [eax]
644795a3 40              inc     eax
644795a4 84d2            test    dl,dl
644795a6 75f9            jne     chrome_634f0000!v8_i18n::BCP47ToICUFormat+0x71 (644795a1)
644795a8 2bc6            sub     eax,esi
644795aa 2bc8            sub     ecx,eax
644795ac 88940d58ffffff  mov     byte ptr [ebp+ecx-0A8h],dl
644795b3 8d8550ffffff    lea     eax,[ebp-0B0h]
644795b9 50              push    eax
644795ba 8d8554ffffff    lea     eax,[ebp-0ACh]
644795c0 50              push    eax
644795c1 57              push    edi


## Attachments

- [stack1.txt](attachments/stack1.txt) (text/x-c; charset=us-ascii, 9.3 KB)
- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 15.7 KB)

## Timeline

### ke...@chromium.org (2011-11-13)

This is an array index out of bounds in BCP47ToICUFormat. It looks like you can write a single zero byte to a bad stack offset (probably arbitrary, though not negative) from this line:
    locale[base_length] = '\0';

I could write the straightforward solution here (add a sanity check), but I may not have time before Tuesday and I've never contributed to v8 before. I'm adding some v8-knowledgeable cc's in case somebody familiar with language tags thinks this needs a more nuanced solution, or if someone has a few spare cycles to take care of the patch.

### sc...@gmail.com (2011-11-13)

Seems nasty. Danno?

### sc...@gmail.com (2011-11-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-11-14)

This is not in core V8, but in the i18n that is hosted in the V8 project. Reassigning to the appropriate owner.

### sc...@gmail.com (2011-11-15)

@cira: when do you think you can get to this? I've tentatively marked as a release blocker for M16.

### ci...@chromium.org (2011-11-15)

I'll work on it today.

### ci...@chromium.org (2011-11-15)

I'll work on it today.

### ci...@chromium.org (2011-11-15)

Btw. i18n is not hosted in v8 project anymore. I've moved it to separate code.google.com/p/v8-i18n project.

I'll remove dead i18n code from v8 tree (I've removed all Chromium and WebKit deps to it).

### bu...@chromium.org (2011-11-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=110195

------------------------------------------------------------------------
r110195 | cira@google.com | Tue Nov 15 14:41:27 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=110195&r2=110194&pathrev=110195

Update v8-i18n project to r7 to fix a stable blocker.

Fix to v8-i18n was submitted in http://codereview.chromium.org/8570009

BUG=104011
TEST=Load crash1.html from bug report and check it doesn't crash browser. 
Review URL: http://codereview.chromium.org/8573014
------------------------------------------------------------------------

### sc...@gmail.com (2011-11-15)

Thanks for the quick fix!

### sc...@gmail.com (2011-11-17)

@slaweck: thanks, nice interesting bug accessible from an interesting v8 API!
The repro is a bit large but this did not impede the quick resolution of the bug, hence a $1000 Chromium Security Reward!

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

### sc...@gmail.com (2011-11-17)

Pulled v8-i18n to @r8 on M16 branch: r19816

### sc...@gmail.com (2011-12-20)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=19816

------------------------------------------------------------------------
r19816 | cevans@google.com | 2011-11-17T09:06:54.221374Z

------------------------------------------------------------------------

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/104011?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051167)*
