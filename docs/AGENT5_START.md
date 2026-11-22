# Запуск Agent 5 у Hermes Desktop — тільки через чотири окремі безкоштовні Bots

**ВАЖЛИВО: попередню версію цієї інструкції скасовано.** Вона помилково наказувала запустити 4 `delegate_task`; це створювало тимчасових Subagents, які могли успадковувати платну модель головного чату. **Не використовувати цю схему.**

Правильний алгоритм детально описаний у [AGENT5_BOT_MODE_HOTFIX.md](AGENT5_BOT_MODE_HOTFIX.md).

## 0. Припини попередній неправильний запуск

Якщо відкрито сесію з `GPT-6-luna` або іншою моделлю без перевіреного безкоштовного маршруту: натисни **Stop** та перевір, чи немає активних фонових Subagents. Не надсилай наступний запит через цей платний модельний маршрут. Спочатку переведи **самого Agent 5** на перевірену безкоштовну локальну або free-tier модель без billable fallback.

## 1. Залишаємо чинний публічний GitHub-репозиторій

```bash
git clone https://github.com/ZvezniyLord/kursova-46-corporate-portal.git
cd kursova-46-corporate-portal
```

Якщо проєкт уже відкрито локально, синхронізуй оновлені `AGENTS.md`, `docs/AGENT5_START.md`, `docs/AGENT5_BOT_MODE_HOTFIX.md` і `docs/AGENT5_ACADEMIC_CONTRACT.md`. Не створюй приватний репозиторій, не публікуй приватні файли/секрети.

## 2. Обов'язкова послідовність

1. У Hermes прочитай встановлений скіл `hermes-agent` і офіційні розділи Bot Mode, Profiles, Models та Skills.
2. Перевір реальні моделі й провайдери в налаштуваннях. Визнач тільки локальні/free-tier маршрути з контрольованими квотами. Якщо неможливо підтвердити нульові витрати, **не стартуй**.
3. На вкладці **BOTS** натисни **+ → New Agent → Advanced → Fresh profile** (або використай безпечний Hermes CLI із доступом до профілів). Створи відсутніх:
   - `course46-mpp` — WBS, Gantt, ресурси, бюджет, Baseline, `.mpp`;
   - `course46-jira` — backlog, epics, stories, sprint, Jira;
   - `course46-prototype` — інтерактивний прототип порталу;
   - `course46-uat` — сценарії приймального тестування і перевірені результати.
4. **У кожного нового бота у Advanced явно закріпи free/local model & provider.** Не залишай model pin порожнім. Не копіюй платні ключі чи конфігурацію через Clone/Duplicate; вимкни Copy API keys, якщо вони оплачувані. За потреби налаштуй `SOUL.md`, потрібні skills і tools.
5. Перевір `hermes profile list` та `hermes profile show <name>`, що всі 4 постійні профілі існують, мають правильні моделі і видимі у BOTS. Головний Agent 5 також повинен мати перевірену безкоштовну модель.
6. **Лише після підтвердження 5/5** створюй `docs/bot-roster.md`, контракт вимог, матрицю трасованості; далі надсилай доручення через `message_agent` у Bot Chat / @бота. Тимчасові `delegate_task` не є постійними ботами.
7. Для вкладених Subagents усередині кожного окремого бота потрібен додатковий аудит `delegation.model/provider`; не дозволяти успадкування платної моделі/провайдера.

## 3. Стартове повідомлення для НОВОЇ безкоштовної сесії Agent 5

> Ти Agent 5, головний оркестратор курсової №46. Попередній підхід із чотирма delegate_task СКАСОВАНИЙ. Прочитай оновлені AGENTS.md, docs/AGENT5_BOT_MODE_HOTFIX.md, docs/AGENT5_ACADEMIC_CONTRACT.md, docs/structure-and-requirements.md та пакет COURSEWORK_SOURCE_PACK.md. Використай встановлений скіл hermes-agent для керування справжніми постійними Bot Mode профілями. Спершу перевір, що і твоя модель, і моделі майбутніх ботів безкоштовні, без billable fallback. Створи через BOTS/New Agent/Advanced/Fresh profile чи відповідний доступний інтерфейс **саме 4 нових незалежних постійних боти**: course46-mpp, course46-jira, course46-prototype, course46-uat. Кожному признач власний явно перевірений free/local provider/model, необхідні skills та SOUL.md. Не дублюй наявні профілі. Не запускай delegate_task замість Bots. Перевір їх через hermes profile list/show і на екрані BOTS; створи docs/bot-roster.md з фактами без секретів. При відсутності GUI/CLI інструментів — STOP і інструкція оператору, без симуляції. ЛИШЕ ПІСЛЯ верифікації 5/5 моделей і профілів сформуй єдиний контракт вимог, почни координацію через message_agent/@ботів і підготовку наукової курсової на основі універсального академічного контракту та пріоритетних вимог Moodle. Репозиторій — публічний. Не вигадуй .mpp, Jira, прототип, UAT, дослідження чи джерела. Звітуй українською про фактично створене.

## 4. Що означає «успішно»

Не текст `created` від моделі й не дерево Subagents, а:
- Чотири окремі постійні профілі з підтвердженими моделями у BOTS;
- Головний профіль теж на перевіреній free/local моделі;
- Скіл `hermes-agent` прочитано;
- `docs/bot-roster.md` містить реальні профілі і моделі;
- Лише потім починається узгоджена генерація артефактів чотирма ботами;
- Фінальний DOCX/PDF перевіряються за [академічним контрактом](AGENT5_ACADEMIC_CONTRACT.md).

## 5. Документація

- https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/reference/profile-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation

**Увага:** завантаження файлів у GitHub не створює локальні профілі на твоєму комп'ютері й не зупиняє вже запущені локальні процеси.
