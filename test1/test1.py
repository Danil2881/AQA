import requests
import pytest
from constants import Base_url
from faker import Faker

faker = Faker()



class TestBookings:


  def test_booking_create(self,session_auth,booking_auth):

    #Создаём книгу
    create = session_auth.post(url="https://restful-booker.herokuapp.com/booking",json=booking_auth)
    assert create.status_code == 200, "Не верный статус код"
    booking_id = create.json().get("bookingid")

    #Проверяем созданную книгу
    look = session_auth.get(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert look.status_code == 200, "Не верный статус код в сравнении id"
    assert look.json().get("firstname") == booking_auth["firstname"], "Не совпадает имя"
    #return booking_id



    # Обновляем данные польностью
    update = session_auth.put(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",json= booking_auth)
    assert update.status_code == 200, "Статус код не верный"
    assert update.json().get("firstname") == booking_auth["firstname"], "Имя не совпадает"

    #Обновляем данные частично

    update_patch = session_auth.patch(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",json = {"firstname":"Danil","additionalneeds":"Dinner"})
    assert update_patch.status_code == 200, "Статус код частичного обновления не верный"
    assert update_patch.json().get("firstname") == "Danil", "Не совпадает имя которое меняли"
    assert update_patch.json().get("additionalneeds") == "Dinner", "Не совпадают доп возможности"
    assert update_patch.json().get("lastname") == booking_auth["lastname"], "Не совпадает фамилия"


    # Удаляем
    del_booking = session_auth.delete(url = f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert del_booking.status_code == 201, "Статус код удаления не верный"

    check_delete = session_auth.get(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert check_delete.status_code == 404, "id Существует"




  def test_negative_tests(self,session_auth,negative_booking):
    #Создаём бронирование без обязательных полей
    negative_creation = session_auth.post(url="https://restful-booker.herokuapp.com/booking",json=negative_booking)
    assert negative_creation.status_code == 500, "Статус код не верный при негативном создании"

  def test_negative_get(self,session_auth,booking_auth):
    negative_get = session_auth.get(url=f"https://restful-booker.herokuapp.com/booking/{11111}")
    assert negative_get.status_code == 404, "Статус код не 404"


  def test_negative_update(self,session_auth,booking_auth,negative_booking):
    negative_update = session_auth.put(url=f"https://restful-booker.herokuapp.com/booking/{11111}",json={})
    assert negative_update.status_code == 400, "Статус код не верный,при  обновленииc с пустым телом"

  def test_negative_del(self,session_auth,booking_auth):
    negative_del = requests.delete(url=f"https://restful-booker.herokuapp.com/booking/{20}")
    assert negative_del.status_code == 403, "Статус код не верный, при удалении без авторизации"
