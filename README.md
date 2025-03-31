# SimpleSMSTestClient

#### ���������� - ������ � ��������� ������� �������� ���-���������
---
##### �������� ������:
���������� ������������� ��� �������� ��� ��������� ����������� ������� �������� �� ��������� ���������� ���������� ���������� � ���������� ������.

���������� ������������ ��������� ����� ���� ������������.

������ �������� ��������� ��������� ������������� ��������� socket ��� asyncio �� ����� (�������� � ����� ������������).

������ �������������� ��������� ��������� �� �������� ����������:
```python main.py parameters``` (Windows)

�� ����� ������ ���������� ������������ ����������� ������������ �� ������ ���������� � ���������� �� ������� ������� � ���� "client.log".

---
##### ��������� ���������� ������:

��� ������� ��������� ��������� �����:
- \-s, \-\-sender - ���������� ����� �����������
- \-r, \-\-recipient - ���������� ����� ����������
- \-m, \-\-message - ���������
- \-c, \-\-config - ��� ����� ������������ ���������� (�� ��������� config.toml)
- \-f, \-\-file - ��� ����� ����������

���� ���������� ������ ������������ �� ���� ��������� ��� � ��������� utf-8, ������ ������ �������� ����� ��� ������ ���������� ���������� ��� �������� ��������� ����������.

����������� � ����� ���������� ������������ ���� \-f ��� ����������� �������������� ������ ����������.

����������� ��� ���������� ������ (-s, -r, -m) � �������� ���������� ������������ ������ ����:```sender_number recipient_number message``` ��� ����������� ������������� ���������.

���� � �������� ���������� ������������ ������ ���������� �������, �� �� ���������� ������������ ���������: ```"This is message"```.

---
##### ���� ������������

������������ ���������� ������������ ���� � ������� TOML �������� ��������� ���:
```
[system]
# ��� ���������� �� ��������� ������� ���������� ����� � ��������
#   0 - socket (�� ���������)
#   1 - asyncio
client_type = 1

[user]
# ��� ������������. ����������� � �����������.
login = "user"

# ������ ������������. ����������� � �����������.
password = "password"

[server]
# ����� �������
address = "http://localhost:4010/send_sms"

# ������������ ����� ����������� ���������� � ��������
# 0 - ��� ����������� (�� ���������)
max_connections = 0

# ������������ ����� �������� ������ �� ������� � ��
# 0 - ��� ����������� (�� ���������)
max_time = 1000
```
�� ��������� ������������ ���� � ������ "config.toml", ������� ����� �������� ����� �������� ���������� ������ - \-c, \-\-config.

---
���������� ����������� � �������������� � ��������������
python 3.11.7
pytest 8.3.5
����������� ����������� �� ���� �������������� � ������� ���-�������.
