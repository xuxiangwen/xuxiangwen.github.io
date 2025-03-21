# Machine Learning Yearning

Technical Strategy for AI Engineers in the Era of Deep Learning.

**Github**：*https://github.com/deeplearning-ai/machine-learning-yearning-cn*

**在线阅读**：*https://deeplearning-ai.github.io/machine-learning-yearning-cn/docs/home/*

**中文版**：https://github.com/deeplearning-ai/machine-learning-yearning-cn/releases

## [Getting Started](https://deeplearning-ai.github.io/machine-learning-yearning-cn/docs/ch02/#collapse-1)

### 机器学习为什么需要策略

案例：建立猫咪图片初创公司

想象一下，你正在建立一家初创公司，这家公司的产品目标是为猫咪爱好者们提供数不尽的猫咪图片，你打算应用**神经网络（neural network）**技术来构建一套计算机视觉系统，通过该系统来识别图片中的猫。

![img](images/ch01_cats.jpg)

但悲剧的是，目前你的学习算法准确度还不够好。为了改进这个猫咪检测器，你正面临着巨大的压力。可你该怎么做呢？

你的团队给出了许多建议，例如：

- 获取更多的数据，即收集更多的猫咪图片
- 收集更加多样化的训练数据集，图片中猫的位置可能不常见，也有可能颜色奇异，或者拍摄时使用不同的相机参数
- 通过增加梯度下降的迭代次数，使算法训练得久一些
- 尝试一个拥有更多层/更多隐藏元/更多参数的，规模更大的神经网络
- 尝试一个更小的神经网络
- 尝试加入正则化（例如 L2 正则化）
- 改变神经网络的架构（激活函数，隐藏元数量等等）
- …

在上面众多的方向中：

- 如果你做出了正确的选择，就将建立起一个效果领先的猫咪图片识别平台，并带领你的公司取得成功。
- 如果你选择了一个糟糕的方向，则可能因此浪费掉几个月的时间。

### 规模驱动机器学习发展

关于深度学习（神经网络）的一些想法在几十年前就有了，那为什么它们到现在才流行起来了呢？

推动其近期发展的主要因素有两个：

- **数据可用性（data availability）**：如今人们在数字设备（笔记本电脑、移动设备等）上花费的时间越来越多，对应的数字化行为与活动产生了海量的数据，而这些数据都可以提供给我们的学习算法用来训练。
- **计算规模（computational scale）**：在近几年前，我们才开始有能力训练出规模足够大的神经网络来使用现有的海量数据集。

然后， 即使你积累了更多的数据，但应用在类似于logistic regression这样较传统的学习算法上，其性能表现（performance）也将趋于 “平稳” 。这意味着算法的学习曲线将 “变得平缓” ，就算提供更多的数据，算法的性能也将不再提升。

![img](images/ch04_01.png)

在同样的监督学习任务下，选择训练一个小型的神经网络（只含有少量的隐藏元/层/参数的神经网络），你可能会获得较好的性能表现：

![img](images/ch04_02.png)

> 该图显示了在小数据集上应用神经网络的效果会更好。在小数据集情况下，传统算法是否会表现得更好，取决于人们如何进行特征选择工程。但如果数据集很大，比如有 100 万个样本数据，神经网络一般是更好的选择。

随着数据量的增加，训练的神经网络规模越来越大，最终往往更好：

![img](images/ch04_03.png)

因此，为了获得最佳的性能表现，你可以这样做：

1. 训练大型的神经网络，效果如同上图的绿色曲线；
2. 拥有海量的数据。

> 在算法训练时，许多其它的细节也同等重要，例如神经网络的架构。但目前来说，提升算法性能的更加可靠的方法仍然是训练更大的网络以及获取更多的数据。

## [Setting up development and test sets](https://deeplearning-ai.github.io/machine-learning-yearning-cn/docs/ch02/#collapse-2)

### 开发集和测试集的定义

继续之前的案例：现在你负责运营一个移动端 app，用户会向这个 app 上传许多不同内容的图片。而你希望这个 app 能够从图片中自动地找到含有猫的图片。

你的团队已经在不同的网站下载了含有猫的图片（正样本，又译作正例），以及不含猫的图片（负样本，又译作反例），从而得到了一个巨型的数据集。他们将数据集按照 70% / 30% 的比例划分为训练集（training set）和测试集（test set），并且使用这些数据构建出了一个在训练集和测试集上均表现良好的猫咪检测器。

可当你将这个分类器（classifier）部署到移动应用中时，却发现它的性能相当之差！

这究竟是什么原因导致的呢？

你会发现，从网站上下载下来作为训练集的图片与用户上传的图片有较大的区别——用户上传的图片大部分是使用手机拍摄的，此类图片往往分辨率较低，且模糊不清，采光也不够理想。但由于用来进行训练和测试的数据集图片均取自网站，这就导致了算法不能够很好地泛化（generalize）到我们所关心的手机图片的实际分布（actual distribution）情况上。

机器学习中，通常我们有三个数据集。

- **训练集（training set）**用于训练模型。
- **开发集（development set）**用于调整参数，选择特征，以及对学习算法作出其它决定。有时也称为**留出交叉验证集（hold-out cross validation set）**。也称验证集（validation set）。
- **测试集（test set）**用于评估算法的性能，但不会据此改变学习算法或参数。

我们的任务是保证训练集，开发集，测试集在分布上的一致性。

现实的情况或许是：你尚未推出移动端 app，还没有任何的用户，因此也无法获取一些准确的反馈数据来为后续的行动提供依据。但你仍然能够尝试去模拟出这种情况，例如邀请你的朋友用手机拍下照片并发送给你。当你的 app 上线后，就能够使用实际的用户数据对开发集和测试集进行更新。

### 开发集和测试集应该服从同一分布

根据公司的核心市场分布情况，你将猫咪 app 的图像数据划分为 “美国” 、 “中国” 、 “印度” 和 “其它地区” 四个区域。在设立开发集和测试集时，可以尝试将 “美国” 和 “印度” 的数据归于开发集，而 “中国” 和 “其它地区” 的数据归于测试集。也就是说我们可以随机地将其中两个区域的数据分配给开发集，另外两个区域的数据分配给测试集。这样做可能产生严重的过拟合：

- 算法仅仅在开发集上表现良好，却在测试集上表现不佳
- 算法仅仅在其中的两个上表现出色，而另外两个表现一般。

### 开发集和测试集应该有多大？

开发集的规模应该尽可能的大，至少要能够区分出你所尝试的不同算法之间的性能差异。例如，如果分类器 A 的准确率为 90.0% ，而分类器 B 的准确率为 90.1% ，那么使用仅含有 100 个样本的开发集将无法检测出这 0.1% 的差异。通常来说，开发集的规模应该在 1,000 到 10,000 个样本数据之间，而当开发集样本容量为 10,000 时，你将很有可能检测到这 0.1% 的性能提升。

在类似广告服务、网络搜索和产品推荐等较为成熟且关键的应用领域，我曾见过一些团队非常积极地去改进算法性能，哪怕只有 0.01% 的提升，因为这将直接影响到公司的利润。在这种情况下，开发集规模可能远超过 10,000 个样本，从而有利于检测到那些不易察觉的效果提升。

那么测试集的大小又该如何确定呢？它的规模应该大到使你能够对整体系统的性能进行一个高度可信的评估。我们的策略是：

- 当数据集<=10,000 个样本，常见的策略是采用 30% 的数据用作测试集。
- 当数据量非常大（比如：超过10亿），测试集的比例可以大大降低。

### 使用单值评估指标进行优化

所谓的**单值评估指标（single-number evaluation metric）**有很多，分类准确率就是其中的一种。根据这个指标，如果分类器 A 的准确率为 97％，而分类器 B 的准确率为 90%，那么可以认为分类器 A 更优秀。

相比之下，**精度**（Precision）和**召回率**（Recall）的组合并不能作为单值评估指标，因为它给出了两个值来对你的分类器进行评估。

| Classifier | Precision | Recall |
| :--------- | :-------- | :----- |
| A          | 95%       | 90%    |
| B          | 98%       | 85%    |

若根据上方表格中的数值对两个分类器进行比较，显然二者都没有较为明显的优势，因此也无法指导你立即做出选择。

为了解决这个问题，计算 “F1 score” ，这是一种经过修正的平均值计算方法，效果或许更好。

| Classifier | Precision | Recall | F1 score  |
| :--------- | :-------- | :----- | :-------- |
| A          | 95%       | 90%    | **92.4%** |
| B          | 98%       | 85%    | **91.0%** |

$$ F1 =  \frac  {2 \cdot Precision \cdot  Recall }  { Precision + Recall  }$$

### 优化指标和满意度指标

下面我们来了解一下组合多个评估指标的另一种方法。

假设你既关心学习算法的准确率（accuracy），又在意其运行时间（running time），请从下面的三个分类器中做出选择：

| Classifier | Accuracy | Running time |
| :--------- | :------- | :----------- |
| A          | 90%      | 80ms         |
| B          | 92%      | 95ms         |
| C          | 95%      | 1,500ms      |

将准确率和与运行时间放入单个公式计算后可以导出单个的指标，这似乎不太符合常理，例如：

有一种替代方案可供选择：首先定义一个 “可接受的” 运行时间，一般低于 100ms 。接着，在限定的运行时间范围内，尽可能地将分类器的准确率最大化。此时，运行时间代表着 “满意度指标” —— 你的分类器必须在这个指标上表现得 “足够好” ，这里指的是运行时间约束上限为 100ms；而准确度则代表着 “优化指标”。

如果要考虑 $ N $ 项不同的标准，比如模型的二进制文件大小（这对移动端 app 尤为重要，因为用户不想下载体积很大的 app）、运行时间和准确率，你或许需要设置 $ N-1 $ 个 “满意度” 指标，即先要求它们满足一定的值或范围，下一步才是定义一个 “优化” 指标。例如分别为二进制文件的大小和运行时间设定可接受的阈值，并尝试根据这些限制来优化准确率指标。

最后再举一个例子，假设你正在设计一个硬件设备，该设备可以根据用户设置的特殊 “唤醒词” 来唤醒系统，类似于 Amazon Echo 的监听词为 “Alexa”，苹果（Apple） Siri 的监听词为 “Hey Siri”，安卓（Android） 的监听词为 “Okay Google”，以及百度（Baidu）应用的监听词 “Hello Baidu.” 我们关心的指标是假正例率（false positive rate，又译作假阳率，误诊率）—— 用户没有说出唤醒词，系统却被唤醒了，以及假反例率（false negative rate，又译作假阴率，漏诊率）——用户说出了唤醒词，系统却没能正确被唤醒。这个系统的一个较为合理的优化对象是尝试去最小化假反例率（优化指标），减少用户说出唤醒词而系统却没能正确唤醒的发生率，同时设置约束为每 24 小时不超过一次误报（满意度指标）。

一旦你的团队在优化评估指标上保持一致，他们将能够取得更快的进展。

### 通过开发集和度量指标加速迭代

对于当前面临的新问题，我们很难提前知道使用哪种方法会是最合适的，即使是一个经验丰富的机器学习研究员，通常也需要在尝试多种多样的方法之后才能发现令人满意的方案。当我要建立一个机器学习系统时，往往会这么做：

1. 尝试一些关于系统构建的**想法（idea）**。
2. 使用**代码（code）**实现想法。
3. 根据**实验（experiment）**结果判断想法是否行得通。（第一个想到的点子一般都行不通！）在此基础上学习总结，从而产生新的想法，并保持这一迭代过程。迭代过程如下图所示：

![img](images/ch10_01.png)

迭代过程循环得越快，你也将进展得越快。

### 小结：建立开发集和测试集

- 保证开发集和测试集的数据分布一致，而这两个数据集和训练集的数据分布不一定一致。
- 为你的团队选择一个单值评估指标进行优化。当需要考虑多项目标时，不妨将它们整合到一个表达式里（比如对多个误差指标取平均），或者设定满意度指标和优化指标。
- 机器学习是一个高度迭代的过程：在出现最终令人满意的方案之前，你可能要尝试很多想法。
- 当你要探索一个全新的应用时，尽可能在一周内建立你的开发集、测试集和评估指标；而在已经相对成熟的应用上，可以考虑花费更长的时间来执行这些工作。
- 传统的 70% / 30% 训练集/测试集划分对于大规模数据并不适用，实际上，开发集和测试集的比例会远低于 30%.
- 开发集的规模应当大到能够检测出算法精度的细微改变，但也不需要太大；测试集的规模应该大到能够使你能对系统的最终性作出一个充分的估计。
- 当开发集和评估指标对于团队已经不能提供一个正确的导向时，尽快修改它们：
  - 如果算法在开发集上过拟合，则需要获取更多的开发集数据。
  - 如果开发集与测试集的数据分布和实际数据分布不同，则需要获取新的开发集和测试集
  - 如果评估指标无法对最重要的任务目标进行度量，则需要修改评估指标。

## [Basic Error Analysis](https://deeplearning-ai.github.io/machine-learning-yearning-cn/docs/ch13/#collapse-3)

 快速构建并迭代你的第一个系统

当你想要构建一个新的垃圾邮件过滤系统时，团队可能会有各式各样不同的想法：

- 收集海量的垃圾邮件作为训练集。例如，设置一个 “蜜罐（honeypot，计算机安全领域又称为诱饵）”，故意地向垃圾邮件系统发送一些虚假邮件地址，以便于能够自动收集到垃圾邮件系统发送到这些地址的垃圾邮件内容。
- 开发用于理解邮件文本内容的功能。
- 开发用于理解邮件信封或邮件头部特征的功能，据此了解邮件经由了哪些网络服务器进行中转。
- 更多…

虽然我在反垃圾邮件领域已经有了一定的经验，却依然难以保证每次都能顺利在上面的方向中进行抉择。如果你在此领域并不是一个专家，难度会变得更大。

**如果在一开始就试图设计和构建出完美的系统会显得有些困难，不妨先花几天时间构建并训练一个最基础的系统。**

### 误差分析：根据开发集样本评估想法

在使用猫咪 app 时，你注意到它将一些狗的图片误分类为猫了，因为有些狗的样子的确很像猫。

团队中有人建议，加入第三方软件来帮助系统更好地处理狗的样本，但这需要一个月的时间去完成。面对团队成员高涨的热情，你会允许他们这样做吗？

在执行这项计划前，我建议你先预估一下该任务能提升多少系统精度。这样你就能够更加理性地判断是否值得花一个月的时间做这件事，还是将这段时间用于其它任务。

具体而言，你可以这样：

1. 收集 100 个开发集中被误分类的样本，即造成系统误差的样本。
2. 人为查看这些样本，并计算其中狗的比例。

查看误分类样本的这一过程称为**误差分析**。在上面的例子中，如果只有 5% 误分类的图像是狗，那么无论你在狗的问题上做多少的算法改进，最终都不会消除超过原有的 5% 误差 . 也即是说 5% 是该计划项目所能起到帮助的“上限”（最大可能值）。所以如果整个系统当前的精度为 90%（对应误差为 10%），那么这种改进最多能将精度提升到 90.5% （对应误差下降到 9.5% ， 改进了原有 10% 误差其中的 5%）。

相反，如果你发现 50% 的误分类图像是狗，那就可以自信地说这个项目将效果明显，它可以将精度从 90% 提升到 95% （相对误差减少 50%，整体误差由 10% 下降到 5%）。

这种简单的误差分析计算过程可以协助你快速评估，从而了解是否需要将处理狗样本的第三方软件进行整合。它为是否值得进行这项投入给出了一个量化的基准。

误差分析也可以帮助你在不同的想法中发现哪些想法将更有前景。我见过许多工程师不愿意进行误差分析，他们更倾向于直接提出一个并实现一个想法，而不考虑该想法是否值得花时间去投入。这是一个普遍的误解：后果可能是你的团队在耗费一个月的时间后却发现收益甚少。

人为检查 100 个样本并不会占用太多的时间。即使你每分钟只检查一张图片，也能够在两小时内完成，而这两个小时可能可以帮你节省一个月的工作量。

**误差分析**（Error Analysis） 指的是检查被算法误分类的开发集样本的过程，以便帮助你找到造成这些误差的原因。这将协助你确定各个项目的优先级（就像上面的例子所提到的那样）并且获得探索新方向的灵感，我们将会在之后再讨论这些内容。接下来的几章会给出一些误差分析的最佳实践。

### 在误差分析时并行评估多个想法

对于改进猫检测器，你的团队有一些想法：

- 修正算法将狗误分类为猫的问题。
- 修正算法将大型猫科动物（比如狮子、黑豹等等,下面用大猫代指）误分类为家猫的问题。
- 改善系统在模糊图像上的表现。
- …

上述的想法都可以以并行的形式进行评估。通常我会创建一个电子表格，一边查看被误分类的 100 个开发集样本一边完善表格内容，同时我也会留下一些能够帮助我记住特定样本的备注。为了说明这一过程，如下所示是一个仅含四个样本的小型开发集的电子表格：

| 图像       | 狗   | 大猫 | 模糊 | 备注                         |
| :--------- | :--- | :--- | :--- | :--------------------------- |
| 1          | √    |      |      | 不常见的美国比特犬           |
| 2          |      |      | √    |                              |
| 3          |      | √    | √    | 狮子；雨天在动物园拍摄的图片 |
| 4          |      | √    |      | 树木后的美洲豹               |
| 占全体比例 | 25%  | 50%  | 50%  |                              |

你会发现表格中图片 3 的”大猫”与“模糊”列都被勾选了，另外由于一个样本可能与多个类别都有关联，所以表格底部的百分比加起来可能不是 100 %.

虽然你可能事先规定了一些类别（狗，大猫，模糊）并进行了手动的分类，但在浏览图像时你可能会受到启发并发现一些新的类别。比如你在浏览一些图片时发现，经过 Instagram 滤镜处理过的图片在识别时对结果造成了误差，你就可以在电子表格中加入一个新的 “Instagram” 列。手动查看误分类样本，并思考人类如何/是否能正确地分类这些样本，这将帮助你发现新的类别以及解决方案。

探寻方法去改进对应误差的类别是很有帮助的。举个例子，如果你能“撤销” Instagram 的滤镜效果并恢复到原始图片，那么 Instagram 分类就能发挥作用。这不代表你只能局限于那些已有的改进途径的类别；这个过程主要是为了帮助你对一些潜在的，有改进效果的方向培养一定的敏感度。

假设你已检查了 100 个开发集的误分类样本，并得到了下面的表格：

| 图像       | 狗   | 大猫 | 模糊 | 备注                         |
| :--------- | :--- | :--- | :--- | :--------------------------- |
| 1          | √    |      |      | 不常见的美国比特犬           |
| 2          |      |      | √    |                              |
| 3          |      | √    | √    | 狮子；雨天在动物园拍摄的图片 |
| 4          |      | √    |      | 树木后的美洲豹               |
| …          | …    | …    | …    |                              |
| 占全体比例 | 8%   | 43%  | 61%  |                              |

现在你应该可以判断出，对于解决狗的误分类问题项目最多可以改进 8% 的误差，处理大猫和模糊类则可以改进更多。因此你将更有可能挑选后两者之一进行处理。如果你的团队有足够的人力并行处理多个方向，则可以要求一部分成员处理大猫类别，另一部分成员处理模糊类别。

误差分析并不会产生一个明确的数学公式来告诉你什么任务的优先级最高。你还需要考虑在不同类别上的预期进展以及解决每个类别所需的工作量。

### 清洗误标注的开发集和测试集样本

在进行误差分析时，你可能会注意到一些开发集的样本被误标注（mislabeled ）了。此处的“误标注”指的是图像在使用算法处理前，已经被负责标注的人员进行了错误的标注，也就是说，某个样本 的分类标签（label） 的值并不正确。例如，一些不是猫的图片被误标注为猫，反之亦然。如果你不确定这些被误标注的图片是否起着关键作用，可以添加一个类别来跟踪记录误标注样本的比例：

| 图像       | 狗   | 大猫 | 模糊 | 误标注 | 备注                   |
| :--------- | :--- | :--- | :--- | :----- | :--------------------- |
| …          |      |      |      |        |                        |
| 89         |      |      |      | √      | 标注者忽略了背景中的猫 |
| 99         |      | √    |      |        |                        |
| 100        |      |      |      | √      | 猫的画像；非真猫       |
| 占全体比例 | 8%   | 43%  | 61%  | 6%     |                        |

那么这个时候，需要修正开发集中的标签吗？回忆一下当初设立开发集的目标——帮助你快速评估算法性能，从而判断算法 A 和 B 哪一个更好。如果开发集中误标注的部分的确影响了你的判断，那么花时间去修正这些标签就是值得的。

举个例子，假设你的分类器表现如下：

- 开发集整体精度…………….. 90% （10% 整体误差）
- 误标注样本造成的误差…… 0.6% （6% 开发集误差）
- 其它原因造成的误差………. 9.4% （94% 开发集误差）

相对于你正在改进的 9.4% 误差，误标记的 0.6% 误差看起来就不那么重要了。在开发集中手动修正误标注样本不会带来不好的影响，但这样的做法并不是必要的：当你不知道整个系统的误差是 10% 还是 9.4% 时，这样处理会看起来不错。

假设你不断地改进猫分类器，并达到了以下性能：

- 开发集整体精度…………….. 98.0% （2.0% 整体误差）
- 误标注样本造成的误差…… 0.6% （30% 开发集误差）
- 其它原因造成的误差………. 1.4% （70% 开发集误差）

此时 30% 的开发集误差是由误标注样本造成的，这对精度估计造成了显著的影响。此时就应该考虑改进开发集样本中的标签质量。处理这些误标注的样本将帮助你找出分类器的误差是接近 1.4% 还是 2.0% ，差异显著。

### 将大型开发集拆分为两个子集，专注其一

假设你有一个含有 5000 个样本的大型开发集，该开发集的错误率为 20% ，这意味着误分类了 1000 张开发集图片。人工手动检查这 1000 张图片会花费很长时间，所以我们在误差分析时没必要使用所有的图片。

在这种情况下，我会将开发集明确地分成两个子集

-  **Eyeball 开发集**（对于语音识别项目，则将数据集称为 Ear 开发集）

  假定准备人工检查100个误分类样本，则可以随机选择10%的样本（即500个）放入Eyeball 开发集中。

- **Blackbox 开发集**。由剩余的 4500 个样本组成。

对Eyeball 中的100个误分类样本，我们需要一一人工检查，从而得到各种错误的比例，然后根据优先级，可以对模型或数据进行优化，这时如果**Eyeball 开发集**的错误率相对**Blackbox 开发集**快速下降，这说明，**Eyeball 开发集**中的错误已经被模型修复了，还有其它错误还没有被发现，这时候需要重新建一个Eyeball 开发集，循环上面的过程。

### 小结：基础误差分析

- 当你开始一个新项目，不要在一开始就试图设计和构建一个完美的系统。相反，应尽可能快（例如在短短几天内）地构建和训练一个系统雏形。然后使用误差分析法去帮助你识别出最有前景的方向，并据此不断迭代改进你的算法。
- 通过手动检查约 100 个被算法错误分类的开发集样本来执行误差分析，并计算主要的错误类别。使用这些信息来确定优先修正哪种类型的错误。
- 考虑将开发集分为人为检查的 Eyeball 开发集和非人为检查的 Blackbox 开发集。如果在 Eyeball 开发集上的性能比在 Blackbox 开发集上好很多，说明你已过拟合 Eyeball 开发集，下一步应该考虑为其获取更多数据。

## [Bias and Variance](https://deeplearning-ai.github.io/machine-learning-yearning-cn/docs/ch20/)

###  偏差和方差：误差的两大来源

机器学习中有两个主要的误差来源：偏差和方差。

- bias：算法在训练集上的错误率。非正式称为算法的**偏差（bias）**。
- variance： 指的是算法在开发集（或测试集）上的表现比训练集上差多少。非正式称为算法的**方差（variance）**。

总误差 = 偏差（bias）+方差（variance）

假设希望构建一个错误率为 5% 的猫识别器。可能会出现如下四种情况。

- low bias，low variance：

  完美情况，说明模型取得不错的结果。比如：训练集错误率是 5%，开发集错误率为 6%。

  - bias：5%
  - variance：1% = 6% - 1%

  已经达到系统目标了。

- low bias，high variance 

  模型过拟合。比如：训练集错误率是 5%，开发集错误率为 16%。

  - bias：5%
  - variance：15% = 16% - 1%

  虽然训练集达到设计目标，但开发集还有很大差距。可能的措施有：

  - 更大的训练数据集
  - 正则化
  - 降低模型复杂度
  - 增加batch normalization和dropout。

- high bias，low variance 

  模型过拟合，还没有学习到足够好的pattern。比如：训练集错误率是 15%，开发集错误率为 16%。

  - bias：15%
  - variance：1% = 16% - 15%

  可能的措施有：

  - 增加模型的复杂度
  - 增加训练时间
  - 尝试不同的模型结构

- high bias，high variance 

  模型同时欠拟合和过拟合。比如：训练集错误率是 15%，开发集错误率为 30%。

  - bias：15%
  - variance：15% = 30% - 15%

  可能需要同时尝试high bias，low variance 和low bias，high variance 的措施。

### 与最优错误率比较

在“猫咪识别”案例中，“理想”错误率应该接近 0%。这时因为，人类总是可以识别出图片中的猫。因此，我们希望模型也能够有这样优秀的表现。

然而，对于其他机器学习问题，可能（错误率接近 0%的）难度很大。比如：构建一个语音识别系统时，发现 14% 的音频片段背景噪声太多，十分难以理解，即使是人类也无法识别出所说的内容。在这种情况下，“最优”的语音识别系统也可能约有 14% 的误差。

假设在这个语音识别问题上，模型表现如下：

- 训练集错误率 = 15%
- 开发集错误率 = 30%

我们可以看到，在训练集上的表现已经接近最优错误率 14%，几乎没有提高的空间了，然而算法没有很好地泛化到开发集上，还有很大的提升空间。

对于偏差有如下公式：
$$
偏差（bias） = 最优错误率（“不可避免偏差”）+ 可避免的偏差
$$

- **最优错误率（“不可避免偏差”）**：14%。我们假设：世界上最好的语音系统，仍会有 14% 的误差。这部分错误是不可避免的。
- **可避免偏差**：1%。即训练错误率和最优错误率之间的差值。
- **方差**：15%。即开发集错误率和训练集错误率之间的差值。

根据上面的概念，上一节high bias，切确的应该说是high 可避免偏差。

### 减少可避免偏差的技术

如果存在着很高的可避免偏差，可以尝试如下方法：

- **加大模型规模**（例如神经元/层的数量）：能够使算法更好地拟合训练集，从而减少偏差。当发现方差也同步增加时，可以加入正则化减少方差的增加。
- **根据误差分析结果修改输入特征**：假设误差分析结果显示，需要增加额外的特征。这些新的特征对处理偏差和方差都有所帮助。理论上，添加更多的特征将增大方差；当这种情况发生时，可以加入正则化来抵消方差的增加。
- **减少或者去除正则化**（L2 正则化，L1 正则化，dropout）：这将减少可避免偏差，但会增大方差。
- **修改模型架构**（比如神经网络架构）同时影响偏差和方差。

需要注意的是，**添加更多的训练数据**：对于偏差通常没有明显的影响。

### 减少方差的技术

如果存在着高方差问题，可以尝试下面的技术：

- **添加更多的训练数据**：这是最简单最可靠的一种处理方差的策略。

- **加入正则化**（L2 正则化，L1 正则化，dropout）：这项技术可以降低方差，但却增大了偏差。

- **加入提前终止**（例如根据开发集误差提前终止梯度下降）：这项技术可以降低方差但却增大了偏差。提前终止（Early stopping）有点像正则化理论，一些学者认为它是正则化技术之一。

- **通过特征选择减少输入特征的数量和种类**：这种技术或许有助于解决方差问题，但也可能增加偏差。稍微减少特征的数量（比如从 1000 个特征减少到 900 个）也许不会对偏差产生很大的影响，但显著地减少它们（比如从 1000 个特征减少到 100 个，10 倍地降低）则很有可能产生很大的影响，因为也许排除了太多有用的特征。

  在现代深度学习研究过程中，当数据充足时，特征选择的比重需要做些调整，现在我们更可能将拥有的所有特征提供给算法，并让算法根据数据来确定哪些特征可以使用。而当训练集很小的时候，特征选择是非常有用的。

- **减小模型规模**（比如神经元/层的数量）：*谨慎使用。*这种技术可以减少方差，同时可能增加偏差。然而不推荐这种处理方差的方法，添加正则化通常能更好的提升分类性能。 减少模型规模的好处是降低了计算成本，从而加快了训练模型的速度。

下面是两种额外的策略，和解决偏差问题章节所提到的方法重复：

- **根据误差分析结果修改输入特征**
- **修改模型架构**（比如神经网络架构）



