# Security: [FLASH] Issues in DefineBitsLossless and DefineBitsLossless2 leads to using uninitialized memory while rendering a picture

| Field | Value |
|-------|-------|
| **Issue ID** | [40081821](https://issues.chromium.org/issues/40081821) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-04-08 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

Issues in DefineBitsLossless and DefineBitsLossless2 leads to using uninitialized memory while rendering a picture. This is caused by the returned value of a zlib function not properly checked.

**VERSION**  

Chrome version 41.0.2272.101, Flash 17.0.0.134 (the code below comes from flash player standalone exe 17.0.0.134)  

Operating System: Win 7 x64 SP1

**REPRODUCTION CASE**

Compile the provided poc with flex sdk:  

mxmlc -static-link-runtime-shared-libraries=true -compress=false -target-player 15.0 -swf-version 25 XBitmapGif.as

And change the bytes in the DefineBitsLossless2 tag, at offset 0x228:  

14 00 14 00 78 to 14 00 14 00 41

To get a DefineBitsLossless tag, change the byte at offset 0x220:  

09 47 00 00 00 to 05 47 00 00 00

Load the provided pocs and see the pointers partially disclosed.

When handling such tags, Flash first allocates a buffer according to the picture's width and height but does not initialize it. If the compressed data stream is corrupted, the zlib function just returns an invalid token and Flash leaves the uninitialized buffer as is.

Look at sub\_54732C:

.text:0054746C loc\_54746C:  

.text:0054746C mov ecx, [esi]  

.text:0054746E push 0  

.text:00547470 push 0  

.text:00547472 push eax  

.text:00547473 push [ebp+var\_10]  

.text:00547476 push [ebp+var\_14]  

.text:00547479 push [ebp+var\_C]  

.text:0054747C call sub\_545459 ; allocate a buffer of 4 \* 14h \* 14h = 640h  

.text:00547481 cmp [ebp+var\_1], 0  

.text:00547485 mov ecx, [esi]  

.text:00547487 setnz al  

.text:0054748A mov [ecx+58h], al  

...  

.text:005474DE loc\_5474DE:  

.text:005474DE lea eax, [ebp+var\_50]  

.text:005474E1 push 0  

.text:005474E3 push eax  

.text:005474E4 call xinflate ; inflate the buffer, but there's no error check?  

.text:005474E9 pop ecx ; thus we can return 0xFFFFFFFD in eax with a corrupt stream  

.text:005474EA pop ecx  

.text:005474EB cmp eax, 1  

.text:005474EE jz short loc\_5474FB  

.text:005474F0 test eax, eax  

.text:005474F2 jnz short loc\_54753A ; which will skip the buffer initialization

Reading this data back is not straightforward. For a DefineBitsLossless tag, we can read values like 0xFFXXYYZZ. For a DefineBitsLossless2 tag an operation is performed on the pixels so we can only read f(pixel). That function is handled by sub\_4CD3B0 and uses a hardcoded table. By conbining both the DefineBitsLossless and DefineBitsLossless2 tags I'm quite convinced we can guess a full pointer.

## Attachments

- [DefineBitsLossless.zip](attachments/DefineBitsLossless.zip) (application/zip, 11.5 KB)
- [DefineBitsLossless_leak.zip](attachments/DefineBitsLossless_leak.zip) (application/zip, 9.6 KB)

## Timeline

### bi...@gmail.com (2015-04-08)

pfffff: Issues in DefineBitsLossless and DefineBitsLossless2 "lead", not "leads". Can I correct that?

### bi...@gmail.com (2015-04-08)

So yes, definitely doable. If we can map the same pointer in both the DefineBitsLossless and DefineBitsLossless2 buffers, we can read 0xFFXXYYZZ and f(0xUUXXYYZZ), where 0xUU is still unknown. 

Then, we only need to compute manually f(0xXXYYZZ), f(0x01XXYYZZ), f(0x02XXYYZZ), ..., f(0xFFXXYYZZ) until we get a match with f(0xUUXXYYZZ). At that moment we can guess 0xUU :).

### in...@chromium.org (2015-04-08)

[Empty comment from Monorail migration]

### bi...@gmail.com (2015-04-09)

Just for fun :) This one should leak a vtable from a BitmapData object on Chrome version 41.0.2272.101 and Flash 17.0.0.134.

### sc...@gmail.com (2015-04-10)

Sent to Adobe. P0 deadline tracking at https://code.google.com/p/google-security-research/issues/detail?id=326.

### sc...@gmail.com (2015-05-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-05-12)

https://helpx.adobe.com/security/products/flash-player/apsb15-09.html

### ti...@google.com (2015-08-17)

As discussed, reward should be paid this week.

### cl...@chromium.org (2015-08-18)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/475018?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081821)*
