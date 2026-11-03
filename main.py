import os
import streamlit as st
from llm_processing import generate_product_card


st.set_page_config(
    page_title="AI-ассистент для B2B-интернет-магазина",
    page_icon=":robot_face:",
    layout="centered")
st.title("AI-ассистент по генерации карточек товаров")

def validate_input(data):
    fields = {
        "name": "Название товара",
        "manufacturer": "Производитель",
        "specs": "Характеристики товара",
        "description": "Описание / Фрагмент тех. паспорта"
    }
    missing = []
    for key, field_name in fields.items():
        if not data.get(key):
            missing.append(field_name)
    return missing

with st.form("product_input_form"):
    st.subheader("Введите данные о товаре:")

    name = st.text_input("Название товара*", 
                         placeholder="Например: Манометр показывающий DM 02")
    manufacturer = st.text_input("Производитель*",
                                 placeholder="Например: Манотомь")
    specs_raw = st.text_area("Характеристики товара (в формате 'Параметр = Значение', каждое на новой строке)",
                             placeholder="диапазон измерений = 0–1,6 МПа\nкласс точности = 1,5\nприсоединение = G1/2")
    description = st.text_area("Описание / Фрагмент тех. паспорта*",
                               placeholder="Например: Прибор предназначен для измерения избыточного давления...")

    submit_button = st.form_submit_button("Сгенерировать карточку товара")



if submit_button: 
    missing_fields = validate_input({
        "name": name,
        "manufacturer": manufacturer,
        "specs": specs_raw,
        "description": description
    })
    if missing_fields:
        for field in missing_fields:
            st.error(f"\u26a0 Пожалуйста, введите {field}")
    else:
        specs = {}
        for line in specs_raw.splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                specs[key.strip()] = value.strip()
        product_data = {
            "name": name,
            "manufacturer": manufacturer,
            "specs": specs,
            "description": description
        }

        with st.spinner("Генерация карточки товара..."):
            output = generate_product_card(product_data, model_name="qwen2.5:3b-instruct")

        st.success("\u2705 Карточка товара успешно сгенерирована!")
        st.markdown("---")
        st.markdown("# Карточка товара:")
        st.markdown(output)

  
    
