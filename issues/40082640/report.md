# Adobe Flash Player Regular Expression Out-Of-Bounds Write Remote Code Execution Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40082640](https://issues.chromium.org/issues/40082640) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | be...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-08-06 |
| **Bounty** | $3,000.00 |

## Description

There's a logic error in the PCRE engine version used in Flash that allows the execution of arbitrary PCRE bytecode, with potential for memory corruption and Remote Code Execution.

Affected flash version: Adobe Flash Player 17.0.0.134 ~ 18.0.0.209

Simplest testcase that will result in an out-of-bounds read access vulnerability is the following:

\x{100}{3,}!!

Above regular expression is compiled into the following bytes：

\x5d\x00\x00\x26\x00\x03\xc4\x80\x1e\xc4\x80

At this point, our emitted bytecode is as follows.

OP_BRA	<---------- /* Start of non-capturing bracket */

OP_EXACT<---------- /* Exactly n matches */

\x03	<---------- /* n = 3 */

\xc4	<---------- /* don't know the next bytes */
\x80
\x1e
\xc4
\x80

When find_recurse() which is in avmshell called, an out-of-bounds read access occurs.

static const uschar *
find_recurse(const uschar *code, BOOL utf8)
{
for (;;)
  {
  register int c = *code; // first fetch \x80 to c
  
  ...
  
  if (c == OP_XCLASS) code += GET(code, 1);

  /* Otherwise, we can get the item's length from the table, except that for
  repeated character types, we have to test for \p and \P, which have an extra
  two bytes of parameters. */

  else
    {
	
	...
	
    /* Add in the fixed length from the table */

    code += _pcre_OP_lengths[c]; // out-of-bounds read and _pcre_OP_lengths[c] will return an instruction length of 0xff

    /* In UTF-8 mode, opcodes that are followed by a character may be followed
    by a multi-byte character. The length in the table is a minimum, so we have
    to arrange to skip the extra bytes. */
  }
}

fetch byte \x80 to variable c and c is treated as an index value:
  register int c = *code;
  ...
  code += _pcre_OP_lengths[c]; 
  
highest opcode is 109,so we read off the end of the lookup table,this will result in out-of-bounds read and _pcre_OP_lengths[c] 
will returns an instruction length of 0xff.

code + 255	<---------- /* somewhere else on the heap */

Search then proceeds until we find the right bytecode for the group we were looking for, or finds OP_END or OP_RECURSE. It then fills in
the opcode for a jump out to where it found that group.

See attached for an execution trace demonstration a heap-groom and arbitrary regexp bytecode execution (the regexp used is slightly different from the above poc).
Prior to this trace, a groom has been performed to leave a gap of size 257 followed by a crafted buffer.

Attachment contains two things:

1) A crash poc which crashes Adobe Flash Player between 17.0.0.134 and 18.0.0.209
2) A brief exploit which will write 0x41414141 to address 0x44444444 which works well on fp_17.0.0.134 ~ fp_18.0.0.203, and just because Adobe added a length cookie to the Vector.* object since fp_18.0.0.209, the exploit can't work on fp_18.0.0.209, but actually this vuln still exists.

Exploit has been tested on 32-bit desktop IE running on windows 7. And if successful, the code will write value 0x41414141 to address 0x44444444. 

The crash poc or the exploit is not 100% reliable, just try again if it can not be reproduced on your environment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### js...@chromium.org (2015-08-06)

matthewyuan@ - Could you add the correct CCs from Adobe?

natashenka@ - IIRC you're one of the people who's been poking at Flash recently, so maybe you'd like to have a look?

### [Deleted User] (2015-08-07)

@Satoshi, can you help find an owner?

### js...@chromium.org (2015-08-07)

Setting the rest of the security flags for traige.

### na...@google.com (2015-08-18)

Thanks, I've reported this issue to Adobe, sorry for the delay.

Do you want to be credited for the issue in the Adobe bulletin? If so, can you reply with the name you want to be credited as.

Also, do you want to apply a deadline to this issue?

### la...@chromium.org (2015-08-18)

[Empty comment from Monorail migration]

### na...@google.com (2015-08-18)

This is PSIRT-4023

### be...@gmail.com (2015-08-19)

[Comment Deleted]

### be...@gmail.com (2015-08-19)

[Comment Deleted]

### [Deleted User] (2015-08-19)

In general, we'd appreciate a 90-day disclosure deadline.  This would align your request with the standard 90-day disclosure for all Google Project Zero and Chromium VRP bugs, and affords us the opportunity to fix the bug while still affording due diligence to both the security and backwards compatibility concerns.

### be...@gmail.com (2015-08-20)

[Comment Deleted]

### la...@chromium.org (2015-10-02)

This issue likely requires triage.  The current issue owner may be inactive (i.e. hasn't fixed an issue in the last 30 days or commented in this particular issue in the last 90 days).  Thanks for helping out!

-Anthony

### [Deleted User] (2015-10-02)

FYI, this is a duplicate of PSIRT 4001, AKA:  
https://code.google.com/p/chromium/issues/detail?id=517383

This is fixed in Q+1, which just reached GMC.  I'm assuming that PSIRT will reach out to you with the final details shortly, as per usual.

### cl...@chromium.org (2015-10-06)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### [Deleted User] (2015-10-20)

The fix should be available in 19.0.0.207 or above.

### be...@gmail.com (2015-10-23)

[Comment Deleted]

### ti...@google.com (2015-11-28)

#15: Sorry for the delay here, let's find out :)

Adding reward-topanel for consideration under the Chrome Reward Program. Details here: https://www.google.com/about/appsecurity/chrome-rewards/

### cl...@chromium.org (2016-01-26)

Bulk update: removing view restriction from closed bugs.

### be...@gmail.com (2016-02-14)

[Comment Deleted]

### ti...@google.com (2016-04-22)

A long time coming... but our panel decided on $3,000 for this report. Congratulations!

Panel notes: Original POC is deleted. On Aug 6th (time of report) offered Flash version v18.0.0.228 and that version does not appear vulnerable to exploitation (even noted by the reporter). Based on that, a baseline payment of $3k was decided.

Our Finance team should be in contact within 7 days to collect payment details. If that doesn't happen, please reach out to me at timwillis@ or update this bug so that I can follow up.

Thanks again for the report and apologies for the significant delay - I've changed the process to keep better tabs on external dependencies like Flash reports. Hopefully some cash coming your way will soften the blow.

Cheers,
Tim

### ti...@google.com (2016-04-23)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/517383?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082640)*
