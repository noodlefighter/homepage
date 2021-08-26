date: 2021-05-27
tags: 

- 嵌入式软件

---

当前MCU上与外部交互的应用层协议，一般都是开发者手动编、解的简单二进制协议；用到序列化格式来做协议的需求，是IoT快速发展后才开始的，比如一些设备会用到JSON。

手头维护的硬件产品，应用协议已经很复杂了，一个二进制协议，实现、写文档都是麻烦事。所以我一直在探索一个快速、适合嵌入式应用的序列化格式方案，试图减轻开发负担。

Cap'n Proto是种快速数据交换格式，目标是数据快速交换、做RPC，由于它的格式在内存中能直接读、写，省略了编、解码的开销，所以相比google的protobuf快。c-capnproto是它在C中的实现。

这篇文章的目标是：研究c-capnproto的基本用法、评估将它用于嵌入式环境的可能性。

<!--more-->

## 什么是cap'n proto

[它的首页](https://capnproto.org)上已经说得很清楚了，翻译一段：

> Cap’n Proto是一种快速的数据交换格式、基于功能（译注：原文capability-based，指各组件专注于单一功能的架构设计）的RPC系统。 它就像JSON，但并不是二进制的，或者说像protobuf，但速度更快。实际上，在基准测试中，Cap’n Proto比协议缓冲区的无限时间快。
>
> 当然，这个基准测试是不公平的。它只会测量在内存中对消息进行编码和解码的时间，由于没有编码/解码步骤，因此Cap'n Proto得分很高。 Cap’n Proto编码既适合作为数据交换格式，又适合作为内存表示形式，因此一旦在内存里构建了结构，就可以直接将数据直接写到磁盘上！

- 不像JSON一样用字符串自解释，而是像protobuf一样用一张额外的“表”（就是.capnp文件）来表示数据中每段内容的意义
- 储存结构像C中的结构体在内存中的样子，但它又是平台无关的，同时支持“pack”功能在传输的时候简单压缩以节省带宽

## c-capnproto

[c-capnproto项目](https://github.com/opensourcerouting/c-capnproto)是Cap'n Proto的C实现，它包括c库和capnp文件翻译器。

用户的程序在运行期间不解析.capnp文件，而是编译前先把.capnp文件翻译成对应C源文件，通过生成的函数、结构体对数据进行操作。比如官方例子 `addressbook.capnp`：

```c
struct Person {
  id @0 :UInt32;
  name @1 :Text;
  email @2 :Text;
  phones @3 :List(PhoneNumber);

  struct PhoneNumber {
    number @0 :Text;
    type @1 :Type;

    enum Type {
      mobile @0;
      home @1;
      work @2;
    }
  }
  ...略
}c
```

生成出来的`addressbook.capnp.c`中，对于Person能看到对应操作函数：

```c
Person_ptr new_Person(struct capn_segment*);
void read_Person(struct Person*, Person_ptr);
void write_Person(const struct Person*, Person_ptr);
void get_Person(struct Person*, Person_list, int i);
void set_Person(const struct Person*, Person_list, int i);

uint32_t Person_get_id(Person_ptr p);
capn_text Person_get_name(Person_ptr p);
capn_text Person_get_email(Person_ptr p);
Person_PhoneNumber_list Person_get_phones(Person_ptr p);
void Person_set_id(Person_ptr p, uint32_t id);
void Person_set_name(Person_ptr p, capn_text name);
void Person_set_email(Person_ptr p, capn_text email);
void Person_set_phones(Person_ptr p, Person_PhoneNumber_list phones);
```

这些函数要怎么用呢，例子`example-test.cpp`，将Person数据序列化，再反序列化：

```c
TEST(Examples, RoundTripPerson) {
  uint8_t buf[4096];
  ssize_t sz = 0; // size
  const char *name = "Firstname Lastname";
  const char *email = "username@domain.com";
  const char *school = "of life";

  {
    struct capn c;
    capn_init_malloc(&c);
    capn_ptr cr = capn_root(&c);
    struct capn_segment *cs = cr.seg;

    // Set initial object in `p`.
    struct Person p = {
      .id = 17,
      .name = chars_to_text(name),
      .email = chars_to_text(email),
    };
    p.employment_which = Person_employment_school;
    p.employment.school = chars_to_text(school);

    p.phones = new_Person_PhoneNumber_list(cs, 2);
    struct Person_PhoneNumber pn0 = {
      .number = chars_to_text("123"),
      .type = Person_PhoneNumber_Type_work,
    };
    set_Person_PhoneNumber(&pn0, p.phones, 0);
    struct Person_PhoneNumber pn1 = {
      .number = chars_to_text("234"),
      .type = Person_PhoneNumber_Type_home,
    };
    set_Person_PhoneNumber(&pn1, p.phones, 1);

    Person_ptr pp = new_Person(cs);
    write_Person(&p, pp);
    int setp_ret = capn_setp(capn_root(&c), 0, pp.p);
    ASSERT_EQ(0, setp_ret);
    sz = capn_write_mem(&c, buf, sizeof(buf), 0 /* packed */);
    capn_free(&c);
  }

  {
    // Deserialize `buf[0..sz-1]` to `rp`.
    struct capn rc;
    int init_mem_ret = capn_init_mem(&rc, buf, sz, 0 /* packed */);
    ASSERT_EQ(0, init_mem_ret);
    Person_ptr rroot;
    struct Person rp;
    rroot.p = capn_getp(capn_root(&rc), 0 /* off */, 1 /* resolve */);
    read_Person(&rp, rroot);

    // Assert deserialized values in `rp`
    EXPECT_EQ(rp.id, (uint32_t) 17);
    EXPECT_CAPN_TEXT_EQ(name, rp.name);
    EXPECT_CAPN_TEXT_EQ(email, rp.email);

    EXPECT_EQ(rp.employment_which, Person_employment_school);
    EXPECT_CAPN_TEXT_EQ(school, rp.employment.school);

    EXPECT_EQ(2, capn_len(rp.phones));

    struct Person_PhoneNumber rpn0;
    get_Person_PhoneNumber(&rpn0, rp.phones, 0);
    EXPECT_CAPN_TEXT_EQ("123", rpn0.number);
    EXPECT_EQ(rpn0.type, Person_PhoneNumber_Type_work);

    struct Person_PhoneNumber rpn1;
    get_Person_PhoneNumber(&rpn1, rp.phones, 1);
    EXPECT_CAPN_TEXT_EQ("234", rpn1.number);
    EXPECT_EQ(rpn1.type, Person_PhoneNumber_Type_home);

    capn_free(&rc);
  }
}
```

读例子可了解到的信息：

- 在这个实现中，数据段都是通过`capn_ptr`来引用的，比如`Person_ptr`本质就是`capn_ptr`
- `read_Person()`这类函数可以把数据读到结构体中；而`write_Person()`这类函数可以把结构体数据写到数据段中



<details>
  <summary>★这里偷偷折叠了一堆解析源码的凌乱废话笔记，别展开★</summary>
看了它的例子还是没搞懂？那就对了，我也一样

看不清行为就没法往下评估，这货根本没写文档，只能自己读代码了

这些函数和结构体做了什么？

```
capn_init_malloc()
capn_setp()
capn_ptr类型？
struct capn_segment类型？
```

带着问题，去看这个库的实现...

`sttruct capn`：

```c
/* struct capn is a common structure shared between segments in the same
 * session/context so that far pointers between segments will be created.
 *
 * lookup is used to lookup segments by id when derefencing a far pointer
 *
 * create is used to create or lookup an alternate segment that has at least
 * sz available (ie returned seg->len + sz <= seg->cap)
 *
 * create_local is used to create a segment for the copy tree and should be
 * allocated in the local memory space.
 *
 * Allocated segments must be zero initialized.
 *
 * create and lookup can be NULL if you don't need multiple segments and don't
 * want to support copying
 *
 * seglist and copylist are linked lists which can be used to free up segments
 * on cleanup, but should not be modified by the user.
 *
 * lookup, create, create_local, and user can be set by the user. Other values
 * should be zero initialized.
 */
struct capn {
	/* user settable */
	struct capn_segment *(*lookup)(void* /*user*/, uint32_t /*id */);
	struct capn_segment *(*create)(void* /*user*/, uint32_t /*id */, int /*sz*/);
	struct capn_segment *(*create_local)(void* /*user*/, int /*sz*/);
	void *user;
	/* zero initialized, user should not modify */
	uint32_t segnum;
	struct capn_tree *copy;
	struct capn_tree *segtree;
	struct capn_segment *seglist, *lastseg;
	struct capn_segment *copylist;
};
```

这个capn结构体，可以理解为capn库的共享数据，在多线程环境中为了避免同步操作，所以推荐插在上下文（context）中。

`struct capn_segment`：

```c
/* struct capn_segment contains the information about a single segment.
 *
 * capn points to a struct capn that is shared between segments in the
 * same session
 *
 * id specifies the segment id, used for far pointers
 *
 * data specifies the segment data. This should not move after creation.
 *
 * len specifies the current segment length. This is 0 for a blank
 * segment.
 *
 * cap specifies the segment capacity.
 *
 * When creating new structures len will be incremented until it reaches cap,
 * at which point a new segment will be requested via capn->create. The
 * create callback can either create a new segment or expand an existing
 * one by incrementing cap and returning the expanded segment.
 *
 * data, len, and cap must all be 8 byte aligned, hence the ALIGNED_(8) macro
 * on the struct definition.
 *
 * data, len, cap, and user should all be set by the user. Other values
 * should be zero initialized.
 */
truct ALIGNED_(8) capn_segment {
	struct capn_tree hdr;
	struct capn_segment *next;
	struct capn *capn;
	uint32_t id;
	/* user settable */
	char *data;
	size_t len, cap;
	void *user;
};
```

翻译：
>
>struct capn_segment包含单个segment的信息。
>
>- capn：指向在同session中，可以被多个segment共用的capn结构体
>- id：指定segment id，用作far pointer
>- data：指定细分数据。 创建后不应移动。
>- len：指定当前段的长度。 对于空白段，该值为0。
>- cap：指定e容量
>
>在创建新结构体时，len将递增，直到达到cap，这时将通过`capn->create()`请求一个新的段。create回调既可以创建新的细分，也可以通过增加上限并返回扩展的细分来扩展现有细分。
>
>data、len、cap必须全部对齐8个字节，所以使用了ALIGNED_（8）宏。data, len, cap, and user应由用户设置，其他值将初始化为零。

`capn_root()`做了什么？

```
capn_ptr capn_root(struct capn *c) {
	capn_ptr r = {CAPN_PTR_LIST};
	r.seg = lookup_segment(c, NULL, 0);
	r.data = r.seg ? r.seg->data : new_data(c, 8, &r.seg);
	r.len = 1;
	...
}
```

在指定的capn中，找一个id为0的segment，若不存在则创建

`capn_setp`：

```
/* capn_getp|setp functions get/set ptrs in list/structs
 * off is the list index or pointer index in a struct
 * capn_setp will copy the data, create far pointers, etc if the target
 * is in a different segment/context.
 * Both of these will use/return inner pointers for composite lists.
 */
capn_ptr capn_getp(capn_ptr p, int off, int resolve);
int capn_setp(capn_ptr p, int off, capn_ptr tgt);
```

> capn_getp|setp 函数 get/set 在 list/structs中的指针
>
> off是struct中指针的index，或者list中元素的index
>
> 如果target指向不同的segment/context，capn_setp()会复制数据、创建far pointers
>
> capn_getp()函数会返回list的内部指针

动态内存使用评估，`capn-malloc.c: create()`：

```
static struct capn_segment *create(void *u, uint32_t id, int sz) {
	struct capn_segment *s;
	sz += sizeof(*s);
	if (sz < 4096) {
		sz = 4096;
	} else {
		sz = (sz + 4095) & ~4095;
	}
	s = (struct capn_segment*) calloc(1, sz);
	s->data = (char*) (s+1);
	s->cap = sz - sizeof(*s);
	s->user = s;
	printf("create()\n");
	return s;
}
```

结合create函数和segment结构体的注释，可以看出：需要用到动态内存时，每次会申请4KiB内存，不够用时再次申请，这样的机制不会造成我们最担心的堆内存碎片问题；这个4096也可以简单地修改为8字节对齐的数，小内存设备也是可以用的。

</details>



## 嵌入式场景下评估

简单评估资源占用，这是我自己用来测试的工程，编码解码测试，算是比较典型的应用，源码就懒得贴了。

编译参数`-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffunction-sections -fdata-sections -Os `，用fpvgcc分析：

```
+---------------------+-----+-------+------+-------+
| FILE                | VEC |   ROM |  RAM | TOTAL |
+---------------------+-----+-------+------+-------+
| libc.a              |     | 27187 | 2544 | 29731 |
| capn.o              |     |  4374 |      |  4374 |
| libgcc.a            |     |  3088 |      |  3088 |
| capn-malloc.o       |     |   971 |      |   971 |
| capn-stream.o       |     |   758 |      |   758 |
| main.o              |     |   703 |      |   703 |
| startup_stm32f4xx.o |     |   462 |      |   462 |
| nypxdp.capnp.o      |     |   460 |      |   460 |
| syscall.o           |     |    68 |    4 |    72 |
| system_stm32f4xx.o  |     |    20 |      |    20 |
| crtn.o              |     |    16 |      |    16 |
| crti.o              |     |     8 |      |     8 |
| TOTALS              |   0 | 38115 | 2548 |       |
+---------------------+-----+-------+------+-------+
```

关于ROM空间：

- 库本身占用约为6K
- 由于使用了malloc、printf，libc.a占用了不少空间，其中printf是log打印，可以直接被去掉的；而malloc有精简的替代如[tinyalloc](https://github.com/thi-ng/tinyalloc)仅1.4KB

RAM由于未使用静态内存，全是栈、堆上空间这里看不出，通过阅读代码可知：

- capn为40bytes
- 每个segment占用64bytes；new对象时，会申请堆内存，首次会申请4K内存（可手动改小），内存不够时再次申请
- 试考虑“在单个数据包大小为N时，RAM开销是多少”时就要考虑，接收方能不能直接在接收缓存区上解析数据——答案是不能，因为进行序列化并不是简单的内存拷贝（详见[Serialization Over a Stream](https://capnproto.org/encoding.html)）



### 总结

先说结论，它的ROM/RAM开销，运行在一般的ARM Cortex-M核MCU（ROM<32K, RAM<16K这种级别）是没有问题的。

承担着这些额外开销，需要一些理由去用它（或者不用它），毕竟这些ROM/RAM都是实打实的、放在每片芯片上的银子

用它的理由：

- .capnp文件可以作为协议文档，而且有一定的自解释性
- 序列化格式的生成、解析无需人工写代码，减少了协议对接错误的可能
- 与其他编程语言协作起来方便，比如与你硬件设备通讯的是Python、Rust，都能找到对应的实现

不用它的理由：

- 它的实现挺复杂，至少不简单，我们的应用真的需要这么完善的序列化格式吗？（类似的序列化[MsgPuck](https://github.com/rtsisyk/msgpuck)虽然功能少，但更加简单而且零开销，但它缺少其他语言的实现、以及像.capnp一样的描述数据结构的文件）



> TODO: 遗漏一个评估要点是性能，这得单独开一篇做个基准测试来同JSON(jsmn)/protobuf(nanopb)对比。