# Conformance、Security 与 Evolution

状态：Draft / Normative

## 1. Conformance levels

标准实现级别：

- Core Reader
- Core Writer
- Complete Reader
- Complete Writer
- Verifier
- Container Codec

`PKG-CONF-001`：实现 MUST 只声明其实际通过 conformance suite 的级别。

`PKG-CONF-002`：Packtell 的正式 Package 2.0 集成目标 SHOULD 至少通过 Complete Reader、Complete Writer、Verifier、Directory Codec 与 ZIP Codec。

## 2. Shared fixtures

`PKG-CONF-010`：Go、JS、Python、PHP 或其他 SDK MUST 使用同一套语言无关 fixtures/vectors 判断兼容性。

建议 fixture：minimal-valid、complete-history、dirty-working-tree、renamed-file、modified-file、missing-object、unknown-extension、bad-signature、path-traversal、case-conflict、cloud-origin、multi-delivery。

`PKG-CONF-011`：`package-go` 是 Reference Implementation；若它与 normative spec/vector 冲突，应修复 Go 实现。

## 3. Security

`PKG-CONF-020`：Parser MUST 在读取 untrusted Package 时设置 entry count、单文件 size、总展开 size、compression ratio、JSON/NDJSON size 与 recursion/depth 等资源策略。

`PKG-CONF-021`：Verifier MUST NOT 执行 Package 内 HTML/JS/binary 来决定 Core validity。

`PKG-CONF-022`：Extract MUST 使用 no-traversal、no-overwrite/staging 与安全 commit 语义；失败不得留下被误认为成功的输出。

`PKG-CONF-023`：Private key、OAuth token、refresh token、PKCE verifier、Cloud session 与 credential MUST NOT 被写入 Package、fixture 或诊断日志。

## 4. Forward compatibility

`PKG-CONF-030`：未知 Protocol major MUST 返回 unsupported，不得猜测解析。

`PKG-CONF-031`：同 major 内未知 optional field SHOULD 被忽略但在可能时 preserve；unknown required capability MUST fail closed。

`PKG-CONF-032`：Extension、Evidence 与 event subschema SHOULD 独立版本化，避免局部变化机械升级整个 Package major。

## 5. Migration 与协议升级

`PKG-CONF-040`：Protocol migration event MUST 与 PackageVersion 业务版本分离；仅协议结构升级且 logical state 不变时 SHOULD NOT 创建新的业务 PackageVersion。

`PKG-CONF-041`：从 2.x 升级到未来 major 时，任何 destructive migration MUST 由新 major 的独立规范定义；2.0 不预授权静默破坏历史。
