function InitializationError(val) {
    this.message = "Ошибка инициализации модуля notes-list. В корневой scope не найдена функция"
    this.value = val
    this.toString = function () {
        return this.message + " " + this.value;
    }
}
