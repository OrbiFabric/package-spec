# Verification、Signing 与 Trust

状态：Draft / Normative

## 1. 验证维度

`PKG-SIGN-001`：Verifier MUST 分开报告至少以下维度：Package Recognition、Tree Structure、Working Tree State、Committed Content Integrity、Version Seal、History Completeness、Evidence/Online Status。

`PKG-SIGN-002`：`DIRTY` Working Tree MUST NOT 自动等同于 committed history invalid。

`PKG-SIGN-003`：Hash integrity 通过 MUST NOT 被描述为现实世界身份已验证。

## 2. Canonical JSON

Package 2.0 复用 `orbifabric.canonical-json.v1`。

`PKG-SIGN-010`：Canonical JSON MUST 使用 UTF-8、无 BOM、无多余空白；object keys 递归按 Unicode code point 对应 UTF-8 byte lexical order 排序；strings 不进行 HTML escaping；禁止 NaN/Infinity 与 identity-critical float。

`PKG-SIGN-011`：所有签名 subject MUST 使用 domain-separated、versioned subject schema；实现不得直接签任意 UI JSON。

## 3. Version Subject

概念 subject：

```text
PackageID
PackageVersionID
Version ordinal / lineage facts
Version manifest digest
Committed content root/digests
Sealed version metadata digest
Protocol / tree profile reference
```

`PKG-SIGN-020`：Version signature MUST 绑定 canonical Version Subject，而不是 ZIP/TAR/container 的完整 bytes。

`PKG-SIGN-021`：Directory、ZIP、TAR 若表示同一 committed logical Version，MUST 可验证到同一 Version Subject digest。

## 4. Signer Profile

Package 2.0 延续 OrbiPack/Packtell 已有 `PackageSigner` 抽象。

标准 signer types 至少包括：

- `local_device`
- `orbifabric_official`

`PKG-SIGN-030`：无 Cloud official signer 时，Packtell Complete Profile 默认 MUST 使用本机独立 Ed25519 package-signing key；private key MUST NOT 被写入 Package。

`PKG-SIGN-031`：连接并选择可用 OrbiFabric official signing profile 时，Packtell MUST 使用 Cloud/official signer 对相同 Version Subject 签名。

`PKG-SIGN-032`：一旦某次 signing operation 已选择 signer profile，失败时 MUST NOT 静默切换为另一 signer 并伪装同一次签名成功。

`PKG-SIGN-033`：Local private key SHOULD 存于 OS secure credential store；Package 只携带验签所需 public key、fingerprint、Key ID、algorithm 与 signature metadata。

`PKG-SIGN-034`：Cloud/official signing response MUST 在客户端嵌入前验证 subject、environment、Key ID、public-key fingerprint 与 Ed25519 signature。

## 5. Trust separation

`PKG-SIGN-040`：Version Signature、Cloud Anchor、Delivery Record/Receipt、Lifecycle Witness MUST 是不同 schema/subject，不得合并成单一“valid”布尔值。

`PKG-SIGN-041`：Cloud Anchor/Witness MAY 晚于 Version 创建，且 MUST NOT 改变 Version identity。

`PKG-SIGN-042`：Verifier SHOULD 区分 local/unregistered signer、cloud-registered/official signer、unknown signer、invalid signature 与 online status。
