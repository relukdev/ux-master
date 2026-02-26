# Skills Stack Analysis & Improvement Plan

> **For Claude:** REQUIRED SUB-SKILL: Use sp-executing-plans to implement this plan task-by-task.

**Goal:** Đánh giá toàn bộ 59 skill hiện có, phân loại chất lượng, và lập kế hoạch bổ sung skill mới cho đa nền tảng, đa thiết bị.

**Architecture:** Phân tích theo 7 nhóm năng lực → đánh giá chất lượng/độ hoàn thiện → xác định GAP → đề xuất skill mới theo ma trận nền tảng × thiết bị.

**Tech Stack:** Markdown skills, YAML frontmatter, reference files, cross-skill linking

---

## 📊 Tổng Quan Hiện Trạng

| Metric | Value |
|--------|-------|
| **Tổng skill directories** | 59 |
| **Content skills** (knowledge-based) | 46 |
| **Workflow skills** (process-based) | 13 |
| **Skill structure** | SKILL.md + references/ (consistent) |
| **Cross-references** | ✅ Most skills link related skills |
| **Scoring system** | ✅ 0-10 rubrics on quality skills |

---

## 🗂️ Phân Loại Skill Hiện Có

### Category 1: Software Engineering (10 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `clean-code` | ⭐⭐⭐⭐⭐ | 95% | 258 lines, 6 disciplines, scoring rubric, reference files |
| `clean-architecture` | ⭐⭐⭐⭐⭐ | 95% | Dependency Rule, component principles, SOLID |
| `pragmatic-programmer` | ⭐⭐⭐⭐ | 90% | DRY, orthogonality, tracer bullets |
| `refactoring-patterns` | ⭐⭐⭐⭐ | 90% | Named transformations, smell-driven |
| `software-design-philosophy` | ⭐⭐⭐⭐ | 90% | Deep modules, information hiding |
| `domain-driven-design` | ⭐⭐⭐⭐ | 90% | Bounded contexts, aggregates, ubiquitous language |
| `release-it` | ⭐⭐⭐⭐ | 85% | Circuit breakers, bulkheads, production resilience |
| `ddia-systems` | ⭐⭐⭐⭐ | 85% | Storage engines, replication, consistency |
| `system-design` | ⭐⭐⭐⭐⭐ | 95% | 224 lines, common designs, estimation |
| `high-perf-browser` | ⭐⭐⭐⭐ | 85% | Network, rendering, Core Web Vitals |

**Assessment:** ✅ **Mạnh nhất.** Đầy đủ từ code quality → architecture → distributed systems. Thiếu: Testing strategies chuyên sâu, DevOps/CI-CD, Security.

---

### Category 2: UI/UX Design (8 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `ux-master` | ⭐⭐⭐⭐⭐ | 95% | 701 lines, 48 UX laws, 37 tests, 17 stacks, harvester v4 |
| `top-design` | ⭐⭐⭐⭐⭐ | 95% | 447 lines, 7 pillars, scoring rubric, case studies |
| `refactoring-ui` | ⭐⭐⭐⭐ | 90% | Visual hierarchy, spacing, color, depth |
| `ux-heuristics` | ⭐⭐⭐⭐ | 85% | Nielsen's 10, severity ratings, info architecture |
| `design-everyday-things` | ⭐⭐⭐⭐ | 85% | Affordances, signifiers, constraints, feedback |
| `microinteractions` | ⭐⭐⭐⭐ | 85% | Triggers, rules, feedback, loops & modes |
| `web-typography` | ⭐⭐⭐⭐ | 85% | Font pairing, web font loading, responsive type |
| `ios-hig-design` | ⭐⭐⭐⭐ | 85% | iOS HIG, SwiftUI, UIKit, Dynamic Island |

**Assessment:** ✅ **Rất mạnh** cho web và iOS. Thiếu: Android Material Design, Design tokens spec, Figma/design tools workflows, Accessibility chuyên sâu.

---

### Category 3: Marketing & Growth (11 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `one-page-marketing` | ⭐⭐⭐⭐ | 85% | Full customer journey, PVP Index |
| `storybrand-messaging` | ⭐⭐⭐⭐ | 85% | Customer-as-hero narrative |
| `made-to-stick` | ⭐⭐⭐⭐ | 85% | SUCCESs checklist |
| `contagious` | ⭐⭐⭐⭐ | 85% | STEPPS framework, virality |
| `influence-psychology` | ⭐⭐⭐⭐ | 85% | Cialdini's 6 principles |
| `cro-methodology` | ⭐⭐⭐⭐ | 85% | Conversion rate, A/B testing |
| `scorecard-marketing` | ⭐⭐⭐⭐ | 80% | Quiz/assessment funnels |
| `hundred-million-offers` | ⭐⭐⭐⭐ | 85% | Value Equation, offer design |
| `blue-ocean-strategy` | ⭐⭐⭐⭐ | 85% | ERRC framework, value innovation |
| `crossing-the-chasm` | ⭐⭐⭐⭐ | 85% | Tech adoption lifecycle |
| `obviously-awesome` | ⭐⭐⭐⭐ | 85% | Product positioning |

**Assessment:** ✅ **Toàn diện.** Đầy đủ chiến lược marketing. Thiếu: Growth hacking / PLG, SEO/Content marketing, Email marketing automation, Analytics/Attribution.

---

### Category 4: Product Management (7 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `inspired-product` | ⭐⭐⭐⭐ | 85% | Empowered teams, dual-track |
| `continuous-discovery` | ⭐⭐⭐⭐ | 85% | Opportunity Solution Trees |
| `lean-startup` | ⭐⭐⭐⭐ | 85% | Build-Measure-Learn, MVP |
| `lean-ux` | ⭐⭐⭐⭐ | 85% | Hypothesis-driven design |
| `design-sprint` | ⭐⭐⭐⭐ | 85% | 5-day prototype & test |
| `jobs-to-be-done` | ⭐⭐⭐⭐ | 85% | Customer jobs analysis |
| `mom-test` | ⭐⭐⭐⭐ | 85% | Customer interview technique |

**Assessment:** ✅ **Đầy đủ.** Thiếu: OKR/KPI frameworks, Agile/Scrum chi tiết, Product analytics.

---

### Category 5: Sales & Negotiation (3 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `predictable-revenue` | ⭐⭐⭐⭐ | 85% | B2B sales process |
| `negotiation` | ⭐⭐⭐⭐ | 85% | Tactical empathy, Ackerman |
| `drive-motivation` | ⭐⭐⭐⭐ | 85% | Autonomy, Mastery, Purpose |

**Assessment:** ⚠️ **Cơ bản.** Thiếu: Customer success, Account management, SaaS metrics.

---

### Category 6: Team & Operations (2 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `traction-eos` | ⭐⭐⭐⭐ | 85% | EOS 6 components |
| `hooked-ux` | ⭐⭐⭐⭐ | 85% | Hook Model, habit loops |

**Assessment:** ⚠️ **Thiếu nhiều.** Không có: Team management, Hiring, Culture building.

---

### Category 7: Workflow & Process (13 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `sp-brainstorming` | ⭐⭐⭐⭐⭐ | 95% | Design exploration, hard-gate |
| `sp-writing-plans` | ⭐⭐⭐⭐⭐ | 95% | TDD-style bite-sized tasks |
| `sp-executing-plans` | ⭐⭐⭐⭐ | 90% | Plan execution with checkpoints |
| `sp-test-driven-development` | ⭐⭐⭐⭐ | 90% | Red-green-refactor |
| `sp-systematic-debugging` | ⭐⭐⭐⭐ | 90% | Scientific debugging method |
| `sp-verification-before-completion` | ⭐⭐⭐⭐ | 90% | Evidence before assertions |
| `sp-requesting-code-review` | ⭐⭐⭐⭐ | 85% | Review preparation |
| `sp-receiving-code-review` | ⭐⭐⭐⭐ | 85% | Technical rigor in feedback |
| `sp-dispatching-parallel-agents` | ⭐⭐⭐⭐ | 85% | Independent task dispatch |
| `sp-subagent-driven-development` | ⭐⭐⭐⭐ | 85% | Subagent per task |
| `sp-using-git-worktrees` | ⭐⭐⭐⭐ | 85% | Isolated feature work |
| `sp-finishing-a-development-branch` | ⭐⭐⭐⭐ | 85% | Merge/PR/cleanup options |
| `sp-writing-skills` | ⭐⭐⭐⭐ | 85% | Creating new skills |
| `sp-using-superpowers` | ⭐⭐⭐ | 80% | Meta-skill discovery |

**Assessment:** ✅ **Đầy đủ cho AI coding workflow.** Thiếu: CI/CD workflow, deployment workflow, monitoring workflow.

---

### Special: Domain-Specific (2 skills)

| Skill | Quality | Completeness | Notes |
|-------|---------|-------------|-------|
| `doc-kit` | ⭐⭐⭐⭐ | 85% | Tech docs, SOP, API reference |
| `boxme-local-dev` | ⭐⭐⭐ | 70% | Project-specific local dev |
| `improve-retention` | ⭐⭐⭐⭐ | 85% | B=MAP behavior design |

---

## 🎯 GAP Analysis — Thiếu Gì?

### Ma Trận Nền Tảng × Thiết Bị Hiện Có

| | Web | iOS | Android | Desktop | Watch | TV | VR/AR |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Design** | ✅ top-design, refactoring-ui | ✅ ios-hig | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UX** | ✅ ux-master, ux-heuristics | ✅ ios-hig | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Dev** | ✅ react, nextjs, vue... | ✅ swiftui | ⚠️ jetpack-compose | ⚠️ electron, tauri | ❌ | ❌ | ❌ |
| **Cross-platform** | — | ⚠️ react-native | ⚠️ react-native, flutter | — | — | — | — |

> **Legend:** ✅ Có skill chuyên dụng | ⚠️ Có nhưng chỉ ở mức stack guideline | ❌ Không có

### Critical Gaps Identified

#### 🔴 Priority 1 — Cross-Platform & Multi-Device (Thiếu hoàn toàn)

| Gap | Impact | Recommended Skill |
|-----|--------|------------------|
| Android Material Design | Thiếu HIG cho Android | `android-material-design` |
| React Native chuyên sâu | Chỉ có stack guideline nhỏ | `react-native-mastery` |
| Flutter chuyên sâu | Chỉ có stack guideline nhỏ | `flutter-mastery` |
| Responsive Multi-device | Thiếu chiến lược adaptive | `responsive-multidevice` |
| Progressive Web App | Không có skill PWA | `pwa-architecture` |
| Desktop App Design | Thiếu patterns cho Electron/Tauri | `desktop-app-design` |
| Cross-platform Architecture | Shared code strategies | `cross-platform-architecture` |

#### 🟡 Priority 2 — Engineering Gaps

| Gap | Impact | Recommended Skill |
|-----|--------|------------------|
| Testing Strategies | Chỉ TDD cơ bản, thiếu E2E/integration | `testing-mastery` |
| DevOps/CI-CD | Không có skill | `devops-cicd` |
| Security Engineering | Không có skill | `security-engineering` |
| API Design | Chỉ doc, thiếu design patterns | `api-design-patterns` |
| Database Design | DDIA chung, thiếu practical patterns | `database-design-patterns` |
| Performance Engineering | Chỉ browser, thiếu backend/mobile | `performance-engineering` |

#### 🟢 Priority 3 — Business & Growth Gaps

| Gap | Impact | Recommended Skill |
|-----|--------|------------------|
| Product-Led Growth | PLG strategies | `product-led-growth` |
| SEO & Content Strategy | Organic traffic | `seo-content-strategy` |
| Data Analytics & Attribution | Decision making | `analytics-attribution` |
| Email & Automation | Lifecycle marketing | `email-automation` |

---

## 📋 Improvement Plan — 20 New Skills

### Phase 1: Cross-Platform Foundations (Priority 🔴)

#### Task 1: `android-material-design`
**Goal:** Android UI design reference equivalent to `ios-hig-design`
- Material Design 3 principles
- Component patterns (TopAppBar, NavigationBar, FAB, BottomSheet)
- Adaptive layouts (compact, medium, expanded)
- Dynamic color / Material You
- Typography (Roboto, type scale)
- Accessibility (TalkBack, content descriptions)
- **References:** Material Design 3 spec, Android Developer Guidelines
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 2: `react-native-mastery`
**Goal:** Deep cross-platform mobile development patterns
- Architecture: Expo vs bare workflow
- Navigation: React Navigation patterns
- State management: Zustand, Jotai, Redux Toolkit
- Performance: Hermes, lazy loading, FlatList optimization
- Platform-specific code: `Platform.select`, `.ios.tsx` / `.android.tsx`
- Native modules: bridging, Turbo Native Modules
- Testing: Detox E2E, React Native Testing Library
- Deployment: EAS Build, CodePush, OTA updates
- **References:** Expo docs, React Native best practices
- **Size:** ~300 lines SKILL.md + 6 reference files

#### Task 3: `flutter-mastery`
**Goal:** Deep Flutter development patterns
- Widget architecture: Stateless vs Stateful, composition patterns
- State management: Riverpod, BLoC, Provider
- Navigation: GoRouter, deep linking
- Platform: adaptive widgets, Cupertino vs Material
- Performance: widget rebuild optimization, DevTools profiling
- Firebase integration: Auth, Firestore, Cloud Functions
- Testing: widget tests, golden tests, integration tests
- Deployment: Fastlane, Codemagic, Play Store / App Store
- **References:** Flutter official docs, Dart packages
- **Size:** ~300 lines SKILL.md + 6 reference files

#### Task 4: `cross-platform-architecture`
**Goal:** Shared code strategies across platforms
- Mono-repo patterns: Nx, Turborepo
- Shared business logic: TypeScript core
- API contract: OpenAPI, tRPC, GraphQL codegen
- Design token sharing: Style Dictionary → Web + iOS + Android
- Feature flag systems: cross-platform rollouts
- State synchronization: offline-first, CRDT
- **References:** Nx docs, Turborepo, Style Dictionary
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 5: `pwa-architecture`
**Goal:** Progressive Web App patterns for app-like web
- Service Workers: caching strategies (stale-while-revalidate, cache-first)
- Manifest: install prompt, splash screen, shortcuts
- Offline: IndexedDB, Background Sync, Periodic Sync
- Push Notifications: Web Push API, VAPID
- App Shell architecture
- Performance: Workbox strategies
- Installability: A2HS criteria, beforeinstallprompt
- **References:** web.dev PWA guidance, Workbox docs
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 6: `desktop-app-design`
**Goal:** Design patterns for Electron & Tauri desktop apps
- Window management: multi-window, tray apps
- Menu system: native menus, context menus
- System integration: file system, notifications, keyboard shortcuts
- Platform conventions: macOS, Windows, Linux differences
- Performance: process architecture, IPC patterns
- Auto-update: Electron Updater, Tauri updater
- **References:** Apple HIG (macOS), Windows Design Language
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 7: `responsive-multidevice`
**Goal:** Adaptive design strategy across ALL device types
- Device spectrum: watch → phone → tablet → laptop → desktop → TV
- Breakpoint strategy: content-based vs device-based
- Container queries: modern responsive patterns
- Input modes: touch, pointer, keyboard, voice, gamepad
- Orientation: portrait vs landscape patterns
- Foldable devices: fold-aware layouts
- TV UI: 10-foot experience, D-pad navigation
- Watch UI: glanceable, complication patterns
- **References:** Responsive Web Design, Android Adaptive
- **Size:** ~250 lines SKILL.md + 5 reference files

---

### Phase 2: Engineering Excellence (Priority 🟡)

#### Task 8: `testing-mastery`
**Goal:** Comprehensive testing strategies beyond TDD
- Testing pyramid: unit → integration → E2E ratios
- E2E: Playwright, Cypress, Detox patterns
- Visual regression: Percy, Chromatic
- API testing: Postman, Supertest, contract testing
- Load testing: k6, Artillery
- Mutation testing: Stryker
- Test architecture: fixtures, factories, fakes vs mocks
- **References:** Testing Library docs, Playwright docs
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 9: `devops-cicd`
**Goal:** CI/CD pipeline design and DevOps best practices
- Pipeline design: stages, gates, environments
- GitHub Actions: workflow patterns, matrix builds
- Docker: multi-stage builds, compose, best practices
- Kubernetes: pods, services, deployments, Helm
- Infrastructure as Code: Terraform, Pulumi
- Monitoring: Prometheus, Grafana, alerting
- Incident management: runbooks, postmortems
- **References:** GitHub Actions docs, Docker docs, Terraform docs
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 10: `security-engineering`
**Goal:** Application security patterns and practices
- OWASP Top 10: prevention strategies
- Authentication: OAuth 2.0, OIDC, passkeys, MFA
- Authorization: RBAC, ABAC, policy engines
- API security: rate limiting, input validation, CORS
- Secrets management: vault, environment variables
- Supply chain: dependency scanning, SBOM
- Secure coding: injection prevention, CSP, SRI
- **References:** OWASP, Auth0 docs, NIST guidelines
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 11: `api-design-patterns`
**Goal:** RESTful, GraphQL, and gRPC API design
- REST: resource design, versioning, pagination, HATEOAS
- GraphQL: schema design, resolvers, N+1, subscriptions
- gRPC: proto design, streaming, deadlines
- Error handling: RFC 7807 Problem Details
- Rate limiting: algorithms, headers, client retry
- Documentation: OpenAPI 3.1, API changelog
- **References:** Google API design guide, Stripe API patterns
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 12: `performance-engineering`
**Goal:** Full-stack performance optimization
- Frontend: Core Web Vitals, bundle optimization, lazy loading
- Backend: profiling, query optimization, connection pooling
- Mobile: startup time, memory management, battery
- Database: indexing, query plans, N+1 detection
- CDN: caching strategies, edge computing
- Observability: APM, distributed tracing
- **References:** web.dev, Android Vitals, iOS Performance
- **Size:** ~250 lines SKILL.md + 5 reference files

---

### Phase 3: Business & Growth (Priority 🟢)

#### Task 13: `product-led-growth`
**Goal:** PLG strategies for SaaS products
- Free tier design: usage limits, feature gating
- Onboarding: time-to-value optimization
- Activation: aha moment identification
- Expansion: usage-based pricing, seat expansion
- Viral loops: invite, collaboration, sharing
- Self-serve: in-app upgrade, usage dashboards
- **References:** OpenView PLG playbook, Lenny's Newsletter
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 14: `seo-content-strategy`
**Goal:** SEO and content marketing for organic growth
- Technical SEO: site speed, crawlability, structured data
- On-page: keyword research, content optimization
- Content architecture: hub & spoke, pillar pages
- Link building: earn-able content, digital PR
- Analytics: Search Console, keyword tracking
- Programmatic SEO: template-based pages
- **References:** Google Search documentation, Ahrefs guides
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 15: `analytics-attribution`
**Goal:** Data-driven decision making
- Event design: taxonomy, naming conventions
- Analytics tools: GA4, Mixpanel, Amplitude
- Attribution: multi-touch models, UTM strategy
- Dashboards: KPI design, north star metrics
- Experimentation: A/B testing framework, statistical significance
- Data warehouse: event schemas, dbt
- **References:** Amplitude playbook, Mixpanel guides
- **Size:** ~200 lines SKILL.md + 4 reference files

---

### Phase 4: Advanced Platform Skills (Stretch)

#### Task 16: `ai-ml-product`
**Goal:** Building AI/ML-powered products
- LLM integration: prompt engineering, RAG, fine-tuning
- AI UX: loading states, confidence indicators, error handling
- Vector databases: Pinecone, pgvector, similarity search
- Cost management: token budgeting, caching, model selection
- Ethics: bias detection, transparency, user control
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 17: `realtime-systems`
**Goal:** Real-time communication and data patterns
- WebSocket: connection management, reconnection
- Server-Sent Events: streaming patterns
- WebRTC: video/audio, data channels
- Realtime databases: Supabase Realtime, Firebase
- Presence: online/offline detection, typing indicators
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 18: `accessibility-mastery`
**Goal:** Deep accessibility beyond WCAG basics
- Screen readers: NVDA, VoiceOver, TalkBack patterns
- ARIA: live regions, complex widgets, landmarks
- Keyboard navigation: focus management, roving tabindex
- Cognitive accessibility: plain language, predictable navigation
- Testing: axe-core, screen reader audits, user testing
- Legal: ADA, EAA, Section 508 compliance
- **Size:** ~250 lines SKILL.md + 5 reference files

#### Task 19: `design-systems-ops`
**Goal:** Building and maintaining design systems at scale
- Token architecture: primitive → semantic → component
- Multi-brand: theming, white-label strategies
- Versioning: breaking changes, migration guides
- Documentation: Storybook, living style guides
- Adoption: governance, contribution model, metrics
- **Size:** ~200 lines SKILL.md + 4 reference files

#### Task 20: `edge-serverless`
**Goal:** Edge and serverless architecture patterns
- Edge Functions: Cloudflare Workers, Vercel Edge
- Serverless: Lambda, Supabase Functions
- Edge databases: D1, Turso, PlanetScale
- Streaming: edge-side rendering, streaming HTML
- Auth at the edge: JWT verification, middleware
- **Size:** ~200 lines SKILL.md + 4 reference files

---

## 📈 Impact Matrix

| Skill | Platform Coverage | Monthly Usage Potential | ROI |
|-------|:--------:|:---------:|:---:|
| `android-material-design` | +Android | High | 🔥🔥🔥 |
| `react-native-mastery` | +iOS+Android | Very High | 🔥🔥🔥🔥 |
| `flutter-mastery` | +iOS+Android+Web+Desktop | Very High | 🔥🔥🔥🔥 |
| `cross-platform-architecture` | All | High | 🔥🔥🔥 |
| `pwa-architecture` | +Web (app-like) | High | 🔥🔥🔥 |
| `responsive-multidevice` | All devices | Very High | 🔥🔥🔥🔥 |
| `testing-mastery` | All | Very High | 🔥🔥🔥🔥 |
| `devops-cicd` | All | Very High | 🔥🔥🔥🔥 |
| `security-engineering` | All | High | 🔥🔥🔥 |
| `api-design-patterns` | All | Very High | 🔥🔥🔥🔥 |
| `performance-engineering` | All | High | 🔥🔥🔥 |
| `product-led-growth` | SaaS | High | 🔥🔥🔥 |
| `ai-ml-product` | All | Very High | 🔥🔥🔥🔥🔥 |

---

## 🗓️ Implementation Timeline

| Phase | Skills | Timeline | Effort |
|-------|--------|----------|--------|
| **Phase 1** | 7 cross-platform skills | Week 1-2 | ~1,750 lines |
| **Phase 2** | 5 engineering skills | Week 3-4 | ~1,250 lines |
| **Phase 3** | 3 business skills | Week 5 | ~600 lines |
| **Phase 4** | 5 advanced skills | Week 6-7 | ~1,050 lines |
| **Total** | **20 new skills** | **~7 weeks** | **~4,650 lines** |

---

## ✅ Quality Standards for New Skills

Mỗi skill mới phải tuân theo cấu trúc đã có:

```
skill-name/
├── SKILL.md          # 200-300 lines, YAML frontmatter
│   ├── name + description (trigger keywords)
│   ├── Core Principle
│   ├── Scoring (0-10 rubric)
│   ├── 4-7 Framework Sections
│   │   ├── Core concept
│   │   ├── Why it works
│   │   ├── Key insights (6-8 bullets)
│   │   ├── Code applications table
│   │   └── Ethical boundary
│   ├── Common Mistakes table
│   ├── Quick Diagnostic table
│   ├── Reference Files links
│   ├── Further Reading (books/resources)
│   └── About the Author
└── references/       # 4-6 reference files
    ├── topic-1.md
    ├── topic-2.md
    └── ...
```

### Mandatory checklist per skill:
- [ ] YAML frontmatter with name, description, license, metadata
- [ ] Cross-references to related skills (min 2)
- [ ] Scoring rubric 0-10
- [ ] At least 1 table per section
- [ ] Code/command examples
- [ ] Common Mistakes table (min 8 entries)
- [ ] Quick Diagnostic table (min 8 questions)
- [ ] Reference files in `references/` directory
- [ ] Further Reading with book links

---

## Verification Plan

### Automated Tests
- Each new skill SKILL.md passes markdown lint: `npx markdownlint-cli2 "skills/*/SKILL.md"`
- YAML frontmatter is valid: `python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"`
- Cross-references point to existing skills: custom script to verify

### Manual Verification
1. Open each new SKILL.md and verify visual hierarchy is clear
2. Verify all internal links to references/ resolve correctly
3. Test search.py integration for new keywords (if applicable)
4. Check scoring rubric makes sense for the domain
5. Verify cross-references lead to correct companion skills
