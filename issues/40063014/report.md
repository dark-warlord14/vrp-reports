# LZ and ZST files which are another form of Archive file is missing into the gesture file types

| Field | Value |
|-------|-------|
| **Issue ID** | [40063014](https://issues.chromium.org/issues/40063014) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | sm...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-02-10 |
| **Bounty** | $500.00 |

## Description

**Steps to reproduce the problem:**  

For LZ archive file:

1. Take any dangerous extension file and add this into archive and give this file any archive name. Suppose "test.lz"
2. You can open this file by direct clicking or extract by 7-zip or WinRAR.
3. In chromium Gesture file list it is not included.

For ZST archive file:

1. Take any dangerous extension file and add this into archive and give this file any archive name. Suppose "test.zst"
2. You can open this file by direct clicking or extract by 7-zip or WinRAR.
3. In chromium Gesture file list it is not included.

**Problem Description:**  

According to the chromium file types policy documentation (<https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/core/resources/download_file_types.asciipb;drc=af17ad3f07c1d8a24381eb7669bec0c2ffb86521>), there are several archive files listed as gesture file types. But, LZ (LZ77 or LZSS which is a classic lossless compression algorithm) and ZST (lossless compression algorithm, especially used for games) extensions which are also archive files are missing into chromium gesture file list. These two archive can contain dangerous files.

**Additional Comments:**  

My report and POC is only focused on that .lz and .zst files which are gesture files and another form of archive files, are missing into chromium gesture file list. I am not talking about SafeBrowsing how it considers these files, though, YES it inspects these files, but maybe SafeBrowsing verdict will be UNKNOWN, or SAFE (in my POC case)

\*\*Chrome version: \*\* 110.0.5481.78 (Official Build) (64-bit) \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [lz and zst gesture.mp4](attachments/lz and zst gesture.mp4) (video/mp4, 5.8 MB)

## Timeline

### [Deleted User] (2023-02-10)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-11)

Assigning to drubery@, because it looks similar to 1414812.

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-13)

> Assigning to drubery@, because it looks similar to 1414812.

I meant 1413029

### th...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### sm...@gmail.com (2023-02-13)

yes, but REV extension belongs to WinRAR, which is a recovery archive format, but LZ and ZST both are archive format in different compression methods.

### sm...@gmail.com (2023-03-02)

Is there any update?  Drubery@

### is...@google.com (2023-03-02)

This issue was migrated from crbug.com/chromium/1414812?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### dr...@chromium.org (2024-06-06)

.LZ does not seem to associate with 7-zip, but .ZST does. I'll add .ZST to our policy.

### dr...@chromium.org (2024-07-03)

Gitwatcher failed, but <https://crrev.com/c/5605695> fixed this.

### sm...@gmail.com (2024-07-13)

Will the fixed issue appear for a decision at the VRP panel?

### am...@chromium.org (2024-07-15)

yes, we will review this at a future VRP panel session. Since this is a low severity issue, there may be some delay before we get to review in order to make a decision.

### pg...@google.com (2024-07-22)

Hello, reporter! How would you like to be credited for the report?

### sm...@gmail.com (2024-07-24)

Want to credit as: Sazzad Mahmud Tomal

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
$500 reward for report of low impact issue 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Thank you for the report. Given the lower impact and low potential for user harm, the Chrome VRP has decided to award you a thank you reward of $500 since we were able to make a change based on your report.

### pe...@google.com (2024-10-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063014)*
