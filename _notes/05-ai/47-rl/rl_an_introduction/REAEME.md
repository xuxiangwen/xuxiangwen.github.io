# 强化学习导论

本文摘自《[Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)》（第二版）[中文翻译](https://rl.qiwihui.com/zh_CN/latest/index.html)。

目前最新英文版见http://incompleteideas.net/book/RLbook2020.pdf

## Chapter 1 Introduction

*强化学习*，更侧重于从交互中进行目标导向的学习，而不是其他机器学习方法。（reinforcement learning, is much more focused on goal-directed learning from interaction than are other approaches to machine learning）

从交互中学习，是强化学习的重要特征。

### Reinforcement Learning

强化学习有如下特征：

- 如何权衡探索（Exploration）与利用（Exploitation）之间的关系 （the trade-off between exploration and exploitation）。

  为了获得大量奖励，强化学习个体必须倾向于过去已经尝试过并且能够有效获益的行动。 但是要发现这样的行为，它必须尝试以前没有选择过的行为。 个体必须充分 *利用* 它既有经验以获得收益，但它也必须 *探索*，以便在未来做出更好的动作选择。 困境在于，任何探索和利用都难以避免失败。 个体必须尝试各种动作，逐步地选择那些看起来最好的动作。 在随机任务中，每一个动作必须经过多次尝试才能得到可靠的预期收益。

- 明确地考虑了目标导向的个体（agent）与不确定环境（environment）相互作用的 *整个* 问题（whole problem），而不是其中的孤立的子问题（subproblems）。而很多其他学习方法大多仅仅考虑孤立的子问题。

next： 1.2 Examples



