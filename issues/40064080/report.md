# Security: arbitrary address write in allocate_temp_range

| Field | Value |
|-------|-------|
| **Issue ID** | [40064080](https://issues.chromium.org/issues/40064080) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-17 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

There is no guarantee that first must be greater than last in allocate\_temp\_range. We can trigger an integer overflow by `DCL TEMP[1000000..0]` and subsequently trigger arbitrary address write/heap buffer overflow.

```
static bool allocate_temp_range(struct vrend_temp_range \*\*temp_ranges, uint32_t \*num_temp_ranges, int first, int last,  
                                int array_id)  
{  
   int idx = \*num_temp_ranges;  
  
   if (array_id > 0) {  
  
      \*temp_ranges = realloc(\*temp_ranges, sizeof(struct vrend_temp_range) \* (idx + 1));  
      if (!\*temp_ranges)  
         return false;  
  
      (\*temp_ranges)[idx].first = first;  
      (\*temp_ranges)[idx].last = last;  
      (\*temp_ranges)[idx].array_id = array_id;  
      (\*temp_ranges)[idx].precise_result = false;  
      (\*num_temp_ranges)++;  
   } else {  
      int ntemps = last - first + 1;        <----- integer overflow  
      \*temp_ranges = realloc(\*temp_ranges, sizeof(struct vrend_temp_range) \* (idx + ntemps));  
      for (int i = 0; i < ntemps; ++i) {  
         (\*temp_ranges)[idx + i].first = first + i;      <----- arbitrary address write or heap buffer overflow  
         (\*temp_ranges)[idx + i].last = first + i;  
         (\*temp_ranges)[idx + i].array_id = 0;  
         (\*temp_ranges)[idx + i].precise_result = false;  
      }  
      (\*num_temp_ranges) += ntemps;  
  
  
   }  
   return true;  
}  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Compile the virgl\_fuzzer.c with -fsanitize=address
2. ASAN\_OPTIONS="allocator\_may\_return\_null=1" ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 2.0 KB)
- [test](attachments/test) (text/plain, 880 B)

## Timeline

### [Deleted User] (2023-04-17)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-18)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/278654363). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/278654363]

### ch...@google.com (2023-04-18)

Dear reporter, can you please provide the linked FoundIn ChromeOS Version for this bug?

### ch...@google.com (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-25)

The fix has flown to ChromeOS side in https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4462757. Mark as fixed for now.

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### ha...@google.com (2023-05-03)

The bug is in CrosVM's virtual GPU renderer, which is already a sandboxed process. Marking it as low severity per the chromeOS severity guidelines

### [Deleted User] (2023-05-03)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

This allows for protection domain bypass (guest->host), therefore it's a P1 High.

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

And again-- congratulations, rinngo! The VRP Panel has decided to award you $7,000 for this report. Thank you for your effort and reporting this issue to us!

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-01)

This issue was migrated from crbug.com/chromium/1433646?no_tracker_redirect=1

[Monorail blocking: b/278654363]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064080)*
