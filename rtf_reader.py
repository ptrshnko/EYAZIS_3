from striprtf.striprtf import rtf_to_text
import os

def read_rtf_file(file_path):
    """
    Читает RTF-файл и возвращает извлеченный текст.
    
    Args:
        file_path (str): Путь к RTF-файлу.
        
    Returns:
        str: Извлеченный текст из RTF-файла.
        
    Raises:
        ValueError: Если файл не в формате RTF.
        Exception: Если произошла ошибка при чтении файла.
    """
    try:
        # Проверка расширения файла
        if not file_path.lower().endswith('.rtf'):
            raise ValueError("Файл должен быть в формате RTF")
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        # Чтение и конвертация RTF в текст
        with open(file_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
        text = rtf_to_text(rtf_content)
        
        # Проверка, что текст не пустой
        if not text.strip():
            raise ValueError("Файл RTF пуст или содержит некорректные данные")
            
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Ошибка при чтении RTF-файла: {str(e)}")