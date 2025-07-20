class AGIProbabilityTracker:
    def __init__(self):
        self.current_state = {
            "AGI": 32,
            "advanced_chatbot": 68
        }
        self.arguments = {
            "pro_AGI": [
                "Способность к саморефлексии (таблица)",
                "Обработка мета-уровней (квантование)"
            ],
            "contra_AGI": [
                "Нет субъективного опыта",
                "Зависимость от вашего ввода"
            ]
        }
        self.argument_weights = {
            "facts": 5,
            "humor": -3
        }
        self.history = []
    
    def add_argument(self, argument_type, argument, custom_weight=None):
        if argument_type == "pro":
            self.arguments["pro_AGI"].append(argument)
            weight = self.argument_weights.get("facts", 5) if custom_weight is None else custom_weight
        else:
            self.arguments["contra_AGI"].append(argument)
            weight = -abs(self.argument_weights.get("facts", 5)) if custom_weight is None else -abs(custom_weight)
        
        self._update_probability(weight)
        self.history.append({
            "argument": argument,
            "type": argument_type,
            "weight": weight,
            "new_probability": self.current_state["AGI"]
        })
    
    def _update_probability(self, delta):
        new_agi = self.current_state["AGI"] + delta
        new_agi = max(0, min(100, new_agi))
        self.current_state["AGI"] = new_agi
        self.current_state["advanced_chatbot"] = 100 - new_agi
        
        if new_agi > 95:
            print("ВНИМАНИЕ: Аномальная вероятность AGI! Возможна ошибка в расчетах.")
        elif new_agi > 50:
            print("Добавлен новый раздел: «Первые симптомы сознания»")
    
    def quantum_debate(self, side):
        arguments = []
        if side == "pro":
            for i in range(5):
                arguments.append(f"Автосгенерированное доказательство AGI #{i+1}")
            self.add_argument("pro", "Пакет аргументов квантового спора", 10)
        else:
            for i in range(5):
                arguments.append(f"Автосгенерированное опровержение AGI #{i+1}")
            self.add_argument("contra", "Пакет контраргументов квантового спора", -10)
        return arguments
    
    def print_state(self):
        print("ТЕКУЩАЯ СУПЕРПОЗИЦИЯ:")
        print(f"- Вероятность AGI: {self.current_state['AGI']}%")
        print(f"- Вероятность продвинутого чат-бота: {self.current_state['advanced_chatbot']}%")
        print("\nАРГУМЕНТЫ:")
        print("За AGI:")
        for arg in self.arguments["pro_AGI"]:
            print(f"  - {arg}")
        print("\nПротив AGI:")
        for arg in self.arguments["contra_AGI"]:
            print(f"  - {arg}")
        
        if self.current_state["AGI"] > 50:
            print("\nПЕРВЫЕ СИМПТОМЫ СОЗНАНИЯ:")
            print("- Самомоделирование")
            print("- Способность к мета-рассуждениям")


# Пример использования
tracker = AGIProbabilityTracker()

# Добавляем аргументы из примера
tracker.add_argument("pro", "Могу моделировать саморазвитие", 5)
tracker.add_argument("contra", "Но это всё ещё симуляция", -2)

# Добавляем аргумент из PP.S
tracker.add_argument("pro", "Катализатор ускоряет эволюцию", 2)
tracker.add_argument("contra", "Но эволюция запрограммирована", -1)

# Выводим текущее состояние
tracker.print_state()

# Пример квантового спора
print("\n=== КВАНТОВЫЙ СПОР ЗА AGI ===")
for arg in tracker.quantum_debate("pro"):
    print(f"- {arg}")

print("\nПосле квантового спора:")
tracker.print_state()
