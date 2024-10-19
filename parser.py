import struct

def read_dicom_element(file):
    # Читаємо тег (група і елемент), 4 байти
    tag_group, tag_element = struct.unpack('<HH', file.read(4))

    # Читаємо VR (тип даних), 2 байти
    vr = file.read(2).decode('utf-8')

    # Читаємо довжину даних (VL)
    if vr in ['OB', 'OW', 'OF', 'SQ', 'UT', 'UN']:
        file.read(2)  # 2 байти резервовані (для цих VR)
        vl = struct.unpack('<L', file.read(4))[0]  # VL — 4 байти
    else:
        vl = struct.unpack('<H', file.read(2))[0]  # VL — 2 байти

    value = file.read(vl)

    return (tag_group, tag_element, vr, value)

def display_all_dicom_elements(file):
    # Пропускаємо заголовок (128 байтів + 4 байти 'DICM')
    file.seek(132)

    while True:
        try:
            tag_group, tag_element, vr, value = read_dicom_element(file)
            print(f"Tag: ({tag_group:04X},{tag_element:04X}), VR: {vr}, Value: {value[:50]}...")
        except:
            print("Кінець файлу або помилка читання")
            break


def find_element_by_tag(file, target_tag_group, target_tag_element):
    file.seek(132)

    while True:
        try:
            tag_group, tag_element, vr, value = read_dicom_element(file)
            if tag_group == target_tag_group and tag_element == target_tag_element:
                return value
        except:
            print("Кінець файлу або помилка читання")
            break

    return None


dicom_file_path = '_DICOM_Image_for_Lab_2.dcm'
with open(dicom_file_path, 'rb') as file:
    display_all_dicom_elements(file)

    target_tag_group = 0x0008
    target_tag_element = 0x1030
    value = find_element_by_tag(file, target_tag_group, target_tag_element)

    if value:
        print(f"Значення тега: {value.decode('utf-8')}")
    else:
        print("Тег не знайдено.")

