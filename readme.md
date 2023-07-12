
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
