# Security: UAF related to XPointer range-to function

| Field | Value |
|-------|-------|
| **Issue ID** | [40084702](https://issues.chromium.org/issues/40084702) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | we...@aevum.de |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-06-26 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

Bugs in xmlXPathEvalExpr and xmlXPtrRangeToFunction can lead to a use-after-free and allow control of the instruction pointer.

**VERSION**  

Chrome Version: 51.0.2704.106 stable  

Operating System: Windows 10, 64-bit

**REPRODUCTION CASE**  

See the attached files range-to-uaf-poc.xml and range-to-uaf-poc.xsl. If you open the XML file locally, make sure to run Chrome with --allow-file-access-from-files.

FULL DETAILS  

The first observation is that xmlXPathEvalExpr which parses and evaluates an XPath expression allows any unparseable content after an expression. After compiling the valid part of the expression, the "cur" element in the xmlXPathParserContextPtr struct points to the beginning of the unparseable content.

If an XPointer expression contains a call to the "range-to" function, xmlXPtrRangeToFunction is invoked during evaluation of the expression. This function calls xmlXPathEvalExpr again, resuming the compilation where the previous call to xmlXPathEvalExpr left off. This leads to additional operations being compiled and added to the xmlXPathStepOp table, possibly reallocating memory for this table.

xmlXPtrRangeToFunction then returns to xmlXPathCompOpEval which is the main runloop for compiled XPath expressions. The "op" argument to xmlXPathCompOpEval points into the StepOp table, assuming the table won't be modified or reallocated during evaluation. If a reallocation occurs as decribed above, "op" points into memory that was previously freed, resulting in a use-after-free.

This can be leveraged to control the instruction pointer if an operation following the "range-to" call is another XPath function call. For function calls, the function pointer is cached in the "cache" element of the StepOp struct. Causing an allocation of the same size as the old StepOp table (10 \* 40 = 400 bytes on 32-bit) will typically reuse the old memory area of the table. Using a 400-byte XPath string literal in the second part of the XPath expression which is parsed in xmlXPtrRangeToFunction gives an attacker control over this memory area. The only limitation is that the string literal is stored as UTF-8.

The POC uses an XPointer expression of the form

```
xpointer(name(range-to(.))0+0+"[400-byte-buffer]")  

```

"name(...)" could be any function. This function call is only used to transfer control to the address provided by the attacker. "name(range-to(.))" is the expression that will be compiled and evaluated initially. '0+0+"[400-byte-buffer]"' is the expression that will be compiled during evaluation of "range-to(.)". This replaces the original StepOp table with the UTF-8 encoded contents of the string literal. "0+0+" is needed to trigger a reallocation. The 400-byte buffer overwrites an array of 10 xmlXPathStepOp structs:

struct \_xmlXPathStepOp {  

xmlXPathOp op;  

int ch1;  

int ch2;  

int value;  

int value2;  

int value3;  

void \*value4;  

void \*value5;  

void \*cache;  

void \*cacheURI;  

};

"value" must be a negative number to pass a check in xmlXPathCompOpEval. Any four-byte UTF-8 character can be used. "cache" contains the target address. The POC simply uses a sequence of 'GRINNING FACE' (U+1F600) characters. The UTF-8 encoding of this character is 0xF0 0x9F 0x98 0x80. Subsequently, xmlXPathCompOpEval jumps to the address 0x80989FF0.

The POC uses the XSLT "document" function to trigger the evaluation of an XPointer expression. Other mechanisms could be probably used as well. The XPointer expression must be percent encoded since it's part of a URL.

A patch fixing this bug will follow in the next days.

DISCLOSURE  

I contribute to libxml2 occasionally. I haven't shared details about this issue with anyone, and I don't plan to do so until it is fixed in Webkit browsers. I didn't write any parts of the buggy code. This bug was found with afl-fuzz and ASan.

## Attachments

- [range-to-uaf-poc.xml](attachments/range-to-uaf-poc.xml) (text/plain, 57 B)
- [range-to-uaf-poc.xsl](attachments/range-to-uaf-poc.xsl) (text/plain, 1.4 KB)
- [uaf.xsl](attachments/uaf.xsl) (text/plain, 1.4 KB)
- [range-to-uaf.diff](attachments/range-to-uaf.diff) (application/octet-stream, 3.8 KB)

## Timeline

### aa...@google.com (2016-06-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>XML]

### me...@google.com (2016-06-27)

range-to-uaf-poc.xsl needs to be renamed to uaf.xsl in the poc.

### sh...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-27)

+dominicc - can you take a look at this?

### we...@aevum.de (2016-06-28)

Here's a patch against libxml2 master fixing the bug.

### do...@chromium.org (2016-07-05)

Thank you for another detailed bug report and repros.

I have uploaded your patch here: https://codereview.chromium.org/2127493002

I have filed a blank upstream bug: https://bugzilla.gnome.org/show_bug.cgi?id=768428

### bu...@chromium.org (2016-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6ad54b72c7f8c422c288dd9c8756d2a15f30e53

commit b6ad54b72c7f8c422c288dd9c8756d2a15f30e53
Author: dominicc <dominicc@chromium.org>
Date: Wed Jul 06 07:06:46 2016

Delete obsolete XPointer range-to function.

BUG=623378

Review-Url: https://codereview.chromium.org/2127493002
Cr-Commit-Position: refs/heads/master@{#403859}

[modify] https://crrev.com/b6ad54b72c7f8c422c288dd9c8756d2a15f30e53/third_party/libxml/README.chromium
[modify] https://crrev.com/b6ad54b72c7f8c422c288dd9c8756d2a15f30e53/third_party/libxml/src/xpath.c
[modify] https://crrev.com/b6ad54b72c7f8c422c288dd9c8756d2a15f30e53/third_party/libxml/src/xpointer.c


### do...@chromium.org (2016-07-06)

ddkilzer, per wellnhofer's point about disclosure, could you indicate when WebKit picks this up so we can push the repro and patches into the upstream bug tracker?

### sh...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### dd...@apple.com (2016-07-06)

> ddkilzer, per wellnhofer's point about disclosure, could you indicate when WebKit picks this up so we can push the repro and patches into the upstream bug tracker?

Will do.  I'm on vacation this week, but I've created a Radar to track the issue internally.  Note that Safari/WebKit does not ship stand-alone libxml2/libxslt updates, so these changes must go into operating systems (macOS, iOS, etc.).


### dd...@apple.com (2016-07-11)

> ddkilzer, per wellnhofer's point about disclosure, could you indicate when WebKit picks this up so we can push the repro and patches into the upstream bug tracker?

This change will ship with the major OS releases (macOS 10.12 Sierra, iOS 10, tvOS 10, watchOS 3) as we don't have another software update release available, and we don't ship libxml2 outside each OS.


### do...@chromium.org (2016-07-12)

wellnhofer would you be comfortable with this getting disclosed upstream now?

### we...@aevum.de (2016-07-12)

dominicc, I leave the decision when/what/where to disclose to you. If you like, I can add some details that are relevant for libxml2 developers to the upstream bug.

### aw...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### do...@chromium.org (2016-07-15)

This is an obscure part of a little-used feature. I haven't seen any blowback from this. I think this is safe to merge.

### go...@chromium.org (2016-07-15)

Thank you dominicc@.

I'm OK to take this merge in for M52 and M53 per https://crbug.com/chromium/623378#c19. awhalley@, what do you think?



### aw...@chromium.org (2016-07-15)

Yes, I agree.

### go...@chromium.org (2016-07-15)

Approving merge to M53 branch 2785 and M52 branch 2743 based on https://crbug.com/chromium/623378#c21. Please merge ASAP (possibly before 5:00 PM PST today, Friday or latest by 4:00 PM PST on Monday).

### go...@chromium.org (2016-07-15)

[Comment Deleted]

### go...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-18)

Ccing reviewer (inferno@). If you can do the merge to M52 and M53 today before 5:00 PM PST would be great as dominicc@ is in Japan.

### bu...@chromium.org (2016-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/33b71091611f766d3902ed4f948b67f08b2a1f69

commit 33b71091611f766d3902ed4f948b67f08b2a1f69
Author: Martin Barbella <mbarbella@chromium.org>
Date: Mon Jul 18 22:51:13 2016

Delete obsolete XPointer range-to function.

BUG=623378

Review-Url: https://codereview.chromium.org/2127493002
Cr-Commit-Position: refs/heads/master@{#403859}
(cherry picked from commit b6ad54b72c7f8c422c288dd9c8756d2a15f30e53)

Review URL: https://codereview.chromium.org/2154263005 .

Cr-Commit-Position: refs/branch-heads/2785@{#206}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/33b71091611f766d3902ed4f948b67f08b2a1f69/third_party/libxml/README.chromium
[modify] https://crrev.com/33b71091611f766d3902ed4f948b67f08b2a1f69/third_party/libxml/src/xpath.c
[modify] https://crrev.com/33b71091611f766d3902ed4f948b67f08b2a1f69/third_party/libxml/src/xpointer.c


### bu...@chromium.org (2016-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/90af22ca17e337cfa3cf8060a97e944643222154

commit 90af22ca17e337cfa3cf8060a97e944643222154
Author: Martin Barbella <mbarbella@chromium.org>
Date: Mon Jul 18 22:56:33 2016

Delete obsolete XPointer range-to function.

BUG=623378

Review-Url: https://codereview.chromium.org/2127493002
Cr-Commit-Position: refs/heads/master@{#403859}
(cherry picked from commit b6ad54b72c7f8c422c288dd9c8756d2a15f30e53)
TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/2154173003 .

Cr-Commit-Position: refs/branch-heads/2743@{#669}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/90af22ca17e337cfa3cf8060a97e944643222154/third_party/libxml/README.chromium
[modify] https://crrev.com/90af22ca17e337cfa3cf8060a97e944643222154/third_party/libxml/src/xpath.c
[modify] https://crrev.com/90af22ca17e337cfa3cf8060a97e944643222154/third_party/libxml/src/xpointer.c


### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Our panel has awarded you $3,500 for this bug, congratulations!  A member of our finance team will be in touch over the next few weeks.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### si...@gmail.com (2016-07-27)

Any idea why libxml2 upstream (Daniel Veillard) was not involved with the bug? 
In most of the previous bugs, libxml2 was involved at a very early stage.

### do...@chromium.org (2016-07-27)

Sorry, that was an oversight on my part. I have copied the details upstream.

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### we...@aevum.de (2016-10-12)

This is now fixed upstream: https://git.gnome.org/browse/libxml2/commit/?id=9ab01a277d71f54d3143c2cf333c5c2e9aaedd9e

### sh...@chromium.org (2016-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dd...@apple.com (2016-10-14)

> Any idea why libxml2 upstream (Daniel Veillard) was not involved with the bug? 
> In most of the previous bugs, libxml2 was involved at a very early stage.

Daniel is very busy.  To get him involved I had to contact him directly a number of times.

Nick Wellnhofer is also an upstream libxml2/libxslt maintainer, so he's also able to review and land patches upstream, but tends to focus mostly on libxslt.

Note that both Daniel and Nick are volunteering their time on these projects.


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/623378?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084702)*
