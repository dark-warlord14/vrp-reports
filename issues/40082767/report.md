# Adobe Flash Player PCRE find_parens Out-Of-Bounds Read Access

| Field | Value |
|-------|-------|
| **Issue ID** | [40082767](https://issues.chromium.org/issues/40082767) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | be...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2015-08-29 |
| **Bounty** | $1,000.00 |

## Description

There’s an error in the PCRE engine version used in Flash that leads to an out-of-bounds read access exception.

Affected version: Adobe Flash Player <= 18.0.0.232

Tested on Windows 7 x64 + IE11(32bit) + fp_18.0.0.232

Crash:

---cut---

0:008> r
eax=0000003e ebx=08767025 ecx=0876702e edx=00000000 esi=0877ffff edi=00000001
eip=69765225 esp=036caf9c ebp=00000003 iopl=0         nv up ei ng nz ac po cy
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210293
Flash32_18_0_0_232!IAEModule_IAEKernel_UnloadModule+0x1bacf5:
69765225 0fb65601        movzx   edx,byte ptr [esi+1]       ds:002b:08780000=??

0:008> u eip
Flash32_18_0_0_232!IAEModule_IAEKernel_UnloadModule+0x1bacf5:
69765225 0fb65601        movzx   edx,byte ptr [esi+1]
69765229 46              inc     esi
6976522a 3bd0            cmp     edx,eax
6976522c 75f7            jne     Flash32_18_0_0_232!IAEModule_IAEKernel_UnloadModule+0x1bacf5 (69765225)
6976522e 85db            test    ebx,ebx
69765230 7417            je      Flash32_18_0_0_232!IAEModule_IAEKernel_UnloadModule+0x1bad19 (69765249)
69765232 8bc6            mov     eax,esi
69765234 2bc1            sub     eax,ecx

---cut---

Simplest testcase that will result in an out-of-bounds read access vulnerability is the following:

\((?&abc))(?P<abc)

attached poc will also crash the avm, and the source code is like:

static int
find_parens(const uschar *ptr, int count, const uschar *name, int lorn,
  BOOL xmode)
{
const uschar *thisname;

for (; *ptr != 0; ptr++)
  {
  int term;
  ...

  if ((*ptr != '<' || ptr[1] == '!' || ptr[1] == '=') &&
       *ptr != '\'')
    continue;

  count++;

  if (name == NULL && count == lorn) return count;
  term = *ptr++;
  if (term == '<') term = '>';
  thisname = ptr;
  while (*ptr != term) ptr++; // crash here, out of bounds read
  if (name != NULL && lorn == ptr - thisname &&
      VMPI_strncmp((const char *)name, (const char *)thisname, lorn) == 0)
    return count;
  }

return -1;
}

if (term == '<') term = '>';
thisname = ptr;
while (*ptr != term) ptr++;

the problem occurs when deal with '<abc', when a '<' character appears, program will try to looking for a '>' character, but in the while loop, program does not check if it is the end of the string, so it will cause an out of bounds read access exception.

Patch:

if (term == '<') term = '>';
thisname = ptr;
while (*ptr != term && *ptr != '\x00') ptr++; // check if it is the end of the pattern

This bug is subject to a 90 day disclosure deadline. If 90 days elapse without a broadly available patch, then the bug report will automatically become visible to the public.

## Attachments

- [poc.zip](attachments/poc.zip) (application/zip, 3.2 KB)

## Timeline

### th...@chromium.org (2015-08-29)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-08-29)

[Empty comment from Monorail migration]

### lg...@chromium.org (2015-08-31)

[Empty comment from Monorail migration]

### la...@chromium.org (2015-10-01)

This issue likely requires triage.  The current issue owner may be inactive (i.e. hasn't fixed an issue in the last 30 days or commented in this particular issue in the last 90 days).  Thanks for helping out!

-Anthony

### cl...@chromium.org (2015-10-29)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### mb...@chromium.org (2015-10-29)

natashenka: Has this one been forwarded along to Adobe yet?

### na...@google.com (2015-10-29)

No, I just reported it, sorry I'm not sure how this slipped. The good news is I'm pretty sure this isn't exploitable, at worst it's an info leak. 

### na...@google.com (2015-10-29)

This is PSIRT-4259

### in...@chromium.org (2015-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

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

### mb...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

Sorry for the delay - but the VRP panel just awarded $1,000 for this report!

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-02-14)

Looks like we rewarded this one a while back but it's still marked ExternalDependency. Did Adobe end up fixing this? Can we close it out if so?

### na...@google.com (2018-02-14)

Yeah, it was fixed

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-24)

This issue was migrated from crbug.com/chromium/526341?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082767)*
