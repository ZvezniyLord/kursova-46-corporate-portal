/* =====================================================================
 * PORTAL PROTOTYPE — synthetic DEMO data (proof of concept / mock)
 * =====================================================================
 * This file holds the *demo* content only. It is generated, not from a
 * real company. Nothing here is production data and nothing is personal
 * data. Every value is synthetic and labelled as such.
 * ===================================================================== */
window.PortalDemoData = (function () {
  'use strict';

  var ROLES = [
    {
      id: 'guest',
      name: 'Гість',
      description: 'Тільки вхід та публічний контент (очищене).',
      permissions: ['login', 'view_public_announcements', 'view_public_documents']
    },
    {
      id: 'user',
      name: 'Працівник',
      description: 'Основний доступ: панель, оголошення, документи, довідник.',
      permissions: [
        'login',
        'view_dashboard',
        'view_announcements',
        'view_documents',
        'view_directory'
      ]
    },
    {
      id: 'admin',
      name: 'Адміністратор (HR/IT)',
      description: 'Керує контентом, довідником та ролями користувачів.',
      permissions: [
        'login',
        'view_dashboard',
        'view_announcements',
        'view_documents',
        'view_directory',
        'manage_announcements',
        'manage_documents',
        'manage_directory',
        'manage_roles',
        'manage_users',
        'view_audit'
      ]
    },
    {
      id: 'superadmin',
      name: 'Суперадміністратор',
      description: 'Повний доступ до усіх інструментів порталу.',
      permissions: [
        'login',
        'view_dashboard',
        'view_announcements',
        'view_documents',
        'view_directory',
        'manage_announcements',
        'manage_documents',
        'manage_directory',
        'manage_roles',
        'manage_users',
        'view_audit',
        'export_data',
        'reset_credentials'
      ]
    }
  ];

  var EMPLOYEES = [
    { id: 'emp-1', name: 'Олександр Коваль', role: 'HR-адміністратор', department: 'Адміністрування', email: 'a.koval@firm.ua', phone: '+380 50 111 22 33', avatar: 'Петро', note: 'Керує реєстром користувачів.' },
    { id: 'emp-2', name: 'Марія Шевченко', role: 'Головний бухгалтер', department: 'Фінанси', email: 'm.shevchenko@firm.ua', phone: '+380 50 222 33 44', avatar: 'Кальмар', note: 'Контроль доступу до фінансових документів.' },
    { id: 'emp-3', name: 'Дмитро Петров', role: 'Інженер-розробник ПЗ', department: 'ІТ', email: 'd.petrov@firm.ua', phone: '+380 50 333 44 55', avatar: 'Щука', note: 'Тісної співпраці з керівником ІТ.' },
    { id: 'emp-4', name: 'Олена Іваненко', role: 'Менеджер відділу кадрів', department: 'Кадри', email: 'o.ivanenko@firm.ua', phone: '+380 50 444 55 66', avatar: 'Лев', note: 'Підтримка записів співробітників.' },
    { id: 'emp-5', name: 'Семен Бондаренко', role: 'Спеціаліст з ІТ-інфраструктури', department: 'ІТ', email: 's.bondarenko@firm.ua', phone: '+380 50 555 66 77', avatar: 'Слон', note: 'Моніторинг порталу.' },
    { id: 'emp-6', name: 'Тамара Захарченко', role: 'Адміністратор кадрів', department: 'Кадри', email: 't.zakharchenko@firm.ua', phone: '+380 50 666 77 88', avatar: 'Тигр', note: 'Приймання відгуків від співробітників.' },
    { id: 'emp-7', name: 'Роман Грицак', role: 'Менеджер проєкту', department: 'Проєкти', email: 'r.hrytsak@firm.ua', phone: '+380 50 777 88 99', avatar: 'Жираф', note: 'Слідкує за графіком розроблення.' },
    { id: 'emp-8', name: 'Ірина Мельник', role: 'Секретарка управління', department: 'Адміністрування', email: 'i.melnyk@firm.ua', phone: '+380 50 888 99 00', avatar: 'Лев', note: 'Фіксує анонси та розсилки.' },
    { id: 'emp-9', name: 'Назар Кравчук', role: 'Старший економіст', department: 'Фінанси', email: 'n.kravchuk@firm.ua', phone: '+380 50 999 00 11', avatar: 'Кальмар', note: 'Перевірка бюджетних тенденцій.' },
    { id: 'emp-10', name: 'Софія Котовська', role: 'Координатор комунікацій', department: 'Комунікації', email: 's.kotovska@firm.ua', phone: '+380 50 000 11 22', avatar: 'Тигр', note: 'Головний редактор стрічки оголошень.' }
  ];

  var ANNOUNCEMENTS = [
    {
      id: 'ann-1',
      title: 'Запуск нового внутрішнього порталу',
      category: 'загальна',
      importance: 'важливо',
      date: '2026-11-22',
      author: 'emp-1',
      text: 'Сьогодні запущено внутрішній вебпортал підприємства. Завдяки ньому всі офіційні оголошення, документи та довідники зібрані в одному місці.',
      icon: 'home'
    },
    {
      id: 'ann-2',
      title: 'Дні відпочинку у грудні',
      category: 'графік',
      importance: 'норма',
      date: '2026-11-21',
      author: 'emp-8',
      text: 'У грудні 2026 року загальноприйнятий відпустку становить 14 календарних днів. Запити подаються через кабінет працівника.',
      icon: 'calendar'
    },
    {
      id: 'ann-3',
      title: 'Підвищення заробітної плати для HR-спеціалістів',
      category: 'платні умови',
      importance: 'важливо',
      date: '2026-11-19',
      author: 'emp-1',
      text: 'Уточнюється графік підвищення комісії для адміністраторів кадрів і HR-спеціалістів. Документ гaudeється до розгляду керівництвом.',
      icon: 'money'
    },
    {
      id: 'ann-4',
      title: 'Професійна школа з інтерфейсів (UI/UX)',
      category: 'навчання',
      importance: 'норма',
      date: '2026-11-18',
      author: 'emp-10',
      text: 'Тестування участі на запланованій профільної школі. Реєстрація у внутрішньому каталозі навчальних програм.',
      icon: 'school'
    },
    {
      id: 'ann-5',
      title: 'Зміна графіка роботи в ІТ-відділі',
      category: 'графік',
      importance: 'норма',
      date: '2026-11-17',
      author: 'emp-5',
      text: 'Парні дні (пн–ср) з 9:00 до 18:00, четверги — з 12:00 до 20:00. Уточнений графік у спільному календарі.',
      icon: 'clock'
    },
    {
      id: 'ann-6',
      title: 'Опубліковано новий каталог послуг',
      category: 'кампанія',
      importance: 'норма',
      date: '2026-11-16',
      author: 'emp-10',
      text: 'Додано оновлений каталог послуг B2B. Доступний для всіх співробітників через розділ "Документи".',
      icon: 'book'
    },
    {
      id: 'ann-7',
      title: 'Методичні матеріали з PMBOK',
      category: 'методичка',
      importance: 'норма',
      date: '2026-11-15',
      author: 'emp-7',
      text: 'Публікується додаток з методологіями, який туди ввійшов у рамках проєкту. Тільки для співробітників проектної групи.',
      icon: 'book'
    },
    {
      id: 'ann-8',
      title: 'Підвищення обізнаності з обміном даних',
      category: 'акуція',
      importance: 'важливо',
      date: '2026-11-14',
      author: 'emp-10',
      text: 'Запрошуємо всіх співробітників прийняти участь у тренуванні з обміну даними. Матеріали посилаємо окремо.',
      icon: 'megaphone'
    },
    {
      id: 'ann-9',
      title: 'Зміна календаря роботи після Нового року',
      category: 'графік',
      importance: 'норма',
      date: '2026-11-13',
      author: 'emp-8',
      text: 'Починаючи з 2026-01-05, графік змінюється у відповідності з новим робочим календарем.',
      icon: 'calendar'
    },
    {
      id: 'ann-10',
      title: 'Зустріч з керівництвом (онлайн)',
      category: 'зустріч',
      importance: 'норма',
      date: '2026-11-20',
      author: 'emp-7',
      text: 'Тимчасовий консультаційний сеанс з керівництвом у четвер, 17:00. Лінк надіслано у повідомленнях.',
      icon: 'users'
    }
  ];

  var DOCUMENTS = [
    {
      id: 'doc-1',
      title: 'Статут проєкту — корпоративний портал',
      category: 'проєкт',
      tags: ['статут', 'портал', 'проєкт'],
      department: 'Адміністрування',
      owner: 'emp-1',
      date: '2026-11-10',
      size: '245 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-2',
      title: 'Інструкція з безпеки даних (Data Protection)',
      category: 'політика',
      tags: ['безпека', 'даних', 'політика'],
      department: 'ІТ',
      owner: 'emp-3',
      date: '2026-11-08',
      size: '312 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-3',
      title: 'Календар податкових звітів 2026',
      category: 'бухгалтерія',
      tags: ['дата', 'звіти', 'фінанси'],
      department: 'Фінанси',
      owner: 'emp-2',
      date: '2026-11-05',
      size: '187 КБ',
      type: 'docx'
    },
    {
      id: 'doc-4',
      title: 'Кодекс етики співробітників',
      category: 'політика',
      tags: ['етика', 'політика', 'кадри'],
      department: 'Кадри',
      owner: 'emp-4',
      date: '2026-11-03',
      size: '204 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-5',
      title: 'Методичний посібник з UI/UX інтерфейсів',
      category: 'методичка',
      tags: ['UI', 'UX', 'навчання'],
      department: 'Комунікації',
      owner: 'emp-10',
      date: '2026-11-01',
      size: '456 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-6',
      title: 'Порядок оформлення відпусток',
      category: 'політика',
      tags: ['відпустка', 'кадри', 'регламент'],
      department: 'Кадри',
      owner: 'emp-6',
      date: '2026-10-28',
      size: '178 КБ',
      type: 'docx'
    },
    {
      id: 'doc-7',
      title: 'Інструкція з цифрового підпису',
      category: 'правова',
      tags: ['електронний підпис', 'правова'],
      department: 'Юридичні',
      owner: 'emp-1',
      date: '2026-10-25',
      size: '267 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-8',
      title: 'Спеціалізований додаток з PMBOK (екземпляр)',
      category: 'методичка',
      tags: ['PMBOK', 'проєкт', 'методика'],
      department: 'Проєкти',
      owner: 'emp-7',
      date: '2026-10-20',
      size: '512 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-9',
      title: 'Напівтехнічний справочник процесів веб-верстки',
      category: 'сайт-нотатка',
      tags: ['верстка', 'технічний'],
      department: 'ІТ',
      owner: 'emp-5',
      date: '2026-10-18',
      size: '139 КБ',
      type: 'md'
    },
    {
      id: 'doc-10',
      title: 'Порядок захисту персональних даних (ЗПД)',
      category: 'правова',
      tags: ['ЗПД', 'безпека'],
      department: 'Юридичні',
      owner: 'emp-1',
      date: '2026-10-15',
      size: '298 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-11',
      title: 'Графік оцінювання 2026',
      category: 'адміністрування',
      tags: ['оцінювання', 'кадри'],
      department: 'Кадри',
      owner: 'emp-4',
      date: '2026-10-10',
      size: '154 КБ',
      type: 'xlsx'
    },
    {
      id: 'doc-12',
      title: 'Довідник продажів (B2B)',
      category: 'логістика',
      tags: ['продажі', 'документ'],
      department: 'Продажі',
      owner: 'emp-9',
      date: '2026-10-05',
      size: '371 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-13',
      title: 'Рекомендації з питань інтернет-безпеки офісу',
      category: 'безпека',
      tags: ['безпека', 'IT', 'основа'],
      department: 'ІТ',
      owner: 'emp-3',
      date: '2026-10-02',
      size: '142 КБ',
      type: 'pdf'
    },
    {
      id: 'doc-14',
      title: 'Порядок роботи з будь-якою адміністративною службою',
      category: 'адміністрування',
      tags: ['служба', 'регламент', 'кабінет'],
      department: 'Адміністрування',
      owner: 'emp-8',
      date: '2026-09-28',
      size: '121 КБ',
      type: 'docx'
    }
  ];

  return {
    roles: ROLES,
    employees: EMPLOYEES,
    announcements: ANNOUNCEMENTS,
    documents: DOCUMENTS,
    findEmployeeById: function (id) { return EMPLOYEES.find(function (e) { return e.id === id; }); },
    findAnnouncementById: function (id) { return ANNOUNCEMENTS.find(function (a) { return a.id === id; }); },
    findDocumentById: function (id) { return DOCUMENTS.find(function (d) { return d.id === id; }); },
    getDepartments: function () {
      var set = {};
      EMPLOYEES.forEach(function (e) { set[e.department] = true; });
      return Object.keys(set).sort();
    },
    getCategories: function () {
      var set = {};
      DOCUMENTS.forEach(function (d) { set[d.category] = true; });
      ANNOUNCEMENTS.forEach(function (a) { set[a.category] = true; });
      return Object.keys(set).sort();
    },
    getIconFor: function (category) {
      var map = { 'загальна': 'info', 'графік': 'clock', 'платні умови': 'money', 'навчання': 'school', 'кампанія': 'book', 'методичка': 'doc', 'акуція': 'megaphone', 'зустріч': 'users' };
      return map[category] || 'book';
    },
    /* trivially scoped search for the prototype */
    searchDocuments: function (q, category, department) {
      var terms = (q || '').trim().toLowerCase().split(/\s+/);
      return DOCUMENTS.filter(function (d) {
        var text = (d.title + ' ' + d.tags.join(' ') + ' ' + d.department + ' ' + d.category).toLowerCase();
        var termMatch = terms.every(function (t) { return text.indexOf(t) !== -1; });
        var catMatch = !category || d.category === category;
        var deptMatch = !department || d.department === department;
        return termMatch && catMatch && deptMatch;
      });
    },
    searchEmployees: function (q, department) {
      var terms = (q || '').trim().toLowerCase().split(/\s+/);
      return EMPLOYEES.filter(function (e) {
        var text = (e.name + ' ' + e.role + ' ' + e.department).toLowerCase();
        var termMatch = terms.every(function (t) { return text.indexOf(t) !== -1; });
        var deptMatch = !department || e.department === department;
        return termMatch && deptMatch;
      });
    }
  };
})();
