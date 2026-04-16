import datetime

def get_time_angles():
    """
    Получает текущее время и конвертирует его в углы поворота.
    """
    now = datetime.datetime.now()
    
    # В круге 360 градусов, в минуте/часе 60 делений.
    # 360 / 60 = 6 градусов на одну секунду или минуту.
    # Pygame вращает против часовой стрелки, поэтому используем минус.
    second_angle = -now.second * 6
    minute_angle = -now.minute * 6
    
    return minute_angle, second_angle