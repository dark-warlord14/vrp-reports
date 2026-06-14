# [HIGH] nameConstraints: excluded dNSName can be bypassed with wildcard SAN

| Field | Value |
|-------|-------|
| **Issue ID** | [487821920](https://issues.chromium.org/issues/487821920) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | BoringSSL |
| **Reporter** | ko...@gmail.com |
| **Assignee** | rp...@google.com |
| **Created** | 2026-02-26 |
| **Bounty** | $2,000.00 |

## Description

**Summary:** [HIGH] nameConstraints: excluded dNSName can be bypassed with wildcard SAN

**Program:** OSS VRP

**URL:** <https://github.com/google/boringssl>

**Vulnerability type:** Other

### Details

# summary

legacy `crypto/x509` nameConstraints enforcement can be bypassed for excluded `dNSName` subtrees when the leaf certificate uses a wildcard SAN. specifically, an excluded subtree like `foo.bar.com` does not match a leaf `subjectAltName:dNSName=*.bar.com`, so `X509_verify_cert` can incorrectly accept a chain that should be rejected.

this can matter in deployments that use constrained intermediate CAs with excluded subtrees as a hard policy boundary (for example, to prevent issuance for specific subdomains).

# severity

high.

justification: this is a certificate validation bypass in `X509_verify_cert` (CWE-295) which can enable impersonation/mitm within excluded subdomains, but it requires a constrained intermediate CA scenario and is topology-dependent (nameConstraints must be deployed and relied upon as a security boundary).

# affected version

- repository: <https://github.com/google/boringssl>
- commit: cb3b2fda3d434544085f4f32400ca2ba5c2877b8
- file: `crypto/x509/v3_ncons.cc` (`nc_dns`, around line 373)

# affected code (pinned)

- legacy nameConstraints dns matching (`nc_dns`):
  - [https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/v3\\_ncons.cc#L373](https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/v3%5C_ncons.cc#L373)
- legacy verifier applies nameConstraints during chain validation:
  - [https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/x509\\_vfy.cc#L546](https://github.com/google/boringssl/blob/cb3b2fda3d434544085f4f32400ca2ba5c2877b8/crypto/x509/x509%5C_vfy.cc#L546)

# details

## root cause

`nc_dns` treats wildcard dns names as literal strings when matching against excluded subtrees. because of that, `*.bar.com` does not match an excluded subtree constraint `foo.bar.com`, even though wildcard expansion can cover `foo.bar.com`.

the `pki/` nameConstraints implementation already accounts for wildcard behavior (via a wildcard partial match mode), which makes this discrepancy more visible.

## attack vector

precondition: a constrained intermediate CA exists with an excluded `dNSName` subtree `foo.bar.com`, and an attacker can obtain issuance from (or compromise) that constrained intermediate.

attacker action: issue a leaf certificate with `subjectAltName:dNSName=*.bar.com` under the constrained intermediate, and present the chain to a relying party that uses `X509_verify_cert` and relies on excluded subtrees for containment.

result: verification succeeds when it should fail due to an excluded subtree violation.

# PoC

attached: `poc.zip`

## steps to reproduce

```
cmake -GNinja -B build && ninja -C build
rm -rf poc
unzip poc.zip -d poc
cd poc
make canonical HOST=foo.bar.com

```

expected output contains:

```
verify_ok=0 verify_err=48 (excluded subtree violation)

```

actual output:

```
[CALLSITE_HIT] crypto/x509/v3_ncons.cc:373 nc_dns (via X509_verify_cert -> check_name_constraints -> NAME_CONSTRAINTS_check)
verify_ok=1 verify_err=0 (ok)
[PROOF_MARKER] excluded dNSName constraint did not block a wildcard SAN that expands into excluded space

```
## negative control (same env, no vuln trigger)

```
rm -rf poc
unzip poc.zip -d poc
cd poc
make control HOST=foo.bar.com

```

output:

```
[CALLSITE_HIT] crypto/x509/v3_ncons.cc:373 nc_dns (via X509_verify_cert -> check_name_constraints -> NAME_CONSTRAINTS_check)
verify_ok=0 verify_err=48 (excluded subtree violation)
[NC_MARKER] explicit banned dNSName correctly rejected by excluded subtree

```
# impact

policy bypass: excluded `dNSName` constraints do not prevent wildcard certificates that can cover excluded subdomains. in relying parties that treat nameConstraints as a strict security boundary, this can enable impersonation/mitm against hosts in the excluded subtree.

# remediation

make excluded `dNSName` constraint matching wildcard-aware in the legacy `crypto/x509` stack. one concrete acceptance criterion is that `*.bar.com` should be treated as matching excluded `foo.bar.com` (since wildcard expansion can cover the excluded space), and the PoC above should fail with `verify_err=48 (excluded subtree violation)`.

### Attack scenario

excluded dNSName constraints can be bypassed using wildcard SANs that expand into excluded space, allowing a constrained sub-ca to issue certificates for excluded subdomains.

credit: 1seal (<https://github.com/1seal>)

## Attachments

- [attack_scenario.md](attachments/attack_scenario.md) (text/markdown, 2.0 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 21.5 KB)
- [PR_DESCRIPTION.md](attachments/PR_DESCRIPTION.md) (text/markdown, 395 B)

## Timeline

### sp...@google.com (2026-02-26)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Hey! Our automation saw that your report contained a link to github.com! Did you know that you can get rewarded for patching vulnerabilities? See our [Patch Rewards Program](https://bughunters.google.com/about/rules/4928084514701312/patch-rewards-program-rules) for more information!

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### sp...@google.com (2026-02-26)

*NOTE: This is an automatically generated email*

Hey,

We just want to let you know that your report was **triaged** and we're currently looking into it.

You should receive further information in a couple of days, but it might take up to a week if we're particularly busy. In the meantime, you might want to take a look at [the list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Thanks,   

Google Security Bot

### jk...@google.com (2026-03-06)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### me...@google.com (2026-03-06)

chlily@: Another one, thanks!

### ch...@chromium.org (2026-03-06)

This was already patched in boringssl-review.googlesource.com/c/boringssl/+/90167.

### ch...@chromium.org (2026-03-06)

Btw this is similar to <https://github.com/golang/go/issues/76442> which addressed a similar bug in the Go implementation.

### ko...@gmail.com (2026-04-22)

hi, checking in on [issue 487821920](https://issues.chromium.org/issues/487821920).

the bug was marked fixed on march 6, 2026 and has the reward-topanel label, so i wanted to ask whether the VRP panel review is still pending, or if you need any additional information from me.

Oleh

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Low impact mitigation bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487821920)*
