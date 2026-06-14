# Security: Type confusion vulnerability in V8Clipboard::setDragImageMethodCustom

| Field | Value |
|-------|-------|
| **Issue ID** | [40077385](https://issues.chromium.org/issues/40077385) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2013-04-11 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

A type confusion vulnerability exists in the code that handles setting drag images for draggable items. The specified drag image is cast to an HTMLImageElement without proper checks being performed to ensure that it is an HTML Image element. The check uses the Node::hasLocalName() function, which operates on a QualifiedName to check that the localName (tag name) is "img", but does not check the namespaceURI of the QualifiedName object. This allows an invalid (e.g. SVG) "img" element to pass the checks and an invalid cast occurs.

The vulnerable code is as follows:

src\third\_party\WebKit\Source\bindings\v8\custom\V8ClipboardCustom.cpp:100  

...  

if (toElement(node)->hasLocalName(HTMLNames::imgTag) && !node->inDocument())  

clipboard->setDragImage(static\_cast<HTMLImageElement\*>(node)->cachedImage(), IntPoint(x, y));  

...

Immediately after the cast is performed, the cachedImage() method is called on the invalid object, which makes several virtual function calls on the object. As the HTMLImageElement's vtable is much larger than an unknown SVGElement, the adjacent memory is used as part of the vtable. The values used vary from run to run, but are often ascii text from part of a string. It is speculated that these values could be controlled if the appropriate heap manipulation was performed before triggering the issue.

A suitable fix for this issue is to use the Node::hasTagName() function, which checks both the localName and the namespaceURI (inside the QualifiedName::matches() function).

**VERSION**  

Chrome Version: 26.0.1410.64 (stable). Vulnerable code confirmed present in trunk.  

Operating System: Windows 8 Pro

**REPRODUCTION CASE**  

A minimised test case is attached. To trigger the crash, click and drag on the image.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

(c74.122c): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

chrome\_6f680000!WebCore::CachedResourceHandleBase::setResource+0x4d:  

6f833e33 ff873c030000 inc dword ptr [edi+33Ch] ds:002b:7155753c=00000000  

2:036:x86> r  

eax=71557200 ebx=042407e4 ecx=042407e4 edx=71557200 esi=00000000 edi=71557200  

eip=6f833e33 esp=0080e1e0 ebp=0080e1fc iopl=0 nv up ei pl nz na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

chrome\_6f680000!WebCore::CachedResourceHandleBase::setResource+0x4d:  

6f833e33 ff873c030000 inc dword ptr [edi+33Ch] ds:002b:7155753c=00000000  

2:036:x86> k L 10  

ChildEBP RetAddr  

0080e1fc 704262c4 chrome\_6f680000!WebCore::CachedResourceHandleBase::setResource+0x4d  

0080e210 70426341 chrome\_6f680000!WebCore::ClipboardChromium::setDragImage+0x31  

0080e228 7050d0b8 chrome\_6f680000!WebCore::ClipboardChromium::setDragImage+0x15  

0080e278 6f942b7e chrome\_6f680000!WebCore::V8Clipboard::setDragImageCallback+0x242  

0080e2e0 6f942904 chrome\_6f680000!v8::internal::HandleApiCallHelper<0>+0x246  

0080e3b4 6f8daa83 chrome\_6f680000!v8::internal::Builtin\_HandleApiCall+0x18  

0080e404 6f8da933 chrome\_6f680000!v8::internal::Invoke+0x144  

0080e444 6f969305 chrome\_6f680000!v8::internal::Execution::Call+0x17b  

0080e498 6faae768 chrome\_6f680000!v8::Function::Call+0x137  

0080e4e8 6faae508 chrome\_6f680000!WebCore::ScriptController::callFunctionWithInstrumentation+0x1de  

0080e50c 704dd449 chrome\_6f680000!WebCore::ScriptController::callFunction+0x37  

0080e530 6faad79e chrome\_6f680000!WebCore::V8LazyEventListener::callListenerFunction+0xc7  

0080e570 6faac418 chrome\_6f680000!WebCore::V8AbstractEventListener::invokeEventHandler+0x102  

0080e5a8 6faac25c chrome\_6f680000!WebCore::V8AbstractEventListener::handleEvent+0x88  

0080e5d8 6f7c6883 chrome\_6f680000!WebCore::EventTarget::fireEventListeners+0x18d  

0080e608 6f7c6bb1 chrome\_6f680000!WebCore::EventTarget::fireEventListeners+0xfc

## Attachments

- [trigger.html](attachments/trigger.html) (text/html; charset=us-ascii, 386 B)

## Timeline

### ts...@chromium.org (2013-04-11)

I can bang out a fix for this today.

### ts...@chromium.org (2013-04-11)

Note: repro'd on chrome 28.0.1475 Linux/64.

### ts...@chromium.org (2013-04-11)

[Empty comment from Monorail migration]

### ke...@chromium.org (2013-04-11)

Nice report.

### ts...@chromium.org (2013-04-11)

https://codereview.chromium.org/14099005/

### in...@chromium.org (2013-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-04-16)

https://src.chromium.org/viewvc/blink?view=rev&revision=148487

### in...@chromium.org (2013-04-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-18)

------------------------------------------------------------------------
r148487 | tsepez@chromium.org | 2013-04-16T19:37:00.341913Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/drag-svg-image-crash-expected.txt?r1=148487&r2=148486&pathrev=148487
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/drag-svg-image-crash.html?r1=148487&r2=148486&pathrev=148487
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/custom/V8ClipboardCustom.cpp?r1=148487&r2=148486&pathrev=148487

Fix test for HTML image element in V8ClipboardCustom.cpp.

Use the hasTagName() method, rather than the hasLocalName() method, so that
namespaces are handled properly.

TBR=haraken@chromium.org
BUG=230176

Review URL: https://codereview.chromium.org/14099005
------------------------------------------------------------------------

### sc...@gmail.com (2013-04-22)

M27: https://src.chromium.org/viewvc/blink?view=rev&revision=148870

### sc...@gmail.com (2013-05-03)

@jonbutler88: Welcome to the Chromium VRP! :D
This report qualifies for a $1500 reward, comprised of a $1000 base reward for a very well reported bug and a $500 bonus for an attempt to demonstrate severity (occasional ascii in faulting register -- note that a deterministic vtable read fault at 0x41414141 would qualify for $1000 bonus.)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### jo...@gmail.com (2013-08-13)

Hi all,

I am preparing slides for our Nordic Sec Conf presentation, and would like to use this bug as an example of a type confusion we found "along the way".

Is that going to cause a problem? The bug has been patched for a while now...

### sc...@gmail.com (2013-08-20)

Sorry no-one replied earlier! Absolutely, go right ahead.

### jo...@gmail.com (2013-10-21)

As a "bump" for the bounty on this one, I am now finally registered as a supplier on the system. I don't mind waiting if you want to bundle this one in with the others I currently have open :)

Cheers,
Jon

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/230176?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/231171]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077385)*
