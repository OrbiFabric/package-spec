# Delivery、Witness 与 Evidence

状态：Draft / Normative

## 1. Delivery 是独立 lifecycle aggregate

`PKG-DELIVERY-001`：Delivery MUST 引用确定的 `package_id` 与 `package_version_id`；Delivery MUST NOT 定义 Package 或 Version identity。

`PKG-DELIVERY-002`：同一 PackageVersion MAY 有多个 Delivery，每个 Delivery MUST 拥有独立 `delivery_id`。

`PKG-DELIVERY-003`：正式 Delivery MUST 引用可验证的 signed Version Subject；Dirty Working Tree MUST 先形成新的 committed Version。

## 2. Portable Delivery history

Complete Profile MAY 保存：

```text
.packtell/evidence/
├── deliveries/<delivery_id>/delivery.json
└── objects/<evidence_id>.json
```

[精确合同](10-implementation-contracts.md)：`PKG-CONTRACT-015`；不保存 verifier cache。

`PKG-DELIVERY-010`：`delivery.json` SHOULD 保存 recipient/purpose/channel/time 等 portable business facts，但 MUST 避免不必要的 secret 与 credential。

`PKG-DELIVERY-011`：Delivery 中用于证明 Package 的签名 MUST 最终指向/验证该 Delivery 所引用 PackageVersion 的 Version Seal；它 MUST NOT 通过签 ZIP bytes 取代 Version Subject。

`PKG-DELIVERY-012`：当 Cloud 产生 Delivery Record、verification capability、signed receipt 或 Lifecycle Witness 时，它们 MUST 作为独立 evidence object 保存，MUST NOT 改写已 committed Version。

## 3. Cloud Evidence

`PKG-DELIVERY-020`：Cloud Anchor、Package Witness、Lifecycle Witness、Delivery Verification Receipt MUST 使用各自 versioned schema、canonical subject 与 signing key purpose。

`PKG-DELIVERY-021`：Offline cryptographic validity 与 online current status MUST 分开报告；`revoked`、`invalidated`、`compromised` 等在线状态 MUST NOT 通过修改历史 signature bytes 表达。

`PKG-DELIVERY-022`：Complete Profile MAY 携带创建时已取得的 Cloud evidence snapshot，但 MUST NOT 宣称该 snapshot 自动代表未来在线状态。

## 4. Evidence append

`PKG-DELIVERY-030`：后续新增 Evidence MUST NOT 改变此前 PackageVersion 的 Version Subject、ContentID、VersionID 或 signature。

`PKG-DELIVERY-031`：Evidence object SHOULD 明确 issuer、subject reference、created/observed time、schema、signature/key metadata 与可选 status reference。

`PKG-DELIVERY-032`：删除或缺失 Evidence MUST NOT 将已通过的 local content integrity 自动改写为失败；Verifier 必须按维度报告。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
