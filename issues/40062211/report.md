# Buffer overflow in the rndis_wlan driver for Linux kernel

| Field | Value |
|-------|-------|
| **Issue ID** | [40062211](https://issues.chromium.org/issues/40062211) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **CVE IDs** | CVE-2023-23559 |
| **Reporter** | sz...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2022-12-13 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description


Buffer overflow in the rndis_wlan driver for Linux kernel


---

### Bug location


#### Which product or website have you found a vulnerability in?

Other - Chrome VRP


---

### The problem


#### Please describe the technical details of the vulnerability

The rndis_wlan driver used to provide support for Broadcom 4320 based
wireless network adapters includes coding issues allowing one to
achieve privilege escalation by executing arbitrary code in kernel
context.

Due to invalid variable types utilized in the rndis_query_oid function
an attacker may bypass implemented validation and overflow the data buffer.

By providing sufficiently large values of RNDIS response length and offset
which are uint32_t the cast to signed integer during assignment to resplen
and respoffs variables will overflow making the latter two negative.

With negative resplen or/and respoffs variables the implemented checks may
be passed leading to a invocation of memcpy. If supplied copylen is negative
it will be again cast to a unexpectedly large unsigned value. Consequently
an overflow of the data buffer will occur. One may control the location at which
supplied payload (up to 1024 bytes) will be copied by manipulating the respoffs.

Besides buffer overflow this issue may be exploited to retrieve contents of
kernel memory space by using a valid length and tweaking respoffs. In this case
selected conents of ram offset against u.buf by a negative value will be copied
to the data buffer. Contents of the latter one may be exposed depending on issues
OID.

```
	if (ret == 0) {
		resplen = le32_to_cpu(u.get_c->len);
		respoffs = le32_to_cpu(u.get_c->offset) + 8;

		if (respoffs > buflen) {
			/* Device returned data offset outside buffer, error. */
			netdev_dbg(dev->net, "%s(%s): received invalid "
				"data offset: %d > %d\n", __func__,
				oid_to_string(oid), respoffs, buflen);

			ret = -EINVAL;
			goto exit_unlock;
		}

		if (resplen > (buflen - respoffs)) {
			/* Device would have returned more data if buffer would
			 * have been big enough. Copy just the bits that we got.
			 */
			copylen = buflen - respoffs;
		} else {
			copylen = resplen;
		}

		if (copylen > *len)
			copylen = *len;

		memcpy(data, u.buf + respoffs, copylen);
```

Reproduction is rather straightforward - one needs to connect a properly crafted
USB device to the host and the overflow may be exploited as soon as during
driver binding phase. I can provide a simple patch for the rndis USB gadget if
you would like to perform some reproduction attempts.

This issue dates back to 2010 and looking at provided ChromeOS base/default configs
(CONFIG_USB_NET_RNDIS_WLAN) all/most versions are affected.

Let me know if you find this case interesting and in scope of the Chrome OS bug
bounty program.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker with physical access to the target may attach a properly crafted malicious device to invoke a buffer overflow during driver binding phase. In worst case one may exploit this issue to achieve arbitrary code execution in kernel context. Unlocking of the device is not required for successful execution.


---

### The cause


#### What version of Chrome have you found the security issue in?

All including Flex?


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Privilege Escalation 


#### How would you like to be publicly acknowledged for your report?

Szymon 




## Timeline

### ch...@appspot.gserviceaccount.com (2022-12-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-12-13)

Thanks for the report Szymon. Has this been reported anywhere else?

### jo...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/262448137]

### sz...@gmail.com (2022-12-14)

Hello,

Since it's a kernel driver issue I reported it to the Linux security team (security@kernel.org) along with a draft patch for review.

Best regards,
Szymon

### [Deleted User] (2022-12-14)

[Empty comment from Monorail migration]

### sz...@gmail.com (2023-01-02)

Hello,

Provided patch addressing this issue is currently under review.
Will you create a CVE for this case?

Best regards,
Szymon

### sz...@gmail.com (2023-01-08)

Hello,

Can you please provide me the following information?
- was this issue triaged and is it considered valid from your perspective?
- do you require any additional details from my side?
- is this reported issue eglible for Chrome Vulnerability Reward Program 
- are you planning to create a CVE for this issue?

Best regards,
Szymon

### ch...@google.com (2023-01-12)

[Empty comment from Monorail migration]

### ku...@google.com (2023-01-12)

We have already removed the vulnerability by temporarily disabling the driver. Jun is working to fix the vulnerability in the driver and enable the driver back into chromeOs.

For the questions in https://crbug.com/chromium/1400589#c9 from Szymon, I would let Jorge answer those.

### sz...@gmail.com (2023-01-12)

Yes, I saw the temporary mitigation in the Chrome OS repository disabling rndis_wlan.

As I mentioned in https://crbug.com/chromium/1400589#c8 a patch is under review for the upstream kernel. Unfortunately it's taking more time than I anticipated. You can check the progress at the Linux kernel mailing list => https://lore.kernel.org/lkml/ece5f6a7fad9eb55d0fbf97c6227571e887c2c33.camel@gmail.com/T/ . I'm not sure if you prefer to fix the vulnerability on your own or you'll simply pick-up the patch applied on the mainstream kernel.

I'm looking forward to your answers to questions from https://crbug.com/chromium/1400589#c9.


### ju...@google.com (2023-01-12)

Hi Syzmon,

I am aware your upstream patch and thankful to your work.

I always prefer the patch in mainstream kernel if it can fix the security vulnerability and resolve my concerns.

You patch generally looks good to me. I found there is more code risking integer overflow. This is the example:

```
respoffs = le32_to_cpu(u.get_c->offset) + 8;
```

And it's better change parameter type "int* len" -> "size_t *len" in function rndis_query_oid.

You can preview my Changeset in https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157711

What do you think those changes? Thanks.

### sz...@gmail.com (2023-01-12)

Hello Jun,

Yes - agree that there's a potential integer overflow in computation of respoffs, yet I don't see it as a security risk - even if the sum of le32_to_cpu(u.get_c->offset) and 8 overflows respoffs will still stay in the buffer boundaries so nothing bad should happen. Do you have other thoughts on this?

As for the len type change, since this value is only controlled by a developer, what benefit do you see in this particular change?

Best regards,
Szymon

### ju...@google.com (2023-01-13)

Hi Syzmon,

> Yes - agree that there's a potential integer overflow in computation of respoffs, yet I don't see it as a security risk - even if the sum of le32_to_cpu(u.get_c->offset) and 8 overflows respoffs will still stay in the buffer boundaries so nothing bad should happen. Do you have other thoughts on this?

Nothing more than worrying about the integer overflow makes debugging a little bit more confusing when the respoffs is too large.

> As for the len type change, since this value is only controlled by a developer, what benefit do you see in this particular change?

Out of my developer's pedantry, I see this as a good practice to developers. But changing the len type doesn't add too much values to the users after traversing all use cases.

Your change is fine to me. Thanks for your clarification.

Best Regards,
Jun

### sz...@gmail.com (2023-01-13)

FYI - Mitre assigned CVE-2023-23559 for this issue.

### sz...@gmail.com (2023-01-16)

Hello Jorge,

May I ask you to please evaluate this issue against the Chrome Vulnerability Reward Program?

Best regards,
Szymon

### ku...@google.com (2023-01-19)

Assigning it to Jorge for https://crbug.com/chromium/1400589#c17 and wifi team will continue to own b/262448137

### sz...@gmail.com (2023-01-26)

Hello,

Could you please let me know how can I get in touch with Jorge or someone else from his team handling this issue?

Best regards,
Szymon

### sz...@gmail.com (2023-02-01)

Hello,

Can you please let me know what is the current status of this issue?
Since the patch was already merged can you please mark the case as fixed so it will be reviewed by the reward panel?

Best regards,
Szymon

### am...@chromium.org (2023-02-01)

Hi Szymon, thank you for reaching out. Based on the internal bug the ChromeOS work is being performed in, the fix patch has been reverted and work on this issue is still in progress. 
I've reached out to the ChromeOS security folks, some of whom are on this bug, and asked them to keep you updated on the progress. 
Once this issue is resolved and both the internal and this bug are closed as Fixed, this issue will be evaluated by the Chrome VRP for a potential reward. 
Thank you for your patience while the ChromeOS team works to fully resolve this issue. 

### sz...@gmail.com (2023-02-01)

Hello Amy,

Thank you very much for the information, your help is invaluable.

Best regards,
Szymon

### sz...@gmail.com (2023-02-01)

Since you mentioned that "the fix patch has been reverted and work on this issue is still in progress" I would like to ask if by "fix patch" you mean the first one by Kevin Lund (https://chromium.googlesource.com/chromiumos/third_party/kernel/+/e3b303e4aa88c6cf9e6df08276b877c5271192f7) disabling CONFIG_USB_NET_RNDIS_WLAN or my patch in the upstream Linux kernel? In latter case have you observed any issues with the patch that were not considered during the code review by involved peers? 

Best regards,
Szymon

### ro...@google.com (2023-02-02)

[Empty comment from Monorail migration]

### ro...@google.com (2023-02-02)

Hi Szymon, the issue was with the config change - it broke Android tethering and we had to revert that. AFAIK no issues with the kernel patch but @zwisler@google.com to keep me straight.

Also I understand you had reached out to Jorge and had not heard back. Apologies for that - he's on paternity leave. Please feel free to reach out on the bug or directly any time!

### ju...@google.com (2023-02-02)

Hi Szymon,

The temporary mitigation as referred by "fix patch has been reverted and work on this issue is still in progress" was reverted in ChromeOS Tip-of-Tree code base in order to bring back rndis_wlan driver, because your security fixes have landed in ChromeOS codebase and incoming releases and refreshes. Your patch has already been applied and will be incorporated going forward.

This issue will be closed once Google's internal bug is closed and evaluated.

Thank you for your patiences.


### zw...@google.com (2023-02-02)

https://crbug.com/chromium/1400589#c26 is the currents state of things, as I understand them.  We have applied your security fix to all relevant ChromeOS kernels, and have observed no regressions or issues with it.  Thank you for the fix!

### sz...@gmail.com (2023-02-03)

Hello,

Great, thank you very much.

Best regards,
Szymon

### ch...@google.com (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations Szymon! The VRP Panel has decided to award you $20,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### sz...@gmail.com (2023-02-17)

Hello Amy,

Thank you very much for this splendid news and your priceless help.
Wish you a great weekend.

Best regards,
Szymon

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1400589?no_tracker_redirect=1

[Monorail blocked-on: b/262448137]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062211)*
