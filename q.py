import os
import win32com.client
import sys

def create_task(bat_file_path):
    # Görev zamanlayıcısını başlat
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    # Yeni bir görev oluştur
    task_definition = scheduler.NewTask(0)

    # Görevin ayarlarını yapılandır
    task_definition.RegistrationInfo.Description = "Oturum Açıldığında Bat Dosyasını Çalıştır"
    task_definition.RegistrationInfo.Author = "Python Script"

    # Görev, oturum açıldığında başlasın
    trigger = task_definition.Triggers.Create(1)  # 1 = 'OnLogon' Trigger
    trigger.UserId = None  # Tüm kullanıcılar için geçerli

    # Görevin çalışma zamanı ayarları
    exec_action = task_definition.Actions.Create(0)  # 0 = Execute action
    exec_action.Path = bat_file_path  # Çalıştırılacak dosyanın yolu

    # Gizli ve öncelikli çalıştırma ayarları
    exec_action.Parameters = ''  # Parametreler boş
    task_definition.Settings.Hidden = True  # Gizli modda çalışacak
    task_definition.Settings.Priority = 7  # Öncelikli çalışacak (1-10 arası)

    # Görevi zamanlayıcıya kaydet
    folder = scheduler.GetFolder('\\')
    folder.RegisterTaskDefinition(
        'Oturum Açıldığında Bat Çalıştır',  # Görev adı
        task_definition,
        6,  # 6 = Create or update task
        None,  # Kullanıcı adı boş bırakılabilir
        None,  # Parola boş bırakılabilir
        3   # 3 = 'Logon' başlatma koşulu
    )

    print(f"Başarılı bir şekilde görev oluşturuldu: {bat_file_path}")

if __name__ == "__main__":
    bat_file_path = r"C:\Yol\Dosyanız.bat"  # Buraya çalıştırmak istediğiniz bat dosyasının yolunu girin
    if os.path.exists(bat_file_path):
        create_task(bat_file_path)
    else:
        print(f"{bat_file_path} bulunamadı. Lütfen geçerli bir dosya yolu belirtin.")
