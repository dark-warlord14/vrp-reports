# Security: Overflow in compareUTF32Strings()

| Field | Value |
|-------|-------|
| **Issue ID** | [40926043](https://issues.chromium.org/issues/40926043) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2023-42852 |
| **Reporter** | pe...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-08-08 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

The string below is interpreted by JavaScriptCore (JSC) as a JavaScript regular expression:

```
/[\q{|34||78}]\*/v  

```

Running this testcase with JSC under gdb results in the following backtrace:

```
[#0] 0x369832fb3ccc → mov ebp, eax  
[#1] 0x369832f64ef2 → raise()  
[#2] 0x369832f4f472 → abort()  
[#3] 0x1eb12be13eaa → WTF::CrashOnOverflow::crash()  
[#4] 0x1eb12be13ea1 → WTF::CrashOnOverflow::overflowed()  
[#5] 0x1eb12bf1d9db → WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::at(this=0x7ffe9ca17bb0, i=0xffffffffffffffff)  
[#6] 0x1eb12de12d35 → WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::operator[](this=0x7ffe9ca17bb0, i=0xffffffffffffffff)  
[#7] 0x1eb12deb9401 → JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(a=@0x7ffe9ca17bb0, b=@0x1df75c028e10)  
[#8] 0x1eb12deb9463 → JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::{lambda(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)#1}::operator()(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&) const(__closure=0x7ffe9ca17ba7, a=@0x7ffe9ca17bb0, b=@0x1df75c028e10)  
[#9] 0x1eb12dedbfd3 → gnu_cxx::ops::_Val_comp_iter<JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::{lambda(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)#1}>::operator()<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>\*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>\*)(this=0x7ffe9ca17ba7, val=@0x7ffe9ca17bb0, it=0x1df75c028e10)  

```

Th problem occurs in the function `JSC::Yarr::CharacterClassConstructor::compareUTF32Strings()`. To understand the problem, the function `JSC::Yarr::CharacterClassConstructor::sort()` is also important.  

The crash occurs when JSC tries to sort vectors.

Below is the function `JSC::Yarr::CharacterClassConstructor::sort()`:

```
static void sort(Vector<Vector<UChar32>>& utf32Strings)  
	{         
		std::sort(utf32Strings.begin(), utf32Strings.end(), [](const Vector<UChar32>& a, const Vector<UChar32>& b)   
			{  
				return compareUTF32Strings(a, b) < 0;  
			});  
	}  

```

`utf32Strings` of type `Vector<Uchar32>` is being sorted when this crash occurs.

From the lambda expression in the function, we can see that this vector stores vector pointers, as confirmed under gdb:

```
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────  
   0x1eb12deb948b <JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int,+0> call   0x1eb12cffa588 <_ZN3WTF6VectorINS0_IiLm0ENS_15CrashOnOverflowELm16ENS_10FastMallocEEELm0ES1_Lm16ES2_E5beginEv>  
   0x1eb12deb9490 <JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int,+0> mov    rsi, rbx  
   0x1eb12deb9493 <JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int,+0> mov    rdi, rax  
 → 0x1eb12deb9496 <JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int,+0> call   0x1eb12dec0b9d <_ZSt4sortIPN3WTF6VectorIiLm0ENS0_15CrashOnOverflowELm16ENS0_10FastMallocEEEZN3JSC4Yarr25CharacterClassConstructor4sortERNS1_IS4_Lm0ES2_Lm16ES3_EEEUlRKS4_SC_E_EvT_SE_T0_>  
   ↳  0x1eb12dec0b9d <void+0>         push   rbp  
	  0x1eb12dec0b9e <void+0>         mov    rbp, rsp  
	  0x1eb12dec0ba1 <void+0>         sub    rsp, 0x20  
	  0x1eb12dec0ba5 <void+0>         mov    QWORD PTR [rbp-0x8], rdi  
	  0x1eb12dec0ba9 <void+0>         mov    QWORD PTR [rbp-0x10], rsi  
	  0x1eb12dec0bad <void+0>         call   0x1eb12dec3cc0 <_ZN9gnu_cxx5ops16__iter_comp_iterIZN3JSC4Yarr25CharacterClassConstructor4sortERN3WTF6VectorINS6_IiLm0ENS5_15CrashOnOverflowELm16ENS5_10FastMallocEEELm0ES7_Lm16ES8_EEEUlRKS9_SD_E_EENS0_15_Iter_comp_iterIT_EESG_>  
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── arguments (guessed) ────  
_ZSt4sortIPN3WTF6VectorIiLm0ENS0_15CrashOnOverflowELm16ENS0_10FastMallocEEEZN3JSC4Yarr25CharacterClassConstructor4sortERNS1_IS4_Lm0ES2_Lm16ES3_EEEUlRKS4_SC_E_EvT_SE_T0_ (  
   $rdi = 0x001df75c028e00,  
   $rsi = 0x001df75c028e40,  
   $rdx = 0x001df75c028e00  
)  
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── source:../../Source/Ja[...].cpp+435 ────  
	430      }  
	431    
	432      static void sort(Vector<Vector<UChar32>>& utf32Strings)  
	433      {  
	434          std::sort(utf32Strings.begin(), utf32Strings.end(), [](const Vector<UChar32>& a, const Vector<UChar32>& b)  
 →  435              {  
	436                  return compareUTF32Strings(a, b) < 0;  
	437              });  
	438      }  
	439    
	440      std::unique_ptr<CharacterClass> charClass()  
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  
gef➤  x/10gx 0x001df75c028e00  
0x1df75c028e00: 0x0000000000000000      0x0000000000000000  
0x1df75c028e10: 0x00001df75c006c20      0x0000000200000002  
0x1df75c028e20: 0x0000000000000000      0x0000000000000000  
0x1df75c028e30: 0x00001df75c006c30      0x0000000200000002  
0x1df75c028e40: 0x0000000000000000  

```

With the GDB output we can conclude that the memory addresses of the Vector `utf32String` starts at `0x1df75c028e00` and ends at `0x1df75c028e40`.

Only 2 pointers ared stored and metadata is stored right after that, after which comes null bytes.

```
gef➤  x/2gx 0x00001df75c006c20  
0x1df75c006c20: 0x0000003400000033      0x0000000000000000  
gef➤  x/2gx 0x00001df75c006c30  
0x1df75c006c30: 0x0000003800000037      0x0000000000000000  

```

From the above we can conclude that `uft32Strings` vector stores vector pointers to the values passed in the regular expression between the "|", as well as their metadata. In this case it will be: `NULL|34|NULL|78`.

To perform the sort the size of vectors will be compared in the function `JSC::Yarr::CharacterClassConstructor::compareUTF32Strings()` in order to sort the Vector utf32Strings in descending order.

```
static ALWAYS_INLINE int compareUTF32Strings(const Vector<UChar32>& a, const Vector<UChar32>& b)   
	{  
				//[1] Longer strings before shorter.  
		if (a.size() > b.size())   
			return -1;  
  
				//[2]  
		if (a.size() < b.size())   
			return 1;  
  
				//[3] Lexically sort for same length strings.  
		for (unsigned i = 0; i < a.size(); ++i) {  
			if (a[i] < b[i])  
				return -1;  
		}  
  
				//[4]  
		return a[a.size() - 1] > b[a.size() - 1] ? 1 : 0;   
	}  

```

The problem happens when comparing the sizes of NULLs. That is, when `a.size()=0` and `b.size()=0`.

The crash occurs in [4], because:

- `a.size()` == `b.size()` so the returns in [1] nor [2] are not triggered
- `i` == `a.size()` == 0 so we never enter the for cycle in [3]
- In [4], since `a.size()` == `0`, `a[-1]` is outside the vector's memory range hence it crashes with an overflow:

We can see this in gdb:

```
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────  
   0x1eb12deb93e6 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    rdi, rax  
   0x1eb12deb93e9 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> call   0x1eb12bf0d0d4 <_ZNK3WTF6VectorIiLm0ENS_15CrashOnOverflowELm16ENS_10FastMallocEE4sizeEv>  
   0x1eb12deb93ee <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> lea    rdx, [rax-0x1] //HERE  
 → 0x1eb12deb93f2 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    rax, QWORD PTR [rbp-0x28]  
   0x1eb12deb93f6 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    rsi, rdx  
   0x1eb12deb93f9 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    rdi, rax  
   0x1eb12deb93fc <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> call   0x1eb12de12d12 <_ZNK3WTF6VectorIiLm0ENS_15CrashOnOverflowELm16ENS_10FastMallocEEixEm>  
   0x1eb12deb9401 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    ebx, DWORD PTR [rax]  
   0x1eb12deb9403 <JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int,+0> mov    rax, QWORD PTR [rbp-0x28]  
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── source:../../Source/Ja[...].cpp+430 ────  
	425          for (unsigned i = 0; i < a.size(); ++i) {  
	426              if (a[i] < b[i])  
	427                  return -1;  
	428          }  
	429          return a[a.size() - 1] > b[a.size() - 1] ? 1 : 0;  
	430      }  
	431    
	432      static void sort(Vector<Vector<UChar32>>& utf32Strings)  
	433      {  
	434          std::sort(utf32Strings.begin(), utf32Strings.end(), [](const Vector<UChar32>& a, const Vector<UChar32>& b)  
	435              {  
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  
gef➤  print $rdx  
$1 = 0xffffffffffffffff  

```

**VERSION**  

Chrome on iOS (tested latest WebKit git f818e6d361ac1db886052adeb3e2f6377513a6b0 from Aug 6)

**REPRODUCTION CASE**  

./WebKit/Tools/Scripts/run-minibrowser poc2.html

**CREDIT INFORMATION**  

Reporter credit: Reporter credit: Pedro Ribeiro (@pedrib1337) and Vitor Pedreira (@0xvhp\_) of Agile Information Security

## Attachments

- [poc2.html](attachments/poc2.html) (text/plain, 112 B)

## Timeline

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### bb...@google.com (2023-08-08)

Not a security bug as this appears to be caught as an abort.  Nevertheless a bug, Moving over to V8 sheriff. 

[Monorail components: Blink>JavaScript]

### pe...@gmail.com (2023-08-09)

Does this affect Blink? It's for Chrome on iOS? Here's another stack trace:

1   0x42b5d17e9 WTFCrash
2   0x4312c794e WTF::CrashOnOverflow::crash()
3   0x4312c792e WTF::CrashOnOverflow::overflowed()
4   0x4314a0cad WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::at(unsigned long) const
5   0x432e34e8d WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::operator[](unsigned long) const
6   0x43303d9ee JSC::Yarr::CharacterClassConstructor::compareUTF32Strings(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)
7   0x43303bef1 JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)::operator()(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&) const
8   0x43303cb20 unsigned int std::__1::__sort3<std::__1::_ClassicAlgPolicy, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&)
9   0x43303de14 unsigned int std::__1::__sort4<std::__1::_ClassicAlgPolicy, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&)
10  0x43303c015 std::__1::enable_if<!__use_branchless_sort<JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>::value, void>::type std::__1::__sort4_maybe_branchless[abi:v15006]<std::__1::_ClassicAlgPolicy, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&)
11  0x43303a37c void std::__1::__introsort<std::__1::_ClassicAlgPolicy, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, std::__1::iterator_traits<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>::difference_type)
12  0x433039e22 void std::__1::__sort<JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&)
13  0x433039db7 void std::__1::__sort_impl[abi:v15006]<std::__1::_ClassicAlgPolicy, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)&)
14  0x433039cf0 void std::__1::sort[abi:v15006]<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&)>(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>*, JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)::'lambda'(WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&, WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc> const&))
15  0x4330391fe JSC::Yarr::CharacterClassConstructor::sort(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)
16  0x43304db56 JSC::Yarr::CharacterClassConstructor::atomClassStringDisjunction(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)
17  0x43304d971 JSC::Yarr::YarrPatternConstructor::atomClassStringDisjunction(WTF::Vector<WTF::Vector<int, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&)
18  0x43304d2f2 JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::ClassStringDisjunctionParserDelegate::end()
19  0x433048d5f JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parseClassStringDisjunction(bool&)
20  0x43304613e JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::TokenType JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parseEscape<(JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::ParseEscapeMode)2, JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::ClassSetParserDelegate>(JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::ClassSetParserDelegate&)
21  0x43302c93d JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parseClassSetEscape(JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::ClassSetParserDelegate&)
22  0x43301a172 JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parseClassSet()
23  0x4330163bc JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parseTokens()
24  0x43301450e JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::parse()
25  0x432f121bf JSC::Yarr::ErrorCode JSC::Yarr::parse<JSC::Yarr::YarrPatternConstructor>(JSC::Yarr::YarrPatternConstructor&, WTF::StringView, JSC::Yarr::CompileMode, unsigned int, bool)
26  0x432f11c53 JSC::Yarr::YarrPattern::compile(WTF::StringView)
27  0x432f14f20 JSC::Yarr::YarrPattern::YarrPattern(WTF::StringView, WTF::OptionSet<JSC::Yarr::Flags>, JSC::Yarr::ErrorCode&)
28  0x432f15234 JSC::Yarr::YarrPattern::YarrPattern(WTF::StringView, WTF::OptionSet<JSC::Yarr::Flags>, JSC::Yarr::ErrorCode&)
29  0x431e953a9 JSC::RegExp::finishCreation(JSC::VM&)
30  0x431e95d2a JSC::RegExp::createWithoutCaching(JSC::VM&, WTF::String const&, WTF::OptionSet<JSC::Yarr::Flags>)
31  0x431eb8beb JSC::RegExpCache::lookupOrCreate(WTF::String const&, WTF::OptionSet<JSC::Yarr::Flags>)
2023-08-08 02:22:11.237 MiniBrowser[682:7113] WebContent process crashed; reloading

### cf...@google.com (2023-08-09)

Hi bbe@, this does not seem to be a V8 bug, probably something for the Chrome on iOS team. 

### bb...@google.com (2023-08-11)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Mobile>iOSWeb]

### bb...@google.com (2023-08-11)

ajuma - this looks like it's really a webkit bug - apologies I miscategorized it.  can you help me get it to the right place ?

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-08-14)

I've filed https://bugs.webkit.org/show_bug.cgi?id=260173 (as a security bug, to be cautious).

### aj...@chromium.org (2023-08-15)

[Empty comment from Monorail migration]

### pe...@gmail.com (2023-09-06)

@ajuma - do you mind adding me to the webkit bug?

### aj...@chromium.org (2023-09-06)

Sure, added you to the bug.

### pe...@gmail.com (2023-11-23)

Turns out it was a security bug indeed, it got assigned a CVE... but Apple credited us as an anonymous researcher? Why? 

It got assigned CVE-2023-42852 by Apple:
https://seclists.org/fulldisclosure/2023/Oct/19

WebKit
Available for: iPhone XS and later, iPad Pro 12.9-inch 2nd generation
and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and
later, iPad Air 3rd generation and later, iPad 6th generation and later,
and iPad mini 5th generation and later
Impact: Processing web content may lead to arbitrary code execution
Description: A logic issue was addressed with improved checks.
WebKit Bugzilla: 260173
CVE-2023-42852: an anonymous researcher

Note the same bug number, but credited to anonymous?

### aj...@chromium.org (2023-11-23)

Thanks for the update! Marking fixed based on that.

amyressler@, based on Apple's assessment, do we need to recategorize this as a security bug?

### aj...@chromium.org (2023-11-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-23)

Thanks for the tag -- yep, converting to security bug now. 

### am...@chromium.org (2023-11-23)

setting as sev-high given the potential for RCE in the renderer; SI-None since this is an external dependency in webkit, so there is no necessary backmerge mechanics 

In terms of the CVE acknowledgement as anonymous by Apple, I'm presuming this is because ajuma@ filed the issue with WebKit. 
I don't have access to radar or webkit bugzilla, but unless it was explicitly specified in 260173, they probably acted on the side of caution and didn't credit you without your consent information from you about how you'd like to be acknowledged/credited. 
I'm sure if you reach out on that issue they will correct accordingly and acknowledge you in their update information. 

### dd...@apple.com (2023-11-24)

> I'm sure if you reach out on that issue they will correct accordingly and acknowledge you in their update information.

Yes, they reached out via the WebKit bug, and I forwarded that to Apple Product Security to make sure it’s seen.



### pe...@gmail.com (2023-11-24)

Thanks for following up with Apple, we appreciate it :-) 
It's our first publicly acknowledged bug in WebKit, so it would be painful not to get credited!

### [Deleted User] (2023-11-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-27)

Thanks so much for forwarding that along to the Apple team ddkilzer@! We additionally appreciate it so these folks can get public credit and acknowledgement. :) 

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations Pedro and Vitor! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process. A p2p-vrp representative of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue in WebKit impacting Chrome on iOS to us -- nice work! 

### pe...@gmail.com (2023-11-30)

Hi Amy, fantastic, thank you very much, we're really excited about it!

We will be continuining our work.

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-30)

This issue was migrated from crbug.com/chromium/1471025?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@gmail.com (2024-12-27)

Hi,

Are you OK with us disclosing details about this bug publicly? I noticed the visibility of this issue is still restricted.

### dd...@apple.com (2024-12-27)

Per the Buzilla bug, this landed in open source WebKit at this commit: <https://commits.webkit.org/270215@main>

### am...@chromium.org (2024-12-27)

Because this was submitted as a type=bug report then converted to limited visibility (by the reporter on 8 August 2023) before the report was converted to type=vulnerability, the default automated restrictions and lifting of them were not able to be applied on this issue and it remained restricted to Googlers. This issue has been resolved in webkit for sometime so I've opened it to public visibility.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40926043)*
