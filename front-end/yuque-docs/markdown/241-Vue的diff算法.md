# Vue的diff算法

> 来源：https://www.yuque.com/xiumubai/doc/sq2c9mxnnl2cs1wg

面试官：你了解vue的diff算法吗？说说看
一、是什么

diff 算法是一种通过同层的树节点进行比较的高效算法

其有两个特点：

●比较只会在同层级进行, 不会跨层级比较
●在diff比较的过程中，循环从两边向中间比较

diff 算法在很多场景下都有应用，在 vue 中，作用于虚拟 dom 渲染成真实 dom 的新旧 VNode 节点比较

二、比较方式

diff整体策略为：深度优先，同层比较

1比较只会在同层级进行, 不会跨层级比较

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F91%2F54%2F91e9c9519a11caa0c5bf70714383f054.png&sign=de4fd8a0ba98363376c1f81e76935b38d34b62234782ca19c2781e99b197f108)

2比较的过程中，循环从两边向中间收拢

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F2d%2Fec%2F2dcd6ad5cf82c65b9cfc43a27ba1e4ec.png&sign=d5debdc2a3e32e85ab78a4d526e6922eaeaf37264e9be1525c4131da9bb16576)

下面举个vue通过diff算法更新的例子：

新旧VNode节点如下图所示：

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F80%2F6d%2F80dc339f73b186479e6d1fc18bfbf66d.png&sign=167aaef734fe44aa08d155ca682d56126637df8fc0c7078fb5d3fd480e1e440e)

第一次循环后，发现旧节点D与新节点D相同，直接复用旧节点D作为diff后的第一个真实节点，同时旧节点endIndex移动到C，新节点的 startIndex 移动到了 C

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F76%2F54%2F76032c78c8ef74047efd42c070e48854.png&sign=70b46805b0418a076a71bf306826bfa0e5abede0dc95827c848c3229f67a6ba8)

第二次循环后，同样是旧节点的末尾和新节点的开头(都是 C)相同，同理，diff 后创建了 C 的真实节点插入到第一次创建的 D 节点后面。同时旧节点的 endIndex 移动到了 B，新节点的 startIndex 移动到了 E

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F1c%2Fd7%2F1c76e7489660188d35f0a38ea8c8ecd7.png&sign=cd1df594fa9d7a850e5ea96115b9837e9a649f30f69daf66f5c3f378c4b2bc7e)

第三次循环中，发现E没有找到，这时候只能直接创建新的真实节点 E，插入到第二次创建的 C 节点之后。同时新节点的 startIndex 移动到了 A。旧节点的 startIndex 和 endIndex 都保持不动

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F4b%2F08%2F4b622c0d61673ec5474465d82305d308.png&sign=88644e624db292d60dc41abc06ae69f2bb4ce391ba87a269fcff79fe854ac55d)

第四次循环中，发现了新旧节点的开头(都是 A)相同，于是 diff 后创建了 A 的真实节点，插入到前一次创建的 E 节点后面。同时旧节点的 startIndex 移动到了 B，新节点的startIndex 移动到了 B

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F59%2Fb4%2F5982417c3e0b2fa9ae940354a0e67ab4.png&sign=a8ad764204d965d841a7f1af74a8cd492797db9b152b8142140f8c1d9a66e581)

第五次循环中，情形同第四次循环一样，因此 diff 后创建了 B 真实节点 插入到前一次创建的 A 节点后面。同时旧节点的 startIndex移动到了 C，新节点的 startIndex 移动到了 F

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2F16%2F86%2F16cf0ef90f6e19d26c0ddffeca067e86.png&sign=a3d0844c221977f6eb52100e4b6d7329e3fca70164282178c5e18bc6f770e9ab)

新节点的 startIndex 已经大于 endIndex 了，需要创建 newStartIdx 和 newEndIdx 之间的所有节点，也就是节点F，直接创建 F 节点对应的真实节点放到 B 节点后面

![](/api/filetransfer/images?url=https%3A%2F%2Fstatic001.infoq.cn%2Fresource%2Fimage%2Fdc%2Fad%2Fdc215b45682cf6c9cc4700a5425673ad.png&sign=5127b5d79f96ce3c3dcd9d5086288e9d9f3c7c1e004a752ceff66c7ef41b01aa)

三、原理分析

当数据发生改变时，set方法会调用Dep.notify通知所有订阅者Watcher，订阅者就会调用patch给真实的DOM打补丁，更新相应的视图

源码位置：src/core/vdom/patch.js

patch函数前两个参数位为oldVnode 和 Vnode ，分别代表新的节点和之前的旧节点，主要做了四个判断：

●没有新节点，直接触发旧节点的destory钩子
●没有旧节点，说明是页面刚开始初始化的时候，此时，根本不需要比较了，直接全是新建，所以只调用 createElm
●旧节点和新节点自身一样，通过 sameVnode 判断节点是否一样，一样时，直接调用 patchVnode去处理这两个节点
●旧节点和新节点自身不一样，当两个节点不一样的时候，直接创建新节点，删除旧节点

下面主要讲的是patchVnode部分

patchVnode主要做了几个判断：

●新节点是否是文本节点，如果是，则直接更新dom的文本内容为新节点的文本内容
●新节点和旧节点如果都有子节点，则处理比较更新子节点
●只有新节点有子节点，旧节点没有，那么不用比较了，所有节点都是全新的，所以直接全部新建就好了，新建是指创建出所有新DOM，并且添加进父节点
●只有旧节点有子节点而新节点没有，说明更新后的页面，旧节点全部都不见了，那么要做的，就是把所有的旧节点删除，也就是直接把DOM 删除

子节点不完全一致，则调用updateChildren

​JavaScriptRun CodeCopy999123456789101112131415161718192021222324252627282930313233343536function updateChildren (parentElm, oldCh, newCh, insertedVnodeQueue, removeOnly) {    let oldStartIdx = 0 // 旧头索引    let newStartIdx = 0 // 新头索引    let oldEndIdx = oldCh.length - 1 // 旧尾索引    let newEndIdx = newCh.length - 1 // 新尾索引    let oldStartVnode = oldCh[0] // oldVnode的第一个child    let oldEndVnode = oldCh[oldEndIdx] // oldVnode的最后一个child    let newStartVnode = newCh[0] // newVnode的第一个child    let newEndVnode = newCh[newEndIdx] // newVnode的最后一个child    let oldKeyToIdx, idxInOld, vnodeToMove, refElm
    // removeOnly is a special flag used only by <transition-group>    // to ensure removed elements stay in correct relative positions    // during leaving transitions    const canMove = !removeOnly
    // 如果oldStartVnode和oldEndVnode重合，并且新的也都重合了，证明diff完了，循环结束    while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {      // 如果oldVnode的第一个child不存在      if (isUndef(oldStartVnode)) {        // oldStart索引右移        oldStartVnode = oldCh[++oldStartIdx] // Vnode has been moved left
      // 如果oldVnode的最后一个child不存在      } else if (isUndef(oldEndVnode)) {        // oldEnd索引左移        oldEndVnode = oldCh[--oldEndIdx]
      // oldStartVnode和newStartVnode是同一个节点      } else if (sameVnode(oldStartVnode, newStartVnode)) {        // patch oldStartVnode和newStartVnode， 索引左移，继续循环        patchVnode(oldStartVnode, newStartVnode, insertedVnodeQueue)        oldStartVnode = oldCh[++oldStartIdx]        newStartVnode = newCh[++newStartIdx]
      // oldEndVnode和newEndVnode是同一个节点
while循环主要处理了以下五种情景：

●当新老 VNode 节点的 start 相同时，直接 patchVnode ，同时新老 VNode 节点的开始索引都加 1
●当新老 VNode 节点的 end相同时，同样直接 patchVnode ，同时新老 VNode 节点的结束索引都减 1
●当老 VNode 节点的 start 和新 VNode 节点的 end 相同时，这时候在 patchVnode 后，还需要将当前真实 dom 节点移动到 oldEndVnode 的后面，同时老 VNode 节点开始索引加 1，新 VNode 节点的结束索引减 1
●当老 VNode 节点的 end 和新 VNode 节点的 start 相同时，这时候在 patchVnode 后，还需要将当前真实 dom 节点移动到 oldStartVnode 的前面，同时老 VNode 节点结束索引减 1，新 VNode 节点的开始索引加 1
●如果都不满足以上四种情形，那说明没有相同的节点可以复用，则会分为以下两种情况：
○从旧的 VNode 为 key 值，对应 index 序列为 value 值的哈希表中找到与 newStartVnode 一致 key 的旧的 VNode 节点，再进行patchVnode，同时将这个真实 dom移动到 oldStartVnode 对应的真实 dom 的前面
○调用 createElm 创建一个新的 dom 节点放到当前 newStartIdx 的位置

小结

●当数据发生改变时，订阅者watcher就会调用patch给真实的DOM打补丁
●通过isSameVnode进行判断，相同则调用patchVnode方法
●patchVnode做了以下操作：
○找到对应的真实dom，称为el
○如果都有都有文本节点且不相等，将el文本节点设置为Vnode的文本节点
○如果oldVnode有子节点而VNode没有，则删除el子节点
○如果oldVnode没有子节点而VNode有，则将VNode的子节点真实化后添加到el
○如果两者都有子节点，则执行updateChildren函数比较子节点
●updateChildren主要做了以下操作：
○设置新旧VNode的头尾指针
○新旧头尾指针进行比较，循环向中间靠拢，根据情况调用patchVnode进行patch重复流程、调用createElem创建一个新节点，从哈希表寻找 key一致的VNode 节点再分情况操作

参考文献

●[https://juejin.cn/post/6881907432541552648#heading-1](https://juejin.cn/post/6881907432541552648#heading-1)
●[https://www.infoq.cn/article/udlcpkh4iqb0cr5wgy7f](https://www.infoq.cn/article/udlcpkh4iqb0cr5wgy7f)
