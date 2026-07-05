# JavaScript实现的10种排序算法

> 来源：https://www.yuque.com/xiumubai/doc/ia5etvvgidfh60zi

排序算法
●冒泡排序算法
●选择排序算法
●插入排序算法
●希尔排序算法
●归并排序算法
●快速排序算法
●堆排序算法
●计数排序算法
●桶排序算法
●基数排序算法
1、冒泡排序算法
冒泡排序（Bubble Sort）是一种简单直观的排序算法。冒泡排序算法的步骤描述如下：
●比较相邻的元素。如果第一个比第二个大，就交换他们两个。
●对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
●针对所有的元素重复以上的步骤，除了最后一个。
●持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
JavaScript实现冒泡排序算法的代码如下：
​9912345678910111213function bubbleSort(arr) {    let len = arr.length;    for (let i = 0; i < len - 1; i++) {        for (let j = 0; j < len - 1 - i; j++) {            if (arr[j] > arr[j+1]) {        // 相邻元素两两对比                let temp = arr[j+1];        // 元素交换                arr[j+1] = arr[j];                arr[j] = temp;            }        }    }    return arr;}2、选择排序算法
选择排序是一种简单直观的排序算法，无论什么数据进去都是 O(n²) 的时间复杂度。选择排序算法的步骤描述如下：
●首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
●再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
●重复第二步，直到所有元素均排序完毕。
JavaScript实现选择排序算法的代码如下：
​9912345678910111213141516function selectionSort(arr) {    let len = arr.length;    let minIndex, temp;    for (let i = 0; i < len - 1; i++) {        minIndex = i;        for (let j = i + 1; j < len; j++) {            if (arr[j] < arr[minIndex]) {     // 寻找最小的数                minIndex = j;                 // 将最小数的索引保存            }        }        temp = arr[i];        arr[i] = arr[minIndex];        arr[minIndex] = temp;    }    return arr;}3、插入排序算法
插入排序是一种最简单直观的排序算法，它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。插入排序算法的步骤描述如下：将第一待排序序列第一个元素看做一个有序序列，把第二个元素到最后一个元素当成是未排序序列。从头到尾依次扫描未排序序列，将扫描到的每个元素插入有序序列的适当位置。（如果待插入的元素与有序序列中的某个元素相等，则将待插入元素插入到相等元素的后面。）JavaScript实现插入排序算法的代码如下：
​991234567891011121314function insertionSort(arr) {    let len = arr.length;    let preIndex, current;    for (let i = 1; i < len; i++) {        preIndex = i - 1;        current = arr[i];        while(preIndex >= 0 && arr[preIndex] > current) {            arr[preIndex+1] = arr[preIndex];            preIndex--;        }        arr[preIndex+1] = current;    }    return arr;}4、 希尔排序算法
希尔排序，也称递减增量排序算法，是插入排序的一种更高效的改进版本。希尔排序算法的步骤描述如下：选择一个增量序列 t1，t2，……，tk，其中 ti > tj, tk = 1；按增量序列个数 k，对序列进行 k 趟排序；每趟排序，根据对应的增量 ti，将待排序列分割成若干长度为 m 的子序列，分别对各子表进行直接插入排序。仅增量因子为 1 时，整个序列作为一个表来处理，表长度即为整个序列的长度。JavaScript实现希尔排序算法的代码如下：
​99123456789101112131415161718function shellSort(arr) {    let len = arr.length,        temp,        gap = 1;    while(gap < len/3) {          //动态定义间隔序列        gap =gap*3+1;    }    for (gap; gap > 0; gap = Math.floor(gap/3)) {        for (let i = gap; i < len; i++) {            temp = arr[i];            for (let j = i-gap; j >= 0 && arr[j] > temp; j-=gap) {                arr[j+gap] = arr[j];            }            arr[j+gap] = temp;        }    }    return arr;}5、归并排序算法
归并排序（Merge sort）是建立在归并操作上的一种有效的排序算法。归并排序算法的步骤描述如下：
申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列；
设定两个指针，最初位置分别为两个已经排序序列的起始位置；
比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置；
重复步骤 3 直到某一指针达到序列尾；
将另一序列剩下的所有元素直接复制到合并序列尾。
JavaScript实现归并排序算法的代码如下：
​99123456789101112131415161718192021222324252627function mergeSort(arr) {  // 采用自上而下的递归方法    let len = arr.length;    if(len < 2) {        return arr;    }    let middle = Math.floor(len / 2),        left = arr.slice(0, middle),        right = arr.slice(middle);    return merge(mergeSort(left), mergeSort(right));} function merge(left, right){    let result = [];    while (left.length && right.length) {        if (left[0] <= right[0]) {            result.push(left.shift());        } else {            result.push(right.shift());        }    }    while (left.length)        result.push(left.shift());    while (right.length)        result.push(right.shift());    return result;}6、 快速排序算法
快速排序是由东尼·霍尔所发展的一种排序算法。它是处理大数据最快的排序算法之一。快速排序是一种分而治之思想在排序算法上的典型应用。本质上来看，快速排序应该算是在冒泡排序基础上的递归分治法。快速排序算法的步骤描述如下：
从数列中挑出一个元素，称为 “基准”（pivot）;
重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作；
递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序；
递归的最底部情形，是数列的大小是零或一，也就是永远都已经被排序好了。虽然一直递归下去，但是这个算法总会退出，因为在每次的迭代（iteration）中，它至少会把一个元素摆到它最后的位置去。
JavaScript实现快速排序算法的代码如下：
​9912345678910111213141516171819202122232425262728293031323334
function quickSort(arr, l, r) {  let len = arr.length,      partitionIndex,      left = typeof l != 'number' ? 0 : l,      right = typeof r != 'number' ? len - 1 : r;
  if (left < right) {      partitionIndex = partition(arr, left, right);      quickSort(arr, left, partitionIndex-1);      quickSort(arr, partitionIndex+1, right);  }  return arr;}
function partition(arr, left ,right) {     // 分区操作  let pivot = left,                      // 设定基准值（pivot）      index = pivot + 1;  for (let i = index; i <= right; i++) {      if (arr[i] < arr[pivot]) {          swap(arr, i, index);          index++;      }          }  swap(arr, pivot, index - 1);  return index-1;}
function swap(arr, i, j) {  let temp = arr[i];  arr[i] = arr[j];  arr[j] = temp;}
7、堆排序算法
堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。堆排序算法的步骤描述如下：创建一个堆 H[0……n-1]；把堆首（最大值）和堆尾互换；把堆的尺寸缩小 1，并调用 shift_down(0)，目的是把新的数组顶端数据调整到相应位置；重复步骤 2，直到堆的尺寸为 1。JavaScript实现堆排序算法的代码如下：let len;    因为声明的多个函数都需要数据长度，所以把len设置成为全局变量
​99123456789101112131415161718192021222324252627282930313233343536function buildMaxHeap(arr) {   // 建立大顶堆    len = arr.length;    for (let i = Math.floor(len/2); i >= 0; i--) {        heapify(arr, i);    }} function heapify(arr, i) {     // 堆调整    let left = 2 * i + 1,        right = 2 * i + 2,        largest = i;     if (left < len && arr[left] > arr[largest]) {        largest = left;    }     if (right < len && arr[right] > arr[largest]) {        largest = right;    }     if (largest != i) {        swap(arr, i, largest);        heapify(arr, largest);    }} function swap(arr, i, j) {    let temp = arr[i];    arr[i] = arr[j];    arr[j] = temp;} function heapSort(arr) {    buildMaxHeap(arr);     for (let i = arr.length-1; i > 0; i--) {8、计数排序算法
计数排序的核心在于将输入的数据值转化为键存储在额外开辟的数组空间中。作为一种线性时间复杂度的排序，计数排序要求输入的数据必须是有确定范围的整数。JavaScript实现计数排序算法的代码如下：
​99123456789101112131415161718192021function countingSort(arr, maxValue) {    let bucket = new Array(maxValue+1),        sortedIndex = 0;        arrLen = arr.length,        bucketLen = maxValue + 1;     for (let i = 0; i < arrLen; i++) {        if (!bucket[arr[i]]) {            bucket[arr[i]] = 0;        }        bucket[arr[i]]++;    }     for (let j = 0; j < bucketLen; j++) {        while(bucket[j] > 0) {            arr[sortedIndex++] = j;            bucket[j]--;        }    }     return arr;}9、桶排序算法
桶排序是计数排序的升级版。它利用了函数的映射关系，高效与否的关键就在于这个映射函数的确定。JavaScript实现桶排序算法的代码如下：
​JavaScriptRun CodeCopy99123456789101112131415161718192021222324252627282930313233343536function bucketSort(arr, bucketSize) {    if (arr.length === 0) {      return arr;    }     let i;    let minValue = arr[0];    let maxValue = arr[0];    for (i = 1; i < arr.length; i++) {      if (arr[i] < minValue) {          minValue = arr[i];                // 输入数据的最小值      } else if (arr[i] > maxValue) {          maxValue = arr[i];                // 输入数据的最大值      }    }     //桶的初始化    let DEFAULT_BUCKET_SIZE = 5;            // 设置桶的默认数量为5    bucketSize = bucketSize || DEFAULT_BUCKET_SIZE;    let bucketCount = Math.floor((maxValue - minValue) / bucketSize) + 1;       let buckets = new Array(bucketCount);    for (i = 0; i < buckets.length; i++) {        buckets[i] = [];    }     //利用映射函数将数据分配到各个桶中    for (i = 0; i < arr.length; i++) {        buckets[Math.floor((arr[i] - minValue) / bucketSize)].push(arr[i]);    }     arr.length = 0;    for (i = 0; i < buckets.length; i++) {        insertionSort(buckets[i]);                      // 对每个桶进行排序，这里使用了插入排序        for (let j = 0; j < buckets[i].length; j++) {            arr.push(buckets[i][j]);                              }10、基数排序算法
基数排序是一种非比较型整数排序算法，其原理是将整数按位数切割成不同的数字，然后按每个位数分别比较。由于整数也可以表达字符串（比如名字或日期）和特定格式的浮点数，所以基数排序也不是只能使用于整数。
JavaScript实现基数排序算法的代码如下：
​JavaScriptRun CodeCopy99123456789101112131415161718192021222324let counter = [];function radixSort(arr, maxDigit) {    let mod = 10;    let dev = 1;    for (let i = 0; i < maxDigit; i++, dev *= 10, mod *= 10) {        for(let j = 0; j < arr.length; j++) {            let bucket = parseInt((arr[j] % mod) / dev);            if(counter[bucket]==null) {                counter[bucket] = [];            }            counter[bucket].push(arr[j]);        }        let pos = 0;        for(let j = 0; j < counter.length; j++) {            let value = null;            if(counter[j]!=null) {                while ((value = counter[j].shift()) != null) {                      arr[pos++] = value;                }          }        }    }    return arr;}
