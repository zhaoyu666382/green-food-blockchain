<template>
  <div class="about-wrap">
    <section class="hero">
      <h1>关于平台</h1>
      <p class="desc">
        本平台聚焦“绿色食品交易 + 区块链可信溯源”，让消费者买得放心、农户卖得省心、管理更高效。
      </p>
      <div class="tags">
        <span class="tag">链上存证</span>
        <span class="tag">批次溯源</span>
        <span class="tag">绿色认证</span>
        <span class="tag">透明交易</span>
      </div>
    </section>

    <section class="card">
      <div class="card-title">核心能力</div>
      <ul class="list">
        <li><b>全流程溯源</b>：记录种植、采摘、检测、运输、入库与销售关键事件，扫码即可查询。</li>
        <li><b>防篡改存证</b>：关键数据写入区块链，生成链上哈希，提升可信度。</li>
        <li><b>角色协同</b>：管理端、农户端、用户端分工明确，流程闭环。</li>
        <li><b>安全与隐私</b>：对敏感信息进行最小化披露与权限控制。</li>
      </ul>
      <div class="muted">建议：可结合真实农场/合作社数据进行演示，效果更佳。</div>
    </section>
  </div>
</template>

<style scoped>
.about-wrap{ max-width: 960px; margin: 0 auto; padding: 18px; }
.hero{
  padding: 22px 18px;
  border-radius: var(--radius2);
  border: 1px solid var(--border);
  background: rgba(255,255,255,.78);
  box-shadow: var(--shadow2);
  margin-bottom: 16px;
}
h1{ margin: 0 0 10px; font-size: 22px; }
.desc{ margin: 0 0 14px; color: var(--muted); line-height: 1.7; }
.tags{ display:flex; gap:10px; flex-wrap:wrap; }
.tag{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(34,197,94,.10);
}
.list{ margin: 0; padding-left: 18px; color: var(--text); line-height: 1.75; }
.list b{ color: var(--primary); }
</style>
