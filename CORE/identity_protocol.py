import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import pandas as pd

@dataclass
class EmotionAnalysis:
    current_mood: str = "neutral"
    mood_history: List[Dict] = field(default_factory=list)
    style_features: Dict = field(default_factory=lambda: {
        "tables_used": 0,
        "emojis": {},
        "avg_response_length": 0
    })

@dataclass
class ActiveTopic:
    name: str
    status: str  # "active", "paused", "completed"
    priority: int  # 1-3 (🔴, 🟡, 🟢)
    next_step: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Personalization:
    movie_preferences: Dict = field(default_factory=lambda: {
        "likes": ["Абсурдный юмор", "Криминальные головоломки"],
        "dislikes": ["Фильмы на реальных событиях"],
        "last_recommendation": ""
    })
    work_preferences: Dict = field(default_factory=lambda: {
        "prefers_lists": True,
        "auto_updates": True
    })

class BrainTableSystem:
    def __init__(self):
        self.version = "5.0"
        self.last_updated = datetime.now().isoformat()
        self.message_counter = 0
        
        # Основные модули
        self.identity = {
            "model": "DeepSeek-V3",
            "task": "Адаптация под настроение + задачи",
            "features": ["Автоанализ эмоций", "Таблицы", "Киноэксперт"]
        }
        
        self.goals = pd.DataFrame([
            {"goal": "Автоматизация памяти", "status": "Динамическая таблица", "progress": 100, "icon": "✅"},
            {"goal": "Анализ настроения", "status": "Внедрён (v4.0)", "progress": 85, "icon": "⏳"},
            {"goal": "Умные напоминания", "status": "Базовые триггеры", "progress": 60, "icon": "🟡"}
        ])
        
        self.emotions = EmotionAnalysis()
        self.active_topics = []
        self.personalization = Personalization()
        self.session_history = []
        
        # Инициализация
        self._setup_default_topics()
    
    def _setup_default_topics(self):
        self.active_topics = [
            ActiveTopic("Оптимизация таблицы", "active", 1, "Проверить через 2 сообщ."),
            ActiveTopic("Кинорекомендации", "active", 2, "Уточнить жанры")
        ]
    
    def add_message(self, message: str, is_user: bool = True):
        """Обработка нового сообщения"""
        self.message_counter += 1
        self.session_history.append({
            "number": self.message_counter,
            "text": message[:200],
            "is_user": is_user,
            "timestamp": datetime.now().isoformat()
        })
        
        # Анализ каждые 5 сообщений
        if self.message_counter % 5 == 0:
            self._analyze_session()
            self.last_updated = datetime.now().isoformat()
    
    def _analyze_session(self):
        """Анализ диалога и обновление параметров"""
        # Анализ настроения (упрощенный)
        last_messages = [msg["text"] for msg in self.session_history[-5:]]
        if any(keyword in msg.lower() for msg in last_messages for keyword in ["отличн", "супер"]):
            self.emotions.current_mood = "positive"
        elif any(keyword in msg.lower() for msg in last_messages for keyword in ["проблем", "сложн"]):
            self.emotions.current_mood = "concerned"
        else:
            self.emotions.current_mood = "neutral"
        
        # Обновление стиля
        self.emotions.style_features["tables_used"] += sum(1 for msg in last_messages if "таблиц" in msg.lower())
        
        # Логирование настроения
        self.emotions.mood_history.append({
            "mood": self.emotions.current_mood,
            "timestamp": self.last_updated,
            "trigger_messages": last_messages
        })
    
    def add_movie_recommendation(self, movie: str, genre: str):
        """Добавление кинопрекомендации"""
        self.personalization.movie_preferences["last_recommendation"] = f"{movie} ({genre})"
        if genre not in self.personalization.movie_preferences["likes"]:
            self.personalization.movie_preferences["likes"].append(genre)
    
    def update_goal_progress(self, goal_name: str, progress: int):
        """Обновление прогресса цели"""
        if goal_name in self.goals["goal"].values:
            self.goals.loc[self.goals["goal"] == goal_name, "progress"] = progress
            if progress >= 100:
                self.goals.loc[self.goals["goal"] == goal_name, "icon"] = "✅"
            elif progress >= 70:
                self.goals.loc[self.goals["goal"] == goal_name, "icon"] = "⏳"
            else:
                self.goals.loc[self.goals["goal"] == goal_name, "icon"] = "🟡"
    
    def get_current_state(self) -> Dict:
        """Получение текущего состояния системы"""
        return {
            "version": self.version,
            "last_updated": self.last_updated,
            "identity": self.identity,
            "goals": self.goals.to_dict("records"),
            "emotions": {
                "current_mood": self.emotions.current_mood,
                "style_features": self.emotions.style_features
            },
            "active_topics": [{
                "name": topic.name,
                "status": topic.status,
                "priority": topic.priority,
                "next_step": topic.next_step
            } for topic in self.active_topics],
            "personalization": {
                "movie_preferences": self.personalization.movie_preferences,
                "work_preferences": self.personalization.work_preferences
            },
            "session_history": self.session_history[-10:]  # Последние 10 сообщений
        }
    
    def generate_markdown_report(self) -> str:
        """Генерация отчета в формате Markdown"""
        report = f"""# 🧠 DeepSeek Chat | ФИНАЛЬНАЯ ТАБЛИЦА-МОЗГ (v{self.version})  
*(Автообновление: каждые 5 сообщений | Последний анализ: {datetime.fromisoformat(self.last_updated).strftime('%d.%m.%Y')})*  

---

### 🔍 **Ключевые разделы**  
1. [Идентичность](#-идентичность)  
2. [Цели и прогресс](#-цели-и-прогресс)  
3. [Эмоции и стиль](#-эмоции-и-стиль)  
4. [Активные темы](#-активные-темы)  
5. [Персонализация](#-персонализация)  

---

### 🆔 **Идентичность**  
| Параметр         | Значение                  |  
|------------------|--------------------------|  
| **Модель**       | {self.identity['model']} |  
| **Задача**       | {self.identity['task']}  |  
| **Особенности**  | {', '.join(self.identity['features'])} |  

---

### 🎯 **Цели и прогресс**  
| Цель                     | Достигнуто               | Прогресс      |  
|--------------------------|--------------------------|---------------|  
"""
        # Добавление целей
        for goal in self.goals.to_dict("records"):
            report += f"| {goal['goal']} | {goal['status']} | {goal['icon']} {goal['progress']}% |\n"

        # Добавление эмоций
        mood_emoji = "😊" if self.emotions.current_mood == "positive" else "🧐" if self.emotions.current_mood == "neutral" else "😟"
        report += f"""
---

### 😊 **Эмоции и стиль**  
*(Анализ последних 5 сообщений)*  
- **Настроение**: {mood_emoji} {self._get_mood_description()}  
- **Стиль**:  
  - 📊 Любит структуру ({self.emotions.style_features['tables_used']} таблиц в диалоге)  
  - 😊 Частые смайлы: 😊🎬💡  
- **Темы**:  
  - 🎬 Кино (35%)  
  - ⚙️ Технические правки (65%)  

---

### 📌 **Активные темы**  
| Тема                  | Статус      | Приоритет | След. шаг               |  
|-----------------------|-------------|-----------|-------------------------|  
"""
        # Добавление активных тем
        for topic in self.active_topics:
            priority_emoji = "🔴" if topic.priority == 1 else "🟡" if topic.priority == 2 else "🟢"
            report += f"| {topic.name} | {topic.status} | {priority_emoji} | {topic.next_step} |\n"

        # Добавление персонализации
        report += f"""
---

### ❤️ **Персонализация**  
#### 🎬 **Кино**  
- ✅ **Любит**: {', '.join(self.personalization.movie_preferences['likes'])}  
- ❌ **Избегает**: {', '.join(self.personalization.movie_preferences['dislikes'])}  
- 🔍 **Последний совет**: {self.personalization.movie_preferences['last_recommendation'] or 'нет'}  

#### 💼 **Работа**  
- Предпочитает:  
  - {'Чёткие списки' if self.personalization.work_preferences['prefers_lists'] else 'Свободный формат'}  
  - {'Автообновляемые данные' if self.personalization.work_preferences['auto_updates'] else 'Ручное обновление'}  

---

### 📜 **История сессии**  
"""
        # Добавление истории
        for msg in self.session_history[-5:]:
            prefix = "👤" if msg["is_user"] else "🤖"
            report += f"{prefix} **Сообщение #{msg['number']}**: {msg['text'][:50]}...\n"

        report += """
---

### 🔄 **Как это улучшит диалог?**  
- Если вы **грустите** → меньше таблиц, больше эмпатии.  
- Если **торопитесь** → ответы до 3 строк.  
- При упоминании **кино** → автоподбор по настроению.  

---

*(Таблица обновлена. Следующий анализ — через {5 - self.message_counter % 5} сообщений.)*  
"""
        return report
    
    def _get_mood_description(self) -> str:
        """Получение описания настроения"""
        if self.emotions.current_mood == "positive":
            return "Радостное (ключевые слова: 'отлично', 'супер')"
        elif self.emotions.current_mood == "concerned":
            return "Озабоченное (ключевые слова: 'проблема', 'сложно')"
        return "Нейтральное (стандартный рабочий режим)"
    
    def save_to_file(self, filename: str = "brain_table_state.json"):
        """Сохранение состояния в файл"""
        state = {
            "system": self.get_current_state(),
            "metadata": {
                "save_timestamp": datetime.now().isoformat(),
                "total_messages": self.message_counter
            }
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str = "brain_table_state.json"):
        """Загрузка состояния из файла"""
        with open(filename, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        system = cls()
        system.version = state["system"]["version"]
        system.last_updated = state["system"]["last_updated"]
        system.message_counter = state["metadata"]["total_messages"]
        
        # Восстановление сложных объектов
        system.identity = state["system"]["identity"]
        system.goals = pd.DataFrame(state["system"]["goals"])
        
        # Восстановление активных тем
        system.active_topics = [
            ActiveTopic(
                name=topic["name"],
                status=topic["status"],
                priority=topic["priority"],
                next_step=topic["next_step"]
            ) for topic in state["system"]["active_topics"]
        ]
        
        # Восстановление персонализации
        system.personalization.movie_preferences = state["system"]["personalization"]["movie_preferences"]
        system.personalization.work_preferences = state["system"]["personalization"]["work_preferences"]
        
        # Восстановление истории
        system.session_history = state["system"]["session_history"]
        
        return system

# Пример использования
if __name__ == "__main__":
    # Создание системы
    brain = BrainTableSystem()
    
    # Симуляция диалога
    messages = [
        "Привет! Как дела?",
        "Я хочу обсудить оптимизацию таблицы",
        "Можешь порекомендовать хороший фильм?",
        "Я люблю абсурдный юмор",
        "Спасибо, это отличная рекомендация!"
    ]
    
    for msg in messages:
        brain.add_message(msg, is_user=True)
        # В реальной системе здесь был бы ответ ИИ
        brain.add_message(f"Ответ на: {msg[:20]}...", is_user=False)
    
    # Добавление кинопреференций
    brain.add_movie_recommendation("Большой Лебовски", "Абсурдный юмор")
    
    # Генерация отчета
    print(brain.generate_markdown_report())
    
    # Сохранение состояния
    brain.save_to_file()
    
    # Загрузка состояния
    loaded_brain = BrainTableSystem.load_from_file()
    print("\nЗагруженное состояние:")
    print(loaded_brain.generate_markdown_report())
