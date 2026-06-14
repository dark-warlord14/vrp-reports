# Stack-buffer-overflow in content::webcrypto::platform::CreatePublicKeyAlgorithm

| Field | Value |
|-------|-------|
| **Issue ID** | [40079993](https://issues.chromium.org/issues/40079993) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebCrypto |
| **Reporter** | [Deleted User] |
| **Assignee** | er...@chromium.org |
| **Created** | 2014-07-05 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0

Steps to reproduce the problem:
Load the provided test-case into Chromium.

What is the expected behavior?

What went wrong?
Sanitizing the parameters of generateKey()

Did this work before? N/A 

Chrome version: 38.0.2084.0  Channel: dev
OS Version: OS X 10.9
Flash Version: Shockwave Flash 14.0 r0

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 255 B)
- [callstack.txt](attachments/callstack.txt) (text/plain, 12.6 KB)

## Timeline

### cl...@chromium.org (2014-07-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-06)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6306487787847680

### cl...@chromium.org (2014-07-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5631095154409472

### fe...@chromium.org (2014-07-07)

I can't replicate this with a linux asan build, but eroman@, can seem to have written this code. Can you take a look at it?

### fe...@chromium.org (2014-07-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-07)

Did you use any special ASAN_OPTIONS on mac ? It does not reproduce on CF on mac. Glider@, Rsesek@, do you have ASAN build to manually verify ?

### rs...@chromium.org (2014-07-07)

You need to run with export ASAN_OPTIONS="strict_memcmp=0 replace_intrin=0" on Mac. I was able to repro on trunk at r281560.

### cl...@chromium.org (2014-07-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5675399352680448

### in...@chromium.org (2014-07-07)

My bad, both the uploads in c#2, c#3 were on linux. Just reuploaded on mac. And yes, we already use strict_memcmp=0 replace_intrin=0 as otherwise it causes startup crashes.

### in...@chromium.org (2014-07-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5675399352680448

Uploader: aarya@google.com
Job Type: Mac_asan_chrome

Crash Type: Stack-buffer-overflow READ 4
Crash Address: 0xb21d4334
Crash State:
  - crash stack -
  content::webcrypto::platform::CreatePublicKeyAlgorithm
  content::webcrypto::platform::GenerateRsaKeyPair
  content::webcrypto::GenerateKeyPair
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=278311:278526

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95d91A4-dqo4Z-WvCSdQwOfirQlDWC4qclhOnIGIH9IeY44Eqa8uDqSDI2hRvoroXNf9m1Dv5iwat1TBezmrRI0Sq2b87z3O5XX36fQYyU0Kpe8zXkWZ-qgmW_OLTrAanQxNxaqbVmYCYiXMAbc4wdESzlXRQ



### er...@chromium.org (2014-07-07)

The bug is in the error checking here:

  SECKEYPublicKey* sec_public_key;
  crypto::ScopedSECKEYPrivateKey scoped_sec_private_key(
      PK11_GenerateKeyPairWithOpFlags(slot.get(),
                                      CKM_RSA_PKCS_KEY_PAIR_GEN,
                                      &rsa_gen_params,
                                      &sec_public_key,
                                      attribute_flags,
                                      operation_flags,
                                      operation_flags_mask,
                                      NULL));
  if (!private_key)  <-------- WRONG VARIABLE
    return Status::OperationError();

It should be testing |scoped_sec_private_key| for nullity, not |private_key|.

The consequence is that the code will later try to read from |sec_public_key|, which is uninitialized.


### er...@chromium.org (2014-07-07)

This is not Mac specific, I can get it to reproduce on Linux too.

### er...@chromium.org (2014-07-08)

Bug history:

(1) Introduced in r232598 (https://codereview.chromium.org/34583010) 8 months ago.
(2) Bug became reachable in M37 once webcrypto was enabled by default (https://codereview.chromium.org/336693003)

### fe...@chromium.org (2014-07-08)

What process is webcrypto running in?

### fe...@chromium.org (2014-07-08)

[Empty comment from Monorail migration]

### er...@chromium.org (2014-07-08)

@felt: Renderer process

### fe...@chromium.org (2014-07-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3e0ce255ba1f92911e934587d4858a5bc2cfcdd

commit e3e0ce255ba1f92911e934587d4858a5bc2cfcdd
Author: eroman@chromium.org <eroman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue Jul 08 04:12:00 2014

[webcrypto] Fix a crash when RSA key generation fails.
BUG=391570
NOTRY=true

Review URL: https://codereview.chromium.org/374743002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@281655 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-08)

------------------------------------------------------------------
r281655 | eroman@chromium.org | 2014-07-08T04:12:00.568116Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/webcrypto/shared_crypto_unittest.cc?r1=281655&r2=281654&pathrev=281655
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/webcrypto/platform_crypto_nss.cc?r1=281655&r2=281654&pathrev=281655

[webcrypto] Fix a crash when RSA key generation fails.
BUG=391570
NOTRY=true

Review URL: https://codereview.chromium.org/374743002
-----------------------------------------------------------------

### in...@chromium.org (2014-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-08)

ClusterFuzz has detected this issue as fixed in range 281528:281665.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5675399352680448

Uploader: aarya@google.com
Job Type: Mac_asan_chrome

Crash Type: Stack-buffer-overflow READ 4
Crash Address: 0xb21d4334
Crash State:
  - crash stack -
  content::webcrypto::platform::CreatePublicKeyAlgorithm
  content::webcrypto::platform::GenerateRsaKeyPair
  content::webcrypto::GenerateKeyPair
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=278311:278526
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=281528:281665

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95d91A4-dqo4Z-WvCSdQwOfirQlDWC4qclhOnIGIH9IeY44Eqa8uDqSDI2hRvoroXNf9m1Dv5iwat1TBezmrRI0Sq2b87z3O5XX36fQYyU0Kpe8zXkWZ-qgmW_OLTrAanQxNxaqbVmYCYiXMAbc4wdESzlXRQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### er...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-07-15)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-07-15)

------------------------------------------------------------------
r283242 | eroman@chromium.org | 2014-07-15T19:54:27.848245Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/child/webcrypto/shared_crypto_unittest.cc?r1=283242&r2=283241&pathrev=283242
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/child/webcrypto/platform_crypto_nss.cc?r1=283242&r2=283241&pathrev=283242

Merge 281655 "[webcrypto] Fix a crash when RSA key generation fa..."

> [webcrypto] Fix a crash when RSA key generation fails.
> BUG=391570
> NOTRY=true
> 
> Review URL: https://codereview.chromium.org/374743002

TBR=eroman@chromium.org

Review URL: https://codereview.chromium.org/397783002
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d1fda106c4d6df1a22369101736a8d10915950c6

commit d1fda106c4d6df1a22369101736a8d10915950c6
Author: eroman@chromium.org <eroman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue Jul 15 19:54:27 2014

Merge 281655 "[webcrypto] Fix a crash when RSA key generation fa..."

> [webcrypto] Fix a crash when RSA key generation fails.
> BUG=391570
> NOTRY=true
> 
> Review URL: https://codereview.chromium.org/374743002

TBR=eroman@chromium.org

Review URL: https://codereview.chromium.org/397783002

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@283242 0039d316-1c4b-4281-b951-d872f2087c98



### [Deleted User] (2014-07-16)

Does this bug qualify for a bounty at Google?

### in...@chromium.org (2014-07-16)

Yes it does. We have reward-topanel label on this, so it will eventually go to the panel for reward discussion. This is currently rated medium severity, if you have additional thoughts on exploitability, this will qualify for higher rewards. [see http://googleonlinesecurity.blogspot.com/2013/08/security-rewards-at-google-two.html]

### [Deleted User] (2014-08-11)

inferno, any updates on this issue?

### in...@chromium.org (2014-08-11)

Hi @cdiehl.private, the rewards discussion stuff happens around the milestone/patch cycles when a fix is getting released. This one is planned for m37, so i estimate atleast 2 weeks later. Thanks for checking, this cannot fall off our radar since the magic 'reward-topanel' label is there.

### mb...@chromium.org (2014-08-22)

Thanks for the report! This qualifies for a $1000 reward. Someone should be reaching out to you soon with additional details.

How would you like to be credited when we mention this bug in our release notes?

### [Deleted User] (2014-08-22)

Thank you.
Christoph Diehl as credit is fine.

### [Deleted User] (2014-09-10)

ping

### ti...@chromium.org (2014-09-18)

Hey Christoph,

Someone from our finance team should be in touch next week to collect payment details. Please let me know if you haven't heard from them by next week by either updating the bug or contacting me directly. 

Congrats on the reward!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************



### [Deleted User] (2014-09-30)

ping

### [Deleted User] (2014-09-30)

Does this quote have any effect on this bug?

"As a special treat, we’re going to back-pay valid submissions from July 1, 2014 at the increased reward levels we’re announcing today. Good times." -- http://googleonlinesecurity.blogspot.de/2014/09/fewer-bugs-mo-money.html

### in...@chromium.org (2014-09-30)

yes it will. Tim should contact you soon.

### ti...@chromium.org (2014-09-30)

re c#37

It certainly does! We have to review all of the reports from 1 July and determine their value under the new system, so bear with us while we do that.

Did you get the email from the finance team today? They told me that they sent it today, so if you don't have it, let me know ASAP so I can personally chase. 

### [Deleted User] (2014-09-30)

No, did not receive any mail.

### ti...@google.com (2014-10-01)

Thanks for letting me know. Figured out what happened - I'll send you an email.

### cl...@chromium.org (2014-10-14)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-10-21)

Processing via our e-payment system can take up to a month, but reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/391570?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079993)*
