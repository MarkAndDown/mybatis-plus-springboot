
CountDownLatch:
我们可以把CountDownLatch理解为一个计数器，给计数器一个初始值，当计数器的值减少的到0的时候，被wait的线程才开始执行；

**CountDownLatch适用的场景是：**适合大任务的拆分，使其并行执行，总的时间取决于最慢任务，总体来说，任务的执行时间大大的减少了；
CountDownLatch作用：就是等待其他线程执行完任务，并且必要时可以对各个任务的结果进行汇总，然后主线程继续往下执行；

下面是CountDownLatch简单实用：

 public void testCountDownLaunch() throws InterruptedException{
        CountDownLatch countLatch  = new CountDownLatch(10);
        for(int i = 0;i < 10;i++){
            new Thread(()-> {
                try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { }
                System.out.println("over + " + Thread.currentThread().getName());
                countLatch.countDown();
            },"A" + i).start();
        }
        countLatch.await();
        System.out.println("发射 。。。。。。");
    }

CyclicBarrier:
可以让一组线程达到一个屏障时被阻塞，直到最后一个线程到达屏障时，所有线程才可以继续执行；根据字面意思就是回环栅栏，其实就是可以重复使用的意思

@Test
    public void testCyclicBarrier() throws Exception {

        CyclicBarrier barrier = new CyclicBarrier(10);
        for(int i = 0;i < 9;i++) {
            new Thread(()-> {
                System.out.println(Thread.currentThread().getName() + "start");
                try { Thread.sleep(1000);
                    barrier.await(); } catch (Exception e) {}
                System.out.println(Thread.currentThread().getName() + "end"); },"A " + i).start();
        }
        System.out.println(Thread.currentThread().getName() + "start");
        barrier.await();
        System.out.println(Thread.currentThread().getName() + "end");

        Thread.sleep(1000);
        
        System.out.println("----------重复使用-------------");
        
        for(int i = 0;i < 10;i++) {
            new Thread(()-> {
                System.out.println(Thread.currentThread().getName() + "start");
                try { Thread.sleep(1000);
                    barrier.await(); } catch (Exception e) {}
                System.out.println(Thread.currentThread().getName() + "end"); },"B " + i).start();
        }
        
        Thread.sleep(1000);
        System.out.println("done 。。。。。。");
    }

Semaphore(信号量):
信号量的两个作用：
多个共享资源的互斥使用
并发线程数的控制
这是一个经典的停车场占车位的例子
public void testSemaphore() throws Exception {
        Semaphore semaphore = new Semaphore(3);
        for (int i = 0; i < 6; i++) {
            new Thread(() -> {
                try {
                    semaphore.acquire();
                    System.out.println(Thread.currentThread().getName() +"抢到车位");
                    Thread.sleep(1000);
                   System.out.println(Thread.currentThread().getName() +"离开车位！！！");
                } catch (Exception e) {
                } finally {
                    semaphore.release();
                }
            }, "B" + i).start();
        }
        Thread.sleep(10000);
    }


volatile: 可见性：
volatile可以使得在多处理器环境下保证了共享变量的可见性，那么到底什么是可见性？     一般在单线程的环境下，如果向一个变量先写入一个值，然后在没有写干涉的情况下读取这个变量的值，那么这个时候读取到的这个变量的值应该是之前写入的那个值。 这本来是一件很正常的事件，但是在多线程环境下，读和写发生在不同的线程中的时候，可能会出现以下的情况：读线程不能及时的读取到其他线程写入的最新的值。这就是所谓的可见性，为了实现跨线程写入的内存可见性，必须要使用一些机制来实现，而volatile就是这样的一种机制。
public class VolatileDemo {

    public static void main(String[] args) throws InterruptedException {
        VolatileTest test = new VolatileTest();
        test.start();
        for (; ; ) {
            if (test.isFlag()) {
                System.out.println("hi");
            }
        }
    }
}

class VolatileTest extends Thread {
    private /*volatile*/ boolean flag = false;

    public boolean isFlag() {
        return flag;
    }

    @Override
    public void run() {
        try {
            Thread.sleep(1000);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        flag = true;
        System.out.println("flag = " + flag);
    }
}

指令重排：

//懒汉式单例类.在第一次调用的时候实例化自己
public class Singleton {
      //私有的构造函数
    private Singleton() {
    }
    //私有的静态变量
    private static Singleton single =null;
    //暴露的公有静态方法
    public static Singleton getInstance() {
        if (single == null) {  //line1
            single=new Singleton(); //line2
        }
        return single;
    }
}
https://zhuanlan.zhihu.com/p/502550223?utm_id=0
懒汉式，确实是在调用getInstance()方法时，才会初始化实例，实现了懒加载。但是在能否满足在多线程下正常工作呢？我们在这里先分析一下假设有两个线程ThreadA和ThreadB
new Singleton()这个操作不是原子操作。至少可以分解成以下上个原子操作：

1.分配内存空间
2.初始化对象
3.将对象指向分配好的地址空间（执行完之后就不再是null了）
其中第2，3步在一些编译器中为了优化单线程中的执行性能是可以重排的。重排之后就是这样的：

　　1.分配内存空间
　　3.将对象指向分配好的地址空间（执行完之后就不再是null了）
　　2.初始化对象
重排之后就有可能出现上边分析的情况：


原子性：
public class Test1 {

     public static volatile  int a=0;
    public static void main(String[] args) throws InterruptedException {
        new Thread(()->{
            for (int i =0;i<10000;i++){
                a++;
            }
        }).start();

        new Thread(()->{
            for (int i =0;i<10000;i++){
                a++;
            }
        }).start();
        Thread.sleep(1000);
        System.out.println("a value = "+ a);
    }

}




import java.util.concurrent.atomic.AtomicInteger;

public class Test2 {

     public static AtomicInteger a =new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        new Thread(()->{
            for (int i =0;i<10000;i++){
                a.incrementAndGet();
            }
        }).start();

        new Thread(()->{
            for (int i =0;i<10000;i++){
                a.incrementAndGet();
            }
        }).start();
        Thread.sleep(1000);
        System.out.println("a value = "+ a);
    }

}
