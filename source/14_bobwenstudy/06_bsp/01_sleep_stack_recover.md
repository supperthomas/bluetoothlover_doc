# STM32 BlueNRG-1低功耗介绍，包含CPU堆栈恢复和外设恢复

在消费类电子产品形态中，通常用锂电池\纽扣电池\干电池等设备供电，需要现有供电情况下能连续使用几个月或者1年，而这些供电电源通常只有20-40mAh左右的电，要达到要求的运行时间，通常要求平均功耗在uA级别，芯片正常工作下的工作级别基本都在mA级别，所以必须设计一系列操作，让芯片在特定场景下进入低功耗模式，减少耗电。

## 低功耗设计要求

由于WFI模式只能做到100uA级别的功耗，这里重点对Sleep模式进行说明。根据实际业务需求，总体来说所设计的低功耗模式需要芯片满足如下需要。

1. 寄存器保电，部分寄存器要能保电，用于控制睡眠模式下芯片行为；
2. 可唤醒，能被外部中断唤醒和自身的特定中断唤醒（如定时器中断，GPIO中断等）；
3. RAM保电，RAM可以选择保电或者不保电，用于恢复现场（保电的RAM越多，功耗越大）；
4. 时钟恢复，要能恢复时钟，做定时；
5. 休眠，静态休眠功耗要在uA级别，芯片空闲工作电流一般为mA级别；

## 芯片定义休眠模式

一般芯片提供了多种睡眠模式供用户选择，通常为Sleep模式和CPU Halt模式。其中CPU Halt模式是指WFI模式，由于WFI模式比较好理解。

从下面8个信号来描述芯片行为。

**VCC**，电源供电信号，高电平代表供电。

**CPU_run**，CPU运行状态，高电平CPU运行。

**RET_Regs**，代表保电区寄存器供电/工作状态，高电平代表供电，RST蓝色方块代表硬件进行初始化。

**Regs**，代表一般寄存器供电/工作状态，高电平代表供电，RST蓝色方块代表硬件进行初始化。

**RET_RAM**，代表保电区RAM供电状态，高电平代表供电。

**RAM**，代表一般RAM供电状态，高电平代表供电。

**LP_CLK**，代表低功耗时钟，通常为32KHz或32.768KHz。

**PLL/HCLK**，代表高频时钟，CPU和外设时钟基本都挂在这个时钟下。

![image-20230614110628312](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614110628312.png)

**Power-up状态**，刚上电时会进行一些芯片的初始化工作，这时时钟陆续就开启了，RET_Regs和Regs会初始化，一段时间后，CPU开始工作。

**WFI状态**，当用户输入wfi指令时，除了cpu停止运行外，其他模块都正常运行，当中断到达后，cpu继续工作。

**SLEEP状态**，当用户配置进入SLEEP状态后，除了RET_Regs/RET_RAM/LP_CLK还在工作外，其他模块都掉电。当要预设条件到达后，芯片唤醒，会在CPU_run信号拉起之前对Regs进行初始化，并开启PLL/HCLK。

### Sleep模式

硬件提供了一个Sleep模式，该模式具备如下特点：

1. 寄存器部分，部分/全部寄存器保电。
2. RAM部分，可以配置哪些RAM保电。
3. 唤醒源，主要就是GPIO/定时器唤醒等。
4. 时钟，只有low power timer工作，可设置超时时间。PLL，HCLK都会关闭。
5. 外设，由于时钟关闭了，所有挂载在PLL，HCLK下的模块都停止工作。

在极端情况下，芯片所有RAM都掉电，只有lpo timer工作，芯片的功耗在uA级别。

### CPU Halt模式

WFI模式，实际省的电并不多，因为所有的寄存器都在工作，只是省掉了Cpu功耗，可以满足绝大多数场景的需要。



## 软件定义休眠模式

从上述可以看出，Sleep模式下硬件提供可以配置的参数很多，那根据不同的配置参数，软件可以有各种玩法，各家芯片提供的说明书基本上也都是围绕于软件定义的模式来讲。

从软件行为的角度来讲，Sleep模式可以分为两种，关机模式和恢复现场模式。

### 关机模式

保留基本的唤醒源，条件到达后自动唤醒，程序重新启动。

这个模式可以理解为关机，系统没什么事情要做了，直到用户按下开关机键（GPIO唤醒），芯片重新启动，从用户侧看，代码从main()第一行执行。

这个模式最省电，基本可以达到0.xuA级别，比电池自身的静态漏电都低。

### 恢复现场模式

这个模式下，芯片调用进入Sleep的API后，Sleep醒来后，CPU继续运行，软件无感。

#### WFI模式

最简单的就是基于WFI的睡眠模式，这个最简单了，一般cpu只要一条`wfi`指令就结束了。从之前的芯片运行图可以看出，这个模式下只是CPU暂停工作，其他模块并不受影响。等待中断触发，cpu继续执行，软件无需做其他业务。

```c
__ASM volatile ("wfi");
```

#### Sleep模式

从之前的图可以看出，这个模式下RAM/Regs/PLL/HCLK掉电了，RAM/Regs掉电的话，里面的值都是非法值，其中Regs会陪硬件Reset，但也不是Sleep之前的值了。这个情况下就需要恢复现场。

需要明确的一点是，芯片进入Sleep后并唤醒后，除了部分内容保持之前状态外，剩下的都是重新开始。对软件而言，实际CPU是从初始地址重新运行的，这时软件需要根据RET中的内容判断是否进行恢复动作，跳转到最后sleep那行PC继续执行。

根据芯片行为，要恢复现场就是需要将掉电的内容恢复默认值，主要包括如下CPU堆栈恢复和外设恢复。

##### CPU堆栈恢复

从之前的描述可知，芯片从Sleep状态醒来后，是CPU会从初始地址重新运行，也就是CPU的PC/SP/R0/R1等内部寄存器都会恢复初始值。从中断机制可知，CPU的寄存器在切换到中断服务函数之前都会压入堆栈，处理完毕后，会从堆栈中将寄存器恢复。同样的，这个模式只是将更多的寄存器压入到堆栈中，确保堆栈在RET_RAM中，芯片醒来后从堆栈恢复CPU即可。

##### 外设恢复

由于大多数外设的Regs值在醒来后都恢复了初始值，所以睡眠之前需要将当前的外设寄存器状态存储在堆栈中。芯片醒来后，再从堆栈中依次将外设恢复即可。



#### 软件业务时序

软件进入Sleep流程如下：

- Step1：关中断，为防止中断改变CPU寄存器和Regs状态，需要先关闭中断。

- Step2：外设保存，将Regs内容拷贝到RET_RAM中。

- Step3：Sleep参数配置，配置唤醒源和唤醒时间等，当然可以放在Step2之前。

- Step4：CPU保存，将CPU Regs内容拷贝到RET_RAM中。如PC/SP/R0/R1等内部寄存器。

- Step5：Sleep Enter，真正通知硬件进入Sleep。

  

软件退出Sleep流程如下：

- Step1：CPU恢复，将RET_RAM中的CPU Regs恢复，之后CPU跳转到最后一行代码。

- Step2：外设恢复，将RET_RAM中的Regs恢复，之后外设就可以正常工作了。

- Step3：开中断，这时候开启中断，函数Return后就可以回到用户调用API的位置，由于硬件相关的东西都恢复了，如果用户使用了RAM中的资源，需要用户自身进行恢复操作。

![image-20230614114958618](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614114958618.png)





## STM32 BlueNRG-1低功耗介绍

通过上面的描述，相信已经对低功耗模式和软件所需进行的工作有一个初步认识，下面围绕于STM32的BlueNRG-1蓝牙芯片来进一步了解代码实现上如何处理。[BlueNRG-1 and BlueNRG-2 low power modes - Application note (st.com)](https://www.st.com/resource/en/application_note/dm00263007-bluenrg-1-and-bluenrg-2-low-power-modes-stmicroelectronics.pdf)

### SDK提供的模式

其实从上面分析可以知道，Sleep mode和Standby mode都是Sleep模式，只是是否开启定时器唤醒，并且会实现CPU堆栈恢复和外设恢复；CPU-Halt mode就是之前说的WFI模式。

![image-20230614134216297](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614134216297.png)

在BlueNRG-1芯片中，所有的恢复都是由软件来进行的，所以通过分析其源码，就可以看到所有睡眠机制。

为了方便使用，软件将低功耗模式分为如下4种。

![image-20230614134722666](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614134722666.png)

对应的功耗由高到底越来越小。

![image-20230614134731818](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614134731818.png)

使用的API就是如下函数。

sleepMode，配置所需进入的SleepMode，里面再进行判断，综合所有模块的sleepMode，选择功耗最高的模式运行。

gpioWakeBitMask/gpioWakeLevelMask，配置GPIO的唤醒源。

返回值，就是Sleep成功和失败的结果。

![image-20230614134807857](C:/Users/wenbo/AppData/Roaming/Typora/typora-user-images/image-20230614134807857.png)



### SDK低功耗模式使用范例

#### SLEEPMODE_RUNNING模式

这个本质并不是低功耗模式，基本不会使用。

![image-20230614135223183](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614135223183.png)



#### SLEEPMODE_CPU_HALT模式

WFI模式，无需配置GPIO唤醒源，直接通过Interrupt/Event唤醒即可。

![image-20230614135309221](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614135309221.png)



#### SLEEPMODE_WAKETIMER模式

这个模式一般会配合VTimer模块使用，配置timer唤醒时间，软件会选择最近的时刻唤醒。考虑到业务需要，还需配置合适的GPIO唤醒源，以便一些突发业务来临后唤醒CPU。

注意，唤醒时间会综合蓝牙和VTimer最近的唤醒时刻。

![image-20230614135358531](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614135358531.png)



#### SLEEPMODE_NOTIMER模式

这个模式一般是软关机模式，一定要配置合适的GPIO唤醒源，不然只能通过Reset唤醒芯片了。

这个相比于关机模式，功耗还是有点高，因为其需要恢复堆栈，RET_RAM还是保电的，功耗比较高。不过蚊子肉再小也是肉，没什么特别需求，无脑选这个模式即可。因为如果有Timer业务，里面的逻辑依然会选WAKETIMER模式。

![image-20230614135634297](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614135634297.png)





### SDK Sleep恢复现场模式代码分析

对于软件而言，最难的部分就是进出Sleep模式的保护现场和恢复现场处理了。相比于Interrupt处理只需要把cpu寄存器保存和恢复，Sleep模式下的保护现场和恢复现场更为麻烦。

下面分别对CPU堆栈恢复和外设恢复进行说明。

#### CPU堆栈恢复

要恢复CPU，需要先了解CPU的特性，不同CPU的行为各不相同，BlueNRG-1的ARM Cortex-CM0+的芯片，CPU寄存器堆栈操作是通过PUSH和POP来完成操作的。

要看懂BlueNRG-1芯片的堆栈恢复操作，需要大家对Cortex-CM0+芯片有一个清晰的认识。

官网直接看CPU手册：[Cortex-M0+ – Arm®](https://www.arm.com/products/silicon-ip-cpu/cortex-m/cortex-m0-plus)。

再看看其他人写的关于Cortex-M系列CPU处理的分析：[痞子衡嵌入式：ARM Cortex-M内核那些事（6）- 系统堆栈机制_51CTO博客_ARM Cortex M](https://blog.51cto.com/henjay724/2713451)

Cortex-M0的中断压栈出栈处理分析：[Cortex-M0异常和中断_长水曰天的博客-CSDN博客](https://blog.csdn.net/Sisyphus415/article/details/129045605)

CM0+的寄存器就如下图所示。

![image-20230614145002580](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614145002580.png)

当中断到达时，CPU会将如下寄存器压入堆栈。退出时根据进入的行为，恢复相关的寄存器。

![image-20230614143101367](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614143101367.png)

保护现场本质目的就是保存这些CPU相关寄存器。



##### 现场保护

在SDK的**sleep.c**文件的`BlueNRG_InternalSleep`函数中有保护现场的代码，也就是调用`CS_contextSave()`函数。从注释可以看出，先配置了Sleep Enable，之后在`CS_contextSave()`函数中真正启动Sleep。

```c

static void BlueNRG_InternalSleep(SleepModes sleepMode, uint8_t gpioWakeBitMask)
{
  ...
  
  //Enable deep sleep
  SystemSleepCmd(ENABLE);
  //The __disable_irq() used at the beginning of the BlueNRG_Sleep() function
  //masks all the interrupts. The interrupts will be enabled at the end of the 
  //context restore. Now induce a context save.
  void CS_contextSave(void);
  CS_contextSave();
  
  ...
}

```

到这里都是汇编代码了，本质就是将`R4->R12/PSP/CONTROL`寄存器保存到堆栈中，并将`MSP`指针保存到`savedMSP`变量中。其他就是一些特别的寄存器保存了。最后调用WFI真正进入Sleep模式。

```assembly
	
//------------------------------------------------------------------------------
//   void CS_contextSave(void)
//   void CS_contextRestore(void)
//
// These two functions are needed for the context switch during the power
// save procedure. The purpose of the CS_contextSave() function is to 
// either save the current context and trigger sleeping through the 'WFI' 
// instruction. 
// The CS_contextRestore() function restores the context saved before 
// to go in deep sleep.  
// All the Cortex M0 registers are saved and restored plus after wakeup
// -----------------------------------------------------------------------------
                 __CODE__
                 __THUMB__
                 __EXPORT__ CS_contextSave
                 __EXPORT__ CS_contextRestore
                 __IMPORT__ savedMSP
                 __IMPORT__ savedICSR
                 __IMPORT__ savedSHCSR
                 __IMPORT__ savedNVIC_ISPR
EXPORT_FUNC(CS_contextSave)
                 MRS    R2, CONTROL             /* load the CONTROL register into R2 */
                 MRS    R1, PSP                 /* load the process stack pointer into R1 */
                 LDR    R0, =0
                 MSR    CONTROL, R0             /* Switch to Main Stack Pointer */
                 ISB
#ifdef CONTEXT_SAVE_V2
                 SUB    SP, #0x44			    /* Move stack pointer in order to be sure that after wake up the __low_level_init()
                                                   will not corrupt data saved in the stack by CS_contextSave routine.
                                                   WARNING: this instruction breaks backward compatibility with previous CS_contextRestore. */ 
#endif

                 PUSH   { r4 - r7, lr }         /* store R4-R7 and LR (5 words) onto the stack */
                 MOV    R3, R8                  /* move {r8 - r12} to {r3 - r7} */    
                 MOV    R4, R9
                 MOV    R5, R10
                 MOV    R6, R11        
                 MOV    R7, R12        
                 PUSH   {R3-R7}                 /* store R8-R12 (5 words) onto the stack */
                 
                 LDR    R4, =savedMSP           /* load address of savedMSP into R4 */
                 MRS    R3, MSP                 /* load the stack pointer into R3 */
                 STR    R3, [R4]                /* store the MSP into savedMSP */

                 PUSH   { r1, r2 }               /*  store PSP, CONTROL */
                 
                 LDR    R4, =0xE000ED04         /* load address of ICSR register into R4 */
                 LDR    R0, [R4]                /* load the ICSR register value into R0 */
                 LDR    R4, =savedICSR          /* load address of savedICSR into R4 */
                 STR    R0, [R4]                /* store the ICSR register value into savedICSR */

                 LDR    R4, =0xE000ED24         /* load address of SHCSR register into R4 */
                 LDR    R0, [R4]                /* load the SHCSR register value into R0 */
                 LDR    R4, =savedSHCSR         /* load address of savedSHCSR into R4 */
                 STR    R0, [R4]                /* store the SHCSR register value into savedSHCSR */

                 LDR    R4, =0xE000E200         /* load address of NVIC_ISPR register into R4 */
                 LDR    R0, [R4]                /* load the NVIC_ISPR register value into R0 */
                 LDR    R4, =savedNVIC_ISPR     /* load address of savedNVIC_ISPR into R4 */
                 STR    R0, [R4]                /* store the NVIC_ISPR register value into savedNVIC_ISPR */

                 LDR    R4, =0x40200008         /* setup the  SYSTEM_CTRL->CTRL_b.MHZ32_SEL = 0 */
                 LDR    R7, [R4]
                 MOVS   R0, #0                 
                 STR    R0, [R4]

                 DSB
                 WFI                            /* all saved, trigger deep sleep */
                 
                 STR    R7, [R4]                /* if WFI will be skipped restore the content of the 
                                                   SYSTEM_CTRL->CTRL_b.MHZ32_SEL with the original value */                 
                 ENDFUNC     
```



##### 现场恢复

CPU从Sleep醒来后就是到最开始的代码了。CM0就是进`RESET_HANDLER`。在`system_BlueNRG1.c`文件中。

```c
__attribute__((noreturn)) void RESET_HANDLER(void)
{
  if(__low_level_init()==1)
    __main();
  else {
    __set_MSP((uint32_t)_INITIAL_SP);
    main();
  }
  while(1);
}
```



而后到`__low_level_init()`函数中进行判断，如果reset_reason是sleep唤醒，就是调用`CS_contextRestore()`函数进行CPU堆栈恢复。

```c

int __low_level_init(void) 
{
  ...
      
  /* If the reset reason is a wakeup from sleep restore the context */
  if (reset_reason >= RESET_BLE_WAKEUP_FROM_IO9) { 
#ifndef NO_SMART_POWER_MANAGEMENT
 
    ...
    
    void CS_contextRestore(void);
    wakeupFromSleepFlag = 1; /* A wakeup from Standby or Sleep occurred */
    CS_contextRestore();     /* Restore the context */
    /* if the context restore worked properly, we should never return here */
    while(1) {
      NVIC_SystemReset();
    }
#else
    return 0;
#endif   
  }
  return 1;
}
```

这个就是和刚刚的反着来了，先将`savedMSP`变量中的`MSP`栈顶指针恢复下，剩下就是各种恢复寄存器了。

```assembly
EXPORT_FUNC(CS_contextRestore)
                /* Even if we fall through the WFI instruction, we will immediately
                 * execute a context restore and end up where we left off with no
                 * ill effects.  Normally at this point the core will either be
                 * powered off or reset (depending on the deep sleep level). */
                LDR    R4, =savedMSP            /* load address of savedMSP into R4 */
                LDR    R4, [R4]                 /* load the MSP from savedMSP */
                MSR    MSP, R4                  /* restore the MSP from R4 */
              
                SUB    SP, #0x8               
                POP    { R0, R1 }               /* load PSP from the stack in R0, and  load CONTROL register from the stack in R1 */
                
                POP    { R3-R7 }                /* load R8-R12 (5 words) from the stack */
                MOV    R8, R3                   /* mov {r3 - r7} to {r8 - r12} */
                MOV    R9, R4
                MOV    R10, R5
                MOV    R11, R6
                MOV    R12, R7
                POP    { R4 - R7 }              /* load R4-R7 (4 words) from the stack */
                POP    { R2 }                   /* load LR from the stack */
#ifdef CONTEXT_SAVE_V2
                ADD	   SP, #0x44                /* Restore MSP to the point where it was before pushing data to the stack in CS_contextSave */
#endif
                
                MSR    PSP, R0                   /* restore PSP from R0 */
                MSR    CONTROL , R1              /* restore CONTROL register from R1 */
                ISB
 
                BX  R2                          /*load PC (1 words) from the stack */
                                 
                ENDFUNC
```



而后代码会回到这，开始执行`SystemSleepCmd(DISABLE)`函数。到此，CPU堆栈恢复工作已完成。

```c
static void BlueNRG_InternalSleep(SleepModes sleepMode, uint8_t gpioWakeBitMask)
{
  ...
  
  //Enable deep sleep
  SystemSleepCmd(ENABLE);
  //The __disable_irq() used at the beginning of the BlueNRG_Sleep() function
  //masks all the interrupts. The interrupts will be enabled at the end of the 
  //context restore. Now induce a context save.
  void CS_contextSave(void);
  CS_contextSave();
  
  //Disable deep sleep, because if no reset occours for an interrrupt pending,
  //the register value remain set and if a simple CPU_HALT command is called from the
  //application the BlueNRG-1 enters in deep sleep without make a context save.
  //So, exiting from the deep sleep the context is restored with wrong random value.
  SystemSleepCmd(DISABLE);
  ...
}

```



##### 堆栈覆盖处理

其实有点需要注意的是，我们不清楚ROM如何处理的，这里其实有一个问题，就是__low_level_init()处理的时候也是有堆栈操作的，这时候堆栈其实会被覆盖。

两种办法：

一个是ROM里面做一下判断，提前将saveMSP值存储到MSP中，但是实话来说这样不是很合理。

一个是进入Sleep前将栈顶可能被冲掉的栈信息保存到RAM中。

BlueNRG-1使用的是后面这个方法。注意看`CSTACK_PREAMBLE_NUMBER`宏定义的注释，就是为了防止这个情况。进入sleep前会将栈顶的一部分内容存到RET_RAM中，醒来后恢复。

```c
/* Important note: The __low_level_init() function is critical for waking up from 
   deep sleep and it should not use more that 20 stack positions
   otherwise a stack corruption will occur when waking up from deep sleep.
   For this reason we are saving and restoring the first 20 words of the stack that 
   will be corrupted during the wake-up procedure from deep sleep.
   If the __low_level_init() will be modified, this define shall be modifed according
   the new function implementation
*/
#define CSTACK_PREAMBLE_NUMBER 25

...

static void BlueNRG_InternalSleep(SleepModes sleepMode, uint8_t gpioWakeBitMask)
{
  ...
  
  //Save the CSTACK number of words that will be restored at wakeup reset
  i = 0;
  ptr = __vector_table[0].__ptr ;
  ptr -= CSTACK_PREAMBLE_NUMBER;
  do {
    cStackPreamble[i] = *ptr;
    i++;
    ptr++;
  } while (i < CSTACK_PREAMBLE_NUMBER); 
  
  ...
  
  //Enable deep sleep
  SystemSleepCmd(ENABLE);
  //The __disable_irq() used at the beginning of the BlueNRG_Sleep() function
  //masks all the interrupts. The interrupts will be enabled at the end of the 
  //context restore. Now induce a context save.
  void CS_contextSave(void);
  CS_contextSave();
  
  //Disable deep sleep, because if no reset occours for an interrrupt pending,
  //the register value remain set and if a simple CPU_HALT command is called from the
  //application the BlueNRG-1 enters in deep sleep without make a context save.
  //So, exiting from the deep sleep the context is restored with wrong random value.
  SystemSleepCmd(DISABLE);
  
  ...
  
  /* Restore the CSTACK number of words that will be saved before the sleep */
  i = 0;
  ptr = __vector_table[0].__ptr ;
  ptr -= CSTACK_PREAMBLE_NUMBER;
  do {
    *ptr = cStackPreamble[i];
    i++;
    ptr++;
  } while (i < CSTACK_PREAMBLE_NUMBER); 

  ...

}
```



#### 外设恢复

相比于CPU堆栈恢复，外设恢复要简单不少。其实就是将外设寄存器保存，再将外设寄存器依次恢复就行了。当然这里有很多中断判定之类的，以及恢复的顺序，这块一般都是各家芯片厂根据自家芯片来定义了，不是通用的就不分析了。

代码都在`BlueNRG_InternalSleep()`函数中。

CTXT，可以决定是将存储的变量放在data区域还是栈中。

SLEEP_SAVE_N_RESTORE_XXX，通过这个宏可以有选择的关闭一些不必要的外设恢复，方便后续优化。

```c

static void BlueNRG_InternalSleep(SleepModes sleepMode, uint8_t gpioWakeBitMask)
{
  uint32_t savedCurrentTime, nvicPendingMask, ioValue, ioLevel, ioEnabled;
  PartInfoType partInfo;
  uint8_t i;
  
  /* Variables used to store system peripheral registers in order to restore the state after
   exit from sleep mode */

/* System Control saved */
  CTXT uint32_t SYS_Ctrl_saved;
  /* NVIC Information Saved */
  CTXT uint32_t NVIC_ISER_saved, NVIC_IPR_saved[8], PENDSV_SYSTICK_IPR_saved;
  /* CKGEN SOC Enabled */
  CTXT uint32_t CLOCK_EN_saved;
  /* GPIO Information saved */
  CTXT uint32_t GPIO_DATA_saved, GPIO_OEN_saved, GPIO_PE_saved, GPIO_DS_saved, GPIO_IS_saved, GPIO_IBE_saved;
  CTXT uint32_t GPIO_IEV_saved, GPIO_IE_saved, GPIO_MODE0_saved, GPIO_MODE1_saved, GPIO_IOSEL_MFTX_saved;
#ifdef BLUENRG2_DEVICE
  CTXT uint32_t GPIO_MODE2_saved, GPIO_MODE3_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_UART
  /* UART Information saved */
  CTXT uint32_t UART_TIMEOUT_saved, UART_LCRH_RX_saved, UART_IBRD_saved, UART_FBRD_saved;
  CTXT uint32_t UART_LCRH_TX_saved, UART_CR_saved, UART_IFLS_saved, UART_IMSC_saved;
  CTXT uint32_t UART_DMACR_saved, UART_XFCR_saved, UART_XON1_saved, UART_XON2_saved;
  CTXT uint32_t UART_XOFF1_saved, UART_XOFF2_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_SPI
  /* SPI Information saved */
  CTXT uint32_t SPI_CR0_saved, SPI_CR1_saved, SPI_CPSR_saved, SPI_IMSC_saved, SPI_DMACR_saved;
  CTXT uint32_t SPI_RXFRM_saved, SPI_CHN_saved, SPI_WDTXF_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_I2C
  /* I2C Information saved */
  CTXT uint32_t I2C_CR_saved[2], I2C_SCR_saved[2], I2C_TFTR_saved[2], I2C_RFTR_saved[2];
  CTXT uint32_t I2C_DMAR_saved[2], I2C_BRCR_saved[2], I2C_IMSCR_saved[2], I2C_THDDAT_saved[2];
  CTXT uint32_t I2C_THDSTA_FST_STD_saved[2], I2C_TSUSTA_FST_STD_saved[2];
#endif
  /* RNG Information saved */
  CTXT uint32_t RNG_CR_saved;
  /* SysTick Information saved */
  CTXT uint32_t SYST_CSR_saved, SYST_RVR_saved;
#if SLEEP_SAVE_N_RESTORE_RTC
  /* RTC Information saved */
  CTXT uint32_t RTC_CWDMR_saved, RTC_CWDLR_saved, RTC_CWYMR_saved, RTC_CWYLR_saved, RTC_CTCR_saved;
  CTXT uint32_t RTC_IMSC_saved, RTC_TCR_saved, RTC_TLR1_saved, RTC_TLR2_saved, RTC_TPR1_saved;
  CTXT uint32_t RTC_TPR2_saved, RTC_TPR3_saved, RTC_TPR4_saved;
#endif
  /* MFTX Information saved */
#if SLEEP_SAVE_N_RESTORE_MFTX1
  CTXT uint32_t T1CRA_saved, T1CRB_saved, T1PRSC_saved, T1CKC_saved, T1MCTRL_saved, T1ICTRL_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_MFTX2  
  CTXT uint32_t T2CRA_saved, T2CRB_saved, T2PRSC_saved, T2CKC_saved, T2MCTRL_saved, T2ICTRL_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_WDG
  /* WDT Information saved */
  CTXT uint32_t WDG_LR_saved, WDG_CR_saved, WDG_LOCK_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_DMA
  /* DMA channel [0..7] Information saved */
  CTXT uint32_t DMA_CCR_saved[8], DMA_CNDTR_saved[8], DMA_CPAR_saved[8], DMA_CMAR[8];
#endif
#if SLEEP_SAVE_N_RESTORE_ADC
  /* ADC Information saved */
  CTXT uint32_t ADC_CTRL_saved, ADC_CONF_saved, ADC_IRQMASK_saved, ADC_OFFSET_LSB_saved, ADC_OFFSET_MSB_saved;
  CTXT uint32_t ADC_THRESHOLD_HI_saved, ADC_THRESHOLD_LO_saved;
#endif
  /* FlASH Config saved */
  CTXT uint32_t FLASH_CONFIG_saved;
  /* PKA Information saved */
  CTXT uint32_t PKA_IEN_saved;

  /* Get partInfo */
  HAL_GetPartInfo(&partInfo);

  /* Save the peripherals configuration */
  /* System Control */
  SYS_Ctrl_saved = SYSTEM_CTRL->CTRL;
  /* FLASH CONFIG */
  FLASH_CONFIG_saved = FLASH->CONFIG;
  /* NVIC */
  NVIC_ISER_saved = NVIC->ISER[0];

  // Issue with Atollic compiler
//  memcpy(NVIC_IPR_saved, (void const *)NVIC->IP, sizeof(NVIC_IPR_saved));
  for (i=0; i<8; i++) {
  	NVIC_IPR_saved[i] = NVIC->IP[i];
  }


  PENDSV_SYSTICK_IPR_saved = *(volatile uint32_t *)SHPR3_REG;
  /* CKGEN SOC Enabled */
  CLOCK_EN_saved = CKGEN_SOC->CLOCK_EN;
  /* GPIO */
  GPIO_DATA_saved = GPIO->DATA;
  GPIO_OEN_saved = GPIO->OEN;
  GPIO_PE_saved = GPIO->PE;
  GPIO_DS_saved = GPIO->DS;
  GPIO_IS_saved = GPIO->IS;
  GPIO_IBE_saved = GPIO->IBE;
  GPIO_IEV_saved = GPIO->IEV;
  GPIO_IE_saved = GPIO->IE;
  GPIO_MODE0_saved = GPIO->MODE0;
  GPIO_MODE1_saved = GPIO->MODE1;
#ifdef BLUENRG2_DEVICE
  GPIO_MODE2_saved = GPIO->MODE2;
  GPIO_MODE3_saved = GPIO->MODE3;
#endif
  GPIO_IOSEL_MFTX_saved = GPIO->MFTX;
#if SLEEP_SAVE_N_RESTORE_UART
  /* UART */
  UART_TIMEOUT_saved = UART->TIMEOUT;
  UART_LCRH_RX_saved = UART->LCRH_RX;
  UART_IBRD_saved = UART->IBRD;
  UART_FBRD_saved = UART->FBRD;
  UART_LCRH_TX_saved =  UART->LCRH_TX;
  UART_CR_saved = UART->CR;
  UART_IFLS_saved = UART->IFLS;
  UART_IMSC_saved = UART->IMSC;
  UART_DMACR_saved = UART->DMACR;
  UART_XFCR_saved = UART->XFCR;
  UART_XON1_saved = UART->XON1;
  UART_XON2_saved = UART->XON2;
  UART_XOFF1_saved = UART->XOFF1;
  UART_XOFF2_saved = UART->XOFF2;
#endif
#if SLEEP_SAVE_N_RESTORE_SPI
  /* SPI */
  SPI_CR0_saved = SPI->CR0; 
  SPI_CR1_saved = SPI->CR1;
  SPI_CPSR_saved = SPI->CPSR;
  SPI_IMSC_saved = SPI->IMSC;
  SPI_DMACR_saved = SPI->DMACR;
  SPI_RXFRM_saved = SPI->RXFRM;
  SPI_CHN_saved = SPI->CHN;
  SPI_WDTXF_saved = SPI->WDTXF;
#endif
#if SLEEP_SAVE_N_RESTORE_I2C
  /* I2C */
  for (i=0; i<2; i++) {
    I2C_Type *I2Cx = (I2C_Type*)(I2C2_BASE+ 0x100000*i);
    I2C_CR_saved[i] = I2Cx->CR;
    I2C_SCR_saved[i] = I2Cx->SCR;
    I2C_TFTR_saved[i] = I2Cx->TFTR;
    I2C_RFTR_saved[i] = I2Cx->RFTR;
    I2C_DMAR_saved[i] = I2Cx->DMAR;
    I2C_BRCR_saved[i] = I2Cx->BRCR;
    I2C_IMSCR_saved[i] = I2Cx->IMSCR;
    I2C_THDDAT_saved[i] = I2Cx->THDDAT;
    I2C_THDSTA_FST_STD_saved[i] = I2Cx->THDSTA_FST_STD;
    I2C_TSUSTA_FST_STD_saved[i] = I2Cx->TSUSTA_FST_STD;
  }
#endif
  /* RNG */
  RNG_CR_saved = RNG->CR;
#if SLEEP_SAVE_N_RESTORE_RTC
  /* RTC */
  RTC_CWDMR_saved = RTC->CWDMR;
  RTC_CWDLR_saved = RTC->CWDLR;
  RTC_CWYMR_saved = RTC->CWYMR;
  RTC_CWYLR_saved = RTC->CWYLR;
  RTC_CTCR_saved = RTC->CTCR;
  RTC_IMSC_saved = RTC->IMSC;
  RTC_TCR_saved = RTC->TCR;
  RTC_TLR1_saved = RTC->TLR1;
  RTC_TLR2_saved = RTC->TLR2;
  RTC_TPR1_saved = RTC->TPR1;
  RTC_TPR2_saved = RTC->TPR2;
  RTC_TPR3_saved = RTC->TPR3;
  RTC_TPR4_saved = RTC->TPR4; 
#endif
  /* MFTX */
#if SLEEP_SAVE_N_RESTORE_MFTX1
  T1CRA_saved = MFT1->TNCRA;
  T1CRB_saved = MFT1->TNCRB;
  T1PRSC_saved = MFT1->TNPRSC;
  T1CKC_saved = MFT1->TNCKC;
  T1MCTRL_saved = MFT1->TNMCTRL;
  T1ICTRL_saved = MFT1->TNICTRL;
#endif
#if SLEEP_SAVE_N_RESTORE_MFTX2
  T2CRA_saved = MFT2->TNCRA;
  T2CRB_saved = MFT2->TNCRB;
  T2PRSC_saved = MFT2->TNPRSC;
  T2CKC_saved = MFT2->TNCKC;
  T2MCTRL_saved = MFT2->TNMCTRL;
  T2ICTRL_saved = MFT2->TNICTRL;
#endif
  /* SysTick */
  SYST_CSR_saved = SysTick->CTRL;
  SYST_RVR_saved = SysTick->LOAD;
#if SLEEP_SAVE_N_RESTORE_WDG
  /* WDT */
  WDG_LR_saved = WDG->LR;
  WDG_CR_saved = WDG->CR;
  if(WDG->LOCK == 0) {
    WDG_LOCK_saved = 0x1ACCE551;
  } else {
    WDG_LOCK_saved = 0;
  }
#endif
#if SLEEP_SAVE_N_RESTORE_DMA
  /* DMA */
  for (i=0; i<8; i++) {
    DMA_CH_Type *DMAx = (DMA_CH_Type*)(DMA_CH0_BASE+ 0x14*i);
    DMA_CNDTR_saved[i] = DMAx->CNDTR;
    DMA_CCR_saved[i] = DMAx->CCR;
    DMA_CPAR_saved[i] = DMAx->CPAR;
    DMA_CMAR[i] = DMAx->CMAR;
  }
#endif
#if SLEEP_SAVE_N_RESTORE_ADC
  /* ADC */
  ADC_CONF_saved = ADC->CONF;
  ADC_IRQMASK_saved = ADC->IRQMASK;
  ADC_OFFSET_MSB_saved = ADC->OFFSET_MSB;
  ADC_OFFSET_LSB_saved = ADC->OFFSET_LSB;
  ADC_THRESHOLD_HI_saved = ADC->THRESHOLD_HI;
  ADC_THRESHOLD_LO_saved = ADC->THRESHOLD_LO;
  ADC_CTRL_saved = ADC->CTRL;
#endif

  /* PKA */
  PKA_IEN_saved = PKA->IEN;
  
  ...
   
  //Enable deep sleep
  SystemSleepCmd(ENABLE);
  //The __disable_irq() used at the beginning of the BlueNRG_Sleep() function
  //masks all the interrupts. The interrupts will be enabled at the end of the 
  //context restore. Now induce a context save.
  void CS_contextSave(void);
  CS_contextSave();
    
  //Disable deep sleep, because if no reset occours for an interrrupt pending,
  //the register value remain set and if a simple CPU_HALT command is called from the
  //application the BlueNRG-1 enters in deep sleep without make a context save.
  //So, exiting from the deep sleep the context is restored with wrong random value.
  SystemSleepCmd(DISABLE);
  
  ...
    

    /* Restore the peripherals configuration */
    /* FLASH CONFIG */
    FLASH->CONFIG = FLASH_CONFIG_saved;
    /* NVIC */
    NVIC->ISER[0] = NVIC_ISER_saved;

    // Issue with Atollic compiler
//    memcpy((void *)NVIC->IP, (void*)NVIC_IPR_saved, sizeof(NVIC_IPR_saved));
    for (i=0; i<8; i++) {
    	NVIC->IP[i] = NVIC_IPR_saved[i];
    }

    *(volatile uint32_t *)SHPR3_REG = PENDSV_SYSTICK_IPR_saved;
    /* CKGEN SOC Enabled */
    CKGEN_SOC->CLOCK_EN = CLOCK_EN_saved;
    /* GPIO */
    GPIO->DATA = GPIO_DATA_saved;
    GPIO->OEN = GPIO_OEN_saved;
    GPIO->PE = GPIO_PE_saved;
    GPIO->DS = GPIO_DS_saved;
    GPIO->IEV = GPIO_IEV_saved;
    GPIO->IBE = GPIO_IBE_saved;
    GPIO->IS = GPIO_IS_saved;
    GPIO->IC = GPIO_IE_saved; 
    GPIO->IE = GPIO_IE_saved;
    GPIO->MODE0 = GPIO_MODE0_saved;
    GPIO->MODE1 = GPIO_MODE1_saved;
#ifdef BLUENRG2_DEVICE
    GPIO->MODE2 = GPIO_MODE2_saved;
    GPIO->MODE3 = GPIO_MODE3_saved;
#endif
    GPIO->MFTX = GPIO_IOSEL_MFTX_saved;
#if SLEEP_SAVE_N_RESTORE_UART
    /* UART */
    UART->TIMEOUT = UART_TIMEOUT_saved;
    UART->LCRH_RX = UART_LCRH_RX_saved;
    UART->IBRD = UART_IBRD_saved;
    UART->FBRD = UART_FBRD_saved;
    UART->LCRH_TX = UART_LCRH_TX_saved;
    UART->CR = UART_CR_saved;
    UART->IFLS = UART_IFLS_saved;
    UART->IMSC = UART_IMSC_saved;
    UART->DMACR = UART_DMACR_saved;
    UART->XFCR = UART_XFCR_saved;
    UART->XON1 = UART_XON1_saved;
    UART->XON2 = UART_XON2_saved;
    UART->XOFF1 = UART_XOFF1_saved;
    UART->XOFF2 = UART_XOFF2_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_SPI
    /* SPI */
    SPI->CR0 = SPI_CR0_saved; 
    SPI->CR1 = SPI_CR1_saved;
    SPI->CPSR = SPI_CPSR_saved;
    SPI->IMSC = SPI_IMSC_saved;
    SPI->DMACR = SPI_DMACR_saved;
    SPI->RXFRM = SPI_RXFRM_saved;
    SPI->CHN = SPI_CHN_saved;
    SPI->WDTXF = SPI_WDTXF_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_I2C
    /* I2C */
    for (i=0; i<2; i++) {
      I2C_Type *I2Cx = (I2C_Type*)(I2C2_BASE+ 0x100000*i);
      I2Cx->CR = I2C_CR_saved[i];
      I2Cx->SCR = I2C_SCR_saved[i];
      I2Cx->TFTR = I2C_TFTR_saved[i];
      I2Cx->RFTR = I2C_RFTR_saved[i];
      I2Cx->DMAR = I2C_DMAR_saved[i];
      I2Cx->BRCR = I2C_BRCR_saved[i];
      I2Cx->IMSCR = I2C_IMSCR_saved[i];
      I2Cx->THDDAT = I2C_THDDAT_saved[i];
      I2Cx->THDSTA_FST_STD = I2C_THDSTA_FST_STD_saved[i];
      I2Cx->TSUSTA_FST_STD = I2C_TSUSTA_FST_STD_saved[i];
    }
#endif
    /* RNG */
    RNG->CR = RNG_CR_saved;  
    /* SysTick */
    SysTick->LOAD = SYST_RVR_saved;
    SysTick->VAL = 0;
    SysTick->CTRL = SYST_CSR_saved;
#if SLEEP_SAVE_N_RESTORE_RTC
    /* RTC */
    RTC->CWDMR = RTC_CWDMR_saved;
    RTC->CWDLR = RTC_CWDLR_saved;
    RTC->CWYMR = RTC_CWYMR_saved;
    RTC->CWYLR = RTC_CWYLR_saved;
    RTC->CTCR = RTC_CTCR_saved;
    RTC->IMSC = RTC_IMSC_saved;
    RTC->TLR1 = RTC_TLR1_saved;
    RTC->TLR2 = RTC_TLR2_saved;
    RTC->TPR1 = RTC_TPR1_saved;
    RTC->TPR2 = RTC_TPR2_saved;
    RTC->TPR3 = RTC_TPR3_saved;
    RTC->TPR4 = RTC_TPR4_saved; 
    RTC->TCR = RTC_TCR_saved; /* Enable moved at the end of RTC configuration */
#endif
    /* MFTX */
#if SLEEP_SAVE_N_RESTORE_MFTX1
    MFT1->TNCRA = T1CRA_saved;
    MFT1->TNCRB = T1CRB_saved;
    MFT1->TNPRSC = T1PRSC_saved;
    MFT1->TNCKC = T1CKC_saved;
    MFT1->TNMCTRL = T1MCTRL_saved & ~((uint32_t)(1<<6));
    MFT1->TNICTRL = T1ICTRL_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_MFTX2
    MFT2->TNCRA = T2CRA_saved;
    MFT2->TNCRB = T2CRB_saved;
    MFT2->TNPRSC = T2PRSC_saved;
    MFT2->TNCKC = T2CKC_saved;
    MFT2->TNMCTRL = T2MCTRL_saved & ~((uint32_t)(1<<6));
    MFT2->TNICTRL = T2ICTRL_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_WDG
    /* WDT */
    WDG->LR = WDG_LR_saved;
    WDG->CR = WDG_CR_saved;
    WDG->LOCK = WDG_LOCK_saved;
#endif
#if SLEEP_SAVE_N_RESTORE_DMA
    /* DMA */
    for (i=0; i<8; i++) {
      DMA_CH_Type *DMAx = (DMA_CH_Type*)(DMA_CH0_BASE+ 0x14*i);
      DMAx->CNDTR = DMA_CNDTR_saved[i];
      DMAx->CCR = DMA_CCR_saved[i] ;
      DMAx->CPAR = DMA_CPAR_saved[i];
      DMAx->CMAR = DMA_CMAR[i];
    }
#endif
#if SLEEP_SAVE_N_RESTORE_ADC
    /* ADC */
    ADC->CONF = ADC_CONF_saved;
    ADC->IRQMASK = ADC_IRQMASK_saved;
    ADC->OFFSET_MSB = ADC_OFFSET_MSB_saved;
    ADC->OFFSET_LSB = ADC_OFFSET_LSB_saved;
    ADC->THRESHOLD_HI = ADC_THRESHOLD_HI_saved;
    ADC->THRESHOLD_LO = ADC_THRESHOLD_LO_saved;
    ADC->CTRL = ADC_CTRL_saved;
#endif
    
    /* PKA */
    PKA->IEN = PKA_IEN_saved;
    //The five IRQs are linked to a real ISR. If any of the five IRQs
    //triggered, then pend their ISR
    //Capture the wake source from the BLE_REASON_RESET register
    if ((CKGEN_SOC->REASON_RST == 0) && gpioWakeBitMask) {
      if ((((CKGEN_BLE->REASON_RST & WAKENED_FROM_IO9) == WAKENED_FROM_IO9) && (GPIO->IE & GPIO_Pin_9))   ||
          (((CKGEN_BLE->REASON_RST & WAKENED_FROM_IO10) == WAKENED_FROM_IO10) && (GPIO->IE & GPIO_Pin_10)) ||
          (((CKGEN_BLE->REASON_RST & WAKENED_FROM_IO11) == WAKENED_FROM_IO11) && (GPIO->IE & GPIO_Pin_11)) ||
          (((CKGEN_BLE->REASON_RST & WAKENED_FROM_IO12) == WAKENED_FROM_IO12) && (GPIO->IE & GPIO_Pin_12)) ||
          (((CKGEN_BLE->REASON_RST & WAKENED_FROM_IO13) == WAKENED_FROM_IO13) && (GPIO->IE & GPIO_Pin_13))) {
        NVIC->ISPR[0] = 1<<GPIO_IRQn;
      }
    }

    // Disable the STANDBY mode 
    if (sleepMode == SLEEPMODE_NOTIMER) {
      BLUE_CTRL->TIMEOUT &= ~(LOW_POWER_STANDBY<<28);
    }
    
    /* Restore the System Control register to indicate which HS crystal is used */
    SYSTEM_CTRL->CTRL = SYS_Ctrl_saved;

    // Wait until the HS clock is ready.
    // If SLEEPMODE_NOTIMER is set, wait the LS clock is ready.  
    if (sleepMode == SLEEPMODE_NOTIMER) {
      DeviceConfiguration(FALSE, TRUE);
    } else {
      DeviceConfiguration(FALSE, FALSE);
    }

    /* If the HS is a 32 MHz */
    if (SYS_Ctrl_saved & 1) {
#ifndef FORCE_CORE_TO_16MHZ
      /* AHB up converter command register write*/
      frequency_switch();
#endif
    }
  }
}
```









### 芯片电流功耗示例

STM32也提供了一下其芯片的运行功耗。

![image-20230614140253692](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614140253692.png)

![image-20230614140306276](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230614140306276.png)









